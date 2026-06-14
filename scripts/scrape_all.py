"""
Scrape tous les sites WoofPrix et génère public/data/products.json.

Utilisation : python scripts/scrape_all.py
S'exécute automatiquement chaque nuit via GitHub Actions (.github/workflows/scrape.yml).

Sites scrapés :
  maxizoo.fr, zoomalia.com, animalis.com, jardiland.com,
  truffaut.com, lafermedesanimaux.com, medor-et-compagnie.fr,
  produits-veto.com, france-veto.com
"""
import json
import os
import sys
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.base import BaseScraper, ScraperResult
from scrapers.maxizoo import MaxiZooScraper
from scrapers.zoomalia import ZoomaliaScraper
from scrapers.animalis import AnimalisScraper
from scrapers.jardiland import JardilandScraper
from scrapers.truffaut import TruffautScraper
from scrapers.laferme import LaFermeScraper
from scrapers.medor import MedorScraper
from scrapers.produitsveto import ProduitsVetoScraper
from scrapers.franceveto import FranceVetoScraper

# ── Catalogue statique (shops, categories, produits) ────────────────────────

SHOPS = [
    {"id": "zooplus", "name": "Zooplus", "url": "https://www.zooplus.fr", "logo": "🛒", "color": "#2D9B6F", "affiliate": True, "network": "awin"},
    {"id": "wanimo", "name": "Wanimo", "url": "https://www.wanimo.com", "logo": "🛒", "color": "#4A90D9", "affiliate": True, "network": "netaffiliation"},
    {"id": "pepette", "name": "Pepette", "url": "https://www.pepette.fr", "logo": "🛒", "color": "#E86C8B", "affiliate": True, "network": "awin"},
    {"id": "directvet", "name": "Direct-Vet", "url": "https://www.direct-vet.fr", "logo": "🛒", "color": "#27AE60", "affiliate": False, "network": None},
    {"id": "cernunos", "name": "Cernunos", "url": "https://www.cernunos.fr", "logo": "🛒", "color": "#8E44AD", "affiliate": False, "network": None},
    {"id": "santevet", "name": "Santévet", "url": "https://www.santevet.com", "logo": "🛒", "color": "#3498DB", "affiliate": False, "network": None},
    {"id": "amazon", "name": "Amazon", "url": "https://www.amazon.fr", "logo": "🛒", "color": "#FF9900", "affiliate": True, "network": "amazon"},
    {"id": "ultrapremium", "name": "Ultra Premium Direct", "url": "https://www.ultrapremiumdirect.com", "logo": "🛒", "color": "#E74C3C", "affiliate": False, "network": None},
    {"id": "maxizoo", "name": "MaxiZoo", "url": "https://www.maxizoo.fr", "logo": "🛒", "color": "#9B59B6", "affiliate": False, "network": None},
    {"id": "zoomalia", "name": "Zoomalia", "url": "https://www.zoomalia.com", "logo": "🛒", "color": "#1ABC9C", "affiliate": False, "network": None},
    {"id": "animalis", "name": "Animalis", "url": "https://www.animalis.com", "logo": "🛒", "color": "#F39C12", "affiliate": False, "network": None},
    {"id": "jardiland", "name": "Jardiland", "url": "https://www.jardiland.com", "logo": "🛒", "color": "#27AE60", "affiliate": False, "network": None},
    {"id": "truffaut", "name": "Truffaut", "url": "https://www.truffaut.com", "logo": "🛒", "color": "#2ECC71", "affiliate": False, "network": None},
    {"id": "laferme", "name": "La Ferme des Animaux", "url": "https://www.lafermedesanimaux.com", "logo": "🛒", "color": "#E67E22", "affiliate": False, "network": None},
    {"id": "medor", "name": "Médor & Compagnie", "url": "https://www.medor-et-compagnie.fr", "logo": "🛒", "color": "#95A5A6", "affiliate": False, "network": None},
    {"id": "petsonic", "name": "Petsonic", "url": "https://www.petsonic.com", "logo": "🛒", "color": "#34495E", "affiliate": False, "network": None},
    {"id": "produitsveto", "name": "Produits-Véto", "url": "https://www.produits-veto.com", "logo": "🛒", "color": "#16A085", "affiliate": False, "network": None},
    {"id": "franceveto", "name": "France-Véto", "url": "https://www.france-veto.com", "logo": "🛒", "color": "#2980B9", "affiliate": False, "network": None},
    {"id": "universveto", "name": "Univers-Véto", "url": "https://www.univers-veto.fr", "logo": "🛒", "color": "#8E44AD", "affiliate": False, "network": None},
]

SHOP_IDS = {s["id"] for s in SHOPS}

