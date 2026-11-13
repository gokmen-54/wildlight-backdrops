#!/usr/bin/env python3
"""
Automated Etsy Showcase & Studio Direct Request Engine (100% International English & Multi-Currency)
- Fetches real-time listings, descriptions, images, and prices from WildlightBackdrops on Etsy.
- Merges extra seasonal & customizable backdrop concepts (0 TL Etsy listing fee until requested).
- Integrates Direct Order & Custom Request Modal to gomoto253@gmail.com with pre-filled details.
- Deploys an English-first luxury digital assets portfolio with USD/EUR/GBP multi-currency support and rich SEO.
"""

import os
import sys
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime

# UTF-8 stdout
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RSS_URL = "https://www.etsy.com/shop/WildlightBackdrops/rss"
SHOWCASE_DIR = r"C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase"
HTML_PATH = os.path.join(SHOWCASE_DIR, "index.html")
EXTRA_CATALOG_PATH = os.path.join(SHOWCASE_DIR, "catalog_extra.json")
STUDIO_EMAIL = "gomoto253@gmail.com"

USD_TRY_RATE = 35.0


def fetch_live_etsy_listings():
    print("[ETSY-SYNC] Fetching live Etsy RSS feed...")
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    items = root.find('channel').findall('item')
    print(f"[ETSY-SYNC] Found {len(items)} live Etsy listings from RSS.")

    listings = []
    for idx, item in enumerate(items):
        raw_title = item.find('title').text if item.find('title') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        desc = item.find('description').text if item.find('description') is not None else ''

        # 1. Clean English Title
        title_clean = raw_title.replace(" by WildlightBackdrops", "").strip()
        display_title = title_clean.split("|")[0].split(",")[0].strip()
        subtitle = title_clean[len(display_title):].strip(" ,|")
        if not subtitle:
            subtitle = "Instant High-Resolution Digital Download for Photoshop, Cricut & Canva"

        # 2. Extract Exact Price
        price_match = re.search(r'(\d+[\.,]\d+)\s*(TRY|TL|USD|\$)', desc, re.IGNORECASE)
        price_try = 149.99
        if price_match:
            price_val_str = price_match.group(1).replace(',', '.')
            try:
                price_try = float(price_val_str)
            except Exception:
                pass

        price_usd_val = price_try / USD_TRY_RATE
        if price_usd_val > 10.0:
            price_usd = 11.99
        elif price_usd_val > 8.5:
            price_usd = 9.99
        elif price_usd_val > 7.0:
            price_usd = 8.49
        elif price_usd_val > 5.0:
            price_usd = 5.49
        else:
            price_usd = 4.29

        price_eur = round(price_usd * 0.93, 2)
        price_gbp = round(price_usd * 0.79, 2)

        # 3. High-Res Image
        img_match = re.search(r'src="([^"]+)"', desc)
        img_url = img_match.group(1) if img_match else ''
        if img_url:
            img_url = re.sub(r'il_\d+x\w+', 'il_794xN', img_url)

        # 4. English Category Tags
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
            "usd": f"${price_usd:.2f}",
            "eur": f"€{price_eur:.2f}",
            "gbp": f"£{price_gbp:.2f}",
            "is_on_etsy": True
        })

    # 5. Put Curated Studio Backdrops FIRST!
    final_listings = []
    if os.path.exists(EXTRA_CATALOG_PATH):
        try:
            with open(EXTRA_CATALOG_PATH, "r", encoding="utf-8") as f:
                extra_items = json.load(f)
                print(f"[ETSY-SYNC] Merging {len(extra_items)} premium studio backdrops at TOP.")
                for x in extra_items:
                    x["is_on_etsy"] = not x.get("is_request_first", False)
                    final_listings.append(x)
        except Exception as e:
            print(f"[UYARI] Extra catalog load error: {e}")

    # Append any relevant RSS listings
    final_listings.extend(listings)
    return final_listings


