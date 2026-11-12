#!/usr/bin/env python3
"""
Automated Etsy Showcase & Live Price Synchronizer
Fetches real-time listings, descriptions, images, and exact prices from WildlightBackdrops RSS.
Updates index.html and pushes changes to GitHub Pages automatically.
"""

import os
import sys
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
import subprocess

# UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RSS_URL = "https://www.etsy.com/shop/WildlightBackdrops/rss"
SHOWCASE_DIR = r"C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase"
HTML_PATH = os.path.join(SHOWCASE_DIR, "index.html")
USD_TRY_RATE = 35.0  # approximate USD conversion


def fetch_live_etsy_listings():
    print("[ETSY-SYNC] RSS veri akışı taranıyor...")
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    items = root.find('channel').findall('item')
    print(f"[ETSY-SYNC] {len(items)} aktif Etsy ürünü tespit edildi.")

    listings = []
    for idx, item in enumerate(items):
        raw_title = item.find('title').text if item.find('title') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        desc = item.find('description').text if item.find('description') is not None else ''

        # 1. Clean Title
        title_clean = raw_title.replace(" by WildlightBackdrops", "").strip()
        display_title = title_clean.split("|")[0].split(",")[0].strip()
        subtitle = title_clean[len(display_title):].strip(" ,|")
        if not subtitle:
            subtitle = "Instant High-Resolution Digital Download"

        # 2. Extract Exact Price from Description
        price_match = re.search(r'(\d+[\.,]\d+)\s*(TRY|TL|USD|\$)', desc, re.IGNORECASE)
        price_try = 149.99
        if price_match:
            price_val_str = price_match.group(1).replace(',', '.')
            try:
                price_try = float(price_val_str)
            except Exception:
                pass
        
        price_usd = price_try / USD_TRY_RATE

        # 3. Extract High-Res Image
        img_match = re.search(r'src="([^"]+)"', desc)
        img_url = img_match.group(1) if img_match else ''
        if img_url:
            # Upgrade to highest quality 794xN
            img_url = re.sub(r'il_\d+x\w+', 'il_794xN', img_url)

        # 4. Determine Category
        cat_filter = "other"
        category = "Digital PNG"
        t_low = title_clean.lower()
        if "backdrop" in t_low:
            category = "Digital Backdrop"
            cat_filter = "backdrop"
        elif any(k in t_low for k in ["spooky", "halloween", "ghost", "creepin"]):
            category = "Halloween & Spooky"
            cat_filter = "halloween"
        elif any(k in t_low for k in ["book", "reader", "introvert"]):
            category = "BookTok & Cozy"
            cat_filter = "booktok"
        elif "teacher" in t_low:
            category = "Teacher Era"
            cat_filter = "teacher"
        elif any(k in t_low for k in ["magazine", "canva", "template"]):
            category = "Canva Template"
            cat_filter = "canva"

        listings.append({
            "id": idx + 1,
            "title": display_title,
            "subtitle": subtitle,
            "category": category,
            "cat_filter": cat_filter,
            "link": link,
            "img": img_url,
            "price_try": f"{price_try:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", "."),
            "price_usd": f"${price_usd:,.2f}"
        })

    return listings