CATEGORIES = [
    {"id": "vermifuges", "name": "Vermifuges", "slug": "vermifuges", "emoji": "💊", "animal": "all"},
    {"id": "antiparasitaires", "name": "Antiparasitaires", "slug": "antiparasitaires", "emoji": "🐛", "animal": "all"},
    {"id": "croquettes-chien", "name": "Croquettes chien", "slug": "croquettes-chien", "emoji": "🍖", "animal": "dog"},
    {"id": "croquettes-chat", "name": "Croquettes chat", "slug": "croquettes-chat", "emoji": "🐟", "animal": "cat"},
    {"id": "patees-boites", "name": "Pâtées & boîtes", "slug": "patees-boites", "emoji": "🥫", "animal": "all"},
    {"id": "soins-hygiene", "name": "Soins & hygiène", "slug": "soins-hygiene", "emoji": "💉", "animal": "all"},
]

# Produits de référence : ce qu'on cherche sur chaque site
PRODUCT_CATALOG = [
    {"id": "milbemax-chien", "name": "Milbemax Chien", "slug": "milbemax-chien",
     "animal": "dog", "animal_label": "Chien", "category": "vermifuges", "category_label": "Vermifuge",
     "emoji": "💊", "description": "Comprimé vermifuge pour chiens contre les vers ronds et plats.",
     "search_terms": ["Milbemax", "Milbemax chien"]},
    {"id": "milbemax-chat", "name": "Milbemax Chat", "slug": "milbemax-chat",
     "animal": "cat", "animal_label": "Chat", "category": "vermifuges", "category_label": "Vermifuge",
     "emoji": "💊", "description": "Comprimé vermifuge pour chats contre les vers ronds et plats.",
     "search_terms": ["Milbemax chat"]},
    {"id": "frontline-combo-chat", "name": "Frontline Combo Chat", "slug": "frontline-combo-chat",
     "animal": "cat", "animal_label": "Chat", "category": "antiparasitaires", "category_label": "Antiparasitaire",
     "emoji": "🐛", "description": "Solution antiparasitaire externe pour chats.",
     "search_terms": ["Frontline combo chat"]},
    {"id": "frontline-combo-chien", "name": "Frontline Combo Chien", "slug": "frontline-combo-chien",
     "animal": "dog", "animal_label": "Chien", "category": "antiparasitaires", "category_label": "Antiparasitaire",
     "emoji": "🐛", "description": "Solution antiparasitaire pour chiens.",
     "search_terms": ["Frontline combo chien"]},
    {"id": "advocate-chat", "name": "Advocate Chat 0,4ml", "slug": "advocate-chat",
     "animal": "cat", "animal_label": "Chat", "category": "antiparasitaires", "category_label": "Antiparasitaire",
     "emoji": "🐛", "description": "Solution spot-on antiparasitaire pour chats.",
     "search_terms": ["Advocate chat"]},
    {"id": "drontal-chien", "name": "Drontal Chien", "slug": "drontal-chien",
     "animal": "dog", "animal_label": "Chien", "category": "vermifuges", "category_label": "Vermifuge",
     "emoji": "💊", "description": "Comprimé vermifuge large spectre pour chiens.",
     "search_terms": ["Drontal chien"]},
    {"id": "royal-canin-adult-10kg", "name": "Royal Canin Adult 10kg", "slug": "royal-canin-adult-10kg",
     "animal": "dog", "animal_label": "Chien", "category": "croquettes-chien", "category_label": "Croquettes",
     "emoji": "🍖", "description": "Croquettes pour chien adulte de taille moyenne.",
     "search_terms": ["Royal Canin adult 10kg", "Royal Canin 10kg"]},
    {"id": "purina-one-chat", "name": "Purina One Chat 1,5kg", "slug": "purina-one-chat",
     "animal": "cat", "animal_label": "Chat", "category": "croquettes-chat", "category_label": "Croquettes",
     "emoji": "🐟", "description": "Croquettes pour chat adulte.",
     "search_terms": ["Purina One chat", "Purina One 1.5kg"]},
    {"id": "hill-prescription-dog", "name": "Hill's Prescription Diet 12kg", "slug": "hill-prescription-dog",
     "animal": "dog", "animal_label": "Chien", "category": "croquettes-chien", "category_label": "Croquettes",
     "emoji": "🍖", "description": "Alimentation diététique pour chiens.",
     "search_terms": ["Hill's Prescription Diet", "Hills Prescription 12kg"]},
    {"id": "frolic-chien", "name": "Frolic Chien 10kg", "slug": "frolic-chien",
     "animal": "dog", "animal_label": "Chien", "category": "croquettes-chien", "category_label": "Croquettes",
     "emoji": "🍖", "description": "Croquettes complètes pour chien au bœuf.",
     "search_terms": ["Frolic chien 10kg"]},
    {"id": "whiskas-chat", "name": "Whiskas Chat 1,4kg", "slug": "whiskas-chat",
     "animal": "cat", "animal_label": "Chat", "category": "croquettes-chat", "category_label": "Croquettes",
     "emoji": "🐟", "description": "Croquettes pour chat adulte au poulet.",
     "search_terms": ["Whiskas chat 1.4kg"]},
    {"id": "revolution-chat", "name": "Revolution Chat 3mg", "slug": "revolution-chat",
     "animal": "cat", "animal_label": "Chat", "category": "antiparasitaires", "category_label": "Antiparasitaire",
     "emoji": "🐛", "description": "Solution spot-on contre puces, tiques et vers du cœur.",
     "search_terms": ["Revolution chat"]},
    {"id": "applaws-chien", "name": "Applaws Chien 2kg", "slug": "applaws-chien",
     "animal": "dog", "animal_label": "Chien", "category": "croquettes-chien", "category_label": "Croquettes",
     "emoji": "🍖", "description": "Croquettes naturelles pour chien, sans céréales.",
     "search_terms": ["Applaws chien 2kg"]},
]

