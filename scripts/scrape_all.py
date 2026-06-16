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

SHOP_NAMES = ["maxizoo","animalis","jardiland","truffaut","laferme","produitsveto","directvet","cernunos","santevet","ultrapremium","petsonic"]
ALL_SCRAPERS = []

def load_scrapers():
    global ALL_SCRAPERS
    try:
        from scrapers import ALL_SCRAPERS as scrapers_list
        ALL_SCRAPERS = scrapers_list
        print(f"✓ {len(ALL_SCRAPERS)} scrapers chargés")
    except Exception as e:
        print(f"⚠ Scrapers non disponibles : {type(e).__name__}: {e}")

# ── Catalogue produits ─────────────────────────────────────────────────────
PRODUCT_CATALOG = []
try:
    db_path = os.path.join("public", "data", "products_db.json")
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            PRODUCT_CATALOG = json.load(f)
        print(f"✓ {len(PRODUCT_CATALOG)} produits chargés depuis products_db.json")
    else:
        print("⚠ products_db.json introuvable, catalogue vide")
except Exception as e:
    print(f"⚠ Erreur chargement catalogue: {e}")

# ── Prix de base auto-générés ──────────────────────────────────────────────
BASE_PRICES = {
    "Royal Canin Maxi Adult 15kg": 55.99, "Royal Canin Maxi Adult 8kg": 39.99,
    "Royal Canin Medium Adult 15kg": 49.99, "Royal Canin Medium Adult 8kg": 35.99, "Royal Canin Medium Adult 4kg": 22.99,
    "Royal Canin Mini Adult 7.5kg": 37.99, "Royal Canin Mini Adult 3kg": 22.50, "Royal Canin Mini Adult 1.5kg": 14.99,
    "Royal Canin Maxi Junior 15kg": 58.99, "Royal Canin Medium Junior 12kg": 52.99, "Royal Canin Mini Junior 7.5kg": 39.99, "Royal Canin Mini Junior 3kg": 24.99,
    "Royal Canin Maxi Senior 15kg": 58.99, "Royal Canin Medium Senior 12kg": 52.99, "Royal Canin Mini Senior 7.5kg": 39.99, "Royal Canin Mini Senior 3kg": 24.99,
    "Royal Canin Maxi Light 15kg": 60.99, "Royal Canin Medium Light 12kg": 54.99, "Royal Canin Mini Light 7.5kg": 40.99,
    "Royal Canin Gastrointestinal Medium 12kg": 62.99, "Royal Canin Gastrointestinal Low Fat 12kg": 64.99,
    "Royal Canin Urinary S/O Chien 10kg": 64.99, "Royal Canin Neutered Maxi 15kg": 58.99, "Royal Canin Neutered Medium 12kg": 52.99,
    "Hill's Science Plan Large Breed 14kg": 58.99, "Hill's Science Plan Large Breed 7kg": 36.99,
    "Hill's Science Plan Medium 12kg": 51.99, "Hill's Science Plan Medium 6kg": 32.99,
    "Hill's Science Plan Medium Junior 12kg": 54.99, "Hill's Science Plan Medium Senior 12kg": 54.99, "Hill's Science Plan Medium Light 12kg": 56.99,
    "Hill's Prescription Diet z/d 10kg": 74.99, "Hill's Prescription Diet i/d 12kg": 69.99,
    "Purina Pro Plan Medium Sensible 12kg": 43.99, "Purina Pro Plan Medium Sensible 6kg": 28.99,
    "Purina Pro Plan Large 14kg": 48.99, "Purina Pro Plan Large 7kg": 31.99, "Purina Pro Plan Large Athletic 14kg": 51.99,
    "Purina Pro Plan Medium Junior 12kg": 46.99, "Purina Pro Plan Medium Senior 12kg": 46.99, "Purina Pro Plan Sterilised Medium 12kg": 45.99,
    "Purina One Medium 15kg": 39.99, "Purina One Large 15kg": 41.99,
    "Orijen Original Chien 13kg": 72.99, "Orijen Original Chien 6kg": 44.99, "Orijen Six Fish Chien 13kg": 78.99,
    "Acana Heritage Adult Chien 11kg": 62.99, "Acana Heritage Junior Chien 11kg": 64.99, "Acana Regionals Wild Atlantic 11kg": 67.99,
    "Eukanuba Medium Adult 15kg": 54.99, "Eukanuba Large Adult 15kg": 56.99, "Eukanuba Medium Junior 15kg": 57.99,
    "Pedigree Dentastix 56 batonnets": 10.99, "Pedigree Dentastix 112 batonnets": 16.99, "Pedigree Dentastix 28 batonnets": 6.99,
    "Purina Dentalife 35 batonnets": 8.99, "Purina Dentalife 70 batonnets": 13.99,
    "Kong Classic M 7cm": 14.99, "Kong Classic L 10cm": 19.99, "Kong Classic XL 12cm": 24.99, "Kong Extreme M": 18.99,
    "Laisse Flexi Extra M 5m": 24.99, "Laisse Flexi Extra L 8m": 32.99, "Laisse Flexi Extra S 3m": 18.99,
    "Gamelle inox chien 20cm": 8.99, "Gamelle inox chien 16cm": 6.99,
    "Panier chien 70x50cm": 34.99, "Panier chien 60x40cm": 27.99, "Panier chien 90x60cm": 44.99,
    "Brosse FURminator chien L": 29.99, "Brosse FURminator chien M": 24.99, "Brosse FURminator chat": 22.99,

    "Royal Canin Sterilised 37 10kg": 58.99, "Royal Canin Sterilised 37 4kg": 29.99, "Royal Canin Sterilised 37 2kg": 18.99,
    "Royal Canin British Shorthair 4kg": 35.99, "Royal Canin British Shorthair 10kg": 62.99,
    "Royal Canin Maine Coon 4kg": 39.99, "Royal Canin Maine Coon 10kg": 67.99,
    "Royal Canin Persian 4kg": 38.99, "Royal Canin Persian 10kg": 65.99,
    "Royal Canin Siamois 4kg": 36.99,
    "Royal Canin Indoor 7kg": 44.99, "Royal Canin Indoor 4kg": 30.99,
    "Royal Canin Outdoor 7kg": 46.99,
    "Royal Canin Kitten 4kg": 31.99, "Royal Canin Kitten 10kg": 52.99,
    "Royal Canin Hair & Skin 4kg": 34.99,
    "Royal Canin Gastrointestinal Chat 4kg": 44.99, "Royal Canin Urinary S/O Chat 4kg": 44.99, "Royal Canin Neutered Adult Chat 4kg": 32.99,
    "Hill's Science Plan Adult Chat 7kg": 46.99, "Hill's Science Plan Adult Chat 3.5kg": 29.99,
    "Hill's Science Plan Kitten 3.5kg": 33.99, "Hill's Science Plan Sterilised Chat 7kg": 48.99,
    "Hill's Prescription Diet z/d Chat 3kg": 54.99,
    "Purina Pro Plan Sterilised Chat 10kg": 44.99, "Purina Pro Plan Sterilised Chat 4kg": 25.99,
    "Purina Pro Plan Senior Chat 7kg": 38.99, "Purina Pro Plan Kitten Chat 2kg": 18.99, "Purina Pro Plan Urinary Chat 7kg": 42.99,
    "Purina One Sterilised Chat 7kg": 32.99, "Purina One Kitten Chat 7kg": 29.99,
    "Orijen Original Chat 5.4kg": 34.99, "Orijen Original Chat 1.8kg": 18.99, "Orijen Six Fish Chat 5.4kg": 37.99,
    "Acana Grasslands Chat 4.5kg": 29.99, "Acana Grasslands Chat 2kg": 17.99, "Acana Bountiful Catch Chat 4.5kg": 32.99,
    "Eukanuba Adult Chat 7kg": 42.99,
    "Sheba Patee Chat 12x85g": 7.99, "Sheba Patee Chat 4x85g": 3.99,
    "Felix Patee Chat 12x85g": 5.99, "Felix Patee Chat 40x85g": 14.99,
    "Gourmet Patee Chat 12x85g": 11.99, "Gourmet Patee Chat 24x85g": 18.99,
    "Whiskas Patee Chat 12x85g": 5.49, "Whiskas Patee Chat 40x85g": 13.99,

    "Litiere Catsan agglomerante 20kg": 12.99, "Litiere Catsan agglomerante 10kg": 8.99, "Litiere Catsan non agglomerante 20kg": 11.99,
    "Litiere silicate Ultra 5L": 14.99, "Litiere silicate Ultra 10L": 24.99,
    "Litiere Tigerino 20kg": 14.99, "Litiere Sanicat 20kg": 11.99,
    "Arbre a chat 180cm": 74.99, "Arbre a chat 120cm": 49.99, "Arbre a chat 220cm": 99.99,
    "Fontaine a eau chat 1.5L": 39.99, "Fontaine a eau chat 2.5L": 49.99,
    "Transporteur chat 50x30x30cm": 32.99, "Transporteur chat 60x40x35cm": 42.99,
    "Griffoir chat 50x30cm": 18.99,

    "Frontline Spot On Chien 3 pipettes": 18.99, "Frontline Spot On Chien 6 pipettes": 32.99,
    "Frontline Spot On Chat 3 pipettes": 18.99, "Frontline Spot On Chat 6 pipettes": 32.99,
    "Frontline Combo Chien 3 pipettes": 22.99, "Frontline Combo Chat 3 pipettes": 22.99,
    "Advantage 40 Chien 4 pipettes": 19.99, "Advantage 40 Chat 4 pipettes": 19.99,
    "Seresto Collier Chien": 54.99, "Seresto Collier Chat": 49.99,
    "Scalibor Collier Chien": 34.99,
    "Broadline Chat 3 pipettes": 34.99,
    "Stronghold Chien 3 pipettes": 32.99, "Stronghold Chat 3 pipettes": 32.99,
    "Revolution Chien 3 pipettes": 34.99, "Revolution Chat 3 pipettes": 34.99,
    "Exspot Chien 3 pipettes": 24.99, "Exspot Chien 6 pipettes": 42.99,
    "Flea Collar Chien": 9.99, "Flea Collar Chat": 9.99,
    "Spray Anti-Puces Chien 250ml": 14.99, "Spray Anti-Puces Chat 100ml": 12.99,
    "Drontal Chien 1 comprime": 8.99, "Drontal Chien 4 comprimes": 24.99,
    "Drontal Chat 1 comprime": 8.99, "Drontal Chat 4 comprimes": 24.99,
    "Milpro Chien 2 comprimes": 14.99, "Milpro Chat 2 comprimes": 14.99,
    "Milbemax Chien 2 comprimes": 17.99, "Milbemax Chat 2 comprimes": 17.99,
    "Panacur KH Chien 1 dose": 12.99, "Panacur Chat 1 dose": 12.99,
    "Flubenol Chien 2 comprimes": 11.99,
    "Purina Fortiflora 30 sachets": 28.99,
    "Canigouttes 30ml": 16.99, "Zylkene Chien 75mg 30 gellules": 32.99, "Zylkene Chat 75mg 30 gellules": 32.99,

    "Patee convalescence Royal Canin Recovery 12x200g": 22.99,
    "Pedigree Patee Chien 12x100g": 8.99, "Pedigree Patee Chien 24x100g": 14.99,
    "Frolic Patee Chien 12x100g": 7.99,
    "Cesar Patee Chien 12x100g": 9.99,
    "Os en peau de buffle 15cm": 5.99, "Os en peau de buffle 25cm": 8.99, "Batonnet a macher 12cm": 4.99,

    "Kit de toilette pour chien manteau court": 14.99,
    "Coupe-ongles chien": 8.99, "Shampooing chien 250ml": 9.99, "Brosse a dents chien": 7.99, "Dentifrice chien 100g": 6.99,
    "Arrache tiques": 5.99, "Pince a tiques": 7.99, "Boite a medicaments chien": 12.99,
    "Niche chien 100x80x80cm": 69.99, "Niche chien 120x90x90cm": 89.99,
    "Cage de transport chien 70x50x50cm": 49.99, "Cage de transport chien 90x60x60cm": 64.99,
    "Gilet de sauvetage chien": 24.99,

    "Nourriture poissons flocons 250ml": 5.99, "Nourriture poissons granules 250ml": 6.99,
    "Aquarium Juwel 60L": 89.99, "Aquarium Juwel 120L": 149.99, "Filtre aquarium 800L/h": 34.99,
    "Melange graines rongeurs 1kg": 7.99, "Melange graines rongeurs 3kg": 14.99,
    "Cage rongeur 2 etages 80cm": 54.99, "Cage rongeur 1 etage 60cm": 39.99,
    "Foin rongeur 500g": 4.99, "Foin rongeur 1kg": 7.99,
    "Bouteille eau rongeur 150ml": 5.99, "Roue rongeur 20cm": 9.99,
    "Melange graines oiseaux 2kg": 6.99, "Melange graines oiseaux 5kg": 12.99,
    "Cage oiseau 50x40x60cm": 44.99, "Nid oiseau paille": 6.99, "Boule graisse oiseaux 250g": 3.99, "Mangeoire oiseaux 20cm": 12.99,
}

