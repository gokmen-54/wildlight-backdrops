import urllib.request
import xml.etree.ElementTree as ET
import re

url = 'https://www.etsy.com/shop/WildlightBackdrops/rss'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    xml_data = resp.read()

root = ET.fromstring(xml_data)
items = root.find('channel').findall('item')
for idx, i in enumerate(items):
    title = i.find('title').text
    desc = i.find('description').text
    # Find any price or currency
    prices = re.findall(r'(\$\d+[\.,]\d+|\d+[\.,]\d+\s*(?:USD|TL|TRY|EUR)|\bPrice:\s*[^<\n]+)', desc, re.IGNORECASE)
    print(f"[{idx+1}] {title[:60]}")
    print(f"    Prices in RSS: {prices}")