# Prix de secours (lorsque le scraping échoue)
FALLBACK_PRICES = {
    "milbemax-chien":  [("zooplus", 5.49, 4.99), ("wanimo", 6.20, 3.90), ("santevet", 9.50, 0)],
    "milbemax-chat":   [("zooplus", 6.90, 4.99), ("wanimo", 7.50, 3.90), ("santevet", 10.10, 0)],
    "frontline-combo-chat":  [("wanimo", 8.90, 3.90), ("zooplus", 9.40, 4.99), ("santevet", 14.30, 0)],
    "frontline-combo-chien": [("zooplus", 11.90, 4.99), ("wanimo", 12.50, 3.90), ("amazon", 14.99, 0)],
    "advocate-chat":  [("zooplus", 12.90, 4.99), ("wanimo", 14.50, 3.90), ("santevet", 19.90, 0)],
    "drontal-chien":  [("zooplus", 7.90, 4.99), ("wanimo", 8.80, 3.90), ("santevet", 11.30, 0)],
    "royal-canin-adult-10kg": [("zooplus", 42.90, 0), ("wanimo", 46.50, 3.90), ("maxizoo", 57.00, 0)],
    "purina-one-chat": [("zooplus", 12.99, 4.99), ("wanimo", 14.20, 3.90), ("zoomalia", 16.50, 0)],
    "hill-prescription-dog": [("zooplus", 68.50, 0), ("wanimo", 72.00, 3.90), ("maxizoo", 79.90, 0)],
    "frolic-chien":   [("zooplus", 24.99, 0), ("wanimo", 27.50, 3.90), ("jardiland", 29.90, 0)],
    "whiskas-chat":   [("zooplus", 10.50, 4.99), ("zoomalia", 11.99, 0), ("jardiland", 13.40, 0)],
    "revolution-chat": [("wanimo", 15.90, 3.90), ("zooplus", 17.40, 4.99), ("santevet", 22.10, 0)],
    "applaws-chien":  [("wanimo", 18.90, 3.90), ("zooplus", 19.50, 0), ("zoomalia", 21.40, 0)],
}

# Mapping: shop_id → URL pattern pour générer un lien si non trouvé
SHOP_URL_PATTERNS = {
    "zooplus": "https://www.zooplus.fr/shop/{}",
    "wanimo": "https://www.wanimo.com/{}.html",
    "amazon": "https://www.amazon.fr/s?k={}",
    "maxizoo": "https://www.maxizoo.fr/catalogsearch/result/?q={}",
    "zoomalia": "https://www.zoomalia.com/recherche?q={}",
    "animalis": "https://www.animalis.com/recherche?q={}",
    "jardiland": "https://www.jardiland.com/search?q={}",
    "truffaut": "https://www.truffaut.com/search?q={}",
    "laferme": "https://www.lafermedesanimaux.com/recherche?q={}",
    "medor": "https://www.medor-et-compagnie.fr/search?q={}",
    "produitsveto": "https://www.produits-veto.com/recherche?q={}",
    "franceveto": "https://www.france-veto.com/recherche?q={}",
    "santevet": "https://www.santevet.com/recherche?q={}",
    "pepette": "https://www.pepette.fr/recherche?q={}",
    "directvet": "https://www.direct-vet.fr/recherche?q={}",
    "cernunos": "https://www.cernunos.fr/recherche?q={}",
    "ultrapremium": "https://www.ultrapremiumdirect.com/recherche?q={}",
    "petsonic": "https://www.petsonic.com/recherche?q={}",
    "universveto": "https://www.univers-veto.fr/recherche?q={}",
}


# ── Fonctions utilitaires ────────────────────────────────────────────────────

