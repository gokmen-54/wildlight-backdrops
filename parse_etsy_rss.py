import urllib.request
import xml.etree.ElementTree as ET
import re
import json

url = 'https://www.etsy.com/shop/WildlightBackdrops/rss'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    xml_data = resp.read()

root = ET.fromstring(xml_data)
channel = root.find('channel')
items = channel.findall('item')
print(f"Total Etsy listings in RSS: {len(items)}")

listings = []
for idx, item in enumerate(items):
    title = item.find('title').text if item.find('title') is not None else ''
    link = item.find('link').text if item.find('link') is not None else ''
    desc = item.find('description').text if item.find('description') is not None else ''
    
    # Extract image src from description html
    img_match = re.search(r'src="([^"]+)"', desc)
    img = img_match.group(1) if img_match else ''
    
    # Upgrade thumbnail to higher resolution (e.g. from 340x270 to il_794xN or il_fullxfull)
    if img:
        img_high = re.sub(r'il_\d+x\w+', 'il_794xN', img)
    else:
        img_high = ''

    # Clean title
    clean_title = re.sub(r'\s+', ' ', title).strip()

    listings.append({
        'id': idx + 1,
        'title': clean_title,
        'link': link,
        'img': img_high or img,
        'thumb': img
    })

print(f"Extracted {len(listings)} listings:")
for l in listings[:5]:
    print(f"- {l['title']}")
    print(f"  Img: {l['img']}")
    print(f"  Url: {l['link']}")

with open(r'C:\Users\1247617\.gemini\antigravity\scratch\wildlight_showcase\etsy_listings.json', 'w', encoding='utf-8') as f:
    json.dump(listings, f, indent=2, ensure_ascii=False)
print("Saved to etsy_listings.json successfully!")
