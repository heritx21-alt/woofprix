#!/usr/bin/env python3
"""
catalog_scraper.py — Scrape les catalogues complets des shops.
Au lieu de chercher chaque produit, on scrape les pages categories
pour obtenir tous les produits d'un coup.
"""
import json, os, re, time, random
from typing import Optional
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup

client = httpx.Client(headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
}, follow_redirects=True, timeout=10)

def parse_price(text: str) -> Optional[float]:
    if not text:
        return None
    text = text.replace("\xa0", " ").replace(",", ".").strip()
    m = re.search(r"(\d+[\.\s]?\d*[\.,]?\d*)", text)
    if m:
        raw = m.group(1).replace(" ", "").replace(",", ".")
        try:
            val = float(raw)
            return val if val > 0.1 else None
        except:
            return None
    return None

def fetch(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = client.get(url)
        if resp.status_code in (403, 429, 503):
            return None
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except Exception as e:
        print(f"  ERR {url[:60]}: {e}")
        return None

# === ANIMALIS ===
def scrape_animalis_category(cat_url: str, max_pages: int = 5) -> list[dict]:
    products = []
    for page in range(1, max_pages + 1):
        url = f"{cat_url}?page={page}"
        print(f"    Page {page}: {url[:70]}...", end=" ")
        soup = fetch(url)
        if not soup:
            print("NO SOUP")
            break

        items = soup.select("[class*=product-tile], [class*=grid-tile], .product, [data-product-id]")
        if not items:
            items = soup.select('a[href*="/PM"], a[href*=".html"]')
            if not items:
                print("NO ITEMS")
                break

        found = 0
        for item in items:
            name_el = item.select_one("[class*=name], [class*=title], a[href*='/PM'], a[href*='.html']")
            price_el = item.select_one("[class*=price], .sales, .price")
            link_el = item.select_one("a[href]")
            img_el = item.select_one("img[src]")

            name = name_el.get_text(strip=True) if name_el else ""
            price_text = price_el.get_text(strip=True) if price_el else ""
            price = parse_price(price_text)
            link = ""
            if link_el:
                link = urljoin(url, link_el.get("href", ""))
            img = ""
            if img_el:
                img = urljoin(url, img_el.get("src", ""))

            if not name or not price:
                continue

            products.append({
                "name": name,
                "price": price,
                "url": link,
                "image": img,
                "source": "animalis",
            })
            found += 1

        print(f"{found} products")
        time.sleep(0.3 + random.random() * 0.2)

        # Check if there's a next page
        next_el = soup.select_one("[rel=next], a[class*=next], [aria-label=Next]")
        if not next_el:
            break

    return products

def main():
    output_dir = os.path.join("public", "data")
    os.makedirs(output_dir, exist_ok=True)

    all_products = {}

    # === ANIMALIS ===
    print("\n=== ANIMALIS ===")
    animalis_cats = [
        "https://www.animalis.com/chiens/alimentation/croquettes/",
        "https://www.animalis.com/chats/alimentation/croquettes/",
        "https://www.animalis.com/chiens/alimentation/patees/",
        "https://www.animalis.com/chats/alimentation/patees/",
        "https://www.animalis.com/chiens/alimentation/friandises/",
        "https://www.animalis.com/chats/alimentation/friandises/",
    ]

    for cat_url in animalis_cats:
        print(f"\n  Category: {cat_url}")
        prods = scrape_animalis_category(cat_url, max_pages=3)
        for p in prods:
            key = f"animalis::{p['name']}"
            all_products[key] = p
        print(f"  Total from this category: {len(prods)}")

    # Save intermediate results
    output = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(all_products),
        "shops": ["animalis"],
        "products": list(all_products.values()),
    }

    output_path = os.path.join(output_dir, "catalog_animalis.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(all_products)} Animalis products to {output_path}")

if __name__ == "__main__":
    main()
