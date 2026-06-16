"""Fetch search results pages from GitHub Actions using httpx (like the scrapers)."""
import os
import re
import json
import httpx
from urllib.parse import quote

# Use httpx with scraper-like headers to avoid blocks
client = httpx.Client(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
    follow_redirects=True,
    timeout=8.0,
)

tests = [
    ("maxizoo", "https://www.maxizoo.fr/search?q=", "Royal Canin Maxi Adult 15kg"),
    ("animalis", "https://www.animalis.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("truffaut", "https://www.truffaut.com/catalogsearch/result/?q=", "Royal Canin Maxi Adult 15kg"),
    ("universveto", "https://www.univers-veto.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("zoomalia", "https://www.zoomalia.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("zoomalia_alt", "https://www.zoomalia.com/resultats?q=", "Royal Canin Maxi Adult 15kg"),
    ("jardiland", "https://www.jardiland.com/search?q=", "Royal Canin Maxi Adult 15kg"),
    ("jardiland_alt", "https://www.jardiland.com/catalogsearch/result/?q=", "Royal Canin Maxi Adult 15kg"),
    ("laferme", "https://www.lafermedesanimaux.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("laferme_alt", "https://www.lafermedesanimaux.com/catalogsearch/result/?q=", "Royal Canin Maxi Adult 15kg"),
    ("medor", "https://www.medor-et-compagnie.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("medor_alt", "https://www.medor-et-compagnie.fr/catalogsearch/result/?q=", "Royal Canin Maxi Adult 15kg"),
    ("medor_alt2", "https://www.medor-et-compagnie.fr/?s=", "Royal Canin Maxi Adult 15kg"),
    ("produitsveto", "https://www.produits-veto.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("produitsveto_alt", "https://www.produits-veto.com/?s=", "Royal Canin Maxi Adult 15kg"),
    ("franceveto", "https://www.france-veto.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("franceveto_alt", "https://www.france-veto.com/?s=", "Royal Canin Maxi Adult 15kg"),
    ("franceveto_alt2", "https://www.france-veto.com/page/recherche?q=", "Royal Canin Maxi Adult 15kg"),
]

output_dir = "public/data/html_samples"
os.makedirs(output_dir, exist_ok=True)

for shop_name, base_url, query in tests:
    url = base_url + quote(query)
    print(f"\n{shop_name}:")
    print(f"  URL: {url}")
    try:
        resp = client.get(url, timeout=8.0)
        html = resp.text
        print(f"  Status: {resp.status_code}, Size: {len(html)} bytes")

        if resp.status_code in (403, 429, 503):
            print(f"  ⚠ BLOCKED ({resp.status_code})")
            path = os.path.join(output_dir, f"{shop_name}_error_{resp.status_code}.html")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            continue

        # Save full HTML
        path = os.path.join(output_dir, f"{shop_name}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved to {path}")

        # Extract useful info
        product_patterns = [
            r'class="[^"]*product[^"]*"',
            r'class="[^"]*item[^"]*"',
            r'class="[^"]*card[^"]*"',
        ]
        for pat in product_patterns:
            matches = re.findall(pat, html[:5000])
            if matches:
                print(f"  Found elements: {list(set(matches))[:5]}")

        # Find price-like text
        prices = re.findall(r'(\d+[.,]\d{2})\s*[€]', html)
        print(f"  Prices found: {prices[:5]}")

        # Find product links
        links = re.findall(r'href="(/[^"]*royal[^"]*)"', html.lower())
        print(f"  Product links: {links[:3]}")

    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")

client.close()
print(f"\n✅ HTML samples saved to {output_dir}/")
