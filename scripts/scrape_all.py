#!/usr/bin/env python3
"""
scrape_all.py — Nouvelle approche : scraper les shops, puis grouper les produits identiques.
"""
import json, os, sys, re, time, unicodedata, threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

SHOP_NAMES = ["animalis","truffaut","produitsveto"]
ALL_SCRAPERS = []

def load_scrapers():
    global ALL_SCRAPERS
    try:
        from scrapers import ALL_SCRAPERS as scrapers_list
        ALL_SCRAPERS = scrapers_list
        print(f"  {len(ALL_SCRAPERS)} scrapers charges")
    except Exception as e:
        print(f"  Erreur chargement scrapers: {e}")

def strip_accents(s):
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def normalize(name):
    name = strip_accents(name.lower())
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def extract_weight(name):
    tokens = set()
    pattern = re.compile(r"\d+[.,]?\d*\s*(?:kg|g|l|ml|cm|m|batonnets|batonnets|etages|etages|litres)", re.I)
    for m in pattern.finditer(name):
        tokens.add(m.group(0).strip().lower().replace(" ", ""))
    return tokens

def jaccard(a, b):
    at = set(normalize(a).split())
    bt = set(normalize(b).split())
    if not at or not bt:
        return 0.0
    return len(at & bt) / len(at | bt)

def product_key(name):
    n = normalize(name)
    w = extract_weight(name)
    tokens = [t for t in n.split() if len(t) > 2]
    brand = tokens[0] if tokens else ""
    weight_str = "".join(sorted(w)) if w else ""
    return f"{brand}__{weight_str}"

SUBCATEGORY_KEYWORDS = {
    "croquettes": ["croquette", "trockenfutter", "dry"],
    "patees": ["patee", "boite", "terrine", "mousseline", "humide", "nassfutter", "wet"],
    "friandises": ["friandise", "batonnet", "os", "dentastix", "dentalife", "macher", "snack", "os", "biscuit"],
    "litiere": ["litiere", "cat sand", "silicate", "agglomerante", "tofu", "vegetale", "litter"],
    "anti-parasitaires": ["frontline", "spot on", "pipette", "antipuce", "anti-puce", "seresto", "collier antiparasitaire", "advantage", "broadline", "stronghold", "revolution", "flea", "tique", "puce"],
    "vermifuges": ["vermifuge", "drontal", "milpro", "milbemax", "panacur", "flubenol", "anthelmin", "ver"],
    "compliments": ["fortiflora", "zylkene", "cartimax", "canigoutte", "complement", "probiotique", "vitamine"],
    "jouets": ["jouet", "kong", "balle", "frisbee", "jeu", "lancer", "squeak", "peluche"],
    "transport": ["transport", "caisse", "sac", "voyage", "cage transport"],
    "gamelles": ["gamelle", "mangeoire", "fontaine", "distributeur"],
    "colliers": ["collier", "laisse", "harnais", "longe", "enrouleur"],
    "paniers": ["panier", "niche", "couchage", "coussin", "corbeille"],
    "toilettage": ["brosse", "furminator", "shampooing", "coupe ongle", "toilettage", "peigne"],
    "aquarium": ["aquarium", "aquariophilie", "filtre", "pompe", "eclairage", "chauffage"],
    "cages": ["cage", "voliere", "cage rongeur", "cage oiseau"],
}

# Animal detection: return "dog", "cat", "rodent", "bird", "fish", "other"
def detect_animal(name):
    n = name.lower()
    if any(kw in n for kw in ["chat", "chaton", "kitten", "cat", "feline"]):
        return "cat"
    if any(kw in n for kw in ["chien", "chiot", "puppy", "dog", "canin", "canine"]):
        return "dog"
    if any(kw in n for kw in ["rongeur", "hamster", "cobaye", "lapin", "cochon d inde", "gerbille", "rat", "souris"]):
        return "rodent"
    if any(kw in n for kw in ["oiseau", "cage oiseau", "voliere", "perruche", "canari", "piaf"]):
        return "bird"
    if any(kw in n for kw in ["poisson", "aquarium", "aquariophilie", "guppy", "neon"]):
        return "fish"
    return "other"

