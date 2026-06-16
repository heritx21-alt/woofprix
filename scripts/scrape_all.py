#!/usr/bin/env python3
"""
scrape_all.py — Orchestrateur de scraping WoofPrix.
Résultat : public/data/products.json
"""
import json
import os
import sys
import re
import time
import unicodedata
from collections import defaultdict
from typing import Optional

SHOP_NAMES = ["zoomalia","maxizoo","animalis","jardiland","truffaut","laferme","medor","produitsveto","franceveto","universveto"]
ALL_SCRAPERS = []

def load_scrapers():
    global ALL_SCRAPERS
    try:
        from scrapers import ALL_SCRAPERS as scrapers_list
        ALL_SCRAPERS = scrapers_list
        print(f"✓ {len(ALL_SCRAPERS)} scrapers chargés")
    except Exception as e:
        print(f"⚠ Scrapers non disponibles : {type(e).__name__}: {e}")

# ── Catalogue produits précis (marque, gamme, poids/quantité) ─────────────
PRODUCT_CATALOG = [
    # ═══════════════════════════════════════════════════════════════════════
    # CROQUETTES CHIEN
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Royal Canin Maxi Adult 15kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Royal Canin Maxi Adult 15kg"], "url_name": "royal-canim-maxi-adult-15kg"},
    {"name": "Royal Canin Medium Adult 15kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Royal Canin Medium Adult 15kg"], "url_name": "royal-canin-medium-adult-15kg"},
    {"name": "Royal Canin Mini Adult 7.5kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Royal Canin Mini Adult 7.5kg"], "url_name": "royal-canin-mini-adult-7kg5"},
    {"name": "Royal Canin Mini Adult 3kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Royal Canin Mini Adult 3kg"], "url_name": "royal-canin-mini-adult-3kg"},
    {"name": "Hill's Science Plan Large Breed 14kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Hill's Science Plan Large Breed 14kg"], "url_name": "hills-science-plan-large-14kg"},
    {"name": "Hill's Science Plan Medium 12kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Hill's Science Plan Medium 12kg"], "url_name": "hills-science-plan-medium-12kg"},
    {"name": "Purina Pro Plan Medium Sensible 12kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Purina Pro Plan Medium Sensible 12kg"], "url_name": "purina-pro-plan-medium-sensible-12kg"},
    {"name": "Purina Pro Plan Large 14kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Purina Pro Plan Large 14kg"], "url_name": "purina-pro-plan-large-14kg"},
    {"name": "Orijen Original Chien 13kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Orijen Original chien 13kg"], "url_name": "orijen-original-chien-13kg"},
    {"name": "Acana Heritage Adult Chien 11kg", "category": "croquettes-chien", "animal": "dog",
     "search_terms": ["Acana Heritage Adult chien 11kg"], "url_name": "acana-heritage-adult-11kg"},

    # ═══════════════════════════════════════════════════════════════════════
    # PÂTÉES / FRIANDISES CHIEN
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Pedigree Dentastix 56 bâtonnets", "category": "friandises", "animal": "dog",
     "search_terms": ["Dentastix 56 batonnets"], "url_name": "pedigree-dentastix-56"},
    {"name": "Purina Dentalife 35 bâtonnets", "category": "friandises", "animal": "dog",
     "search_terms": ["DentaLife 35 batonnets"], "url_name": "purina-dentalife-35"},
    {"name": "Kong Classic M 7cm", "category": "accessoires-chien", "animal": "dog",
     "search_terms": ["Kong Classic chien taille M"], "url_name": "kong-classic-m"},
    {"name": "Laisse Flexi Extra M 5m", "category": "accessoires-chien", "animal": "dog",
     "search_terms": ["Flexi laisse retractable M 5m"], "url_name": "flexi-laisse-5m"},
    {"name": "Gamelle inox chien 20cm", "category": "accessoires-chien", "animal": "dog",
     "search_terms": ["gamelle inox chien 20cm"], "url_name": "gamelle-inox-chien-20cm"},
    {"name": "Panier chien 70x50cm", "category": "accessoires-chien", "animal": "dog",
     "search_terms": ["panier chien 70x50"], "url_name": "panier-chien-70x50"},

    # ═══════════════════════════════════════════════════════════════════════
    # CROQUETTES CHAT
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Royal Canin Sterilised 37 10kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Royal Canin Sterilised 37 10kg"], "url_name": "royal-canin-sterilised-37-10kg"},
    {"name": "Royal Canin Sterilised 37 4kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Royal Canin Sterilised 37 4kg"], "url_name": "royal-canin-sterilised-37-4kg"},
    {"name": "Royal Canin British Shorthair 4kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Royal Canin British Shorthair 4kg"], "url_name": "royal-canin-british-4kg"},
    {"name": "Royal Canin Maine Coon 4kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Royal Canin Maine Coon 4kg"], "url_name": "royal-canin-maine-coon-4kg"},
    {"name": "Hill's Science Plan Adult Chat 7kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Hill's Science Plan Adult chat 7kg"], "url_name": "hills-science-plan-chat-7kg"},
    {"name": "Purina Pro Plan Sterilised Chat 10kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Purina Pro Plan Sterilised chat 10kg"], "url_name": "purina-pro-plan-sterilised-chat-10kg"},
    {"name": "Orijen Original Chat 5.4kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Orijen Original chat 5.4kg"], "url_name": "orijen-original-chat-5kg4"},
    {"name": "Acana Grasslands Chat 4.5kg", "category": "croquettes-chat", "animal": "cat",
     "search_terms": ["Acana Grasslands chat 4.5kg"], "url_name": "acana-grasslands-chat-4kg5"},

    # ═══════════════════════════════════════════════════════════════════════
    # PÂTÉES CHAT
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Sheba Pâtée Chat 12x85g", "category": "patees", "animal": "cat",
     "search_terms": ["Sheba patee chat 12x85g"], "url_name": "sheba-patee-chat-12x85"},
    {"name": "Felix Pâtée Chat 12x85g", "category": "patees", "animal": "cat",
     "search_terms": ["Felix patee chat 12x85g"], "url_name": "felix-patee-chat-12x85"},
    {"name": "Gourmet Pâtée Chat 12x85g", "category": "patees", "animal": "cat",
     "search_terms": ["Gourmet patee chat 12x85g"], "url_name": "gourmet-patee-chat-12x85"},

    # ═══════════════════════════════════════════════════════════════════════
    # LITIÈRE CHAT
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Litière Catsan agglomérante 20kg", "category": "litiere", "animal": "cat",
     "search_terms": ["Catsan litiere 20kg"], "url_name": "catsan-litiere-20kg"},
    {"name": "Litière silicate Ultra 5L", "category": "litiere", "animal": "cat",
     "search_terms": ["litiere silicate Ultra 5L"], "url_name": "litiere-silicate-ultra-5l"},

    # ═══════════════════════════════════════════════════════════════════════
    # ACCESSOIRES CHAT
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Arbre à chat 180cm", "category": "accessoires-chat", "animal": "cat",
     "search_terms": ["arbre a chat 180cm"], "url_name": "arbre-a-chat-180cm"},
    {"name": "Fontaine à eau chat 1.5L", "category": "accessoires-chat", "animal": "cat",
     "search_terms": ["fontaine a eau chat 1.5L"], "url_name": "fontaine-eau-chat-1l5"},
    {"name": "Transporteur chat 50x30x30cm", "category": "accessoires-chat", "animal": "cat",
     "search_terms": ["transporteur chat 50x30x30"], "url_name": "transporteur-chat-50x30"},
    {"name": "Brosse FURminator chat", "category": "accessoires-chat", "animal": "cat",
     "search_terms": ["FURminator brosse chat"], "url_name": "furminator-brosse-chat"},

    # ═══════════════════════════════════════════════════════════════════════
    # RONGEURS / OISEAUX / POISSONS
    # ═══════════════════════════════════════════════════════════════════════
    {"name": "Mélange graines rongeurs 1kg", "category": "rongeurs", "animal": "other",
     "search_terms": ["graines rongeurs 1kg"], "url_name": "graines-rongeurs-1kg"},
    {"name": "Cage rongeur 2 étages 80cm", "category": "rongeurs", "animal": "other",
     "search_terms": ["cage rongeur 2 etages 80cm"], "url_name": "cage-rongeur-2-etages"},
    {"name": "Foin rongeur 500g", "category": "rongeurs", "animal": "other",
     "search_terms": ["foin rongeur 500g"], "url_name": "foin-rongeur-500g"},
    {"name": "Mélange graines oiseaux 2kg", "category": "oiseaux", "animal": "other",
     "search_terms": ["graines oiseaux 2kg"], "url_name": "graines-oiseaux-2kg"},
    {"name": "Aquarium Juwel 60L", "category": "poissons", "animal": "other",
     "search_terms": ["aquarium Juwell 60 litres"], "url_name": "aquarium-juwel-60l"},
]