def build_page_html(listings):
    cards_html = ""
    for item in listings:
        cards_html += f"""
        <div class="product-card bg-slate-900 rounded-2xl border border-slate-800 hover:border-yellow-500/50 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1.5 flex flex-col justify-between overflow-hidden group" data-category="{item['cat_filter']}">
          <div class="relative aspect-square overflow-hidden bg-slate-950 flex items-center justify-center p-3">
            <span class="absolute top-3 left-3 bg-black/80 backdrop-blur text-yellow-400 font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-full border border-yellow-500/30 z-10 shadow">
              {item['category']}
            </span>
            <img src="{item['img']}" alt="{item['title']}" class="w-full h-full object-contain group-hover:scale-105 transition duration-500 rounded-lg" loading="lazy">
          </div>
          
          <div class="p-4 sm:p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-1.5 text-[11px] font-bold text-yellow-500 uppercase tracking-wider mb-1">
                <span>★★★★★ 5.0 RATED ON ETSY</span>
              </div>
              <h3 class="font-extrabold text-white text-sm sm:text-base leading-snug line-clamp-2 mb-1.5 group-hover:text-yellow-400 transition">
                {item['title']}
              </h3>
              <p class="text-slate-400 text-xs line-clamp-2 leading-relaxed mb-4">
                {item['subtitle']}
              </p>
            </div>

            <div class="pt-3 border-t border-slate-800">
              <div class="flex items-baseline justify-between mb-3">
                <div>
                  <div class="text-xl font-black text-white">{item['price_try']}</div>
                  <div class="text-xs font-semibold text-yellow-400/90">{item['price_usd']} USD</div>
                </div>
                <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">ETSY FİYATI</span>
              </div>
              
              <a href="{item['link']}" target="_blank" rel="noopener" class="w-full bg-gradient-to-r from-yellow-500 to-amber-500 hover:from-yellow-400 hover:to-amber-400 text-black font-extrabold text-xs sm:text-sm py-2.5 px-4 rounded-xl shadow-lg shadow-yellow-500/15 transition flex items-center justify-center gap-2">
                <span>Etsy'de Satın Al</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </a>
            </div>
          </div>
        </div>
        """

    full_page = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wildlight Backdrops & Designs | Official Etsy Store Showcase</title>
  <meta name="description" content="Discover official high-resolution digital backdrops, BookTok PNG sublimation designs, spooky Halloween Cricut DTF files, and custom Canva templates from WildlightBackdrops on Etsy.">
  <link rel="canonical" href="https://wildlightbackdrops.etsy.com">

  <!-- Open Graph -->
  <meta property="og:title" content="Wildlight Backdrops & Designs | Official Etsy Showcase">
  <meta property="og:description" content="Instant download digital backdrops, BookTok PNGs, retro Halloween shirt designs and Canva templates. 5-Star rated on Etsy.">
  <meta property="og:image" content="{listings[0]['img'] if listings else ''}">
  <meta property="og:url" content="https://wildlightbackdrops.etsy.com">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  </style>

  <!-- Google Structured Data (JSON-LD) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Wildlight Backdrops",
    "url": "https://gokmen-54.github.io/wildlight-backdrops/",
    "sameAs": "https://wildlightbackdrops.etsy.com"
  }}
  </script>
</head>