# Subcategory detection
def detect_subcategory(name):
    n = name.lower()
    scores = {}
    for sub, keywords in SUBCATEGORY_KEYWORDS.items():
        score = sum(2 if kw in n else 0 for kw in keywords)
        if score:
            scores[sub] = score
    if scores:
        return max(scores, key=scores.get)
    return "autre"

# Map subcategory -> parent category
SUBCAT_TO_CATEGORY = {
    "croquettes": "food", "patees": "food", "friandises": "food",
    "litiere": "health",
    "anti-parasitaires": "health", "vermifuges": "health", "compliments": "health",
    "jouets": "accessories", "transport": "accessories", "gamelles": "accessories",
    "colliers": "accessories", "paniers": "accessories", "toilettage": "accessories",
    "aquarium": "accessories", "cages": "accessories",
    "autre": "other",
}

CATEGORY_LABELS = {
    "food": "Alimentation", "health": "Soins & Sante", "accessories": "Accessoires", "other": "Autre",
}

SUBCATEGORY_LABELS = {
    "croquettes": "Croquettes", "patees": "Patees", "friandises": "Friandises",
    "litiere": "Litiere",
    "anti-parasitaires": "Anti-parasitaires", "vermifuges": "Vermifuges", "compliments": "Complements",
    "jouets": "Jouets", "transport": "Transport", "gamelles": "Gamelles",
    "colliers": "Colliers & Laisses", "paniers": "Paniers & Couchage", "toilettage": "Toilettage",
    "aquarium": "Aquarium", "cages": "Cages & Volieres",
    "autre": "Autre",
}

ANIMAL_LABELS = {
    "dog": "Chien", "cat": "Chat", "rodent": "Rongeurs", "bird": "Oiseaux", "fish": "Poissons", "other": "Autre",
}

def classify_product(name):
    animal = detect_animal(name)
    subcategory = detect_subcategory(name)
    category = SUBCAT_TO_CATEGORY.get(subcategory, "other")
    return {
        "animal": animal,
        "animalLabel": ANIMAL_LABELS.get(animal, "Autre"),
        "category": category,
        "categoryLabel": CATEGORY_LABELS.get(category, "Autre"),
        "subcategory": subcategory,
        "subcategoryLabel": SUBCATEGORY_LABELS.get(subcategory, "Autre"),
    }