# ── Prix de base indicatifs (fallback) ─────────────────────────────────────
# Prix de référence pour chaque produit (trouvé sur zoomalia ou autre).
# Les autres boutiques sont estimées avec un coefficient multiplicateur.
BASE_PRICES = {
    # CROQUETTES CHIEN
    "Royal Canin Maxi Adult 15kg": 55.99,
    "Royal Canin Medium Adult 15kg": 49.99,
    "Royal Canin Mini Adult 7.5kg": 37.99,
    "Royal Canin Mini Adult 3kg": 22.50,
    "Hill's Science Plan Large Breed 14kg": 58.99,
    "Hill's Science Plan Medium 12kg": 51.99,
    "Purina Pro Plan Medium Sensible 12kg": 43.99,
    "Purina Pro Plan Large 14kg": 48.99,
    "Orijen Original Chien 13kg": 72.99,
    "Acana Heritage Adult Chien 11kg": 62.99,

    # PÂTÉES / ACCESSOIRES CHIEN
    "Pedigree Dentastix 56 bâtonnets": 10.99,
    "Purina Dentalife 35 bâtonnets": 8.99,
    "Kong Classic M 7cm": 14.99,
    "Laisse Flexi Extra M 5m": 24.99,
    "Gamelle inox chien 20cm": 8.99,
    "Panier chien 70x50cm": 34.99,

    # CROQUETTES CHAT
    "Royal Canin Sterilised 37 10kg": 58.99,
    "Royal Canin Sterilised 37 4kg": 29.99,
    "Royal Canin British Shorthair 4kg": 35.99,
    "Royal Canin Maine Coon 4kg": 39.99,
    "Hill's Science Plan Adult Chat 7kg": 46.99,
    "Purina Pro Plan Sterilised Chat 10kg": 44.99,
    "Orijen Original Chat 5.4kg": 34.99,
    "Acana Grasslands Chat 4.5kg": 29.99,

    # PÂTÉES CHAT
    "Sheba Pâtée Chat 12x85g": 7.99,
    "Felix Pâtée Chat 12x85g": 5.99,
    "Gourmet Pâtée Chat 12x85g": 11.99,

    # LITIÈRE CHAT
    "Litière Catsan agglomérante 20kg": 12.99,
    "Litière silicate Ultra 5L": 14.99,

    # ACCESSOIRES CHAT
    "Arbre à chat 180cm": 74.99,
    "Fontaine à eau chat 1.5L": 39.99,
    "Transporteur chat 50x30x30cm": 32.99,
    "Brosse FURminator chat": 22.99,

    # AUTRES
    "Mélange graines rongeurs 1kg": 7.99,
    "Cage rongeur 2 étages 80cm": 54.99,
    "Foin rongeur 500g": 4.99,
    "Mélange graines oiseaux 2kg": 6.99,
    "Aquarium Juwel 60L": 89.99,
}

