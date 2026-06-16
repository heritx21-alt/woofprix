"""Quick test Petsonic."""
import httpx, re
from bs4 import BeautifulSoup

client = httpx.Client(headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=3.0)

for path in ["/?s=", "/catalogsearch/result/?q=", "/buscar?q="]:
    url = f"https://www.petsonic.com{path}Royal+Canin+Maxi+Adult+15kg"
    try:
        r = client.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        t = soup.select_one("title")
        title = t.get_text(strip=True)[:60] if t else ""
        prices = re.findall(r"(\d+[.,]\d{2})\s*[€]", r.text)
        print(f"{path:30s} {r.status_code} {len(r.text):>7}b title={title[:40]}")
        for sel in ["li.product", ".product-item", ".product", "[class*=product]"]:
            items = soup.select(sel)
            if items:
                print(f"  {sel}: {len(items)} [{items[0].get_text(strip=True)[:40]}]")
    except Exception as e:
        print(f"{path}: {type(e).__name__}")

client.close()