def main():
    output_dir = os.path.join("public", "data")
    os.makedirs(output_dir, exist_ok=True)

    # Charger les search terms depuis le catalogue existant
    db_path = os.path.join(output_dir, "products_db.json")
    catalog = []
    if os.path.exists(db_path):
        catalog = json.load(open(db_path, encoding="utf-8"))
        print(f"  {len(catalog)} produits dans le catalogue")

    search_terms = [p["search_terms"][0] for p in catalog]

    # Phase 1: Scraping
    print("\n=== PHASE 1: SCRAPING ===")
    load_scrapers()

    lock = threading.Lock()
    all_raw = []

    def scrape_scraper(scraper_name, scraper_class):
        scraper = scraper_class()
        raw = []
        for term in search_terms:
            try:
                results = scraper.search_product(term)
            except Exception as e:
                with lock:
                    print(f"  [{scraper_name}] {term[:40]} ERR: {e}")
                continue

            if not results:
                continue

            best = results[0]
            raw.append({
                "shop": scraper_name,
                "product_name": best.product_name,
                "price": round(best.price, 2),
                "url": best.url,
                "image_url": best.image_url or "",
                "description": best.description or "",
                "in_stock": best.in_stock,
                "search_term": term,
            })

        scraper.close()
        return raw

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(scrape_scraper, n, c): n for n, c in ALL_SCRAPERS}
        for f in as_completed(futures):
            raw = f.result()
            all_raw.extend(raw)
            print(f"  {raw[0]['shop'] if raw else '?'}: {len(raw)} produits trouves")

    print(f"\n  Total: {len(all_raw)} produits bruts scapes")

    # Phase 2: Groupement par produit similaire
    print("\n=== PHASE 2: GROUPEMENT ===")

    groups = defaultdict(list)
    for p in all_raw:
        key = product_key(p["product_name"])
        groups[key].append(p)

    # Fusionner les groupes en produits finaux
    products_json = []

    for key, items in groups.items():
        if not items:
            continue

        # Deduplicate: cheapest price per shop
        best_per_shop = {}
        for i in items:
            s = i["shop"]
            if s not in best_per_shop or i["price"] < best_per_shop[s]["price"]:
                best_per_shop[s] = i

        deduped = list(best_per_shop.values())

        # Prendre le nom le plus court comme nom principal
        names = sorted(set(i["product_name"] for i in deduped), key=lambda x: len(x))
        main_name = names[0]

        best_price = min(i["price"] for i in deduped)
        best_shop = next(i["shop"] for i in deduped if i["price"] == best_price)
        best_image = next((i["image_url"] for i in deduped if i["image_url"]), "")
        best_desc = next((i["description"] for i in deduped if i["description"]), "")

        prices = []
        for i in sorted(deduped, key=lambda x: x["price"]):
            prices.append({
                "shop": i["shop"],
                "price": i["price"],
                "url": i["url"],
                "in_stock": i["in_stock"],
                "image_url": i["image_url"],
                "description": i["description"],
                "source": "scraped",
            })

        # Clean product name: remove shop prefix like "Animalis-", "Royal Canin Royal Canin"
        clean_name = main_name
        for shop_word in ["animalis", "truffaut", "jardiland", "produitsveto"]:
            prefix = shop_word.capitalize() + "- "
            if clean_name.lower().startswith(shop_word.lower()):
                clean_name = clean_name[len(prefix):] if clean_name.startswith(prefix) else clean_name
        # Remove duplicate brand: "Royal Canin Royal Canin" -> "Royal Canin"
        words = clean_name.split()
        if len(words) > 2 and words[0].lower() == words[1].lower():
            clean_name = " ".join(words[1:])

        # Classification: animal, category, subcategory
        cls = classify_product(clean_name)

        # Brand: take first real word (skip numbers/short words)
        words = [w for w in normalize(clean_name).split() if len(w) > 1 and not w.isdigit()]
        brand = words[0].title() if words else ""

        # Weight
        w = extract_weight(clean_name)
        weight_str = ", ".join(sorted(w)) if w else ""

        products_json.append({
            "name": clean_name,
            "slug": normalize(clean_name).replace(" ", "-"),
            "animal": cls["animal"],
            "animalLabel": cls["animalLabel"],
            "category": cls["category"],
            "categoryLabel": cls["categoryLabel"],
            "subcategory": cls["subcategory"],
            "subcategoryLabel": cls["subcategoryLabel"],
            "brand": brand,
            "weight": weight_str,
            "best_price": best_price,
            "best_shop": best_shop,
            "image": best_image,
            "description": best_desc,
            "prices": prices,
        })

    # Trier par animal, categorie, puis nom
    animal_order = ["dog", "cat", "rodent", "bird", "fish", "other"]
    cat_order = ["food", "health", "accessories", "other"]
    products_json.sort(key=lambda p: (
        animal_order.index(p["animal"]) if p["animal"] in animal_order else 99,
        cat_order.index(p["category"]) if p["category"] in cat_order else 99,
        normalize(p["name"])
    ))

    output = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(products_json),
        "total_shops": len(SHOP_NAMES),
        "products": products_json,
    }

    output_path = os.path.join(output_dir, "products.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n  {len(products_json)} produits finaux")
    print(f"  {sum(len(p['prices']) for p in products_json)} prix au total")
    print(f"  Fichier: {output_path}")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"\n  ERREUR: {e}")
        import traceback
        traceback.print_exc()
    print("\n  Termine")
    sys.exit(0)
