"""Check Cernunos search page correctly."""
import httpx, re
from bs4 import BeautifulSoup

c = httpx.Client(headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=5.0)
r = c.get("https://www.cernunos.fr/search?q=Royal+Canin+Maxi+Adult+15kg")
soup = BeautifulSoup(r.text, "lxml")
print(f"Title: {soup.select_one('title').get_text(strip=True)[:80]}")

# Find product elements with prices and links
prices = re.findall(r"(\d+[.,]\d{2})\s*[€]", r.text)
print(f"Prices: {prices[:10]}")

# Find elements containing both a price and a product link
for el in soup.find_all(class_=True):
    cls = " ".join(el.get("class", []))
    txt = el.get_text(strip=True)
    if any(price in txt for price in prices[:3]) and len(txt) > 30:
        a = el.select_one("a[href*='/products/']")
        price_el = el.select_one(".price, [class*=price]")
        img = el.select_one("img[src]")
        if a and price_el:
            print(f"\n<{el.name} class=\"{cls}\">")
            print(f"  text: {txt[:120]}")
            print(f"  href: {a.get('href','')}")
            print(f"  price: {price_el.get_text(strip=True)[:20]}")
            if img: print(f"  img: {img.get('src','')[:60]}")
            print(f"  HTML: {str(el)[:400]}")
            print()
            break

# Also try more specific selectors
for sel in [".product-item", ".product", "[class*=product]", "li.product"]:
    items = soup.select(sel)
    if items:
        print(f"\n--- {sel}: {len(items)} items ---")
        for it in items[:2]:
            txt = it.get_text(strip=True)[:80]
            if len(txt) > 20:
                print(f"  [{txt}]")

c.close()