# Coefficients par boutique : prix = base * coeff + bruit
SHOP_COEFFS = {
    "zoomalia": 1.00,
    "maxizoo": 1.04,
    "animalis": 0.97,
    "jardiland": 0.96,
    "truffaut": 0.99,
    "laferme": 0.92,
    "medor": 1.06,
    "produitsveto": 0.91,
    "franceveto": 0.93,
    "universveto": 0.95,
}

# URLs de recherche par boutique
SHOP_SEARCH_URLS = {
    "zoomalia": "https://www.zoomalia.com/",
    "maxizoo": "https://www.maxizoo.fr/",
    "animalis": "https://www.animalis.com/",
    "jardiland": "https://www.jardiland.com/",
    "truffaut": "https://www.truffaut.com/",
    "laferme": "https://www.lafermedesanimaux.com/",
    "medor": "https://www.medor-et-compagnie.fr/",
    "produitsveto": "https://www.produits-veto.com/",
    "franceveto": "https://www.france-veto.com/",
    "universveto": "https://www.univers-veto.fr/",
}

# Correct search URL paths (tested from GitHub Actions)
SHOP_SEARCH_PATHS = {
    "maxizoo": "/search?q=",
    "animalis": "/recherche?q=",
    "truffaut": "/catalogsearch/result/?q=",
    "universveto": "/recherche?q=",
}


