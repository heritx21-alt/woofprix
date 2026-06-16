"""Fetch search results pages from GitHub Actions and save HTML samples for debugging."""
import urllib.request
import urllib.error
import ssl
import os
import json
from urllib.parse import quote

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
}

# Test each working search URL with a specific product query
tests = [
    ("maxizoo", "https://www.maxizoo.fr/search?q=", "Royal Canin Maxi Adult 15kg"),
    ("animalis", "https://www.animalis.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("truffaut", "https://www.truffaut.com/catalogsearch/result/?q=", "Royal Canin Maxi Adult 15kg"),
    ("universveto", "https://www.univers-veto.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("zoomalia", "https://www.zoomalia.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("jardiland", "https://www.jardiland.com/search?q=", "Royal Canin Maxi Adult 15kg"),
    ("laferme", "https://www.lafermedesanimaux.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("medor", "https://www.medor-et-compagnie.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("produitsveto", "https://www.produits-veto.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("franceveto", "https://www.france-veto.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
]

output_dir = "public/data/html_samples"
os.makedirs(output_dir, exist_ok=True)

for shop_name, base_url, query in tests:
    url = base_url + quote(query)
    print(f"\n{shop_name}:")
    print(f"  URL: {url}")
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, context=ctx, timeout=8)
        html = resp.read().decode('utf-8', errors='replace')
        resp.close()
        print(f"  Status: {resp.status}, Size: {len(html)} bytes")

        # Save full HTML for analysis
        path = os.path.join(output_dir, f"{shop_name}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved to {path}")

        # Extract useful info
        import re
        # Find product-like elements
        product_patterns = [
            r'class="[^"]*product[^"]*"',
            r'class="[^"]*item[^"]*"',
            r'class="[^"]*card[^"]*"',
        ]
        for pat in product_patterns:
            matches = re.findall(pat, html[:5000])
            if matches:
                print(f"  Found elements: {matches[:5]}")

        # Find price-like text
        prices = re.findall(r'(\d+[.,]\d{2})\s*[€€]', html)
        print(f"  Prices found: {prices[:5]}")

        # Find product links
        links = re.findall(r'href="(/[^"]*royal[^"]*)"', html.lower())
        print(f"  Product links: {links[:3]}")

    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")

print(f"\n✅ HTML samples saved to {output_dir}/")