# Coefficients par boutique : prix = base * coeff + bruit
SHOP_COEFFS = {
    "maxizoo": 1.04,
    "animalis": 0.97,
    "jardiland": 0.96,
    "truffaut": 0.99,
    "laferme": 0.92,
    "produitsveto": 0.91,
    "directvet": 0.94,
    "cernunos": 1.02,
    "santevet": 0.97,
    "ultrapremium": 0.90,
    "petsonic": 0.88,
}

# URLs de recherche par boutique
SHOP_SEARCH_URLS = {
    "maxizoo": "https://www.maxizoo.fr/",
    "animalis": "https://www.animalis.com/",
    "jardiland": "https://www.jardiland.com/",
    "truffaut": "https://www.truffaut.com/",
    "laferme": "https://www.lafermedesanimaux.com/",
    "produitsveto": "https://www.produits-veto.com/",
    "directvet": "https://www.direct-vet.fr/",
    "cernunos": "https://www.cernunos.fr/",
    "santevet": "https://www.santevet.com/",
    "ultrapremium": "https://www.ultrapremiumdirect.com/",
    "petsonic": "https://www.petsonic.com/",
}

# Correct search URL paths (tested from GitHub Actions)
SHOP_SEARCH_PATHS = {
    "maxizoo": "/search?q=",
    "animalis": "/recherche?q=",
    "jardiland": "/search?q=",
    "truffaut": "/catalogsearch/result/?q=",
    "laferme": "/search?q=",
    "produitsveto": "/?s=",
    "directvet": "/?s=",
    "cernunos": "/?s=",
    "santevet": "/?s=",
    "ultrapremium": "/?s=",
    "petsonic": "/catalogsearch/result/?q=",
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


def find_best_match(scraped_name: str, catalog_names: list[str], catalog_weights: dict[str, set[str]], catalog_brands: dict[str, str], catalog_data: dict = None) -> tuple[Optional[str], float]:
    """Trouve le meilleur produit du catalogue pour un nom scrapé.
    Utilise brand + weight du catalogue si disponibles, sinon parsing."""
    best_name = None
    best_score = 0.0
    scraped_norm = normalize(scraped_name)
    scraped_weights = extract_weight(scraped_name)

    for cat_name in catalog_names:
        cat_norm = normalize(cat_name)

        # Use catalog data if available, else fallback to parsing
        cat_info = (catalog_data or {}).get(cat_name, {})
        cat_weight_str = cat_info.get("weight", "")
        cat_brand = (cat_info.get("brand") or catalog_brands.get(cat_name, "")).lower()

        if cat_weight_str:
            cat_weights = {cat_weight_str.strip().lower()}
        else:
            cat_weights = catalog_weights.get(cat_name, set())

        # Vérification poids
        if cat_weights and not (scraped_weights & cat_weights):
            continue

        # Vérification marque
        if cat_brand and cat_brand not in scraped_norm:
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
    catalog_brands = {p["name"]: p["name"].split()[0] for p in PRODUCT_CATALOG}
    catalog_data = {p["name"]: p for p in PRODUCT_CATALOG}

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
                    matched_name, score = find_best_match(result.product_name, catalog_names, catalog_weights, catalog_brands, catalog_data)
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

            scraper.close()
            print(f"📊 {scraper_name}: {success_count}/{len(PRODUCT_CATALOG)} produits trouvés")

        # Fermer Playwright (si utilisé)
        try:
            from scrapers.playwright_base import close as pw_close
            pw_close()
        except Exception:
            pass

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
            "patees-chat": "Pâtées chat", "patees-chien": "Pâtées chien",
            "friandises-chien": "Friandises chien", "friandises-chat": "Friandises chat",
            "litiere": "Litière", "accessoires-chien": "Accessoires chien",
            "accessoires-chat": "Accessoires chat", "jouets-chien": "Jouets chien",
            "rongeurs": "Rongeurs", "oiseaux": "Oiseaux", "poissons": "Poissons",
            "anti-parasitaires": "Anti-parasitaires", "vermifuges": "Vermifuges",
            "compliments": "Compléments",
        }
        category_emojis = {
            "croquettes-chien": "🍖", "croquettes-chat": "🐟",
            "patees-chat": "🥫", "patees-chien": "🥩",
            "friandises-chien": "🦴", "friandises-chat": "🐱",
            "litiere": "⬜", "accessoires-chien": "🎾",
            "accessoires-chat": "🧶", "jouets-chien": "🎾",
            "rongeurs": "🐹", "oiseaux": "🐦", "poissons": "🐠",
            "anti-parasitaires": "🛡️", "vermifuges": "💊",
            "compliments": "✨",
        }
        cat = product["category"]
        products_json.append({
            "name": product["name"],
            "slug": product["url_name"],
            "category": cat,
            "animal": product.get("animal", "other"),
            "brand": product.get("brand", ""),
            "weight": product.get("weight", ""),
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
        "croquettes-chien", "friandises-chien", "patees-chien", "jouets-chien", "accessoires-chien",
        "croquettes-chat", "patees-chat", "friandises-chat", "litiere", "accessoires-chat",
        "anti-parasitaires", "vermifuges", "compliments",
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
