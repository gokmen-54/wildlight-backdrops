import urllib.request
import urllib.parse
import re
import json

def get_competitor_data():
    keyword = "christmas digital backdrop"
    url = f"https://www.etsy.com/search?q={urllib.parse.quote(keyword)}&explicit=1"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8', errors='ignore')
            
            # Extract raw h3 or listing titles
            raw_h3 = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
            clean_titles = []
            for h in raw_h3:
                txt = re.sub(r'<[^>]+>', '', h).strip()
                txt = re.sub(r'\s+', ' ', txt)
                if len(txt) > 20 and not any(skip in txt.lower() for skip in ['filter', 'search', 'results', 'shop']):
                    clean_titles.append(txt)
                    
            print(f"Fetched {len(clean_titles)} top-ranking Etsy listing titles for '{keyword}':\n")
            for i, t in enumerate(clean_titles[:10], 1):
                print(f"{i}. {t}")
                
            # Extract keywords from these winning titles
            words = {}
            for t in clean_titles:
                tokens = re.findall(r'\b[a-zA-Z]{3,}\b', t.lower())
                for tok in tokens:
                    words[tok] = words.get(tok, 0) + 1
                    
            sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
            print("\n--- EN ÇOK KULLANILAN EN POPÜLER KELİMELER (TOP KEYWORDS) ---")
            for w, c in sorted_words[:20]:
                print(f" - {w}: {c} kez geçiyor")
                
    except Exception as e:
        print("Scrape error:", e)

if __name__ == '__main__':
    get_competitor_data()