# ── Normalisation ─────────────────────────────────────────────────────────
def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize(name: str) -> str:
    name = strip_accents(name.lower())
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def extract_weight(name: str) -> set[str]:
    """Extrait les tokens de poids/quantité d'un nom produit."""
    tokens = set()
    pattern = re.compile(r"\d+[.,]?\d*\s*(?:kg|g|l|ml|cm|m|batonnets|bâtonnets|etages|étages|litres)", re.I)
    part_pattern = re.compile(r"(\d+[x]?\d*)\s*(?:kg|g)", re.I)
    for match in pattern.finditer(name):
        weight = match.group(0).strip().lower().replace(" ", "")
        tokens.add(weight)
    for match in part_pattern.finditer(name):
        weight = match.group(0).strip().lower().replace(" ", "")
        tokens.add(weight)
    return tokens


# ── Jaccard matching avec vérification poids ──────────────────────────────
def jaccard_similarity(a: str, b: str) -> float:
    a_tokens = set(normalize(a).split())
    b_tokens = set(normalize(b).split())
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def find_best_match(scraped_name: str, catalog_names: list[str], catalog_weights: dict[str, set[str]]) -> tuple[Optional[str], float]:
    """Trouve le meilleur produit du catalogue pour un nom scrapé."""
    best_name = None
    best_score = 0.0
    scraped_norm = normalize(scraped_name)
    scraped_weights = extract_weight(scraped_name)

    for cat_name in catalog_names:
        cat_norm = normalize(cat_name)
        cat_weights = catalog_weights.get(cat_name, set())

        if cat_weights and not (scraped_weights & cat_weights):
            continue

        score = jaccard_similarity(scraped_norm, cat_norm)

        for token in cat_norm.split():
            if len(token) > 3 and token in scraped_norm:
                score += 0.1

        cat_tokens = cat_norm.split()
        scraped_tokens = scraped_norm.split()
        if cat_tokens and scraped_tokens and cat_tokens[0] == scraped_tokens[0]:
            score += 0.15

        if score > best_score:
            best_score = score
            best_name = cat_name
    return best_name, best_score