def build_page_html(listings):
    cards_html = ""
    ld_items = []

    for idx, item in enumerate(listings):
        raw_usd = item['usd'].replace('$', '').strip()
        try:
            usd_float = float(raw_usd)
            direct_usd = f"${usd_float * 0.90:.2f}"
        except Exception:
            direct_usd = item['usd']

        clean_title = item['title'].replace('"', '&quot;').replace("'", "&#39;")
        clean_img = item['img'].replace('"', '&quot;')
        clean_link = item['link'].replace('"', '&quot;')

        ld_items.append(f"""          {{
            "@type": "ListItem",
            "position": {idx + 1},
            "item": {{
              "@type": "Product",
              "name": "{clean_title}",
              "image": "{clean_img}",
              "description": "{item['subtitle'].replace('"', '&quot;')}",
              "sku": "WLD-{item['id']}",
              "offers": {{
                "@type": "Offer",
                "price": "{raw_usd}",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "{clean_link}",
                "seller": {{
                  "@type": "Organization",
                  "name": "Wildlight Backdrops"
                }}
              }}
            }}
          }}""")

        # Buttons logic
        if item.get("is_on_etsy", True):
            etsy_btn_html = f"""
            <a href="{item['link']}" target="_blank" rel="noopener" class="w-full bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-500 hover:from-amber-300 hover:to-yellow-300 text-slate-950 font-black text-xs sm:text-sm py-2.5 px-3 rounded-xl shadow-md shadow-amber-400/15 transition flex items-center justify-center gap-1.5">
              <span>Buy on Etsy</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </a>
            """
            badge_html = f"""<span class="absolute top-3 left-3 bg-black/85 backdrop-blur text-amber-400 font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-full border border-amber-400/30 z-10 shadow">{item['category']}</span>"""
        else:
            etsy_btn_html = ""
            badge_html = f"""<span class="absolute top-3 left-3 bg-indigo-600/90 backdrop-blur text-white font-extrabold text-[10px] sm:text-xs px-2.5 py-1 rounded-full border border-indigo-400/30 z-10 shadow">✨ SEASONAL REQUEST</span>"""

        direct_order_btn = f"""
        <button onclick="openOrderModal('{clean_title}', '{item['usd']}', '{direct_usd}', '{clean_img}', '{clean_link}', {str(item.get('is_on_etsy', True)).lower()})" class="w-full bg-slate-800 hover:bg-slate-700 hover:border-emerald-500 text-emerald-400 border border-slate-700 font-bold text-xs py-2 px-3 rounded-xl transition flex items-center justify-center gap-1.5 mt-2">
          <span>⚡ Direct Order / Request (Save 10%)</span>
        </button>
        """

        specs_html = f"""<div class="text-[10px] text-amber-300 font-mono bg-amber-950/50 border border-amber-800/50 rounded-md px-2 py-0.5 mb-2 inline-block">📐 {item['specs']}</div>""" if item.get('specs') else ""

        cards_html += f"""
        <div class="product-card bg-slate-900 rounded-2xl border border-slate-800 hover:border-amber-400/60 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1.5 flex flex-col justify-between overflow-hidden group" data-category="{item['cat_filter']}">
          <div class="relative aspect-square overflow-hidden bg-slate-950 flex items-center justify-center p-2">
            {badge_html}
            <img src="{item['img']}" alt="{item['title']}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500 rounded-xl" loading="lazy">
          </div>
          
          <div class="p-4 sm:p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-1.5 text-[11px] font-bold text-amber-400 uppercase tracking-wider mb-1">
                <span>★★★★★ 5.0 RATED STUDIO</span>
              </div>
              <h3 class="font-extrabold text-white text-sm sm:text-base leading-snug line-clamp-2 mb-1.5 group-hover:text-amber-400 transition">
                {item['title']}
              </h3>
              {specs_html}
              <p class="text-slate-400 text-xs line-clamp-2 leading-relaxed mb-4">
                {item['subtitle']}
              </p>
            </div>

            <div class="pt-3 border-t border-slate-800">
              <div class="flex items-baseline justify-between mb-3">
                <div>
                  <div class="text-2xl font-black text-white price-display" data-usd="{item['usd']}" data-eur="{item['eur']}" data-gbp="{item['gbp']}">{item['usd']}</div>
                  <div class="text-[10px] font-semibold text-emerald-400 uppercase tracking-wider">Direct Order: {direct_usd}</div>
                </div>
                <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">0% ETSY FEE</span>
              </div>
              
              {etsy_btn_html}
              {direct_order_btn}
            </div>
          </div>
        </div>
        """

    json_items_ld = ",\n".join(ld_items)
    full_page = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wildlight Backdrops & Digital Designs | Official 5-Star Etsy Store</title>
  <meta name="description" content="Discover official high-resolution digital backdrops, BookTok PNG sublimation designs, cozy retro Halloween Cricut DTF downloads, and custom Canva templates from WildlightBackdrops. Order on Etsy or direct.">
  <meta name="keywords" content="digital backdrops, photography backdrops, booktok png, cozy reader sublimation, introvert shirt design, halloween png, retro teacher dtf, canva birthday magazine template, instant download etsy">
  <link rel="canonical" href="https://gokmen-54.github.io/wildlight-backdrops/">

  <!-- Pinterest & Facebook Open Graph Product Meta -->
  <meta property="og:type" content="product">
  <meta property="og:title" content="Wildlight Backdrops & Digital Designs | Official Etsy Store">
  <meta property="og:description" content="Instant download digital backdrops, BookTok PNGs, retro Halloween sublimation and Canva templates. 5-Star rated on Etsy.">
  <meta property="og:image" content="{listings[0]['img'] if listings else ''}">
  <meta property="og:url" content="https://gokmen-54.github.io/wildlight-backdrops/">
  <meta property="product:price:amount" content="{listings[0]['usd'].replace('$', '') if listings else '4.29'}">
  <meta property="product:price:currency" content="USD">
  <meta property="og:availability" content="instock">
  <meta name="pinterest-rich-pin" content="true">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Wildlight Backdrops | 8K Digital Art & PNGs on Etsy">
  <meta name="twitter:description" content="Instant download digital backdrops, BookTok & Halloween sublimation files. Commercial license included.">
  <meta name="twitter:image" content="{listings[0]['img'] if listings else ''}">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
  </style>

  <!-- Google & Pinterest Structured Data (JSON-LD ItemList & Products) -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Store",
        "@id": "https://gokmen-54.github.io/wildlight-backdrops/#store",
        "name": "Wildlight Backdrops",
        "url": "https://gokmen-54.github.io/wildlight-backdrops/",
        "sameAs": "https://wildlightbackdrops.etsy.com",
        "description": "Handcrafted digital photography backdrops, sublimation PNG designs, and customizable Canva templates.",
        "email": "{STUDIO_EMAIL}",
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "5.0",
          "reviewCount": "54"
        }}
      }},
      {{
        "@type": "ItemList",
        "name": "Featured Digital Products",
        "itemListElement": [
{json_items_ld}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "How do I download my digital backdrops and designs?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Immediately upon checkout, high-resolution 300 DPI files are delivered to your email. If purchased on Etsy, they are also available instantly in your Etsy downloads."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Are commercial licenses included for photographers and crafters?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Yes! Every digital backdrop and PNG graphic includes standard commercial licensing for photo studio sessions, client portraiture, and physical merchandise."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Can I request custom studio backdrop resolutions or custom designs?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Yes, click the Direct Order / Request button on any design or email our studio desk directly at gomoto253@gmail.com. We respond within 1 hour."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
</head>

<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-amber-400 selection:text-black min-h-screen flex flex-col justify-between overflow-x-hidden">

  <!-- Top Announcement Bar with Currency Selector & Studio Email -->
  <div class="bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 text-slate-950 text-xs font-black py-2.5 px-4 text-center tracking-wide flex items-center justify-between flex-wrap gap-2">
    <div class="flex-1 text-center sm:text-left flex items-center gap-2">
      <span>✨ STUDIO DIRECT DESK: <b>{STUDIO_EMAIL}</b> • SAVE 10% ON DIRECT ORDERS OR REQUEST CUSTOM ETSY LISTINGS!</span>
    </div>
    
    <!-- Currency Switcher -->
    <div class="flex items-center gap-1.5 mx-auto sm:mx-0">
      <span class="text-[10px] uppercase font-bold text-slate-800">Currency:</span>
      <button class="currency-btn active bg-slate-950 text-amber-400 px-2.5 py-0.5 rounded text-[11px] font-bold" data-curr="usd">USD ($)</button>
      <button class="currency-btn bg-black/20 hover:bg-black/30 text-slate-900 px-2.5 py-0.5 rounded text-[11px] font-bold transition" data-curr="eur">EUR (€)</button>
      <button class="currency-btn bg-black/20 hover:bg-black/30 text-slate-900 px-2.5 py-0.5 rounded text-[11px] font-bold transition" data-curr="gbp">GBP (£)</button>
    </div>
  </div>

  <!-- Header Navigation -->
  <header class="border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between">
      
      <!-- Brand Logo -->
      <a href="#" class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-400 to-yellow-500 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-amber-400/20">
          W
        </div>
        <div>
          <span class="text-xl font-extrabold tracking-tight text-white block">Wildlight<span class="text-amber-400">Backdrops</span></span>
          <span class="text-[10px] text-slate-400 uppercase tracking-widest block font-bold">Official Etsy Store & Direct Studio</span>
        </div>
      </a>

      <!-- Quick Nav -->
      <nav class="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-300">
        <a href="#products" class="hover:text-amber-400 transition">Featured Designs</a>
        <a href="#how-it-works" class="hover:text-amber-400 transition">How Direct Orders Work</a>
        <a href="#reviews" class="hover:text-amber-400 transition">Customer Reviews</a>
      </nav>

      <!-- CTA Buttons -->
      <div class="flex items-center gap-3">
        <button onclick="openCustomStudioModal()" class="hidden sm:inline-flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-emerald-400 border border-emerald-500/30 font-bold text-xs py-2 px-4 rounded-full transition">
          <span>⚡ Custom Design Request</span>
        </button>
        <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs sm:text-sm py-2.5 px-5 sm:px-6 rounded-full shadow-lg shadow-amber-400/25 transition transform hover:scale-105">
          Visit Etsy Shop ➔
        </a>
      </div>

    </div>
  </header>

  <!-- Hero Banner -->
  <section class="relative pt-16 pb-20 overflow-hidden border-b border-slate-800">
    <div class="absolute inset-0 bg-gradient-to-b from-amber-500/10 via-transparent to-transparent pointer-events-none"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center relative z-10">
      
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-amber-400/30 text-amber-400 text-xs font-bold mb-6">
        <span>★ 5.0 STAR RATED DIGITAL CREATIVE ASSETS</span>
      </div>

      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white max-w-4xl mx-auto leading-tight mb-4">
        Masterpiece Digital Backdrops & <span class="bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-transparent">Creative Designs</span>
      </h1>

      <p class="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto mb-8 leading-relaxed">
        Curated 300 DPI high-resolution photography backdrops, BookTok & retro Halloween PNGs, and custom Canva templates. Buy instantly on Etsy or order direct via email with 10% discount.
      </p>

      <!-- Value Props -->
      <div class="flex flex-wrap items-center justify-center gap-4 sm:gap-8 text-xs font-bold text-slate-300">
        <div class="flex items-center gap-2 bg-slate-900/60 border border-slate-800 px-3.5 py-1.5 rounded-full">
          <span>⚡ Instant Digital Download</span>
        </div>
        <div class="flex items-center gap-2 bg-slate-900/60 border border-slate-800 px-3.5 py-1.5 rounded-full">
          <span>🛡️ Commercial Use Allowed</span>
        </div>
        <div class="flex items-center gap-2 bg-slate-900/60 border border-slate-800 px-3.5 py-1.5 rounded-full">
          <span>🎨 Custom Commissions Welcome</span>
        </div>
      </div>

    </div>
  </section>

  <!-- Main Showcase Grid Section -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 py-16 w-full" id="products">
    
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10 pb-6 border-b border-slate-800">
      <div>
        <h2 class="text-2xl sm:text-3xl font-black text-white">Featured Studio Catalog</h2>
        <p class="text-slate-400 text-sm mt-1">Select any design to purchase directly on Etsy or place a direct commission request.</p>
      </div>

      <!-- Interactive Filter Buttons -->
      <div class="flex flex-wrap items-center gap-2 text-xs font-bold" id="filter-container">
        <button class="filter-btn active bg-amber-400 text-slate-950 px-4 py-2 rounded-full shadow-md" data-filter="all">All Designs ({len(listings)})</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="backdrop">Backdrops</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="booktok">BookTok & Cozy</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="halloween">Spooky Halloween</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="teacher">Teacher Life</button>
        <button class="filter-btn bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-full transition" data-filter="canva">Canva Templates</button>
      </div>
    </div>

    <!-- Product Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="product-grid">
      {cards_html}
    </div>

  </section>

  <!-- FAQ Section for Google & Search Ranking -->
  <section class="max-w-5xl mx-auto px-4 sm:px-6 py-12 border-t border-slate-800">
    <div class="bg-slate-900/60 rounded-3xl border border-slate-800 p-8 sm:p-10">
      <h2 class="text-xl sm:text-2xl font-black text-white mb-6">Frequently Asked Questions (FAQ)</h2>
      <div class="space-y-6 text-xs sm:text-sm text-slate-300">
        <div class="border-b border-slate-800/80 pb-4">
          <h3 class="font-bold text-amber-400 mb-1">How do I download my digital backdrops and designs?</h3>
          <p class="text-slate-400 leading-relaxed">Immediately upon order completion, you will receive full-resolution 300 DPI master files straight to your email. If purchased on Etsy, downloads are also available immediately in your Etsy account dashboard.</p>
        </div>
        <div class="border-b border-slate-800/80 pb-4">
          <h3 class="font-bold text-amber-400 mb-1">Are commercial licenses included for photographers and crafters?</h3>
          <p class="text-slate-400 leading-relaxed">Yes! All photography backdrops and PNG graphics include standard commercial licensing for photo studio sessions, client portrait composites, and physical merchandise printing.</p>
        </div>
        <div>
          <h3 class="font-bold text-amber-400 mb-1">Can I request custom resolutions or seasonal backdrops?</h3>
          <p class="text-slate-400 leading-relaxed">Absolutely. Click the Direct Order / Request button on any design or email our studio desk directly at <b>{STUDIO_EMAIL}</b>. We deliver custom requests and adaptations within 1 hour.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- How Direct Orders Work Section -->
  <section class="max-w-7xl mx-auto px-4 sm:px-6 py-12 border-t border-slate-800" id="how-it-works">
    <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 rounded-3xl border border-slate-800 p-8 sm:p-12 text-center sm:text-left flex flex-col md:flex-row items-center justify-between gap-8">
      <div class="max-w-2xl">
        <span class="text-xs font-extrabold text-amber-400 uppercase tracking-widest block mb-2">Zero Marketplace Fees • 10% Savings</span>
        <h3 class="text-2xl sm:text-3xl font-black text-white mb-3">How Direct Studio Orders & Custom Requests Work</h3>
        <p class="text-slate-400 text-sm leading-relaxed mb-4">
          Looking for a custom seasonal backdrop, high-res resolution adaptation, or want to buy direct without Etsy marketplace fees?
        </p>
        <ul class="text-slate-300 text-xs sm:text-sm space-y-2 text-left">
          <li class="flex items-center gap-2">✓ <b>1. Send a Request:</b> Click any "Direct Order" button or email <b>{STUDIO_EMAIL}</b>.</li>
          <li class="flex items-center gap-2">✓ <b>2. Two Convenient Ways to Buy:</b> Receive direct download payment link (Save 10%) OR ask us to publish a custom Etsy listing for you!</li>
          <li class="flex items-center gap-2">✓ <b>3. Rapid Delivery:</b> Digital assets delivered straight to your email within 1 hour.</li>
        </ul>
      </div>

      <div class="flex flex-col gap-3 w-full sm:w-auto">
        <button onclick="openCustomStudioModal()" class="bg-gradient-to-r from-amber-400 to-yellow-400 text-slate-950 font-black text-sm py-3.5 px-8 rounded-2xl shadow-xl shadow-amber-400/20 hover:from-amber-300 hover:to-yellow-300 transition text-center">
          Open Direct Request Desk
        </button>
        <a href="mailto:{STUDIO_EMAIL}?subject=Custom%20Design%20Inquiry%20-%20Wildlight%20Backdrops" class="bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-3 px-6 rounded-2xl border border-slate-700 text-center transition">
          Direct Email: {STUDIO_EMAIL}
        </a>
      </div>
    </div>
  </section>

  <!-- Sticky Mobile Bottom Bar -->
  <div class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-950/95 border-t border-slate-800 backdrop-blur-lg px-4 py-3 flex items-center justify-between shadow-2xl">
    <div>
      <span class="text-xs font-bold text-white block">Wildlight Studio</span>
      <span class="text-[10px] text-amber-400 font-semibold block">{STUDIO_EMAIL}</span>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="openCustomStudioModal()" class="bg-slate-800 text-emerald-400 font-bold text-xs py-2 px-3 rounded-full border border-emerald-500/30">
        ⚡ Request
      </button>
      <a href="https://wildlightbackdrops.etsy.com" target="_blank" rel="noopener" class="bg-amber-400 text-slate-950 font-black text-xs py-2 px-4 rounded-full shadow-md">
        Etsy Shop ➔
      </a>
    </div>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 py-12 bg-black text-slate-500 text-xs mt-12 pb-20 md:pb-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-amber-400 flex items-center justify-center text-slate-950 font-black">W</div>
        <div>
          <span class="font-bold text-white text-sm block">Wildlight Backdrops</span>
          <span class="text-[10px] text-slate-400">Official Etsy Store & Direct Creative Studio</span>
        </div>
      </div>
      <div class="text-center md:text-right">
        <p class="text-slate-300 font-medium mb-1">Direct Orders & Inquiries: <a href="mailto:{STUDIO_EMAIL}" class="text-amber-400 hover:underline">{STUDIO_EMAIL}</a></p>
        <p>© 2026 WildlightBackdrops. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <!-- DIRECT ORDER / CUSTOM REQUEST MODAL -->
  <div id="orderModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl relative overflow-hidden text-left" onclick="event.stopPropagation()">
      
      <!-- Close Button -->
      <button onclick="closeOrderModal()" class="absolute top-4 right-4 w-9 h-9 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition">
        ✕
      </button>

      <div class="flex items-center gap-4 mb-6">
        <img id="modalItemImg" src="" alt="" class="w-20 h-20 rounded-xl object-contain bg-slate-950 p-1 border border-slate-800">
        <div>
          <span class="text-[10px] font-black uppercase text-amber-400 tracking-wider block mb-1">Direct Studio Order & Request</span>
          <h3 id="modalItemTitle" class="text-base sm:text-lg font-black text-white leading-snug"></h3>
          <div class="flex items-center gap-2 mt-1">
            <span class="text-xs text-slate-400 line-through" id="modalRegularPrice"></span>
            <span class="text-emerald-400 font-black text-base" id="modalDirectPrice"></span>
            <span class="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">Save 10%</span>
          </div>
        </div>
      </div>

      <div class="bg-slate-950/80 border border-slate-800/80 rounded-2xl p-4 mb-6 text-xs text-slate-300 space-y-2">
        <p class="font-bold text-white flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span> How to Complete This Order:
        </p>
        <p>Send a quick request to our studio email (<b>{STUDIO_EMAIL}</b>). We will respond within 1 hour with:</p>
        <ul class="space-y-1 text-slate-400 pl-4 list-disc">
          <li><b>Option A:</b> Direct Download Link with 10% Discount (Zero marketplace fees).</li>
          <li><b>Option B:</b> Custom private Etsy listing link if you prefer checking out on Etsy.</li>
        </ul>
      </div>

      <!-- Action Buttons -->
      <div class="space-y-2.5">
        <a id="modalGmailBtn" href="#" target="_blank" class="w-full bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold text-xs sm:text-sm py-3 px-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2">
          <span>✉️ Send Request via Gmail (Pre-filled)</span>
        </a>

        <a id="modalMailtoBtn" href="#" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-3 px-4 rounded-xl border border-slate-700 transition flex items-center justify-center gap-2">
          <span>📧 Open Default Mail Client</span>
        </a>

        <button onclick="copyModalRequest()" class="w-full bg-slate-950 hover:bg-black text-slate-300 hover:text-white font-medium text-xs py-2.5 px-4 rounded-xl border border-slate-800 transition flex items-center justify-center gap-1.5">
          <span id="copyBtnText">📋 Copy Request Details to Clipboard</span>
        </button>
      </div>

      <div class="mt-4 text-center">
        <span class="text-[11px] text-slate-500">Official Studio Desk: {STUDIO_EMAIL}</span>
      </div>

    </div>
  </div>

  <!-- Filter & Currency Switcher JS -->
  <script>
    // Category Filtering
    document.querySelectorAll('.filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.filter-btn').forEach(b => {{
          b.classList.remove('bg-amber-400', 'text-slate-950', 'shadow-md');
          b.classList.add('bg-slate-900', 'text-slate-300');
        }});
        btn.classList.remove('bg-slate-900', 'text-slate-300');
        btn.classList.add('bg-amber-400', 'text-slate-950', 'shadow-md');

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

    // Currency Switcher (USD, EUR, GBP)
    document.querySelectorAll('.currency-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.currency-btn').forEach(b => {{
          b.classList.remove('bg-slate-950', 'text-amber-400');
          b.classList.add('bg-black/20', 'text-slate-900');
        }});
        btn.classList.remove('bg-black/20', 'text-slate-900');
        btn.classList.add('bg-slate-950', 'text-amber-400');

        const curr = btn.getAttribute('data-curr');
        document.querySelectorAll('.price-display').forEach(el => {{
          el.innerText = el.getAttribute('data-' + curr);
        }});
      }});
    }});

    // Modal Control
    let currentRequestText = "";

    function openOrderModal(title, regularPrice, directPrice, img, link, isOnEtsy) {{
      document.getElementById('modalItemImg').src = img;
      document.getElementById('modalItemTitle').innerText = title;
      document.getElementById('modalRegularPrice').innerText = regularPrice;
      document.getElementById('modalDirectPrice').innerText = directPrice;

      const subject = encodeURIComponent("Direct Order / Custom Request: " + title);
      const bodyText = "Hello Wildlight Backdrops Team,\\n\\n" +
        "I would like to order / request this design:\\n" +
        "- Design: " + title + "\\n" +
        "- Regular Price: " + regularPrice + "\\n" +
        "- Direct Price (10% Discount): " + directPrice + "\\n" +
        "- Link / Reference: " + (link || "Direct Studio Request") + "\\n\\n" +
        "Please let me know how to complete payment (Direct Download link or a custom Etsy listing).\\n\\n" +
        "Thank you!";

      currentRequestText = bodyText;

      const encodedBody = encodeURIComponent(bodyText);
      const recipient = "{STUDIO_EMAIL}";

      // Gmail Web Link
      const gmailUrl = "https://mail.google.com/mail/?view=cm&fs=1&to=" + recipient + "&su=" + subject + "&body=" + encodedBody;
      document.getElementById('modalGmailBtn').href = gmailUrl;

      // Mailto Link
      const mailtoUrl = "mailto:" + recipient + "?subject=" + subject + "&body=" + encodedBody;
      document.getElementById('modalMailtoBtn').href = mailtoUrl;

      const modal = document.getElementById('orderModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }}

    function openCustomStudioModal() {{
      openOrderModal("Custom Studio Backdrop / Design Request", "Custom", "10% OFF", "{listings[0]['img'] if listings else ''}", "https://gokmen-54.github.io/wildlight-backdrops/", false);
    }}

    function closeOrderModal() {{
      const modal = document.getElementById('orderModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.getElementById('copyBtnText').innerText = "📋 Copy Request Details to Clipboard";
    }}

    function copyModalRequest() {{
      if (navigator.clipboard && currentRequestText) {{
        navigator.clipboard.writeText(currentRequestText.replace(/\\\\n/g, '\\n')).then(() => {{
          document.getElementById('copyBtnText').innerText = "✅ Copied to Clipboard! (Send to {STUDIO_EMAIL})";
        }});
      }}
    }}

    // Close on outer click
    document.getElementById('orderModal').addEventListener('click', (e) => {{
      if (e.target.id === 'orderModal') {{
        closeOrderModal();
      }}
    }});
  </script>

</body>
</html>
"""
    return full_page


def sync_and_deploy():
    listings = fetch_live_etsy_listings()
    if not listings:
        print("[ETSY-SYNC] No listings found.")
        return

    html = build_page_html(listings)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[ETSY-SYNC] {HTML_PATH} written with 100% English & Multi-currency support.")

    # Save JSON data
    json_path = os.path.join(SHOWCASE_DIR, "etsy_listings.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)

    # Generate sitemap.xml and robots.txt for Google & Pinterest
    sitemap_path = os.path.join(SHOWCASE_DIR, "sitemap.xml")
    today = datetime.now().strftime("%Y-%m-%d")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://gokmen-54.github.io/wildlight-backdrops/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
""")

    robots_path = os.path.join(SHOWCASE_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(f"""User-agent: *
Allow: /
Sitemap: https://gokmen-54.github.io/wildlight-backdrops/sitemap.xml
""")

    # Git push to GitHub Pages
    subprocess.run(["git", "add", "."], cwd=SHOWCASE_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat: integrate studio direct order modal to gomoto253@gmail.com and extra catalog"], cwd=SHOWCASE_DIR)
    res = subprocess.run(["git", "push", "origin", "main"], cwd=SHOWCASE_DIR, capture_output=True, text=True)
    print("[ETSY-SYNC] Deployed to GitHub Pages:", res.stdout, res.stderr)


if __name__ == "__main__":
    sync_and_deploy()
