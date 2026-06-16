"""Test all untried shops at once."""
import httpx, os, json
from bs4 import BeautifulSoup

client = httpx.Client(headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
}, follow_redirects=True, timeout=4.0)

q = "Royal+Canin+Maxi+Adult+15kg"
os.makedirs("public/data/html_samples", exist_ok=True)

tests = {
    "medor": [
        f"https://www.medor-et-compagnie.fr/?s={q}",
        f"https://www.medor-et-compagnie.fr/recherche?q={q}",
        f"https://www.medor-et-compagnie.fr/search?q={q}",
        f"https://www.medor-et-compagnie.fr/catalogsearch/result/?q={q}",
    ],
    "directvet": [
        f"https://www.direct-vet.fr/?s={q}",
        f"https://www.direct-vet.fr/recherche?q={q}",
        f"https://www.direct-vet.fr/search?q={q}",
    ],
    "cernunos": [
        f"https://www.cernunos.fr/?s={q}",
        f"https://www.cernunos.fr/recherche?q={q}",
        f"https://www.cernunos.fr/search?q={q}",
    ],
    "santevet": [
        f"https://www.santevet.com/?s={q}",
        f"https://www.santevet.com/recherche?q={q}",
        f"https://www.santevet.com/search?q={q}",
    ],
    "ultrapremium": [
        f"https://www.ultrapremiumdirect.com/?s={q}",
        f"https://www.ultrapremiumdirect.com/recherche?q={q}",
        f"https://www.ultrapremiumdirect.com/search?q={q}",
    ],
    "petsonic": [
        f"https://www.petsonic.com/?s={q}",
        f"https://www.petsonic.com/recherche?q={q}",
        f"https://www.petsonic.com/search?q={q}",
        f"https://www.petsonic.com/catalogsearch/result/?q={q}",
    ],
}

results = {}
for shop, urls in tests.items():
    print(f"\n=== {shop} ===")
    for url in urls:
        try:
            r = client.get(url, timeout=4.0)
            title = ""
            if r.status_code == 200 and len(r.text) > 500:
                soup = BeautifulSoup(r.text, "lxml")
                t = soup.select_one("title")
                title = t.get_text(strip=True)[:60] if t else ""
            print(f"  {r.status_code} {len(r.text):>7}b  {title}")
            if r.status_code == 200 and len(r.text) > 1000:
                path = f"public/data/html_samples/{shop}.html"
                with open(path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"  -> saved {path}")
                results[shop] = url
                break
        except Exception as e:
            print(f"  ERROR {type(e).__name__}")

client.close()
print(f"\n=== RESULTATS ===")
for s, u in results.items():
    print(f"  {s}: OK" if u else f"  {s}: KO")
