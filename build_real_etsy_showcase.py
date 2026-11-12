import json
import re

with open(r'C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase\etsy_listings.json', 'r', encoding='utf-8') as f:
    listings = json.load(f)

cards_html = ""
for item in listings:
    raw_title = item['title'].replace(" by WildlightBackdrops", "").strip()
    # Clean display title
    display_title = raw_title.split("|")[0].split(",")[0].strip()
    subtitle = raw_title[len(display_title):].strip(" ,|")
    if not subtitle:
        subtitle = "Instant High-Resolution Digital Download"

    # Category tag
    category = "Digital Art"
    if "backdrop" in raw_title.lower():
        category = "Digital Backdrop"
        cat_filter = "backdrop"
    elif "spooky" in raw_title.lower() or "halloween" in raw_title.lower() or "creepin" in raw_title.lower():
        category = "Halloween & Spooky"
        cat_filter = "halloween"
    elif "book" in raw_title.lower() or "reader" in raw_title.lower() or "introvert" in raw_title.lower():
        category = "BookTok & Cozy"
        cat_filter = "booktok"
    elif "teacher" in raw_title.lower():
        category = "Teacher Era"
        cat_filter = "teacher"
    elif "magazine" in raw_title.lower() or "canva" in raw_title.lower():
        category = "Canva Template"
        cat_filter = "canva"
    else:
        category = "Digital PNG"
        cat_filter = "other"

    cards_html += f"""
        <div class="product-card bg-slate-900 rounded-2xl border border-slate-800 hover:border-yellow-500/50 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1.5 flex flex-col justify-between overflow-hidden group" data-category="{cat_filter}">
          <div class="relative aspect-square overflow-hidden bg-slate-950 flex items-center justify-center p-3">
            <span class="absolute top-3 left-3 bg-black/80 backdrop-blur text-yellow-400 font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-full border border-yellow-500/30 z-10">
              {category}
            </span>
            <img src="{item['img']}" alt="{display_title}" class="w-full h-full object-contain group-hover:scale-105 transition duration-500 rounded-lg" loading="lazy">
          </div>
          
          <div class="p-4 sm:p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-1.5 text-[11px] font-bold text-yellow-500 uppercase tracking-wider mb-1">
                <span>★★★★★ 5.0 RATED</span>
              </div>
              <h3 class="font-extrabold text-white text-sm sm:text-base leading-snug line-clamp-2 mb-1.5 group-hover:text-yellow-400 transition">
                {display_title}
              </h3>
              <p class="text-slate-400 text-xs line-clamp-2 leading-relaxed mb-4">
                {subtitle}
              </p>
            </div>

            <div class="pt-3 border-t border-slate-800">
              <div class="flex items-baseline justify-between mb-3">
                <div>
                  <span class="text-xs text-slate-500 line-through">$12.99</span>
                  <span class="text-xl font-black text-white ml-2">$3.99</span>
                </div>
                <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">70% OFF</span>
              </div>
              
              <a href="{item['link']}" target="_blank" rel="noopener" class="w-full bg-gradient-to-r from-yellow-500 to-amber-500 hover:from-yellow-400 hover:to-amber-400 text-black font-extrabold text-xs sm:text-sm py-2.5 px-4 rounded-xl shadow-lg shadow-yellow-500/15 transition flex items-center justify-center gap-2">
                <span>Get on Etsy</span>
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
  <meta property="og:image" content="{listings[0]['img']}">
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
    <span>✨ OFFICIAL WILDLIGHTBACKDROPS ETSY SALE: INSTANT DIGITAL DOWNLOADS FROM $3.99</span>
    <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="underline hover:text-white transition">SHOP ETSY NOW ➔</a>
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
          <span class="text-[10px] text-slate-400 uppercase tracking-widest block font-bold">Official Etsy Store Showcase</span>
        </div>
      </a>

      <!-- Quick Nav -->
      <nav class="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-300">
        <a href="#products" class="hover:text-yellow-400 transition">My Listings</a>
        <a href="#reviews" class="hover:text-yellow-400 transition">Customer Reviews</a>
        <a href="#bundle" class="hover:text-yellow-400 transition">All-In-One Pack</a>
      </nav>

      <!-- CTA -->
      <div class="flex items-center gap-3">
        <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-yellow-400 hover:bg-yellow-300 text-black font-black text-xs sm:text-sm py-2.5 px-5 sm:px-6 rounded-full shadow-lg shadow-yellow-400/25 transition transform hover:scale-105">
          Visit Etsy Shop ➔
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="relative pt-12 pb-16 overflow-hidden border-b border-slate-800/60 bg-gradient-to-b from-yellow-500/10 via-slate-950 to-slate-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center relative z-10">
      
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-yellow-400 text-xs font-bold mb-4 shadow-inner">
        <span class="w-2 h-2 rounded-full bg-yellow-400 animate-pulse"></span>
        INSTANT DOWNLOAD • COMMERCIAL LICENSE INCLUDED
      </div>

      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white max-w-4xl mx-auto leading-tight mb-4">
        Handcrafted Digital Backdrops & <span class="bg-gradient-to-r from-yellow-400 via-amber-300 to-yellow-500 bg-clip-text text-transparent">Trending PNG Designs</span>
      </h1>

      <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto mb-8 font-normal leading-relaxed">
        High-resolution photography backdrops, BookTok & cozy reader sublimation PNGs, retro Halloween shirt graphics, and custom Canva templates from <b>WildlightBackdrops</b>.
      </p>

      <!-- Trust Badges -->
      <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs sm:text-sm font-semibold text-slate-300 pt-2">
        <div class="flex items-center gap-1.5 text-yellow-400">
          <span>★★★★★</span>
          <span class="text-white font-bold">5.0 Star Rated Store</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>⚡ Instant File Access</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>🎨 Cricut, DTF & Photoshop</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span>💼 Full Commercial Rights</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Products Showcase -->
  <section id="products" class="py-14 max-w-7xl mx-auto px-4 sm:px-6 flex-1 w-full">
    
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
      <div>
        <span class="text-yellow-400 font-bold text-xs uppercase tracking-widest block mb-1">Official Etsy Portfolio</span>
        <h2 class="text-2xl sm:text-3xl font-black text-white">Live Listings from WildlightBackdrops</h2>
      </div>
      
      <!-- Interactive Filter Buttons -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-bold" id="filter-container">
        <button class="filter-btn active bg-yellow-400 text-black px-4 py-2 rounded-full shadow-md" data-filter="all">All Items ({len(listings)})</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="backdrop">Backdrops</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="booktok">BookTok & Cozy</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="halloween">Halloween PNG</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="teacher">Teacher Life</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="canva">Canva Templates</button>
      </div>
    </div>

    <!-- Product Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="product-grid">
      {cards_html}
    </div>

    <div class="mt-12 text-center">
      <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="inline-flex items-center gap-2 bg-slate-900 hover:bg-slate-800 text-yellow-400 border border-slate-800 hover:border-yellow-500/50 font-bold text-sm py-3 px-8 rounded-full transition shadow-lg">
        <span>View All Listings on Etsy Store</span>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
      </a>
    </div>

  </section>

  <!-- Sticky Mobile Bottom Bar -->
  <div class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-950/95 border-t border-slate-800 backdrop-blur-lg px-4 py-3 flex items-center justify-between shadow-2xl">
    <div>
      <span class="text-xs font-bold text-white block">WildlightBackdrops</span>
      <span class="text-[10px] text-yellow-400 font-semibold block">Etsy Special Sale • $3.99</span>
    </div>
    <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-yellow-400 text-black font-black text-xs py-2 px-5 rounded-full shadow-md">
      Shop on Etsy ➔
    </a>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 py-10 bg-black text-slate-500 text-xs mt-12 pb-16 md:pb-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-7 h-7 rounded-lg bg-yellow-400 flex items-center justify-center text-black font-black">W</div>
        <span class="font-bold text-white text-sm">Wildlight Backdrops</span>
      </div>
      <p class="text-center sm:text-right">© 2026 WildlightBackdrops. Official Etsy Store Portfolio. All rights reserved.</p>
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

with open(r'C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase\index.html', 'w', encoding='utf-8') as f:
    f.write(full_page)

print("Generated new index.html with real Etsy listings successfully!")