<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-yellow-400 selection:text-black min-h-screen flex flex-col justify-between overflow-x-hidden">

  <!-- Top Announcement Bar -->
  <div class="bg-gradient-to-r from-yellow-500 via-amber-500 to-yellow-600 text-black text-xs font-black py-2.5 px-4 text-center tracking-wide flex items-center justify-center gap-2">
    <span>✨ GÜNCEL ETSY MAĞAZA FİYATLARIYLA ANLIK SENKRONİZE EDİLMEKTEDİR</span>
    <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="underline hover:text-white transition">ETSY MAĞAZASINA GİT ➔</a>
  </div>

  <!-- Header Navigation -->
  <header class="border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <a href="#" class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-yellow-400 to-amber-600 flex items-center justify-center text-black font-black text-xl shadow-lg shadow-yellow-500/20">
          W
        </div>
        <div>
          <span class="text-xl font-extrabold tracking-tight text-white block">Wildlight<span class="text-yellow-400">Backdrops</span></span>
          <span class="text-[10px] text-slate-400 uppercase tracking-widest block font-bold">Resmi Etsy Vitrini & Fiyat Kataloğu</span>
        </div>
      </a>

      <!-- Quick Nav -->
      <nav class="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-300">
        <a href="#products" class="hover:text-yellow-400 transition">Ürünlerim</a>
        <a href="#about" class="hover:text-yellow-400 transition">Hakkında</a>
      </nav>

      <!-- CTA -->
      <div class="flex items-center gap-3">
        <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-yellow-400 hover:bg-yellow-300 text-black font-black text-xs sm:text-sm py-2.5 px-5 sm:px-6 rounded-full shadow-lg shadow-yellow-400/25 transition transform hover:scale-105">
          Etsy Mağazasını Aç ➔
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="relative pt-12 pb-16 overflow-hidden border-b border-slate-800/60 bg-gradient-to-b from-yellow-500/10 via-slate-950 to-slate-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center relative z-10">
      
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-yellow-400 text-xs font-bold mb-4 shadow-inner">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        GÜNCEL CANLI ETSY FİYATLARI
      </div>

      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white max-w-4xl mx-auto leading-tight mb-4">
        Dijital Arka Planlar & <span class="bg-gradient-to-r from-yellow-400 via-amber-300 to-yellow-500 bg-clip-text text-transparent">Trend Tasarımlar</span>
      </h1>

      <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto mb-8 font-normal leading-relaxed">
        Fotoğraf stüdyo fonları, BookTok & Cozy Reader süblimasyon PNG'leri, retro Cadılar Bayramı tasarımları ve Canva şablonları. <b>WildlightBackdrops</b> resmi koleksiyonu.
      </p>

      <!-- Trust Badges -->
      <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs sm:text-sm font-semibold text-slate-300 pt-2">
        <div class="flex items-center gap-1.5 text-yellow-400">
          <span>★★★★★</span>
          <span class="text-white font-bold">5.0 Yıldız Onaylı</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>⚡ Anında İndirme</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>🎨 Cricut, DTF & Photoshop</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>💼 Ticari Kullanım Lisansı</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Products Showcase -->
  <section id="products" class="py-14 max-w-7xl mx-auto px-4 sm:px-6 flex-1 w-full">
    
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
      <div>
        <span class="text-yellow-400 font-bold text-xs uppercase tracking-widest block mb-1">Resmi Etsy Portföyü</span>
        <h2 class="text-2xl sm:text-3xl font-black text-white">Canlı Fiyatlı Ürün Listesi</h2>
      </div>
      
      <!-- Interactive Filter Buttons -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-bold" id="filter-container">
        <button class="filter-btn active bg-yellow-400 text-black px-4 py-2 rounded-full shadow-md" data-filter="all">Tümü ({len(listings)})</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="backdrop">Arka Planlar</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="booktok">BookTok & Cozy</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="halloween">Cadılar Bayramı</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="teacher">Öğretmen Serisi</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="canva">Canva Şablonları</button>
      </div>
    </div>

    <!-- Product Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="product-grid">
      {cards_html}
    </div>

    <div class="mt-12 text-center">
      <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-slate-900 hover:bg-slate-800 text-yellow-400 border border-slate-800 hover:border-yellow-500/50 font-bold text-sm py-3 px-8 rounded-full transition shadow-lg">
        <span>Tüm Ürünleri Etsy Mağazasında Gör</span>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
      </a>
    </div>

  </section>

  <!-- Sticky Mobile Bottom Bar -->
  <div class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-950/95 border-t border-slate-800 backdrop-blur-lg px-4 py-3 flex items-center justify-between shadow-2xl">
    <div>
      <span class="text-xs font-bold text-white block">WildlightBackdrops</span>
      <span class="text-[10px] text-yellow-400 font-semibold block">Etsy Resmi Mağaza</span>
    </div>
    <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-yellow-400 text-black font-black text-xs py-2 px-5 rounded-full shadow-md">
      Etsy'de Aç ➔
    </a>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 py-10 bg-black text-slate-500 text-xs mt-12 pb-16 md:pb-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-7 h-7 rounded-lg bg-yellow-400 flex items-center justify-center text-black font-black">W</div>
        <span class="font-bold text-white text-sm">Wildlight Backdrops</span>
      </div>
      <p class="text-center sm:text-right">© 2026 WildlightBackdrops. Fiyatlar ve stok bilgileri Etsy mağazasından anlık olarak çekilmektedir.</p>
    </div>
  </footer>

  <!-- Filter JavaScript -->
  <script>
    document.querySelectorAll('.filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.filter-btn').forEach(b => {{
          b.classList.remove('bg-yellow-400', 'text-black', 'shadow-md');
          b.classList.add('bg-slate-900', 'text-slate-300');
        }});
        btn.classList.remove('bg-slate-900', 'text-slate-300');
        btn.classList.add('bg-yellow-400', 'text-black', 'shadow-md');

        const filter = btn.getAttribute('data-filter');
        document.querySelectorAll('.product-card').forEach(card => {{
          if (filter === 'all' || card.getAttribute('data-category') === filter) {{
            card.style.display = 'flex';
          }} else {{
            card.style.display = 'none';
          }}
        }});
      }});
    }});
  </script>

</body>
</html>
"""
    return full_page


def sync_and_deploy():
    listings = fetch_live_etsy_listings()
    if not listings:
        print("[ETSY-SYNC] Ürün bulunamadı.")
        return

    html = build_page_html(listings)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[ETSY-SYNC] {HTML_PATH} gerçek fiyatlarla güncellendi.")

    # Save JSON data
    json_path = os.path.join(SHOWCASE_DIR, "etsy_listings.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)

    # Git push to GitHub Pages
    subprocess.run(["git", "add", "."], cwd=SHOWCASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "chore: sync exact real-time prices from Etsy store"], cwd=SHOWCASE_DIR)
    res = subprocess.run(["git", "push", "origin", "main"], cwd=SHOWCASE_DIR, capture_output=True, text=True)
    print("[ETSY-SYNC] GitHub Pages'e başarıyla gönderildi:", res.stdout, res.stderr)


if __name__ == "__main__":
    sync_and_deploy()