def build_url(shop_id: str, product_name: str, scraped_url: str = "") -> str:
    """Construit la meilleure URL possible pour un produit chez un shop."""
    if scraped_url and scraped_url.startswith("http"):
        return scraped_url
    pattern = SHOP_URL_PATTERNS.get(shop_id)
    if pattern:
        from urllib.parse import quote
        return pattern.format(quote(product_name.lower().replace(" ", "-")))
    shop = next((s for s in SHOPS if s["id"] == shop_id), None)
    return f"https://www.{shop_id}.fr" if not shop else shop["url"]


def normalize_name(name: str) -> str:
    """Normalise un nom de produit pour la comparaison."""
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def score_match(result_name: str, search_terms: list[str]) -> int:
    """Score de correspondance entre un résultat scrappé et les termes de recherche."""
    n = normalize_name(result_name)
    score = 0
    for term in search_terms:
        tn = normalize_name(term)
        if tn in n:
            score += 10
        words = tn.split()
        matches = sum(1 for w in words if w in n)
        if words:
            score += int(matches / len(words) * 5)
    return score


# ── Orchestrateur de scraping ────────────────────────────────────────────────

def scrape_all() -> list[dict]:
    """Scrape chaque produit sur tous les sites et retourne la liste enrichie."""

    scrapers: list[BaseScraper] = [
        MaxiZooScraper(),
        ZoomaliaScraper(),
        AnimalisScraper(),
        JardilandScraper(),
        TruffautScraper(),
        LaFermeScraper(),
        MedorScraper(),
        ProduitsVetoScraper(),
        FranceVetoScraper(),
    ]

    scraper_map = {s.name: s for s in scrapers}

    products_output = []

    for product in PRODUCT_CATALOG:
        pid = product["id"]
        print(f"\n🔍 [{pid}] {product['name']}")

        all_prices = {}

        # 1. Scraping de chaque site pour ce produit
        for term in product["search_terms"]:
            for scraper in scrapers:
                sid = scraper.name
                if sid in all_prices:
                    continue
                print(f"  → {scraper.name}… ", end="", flush=True)
                try:
                    results = scraper.search_product(term)
                except Exception as e:
                    print(f"⚠ erreur: {e}")
                    continue

                if not results:
                    print("∅")
                    continue

                best_match = None
                best_score = 0
                for r in results:
                    s = score_match(r.product_name, [term, product["name"]])
                    if s > best_score:
                        best_score = s
                        best_match = r

                if best_match and best_score >= 5:
                    all_prices[sid] = {
                        "shop": sid,
                        "price": round(best_match.price, 2),
                        "shipping": best_match.shipping,
                        "url": build_url(sid, product["name"], best_match.url),
                        "in_stock": best_match.in_stock,
                    }
                    print(f"✓ {best_match.price:.2f}€")
                else:
                    print("∅ (aucune correspondance)")

        # 2. Fallback : prix statiques pour les shops non scrapés
        fallback = FALLBACK_PRICES.get(pid, [])
        for shop_id, price, shipping in fallback:
            if shop_id not in all_prices:
                all_prices[shop_id] = {
                    "shop": shop_id,
                    "price": price,
                    "shipping": shipping,
                    "url": build_url(shop_id, product["name"]),
                    "in_stock": True,
                }

        # 3. Trier les prix du moins cher au plus cher
        sorted_prices = sorted(all_prices.values(), key=lambda p: p["price"])

        products_output.append({
            "id": product["id"],
            "name": product["name"],
            "slug": product["slug"],
            "animal": product["animal"],
            "animalLabel": product["animal_label"],
            "category": product["category"],
            "categoryLabel": product["category_label"],
            "emoji": product["emoji"],
            "description": product["description"],
            "prices": sorted_prices,
        })

        print(f"  → {len(sorted_prices)} prix trouvés (meilleur: {sorted_prices[0]['price']:.2f}€)" if sorted_prices
              else "  → ⚠ aucun prix trouvé")

    # Fermeture des clients HTTP
    for s in scrapers:
        s.close()

    return products_output


# ── Génération du JSON final ─────────────────────────────────────────────────

def main():
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(project_root, "public", "data", "products.json")

    print("=" * 50)
    print("WoofPrix — Scraping automatique des prix")
    print("=" * 50)

    products = scrape_all()

    total_prices = sum(len(p["prices"]) for p in products)
    shop_ids_found = set()
    for p in products:
        for pr in p["prices"]:
            shop_ids_found.add(pr["shop"])

    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "stats": {
            "products_count": len(products),
            "shops_count": len(shop_ids_found),
            "prices_count": total_prices,
        },
        "shops": SHOPS,
        "categories": CATEGORIES,
        "products": products,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Scraping terminé :")
    print(f"   {len(products)} produits")
    print(f"   {total_prices} prix")
    print(f"   {len(shop_ids_found)} sites avec données")
    print(f"   → {output_path}")


if __name__ == "__main__":
    main()
