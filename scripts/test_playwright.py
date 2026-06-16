"""Test blocked shops with Playwright (headless browser) to bypass Cloudflare/captchas."""
import os, re, sys, json
from urllib.parse import quote

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright non installé. Installez: pip install playwright && playwright install chromium")
    sys.exit(0)

tests = [
    ("zoomalia", "https://www.zoomalia.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("jardiland", "https://www.jardiland.com/search?q=", "Royal Canin Maxi Adult 15kg"),
    ("laferme", "https://www.lafermedesanimaux.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("medor", "https://www.medor-et-compagnie.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("produitsveto", "https://www.produits-veto.com/recherche?q=", "Royal Canin Maxi Adult 15kg"),
    ("franceveto", "https://www.france-veto.com/?post_type=product&s=", "Royal Canin Maxi Adult 15kg"),
    ("universveto", "https://www.univers-veto.fr/recherche?q=", "Royal Canin Maxi Adult 15kg"),
]

output_dir = "public/data/html_samples"
os.makedirs(output_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
        locale="fr-FR",
        viewport={"width": 1280, "height": 720},
    )

    for shop_name, base_url, query in tests:
        url = base_url + quote(query)
        print(f"\n{shop_name}:")
        print(f"  URL: {url}")
        try:
            page = context.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            html = page.content()
            print(f"  Status: {page.evaluate('window.location.href')}")
            print(f"  Size: {len(html)} bytes")

            if len(html) < 500:
                print(f"  ⚠ page trop petite, probablement bloque")
                page.close()
                continue

            path = os.path.join(output_dir, f"{shop_name}_pw.html")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  Sauvegarde -> {path}")

            # Quick analysis
            prices = re.findall(r'(\d+[.,]\d{2})\s*[€]', html)
            print(f"  Prix trouves: {prices[:5]}")
            product_classes = set(re.findall(r'class="([^"]*product[^"]*)"', html[:10000], re.I))
            if product_classes:
                print(f"  Classes produit: {sorted(product_classes)[:10]}")

            page.close()
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")

    browser.close()

print(f"\n✅ Tests Playwright termines. Fichiers dans {output_dir}/")
