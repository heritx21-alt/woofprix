#!/usr/bin/env python3
"""Test multiple search URL patterns for each shop to find working ones."""
import urllib.request
import urllib.error
import ssl
import time
import sys
from urllib.parse import quote

# Each shop: base_url + list of search path patterns to try
SHOPS = {
    "zoomalia": {
        "base": "https://www.zoomalia.com",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
            "/catalogsearch/result/?q=",
            "/?s=",
        ],
    },
    "maxizoo": {
        "base": "https://www.maxizoo.fr",
        "paths": [
            "/catalogsearch/result/?q=",
            "/catalogsearch/result?q=",
            "/recherche?q=",
            "/search?q=",
            "/?s=",
        ],
    },
    "animalis": {
        "base": "https://www.animalis.com",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
            "/catalogsearch/result/?q=",
        ],
    },
    "jardiland": {
        "base": "https://www.jardiland.com",
        "paths": [
            "/search?q=",
            "/recherche?q=",
            "/catalogsearch/result/?q=",
            "/?s=",
        ],
    },
    "truffaut": {
        "base": "https://www.truffaut.com",
        "paths": [
            "/search?q=",
            "/recherche?q=",
            "/catalogsearch/result/?q=",
            "/?s=",
        ],
    },
    "laferme": {
        "base": "https://www.lafermedesanimaux.com",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
            "/catalogsearch/result/?q=",
        ],
    },
    "medor": {
        "base": "https://www.medor-et-compagnie.fr",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
        ],
    },
    "produitsveto": {
        "base": "https://www.produits-veto.com",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
        ],
    },
    "franceveto": {
        "base": "https://www.france-veto.com",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
        ],
    },
    "universveto": {
        "base": "https://www.univers-veto.fr",
        "paths": [
            "/recherche?q=",
            "/recherche/?q=",
            "/search?q=",
        ],
    },
}

TEST_QUERY = "croquettes"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
}

results = {}

for shop_name, shop_data in SHOPS.items():
    print(f"\n{'='*60}")
    print(f"🔍 {shop_name.upper()} ({shop_data['base']})")
    print(f"{'='*60}")
    shop_results = []
    base_url = shop_data["base"]

    for path in shop_data["paths"]:
        url = f"{base_url}{path}{quote(TEST_QUERY)}"
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            resp = urllib.request.urlopen(req, context=ctx, timeout=5)
            code = resp.status
            length = len(resp.read())
            resp.close()
            status = f"✅ {code} ({length} octets)"
            shop_results.append((path, code, url, True))
        except urllib.error.HTTPError as e:
            status = f"❌ {e.code}"
            shop_results.append((path, e.code, url, False))
        except Exception as e:
            status = f"⏱ timeout/error: {type(e).__name__}"
            shop_results.append((path, 0, url, False))
        print(f"  {path:40s} {status}")
        time.sleep(0.5)

    # Also test the homepage
    try:
        req = urllib.request.Request(base_url + "/", headers=headers)
        resp = urllib.request.urlopen(req, context=ctx, timeout=5)
        print(f"  {'/ (homepage)':40s} ✅ {resp.status}")
        resp.close()
    except Exception as e:
        print(f"  {'/ (homepage)':40s} ❌ {type(e).__name__}")

    results[shop_name] = shop_results

print(f"\n\n{'='*60}")
print("📊 RÉSULTATS")
print(f"{'='*60}")
for shop_name, shop_results in results.items():
    working = [r for r in shop_results if r[3]]
    print(f"\n{shop_name}: {len(working)} working pattern(s)")
    for path, code, url, ok in shop_results:
        if ok:
            print(f"  ✅ {path} → {code}")
