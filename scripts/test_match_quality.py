"""Test if DirectVet/UltraPremium results match our catalog."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrapers"))
from base import BaseScraper, ScraperResult

import httpx, re, unicodedata
from urllib.parse import quote
from bs4 import BeautifulSoup

def normalize(name):
    name = unicodedata.normalize("NFKD", name.lower())
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^a-z0-9\s]", "", name)
    return re.sub(r"\s+", " ", name).strip()

def extract_weight(name):
    tokens = set()
    for m in re.finditer(r"\d+[.,]?\d*\s*(?:kg|g|l|ml|cm|m|batonnets|bâtonnets|etages|étages|litres)", name, re.I):
        tokens.add(m.group(0).strip().lower().replace(" ", ""))
    for m in re.finditer(r"(\d+[x]?\d*)\s*(?:kg|g)", name, re.I):
        tokens.add(m.group(0).strip().lower().replace(" ", ""))
    return tokens

catalog = [
    "Royal Canin Maxi Adult 15kg",
    "Royal Canin Medium Adult 15kg",
    "Royal Canin Mini Adult 7.5kg",
    "Royal Canin Mini Adult 3kg",
    "Hill's Science Plan Large Breed 14kg",
    "Hill's Science Plan Medium 12kg",
    "Purina Pro Plan Medium Sensible 12kg",
    "Purina Pro Plan Large 14kg",
    "Orijen Original Chien 13kg",
    "Acana Heritage Adult Chien 11kg",
    "Pedigree Dentastix 56 batonnets",
    "Purina Dentalife 35 batonnets",
    "Kong Classic M 7cm",
    "Laisse Flexi Extra M 5m",
    "Gamelle inox chien 20cm",
    "Panier chien 70x50cm",
    "Royal Canin Sterilised 37 10kg",
    "Royal Canin Sterilised 37 4kg",
    "Royal Canin British Shorthair 4kg",
    "Royal Canin Maine Coon 4kg",
    "Hill's Science Plan Adult Chat 7kg",
    "Purina Pro Plan Sterilised Chat 10kg",
    "Orijen Original Chat 5.4kg",
    "Acana Grasslands Chat 4.5kg",
    "Sheba Patee Chat 12x85g",
    "Felix Patee Chat 12x85g",
    "Gourmet Patee Chat 12x85g",
    "Litiere Catsan agglomerante 20kg",
    "Litiere silicate Ultra 5L",
    "Arbre a chat 180cm",
    "Fontaine a eau chat 1.5L",
    "Transporteur chat 50x30x30cm",
    "Brosse FURminator chat",
    "Melange graines rongeurs 1kg",
    "Cage rongeur 2 etages 80cm",
    "Foin rongeur 500g",
    "Melange graines oiseaux 2kg",
    "Aquarium Juwel 60L",
]

# Test DirectVet results
print("=== DIRECTVET - checking match quality ===")
# Simulate scraper
c = httpx.Client(headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=5.0)
r = c.get("https://www.direct-vet.fr/?s=Royal+Canin+Maxi+Adult+15kg")
soup = BeautifulSoup(r.text, "lxml")
items = soup.select(".ajax_block_product, .product_block")
print(f"Total items from scraper: {len(items)}")

for item in items:
    name_el = item.select_one("h5[itemprop='name'] a, [itemprop='name'] a, h5 a")
    price_el = item.select_one(".price, .product-price, [itemprop='price']")
    if not name_el or not price_el: continue
    name = name_el.get_text(strip=True)
    
    # Try matching each catalog item
    for cat in catalog:
        cat_norm = normalize(cat)
        scraped_norm = normalize(name)
        cat_weight = extract_weight(cat)
        scraped_weight = extract_weight(name)
        cat_brand = cat.split()[0].lower()
        
        if cat_weight and not (scraped_weight & cat_weight): continue
        if cat_brand and cat_brand not in scraped_norm: continue
        
        # Jaccard
        a_tokens = set(cat_norm.split())
        b_tokens = set(scraped_norm.split())
        if not a_tokens or not b_tokens: continue
        jaccard = len(a_tokens & b_tokens) / len(a_tokens | b_tokens)
        if jaccard >= 0.35:
            price = re.search(r"(\d+[.,]\d{2})", price_el.get_text(strip=True))
            price_val = float(price.group(1).replace(",", ".")) if price else 0
            print(f"  MATCH: {cat:40s} | j={jaccard:.2f} | price={price_val:.2f} | scraped=[{name[:50]}]")
            break

c.close()