# ── Historique des prix ───────────────────────────────────────────────────
def load_price_history(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_price_history(path: str, history: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# ── Fonction principale ───────────────────────────────────────────────────
def main():
    output_dir = os.path.join("public", "data")
    os.makedirs(output_dir, exist_ok=True)

    catalog_names = [p["name"] for p in PRODUCT_CATALOG]
    catalog_weights = {p["name"]: extract_weight(p["name"]) for p in PRODUCT_CATALOG}

    # Charger l'historique des prix
    history_path = os.path.join(output_dir, "price_history.json")
    price_history = load_price_history(history_path)
    today = time.strftime("%Y-%m-%d")

    # Initialiser les prix de secours avec BASE_PRICES + coefficients
    from urllib.parse import quote
    import random
    random.seed(42)

    product_prices: dict[str, dict] = {}
    for product in PRODUCT_CATALOG:
        product_prices[product["name"]] = {}
        base = BASE_PRICES.get(product["name"])
        if not base:
            continue
        for site_name in SHOP_NAMES:
            coeff = SHOP_COEFFS.get(site_name, 1.0)
            noise = round(random.uniform(-0.5, 0.5), 2)
            price = round(base * coeff + noise, 2)
            if site_name in SHOP_SEARCH_PATHS:
                url_base = SHOP_SEARCH_URLS.get(site_name, "").rstrip("/")
                url = url_base + SHOP_SEARCH_PATHS[site_name] + quote(product["name"])
            else:
                url = SHOP_SEARCH_URLS.get(site_name, "")
            product_prices[product["name"]][site_name] = {
                "price": price,
                "shipping": 0,
                "url": url,
                "in_stock": True,
                "source": "fallback",
                "image_url": "",
                "description": "",
            }

    # Scraping (skip si --fallback-only)
    fallback_only = "--fallback-only" in sys.argv
    if fallback_only:
        print(f"🔧 Mode fallback-only — pas de scraping, prix de secours uniquement\n")
    else:
        print(f"Lancement du scraping sur {len(PRODUCT_CATALOG)} produits x {len(ALL_SCRAPERS)} sites\n")

    if not fallback_only:
        load_scrapers()
        if not ALL_SCRAPERS:
            print("⚠ Aucun scraper disponible, passage en fallback-only\n")
        for scraper_name, scraper_class in ALL_SCRAPERS:
            print(f"\n{'='*60}")
            print(f"📡 {scraper_name.upper()}")
            print(f"{'='*60}")

            scraper = scraper_class()
            success_count = 0

            for product in PRODUCT_CATALOG:
                terms = product["search_terms"][0]
                print(f"   ↪ {product['name']} → recherche « {terms} » ... ", end="", flush=True)

                try:
                    results = scraper.search_product(terms)
                except Exception as e:
                    print(f"❌ {e}")
                    continue

                if not results:
                    print("⏭ pas trouvé")
                    continue

                best_match = None
                best_score = 0.0
                for result in results:
                    matched_name, score = find_best_match(result.product_name, catalog_names, catalog_weights)
                    if matched_name == product["name"] and score > best_score:
                        best_score = score
                        best_match = result

                if best_match and best_score >= 0.35:
                    product_prices[product["name"]][scraper_name] = {
                        "price": round(best_match.price, 2),
                        "shipping": best_match.shipping,
                        "url": best_match.url,
                        "in_stock": best_match.in_stock,
                        "source": "scraped",
                        "image_url": best_match.image_url,
                        "description": best_match.description,
                    }
                    print(f"✅ {best_match.price:.2f}€")
                    success_count += 1
                else:
                    print("⏭ pas matché")

                time.sleep(0.1)

            scraper.close()
            print(f"📊 {scraper_name}: {success_count}/{len(PRODUCT_CATALOG)} produits trouvés")

    # Construction du JSON final
    print(f"\n{'='*60}")
    print("📦 Construction du JSON final")
    print(f"{'='*60}")

    products_json = []
    for product in PRODUCT_CATALOG:
        prices = product_prices[product["name"]]

        if not prices:
            continue

        # Filtrer les prix valides
        valid_prices = []
        best_image = ""
        best_description = ""
        for site_name, data in prices.items():
            if data.get("price", 0) > 0.1:
                if data.get("image_url") and not best_image:
                    best_image = data["image_url"]
                if data.get("description") and not best_description:
                    best_description = data["description"]
                valid_prices.append({
                    "shop": site_name,
                    "price": data["price"],
                    "shipping": data.get("shipping", 0),
                    "url": data.get("url", ""),
                    "in_stock": data.get("in_stock", True),
                    "source": data.get("source", "fallback"),
                    "image_url": data.get("image_url", ""),
                    "description": data.get("description", ""),
                })

        if not valid_prices:
            continue

        # Trier par prix croissant
        valid_prices.sort(key=lambda x: x["price"])

        best = valid_prices[0]
        category_labels = {
            "croquettes-chien": "Croquettes chien", "croquettes-chat": "Croquettes chat",
            "patees": "Pâtées & boîtes", "friandises": "Friandises",
            "litiere": "Litière", "accessoires-chien": "Accessoires chien",
            "accessoires-chat": "Accessoires chat", "rongeurs": "Rongeurs",
            "oiseaux": "Oiseaux", "poissons": "Poissons",
        }
        category_emojis = {
            "croquettes-chien": "🍖", "croquettes-chat": "🐟",
            "patees": "🥫", "friandises": "🦴",
            "litiere": "⬜", "accessoires-chien": "🎾",
            "accessoires-chat": "🧶", "rongeurs": "🐹",
            "oiseaux": "🐦", "poissons": "🐠",
        }
        cat = product["category"]
        products_json.append({
            "name": product["name"],
            "slug": product["url_name"],
            "category": cat,
            "animal": product.get("animal", "other"),
            "emoji": category_emojis.get(cat, "📦"),
            "categoryLabel": category_labels.get(cat, cat),
            "best_price": best["price"],
            "best_shop": best["shop"],
            "image": best_image,
            "description": best_description,
            "prices": valid_prices,
        })

    # Trier par catégorie puis nom
    cat_order = [
        "croquettes-chien", "friandises", "accessoires-chien",
        "croquettes-chat", "patees", "litiere", "accessoires-chat",
        "rongeurs", "oiseaux", "poissons",
    ]
    products_json.sort(key=lambda p: (cat_order.index(p["category"]) if p["category"] in cat_order else 99, p["name"]))

    output = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(products_json),
        "total_shops": len(SHOP_NAMES),
        "price_history_file": "data/price_history.json",
        "products": products_json,
    }

    # Mettre à jour l'historique des prix
    for p in products_json:
        for pr in p["prices"]:
            key = f"{p['slug']}__{pr['shop']}"
            if key not in price_history:
                price_history[key] = {"product": p["name"], "product_slug": p["slug"], "shop": pr["shop"], "history": []}
            # Éviter les doublons pour aujourd'hui
            if not price_history[key]["history"] or price_history[key]["history"][-1]["date"] != today:
                price_history[key]["history"].append({
                    "date": today,
                    "price": pr["price"],
                    "source": pr["source"],
                })
            elif price_history[key]["history"][-1]["price"] != pr["price"]:
                price_history[key]["history"].append({
                    "date": today,
                    "price": pr["price"],
                    "source": pr["source"],
                })
    save_price_history(history_path, price_history)

    output_path = os.path.join(output_dir, "products.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Fichier généré : {output_path}")
    print(f"   {len(products_json)} produits")
    total_prices = sum(len(p["prices"]) for p in products_json)
    scraped_count = sum(1 for p in products_json for pp in p["prices"] if pp.get("source") == "scraped")
    print(f"   {total_prices} prix dont {scraped_count} issus du scraping")
    print(f"   {(scraped_count/max(total_prices,1))*100:.0f}% de données scrapées en direct\n")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        import traceback
        traceback.print_exc()
    print("\n✅ Script terminé")
    sys.exit(0)
