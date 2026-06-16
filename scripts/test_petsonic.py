"""Test Petsonic with different paths and find selectors."""
import httpx, re
from bs4 import BeautifulSoup

c = httpx.Client(headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=5.0)

# Test paths
for path in ["/catalogsearch/result/?q=", "/?s=", "/search?q="]:
    url = f"https://www.petsonic.com{path}Royal+Canin+Maxi+Adult+15kg"
    try:
        r = c.get(url, timeout=4.0)
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.select_one("title")
        t = title.get_text(strip=True)[:60] if title else ""
        prices = re.findall(r"(\d+[.,]\d{2})\s*[€]", r.text)
        print(f"\n{path}: {r.status_code} {len(r.text)}b title={t}")
        print(f"  Prices: {prices[:5]}")
        
        # Find any element with class containing product and has a link
        found = False
        for sel in [".product-item", ".product", "li.product", ".item.product", "[class*=product]"]:
            items = soup.select(sel)
            if items and len(items) < 100:
                for it in items[:3]:
                    a = it.select_one("a[href]")
                    price = it.select_one("[class*=price]")
                    txt = it.get_text(strip=True)[:60]
                    if a and price and len(txt) > 10:
                        print(f"  {sel}: [{txt}] price={price.get_text(strip=True)[:15]}")
                        found = True
                        break
                if found: break
        
        if not found:
            # Save page for debugging
            import os
            os.makedirs("public/data/html_samples", exist_ok=True)
            with open(f"public/data/html_samples/petsonic_path_{path.replace('/','_').replace('?','_')}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"  -> saved for debug")
    except Exception as e:
        print(f"\n{path}: {type(e).__name__}")

c.close()
