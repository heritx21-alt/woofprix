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

CATEGORY_KEYWORDS = {
    "croquettes-chien": ["croquette", "chien", "chiot", "puppy", "adult", "medium", "maxi", "mini", "large", "senior"],
    "croquettes-chat": ["croquette", "chat", "chaton", "kitten", "sterilise", "indoor", "outdoor"],
    "patees-chien": ["patee", "boite", "terrine", "mousseline", "chien", "poulet", "saumon"],
    "patees-chat": ["patee", "boite", "terrine", "mousseline", "chat", "poulet", "saumon", "thon"],
    "friandises-chien": ["friandise", "batonnet", "os", "dentastix", "dentalife", "macher", "snack", "chien"],
    "friandises-chat": ["friandise", "chat", "cat", "snack"],
    "litiere": ["litiere", "cat sand", "silicate", "agglomerante", "tofu", "vegetale"],
    "anti-parasitaires": ["frontline", "spot on", "pipette", "antipuce", "anti-puce", "seresto", "collier", "advantage", "broadline", "stronghold", "revolution", "flea"],
    "vermifuges": ["vermifuge", "drontal", "milpro", "milbemax", "panacur", "flubenol", "anthelmin"],
    "compliments": ["fortiflora", "zylkene", "cartimax", "canigoutte", "complement", "probiotique"],
    "jouets-chien": ["jouet", "kong", "balle", "frisbee", "jeu", "chien", "lancer"],
    "accessoires-chien": ["laisse", "collier", "harnais", "gamelle", "panier", "niche", "brosse", "furminator", "transport", "caisse"],
    "accessoires-chat": ["arbre", "griffoir", "fontaine", "transport", "caisse", "panier", "brosse"],
    "rongeurs": ["rongeur", "hamster", "cobaye", "lapin", "cochon", "cage", "graine", "foin"],
    "oiseaux": ["oiseau", "cage", "voliere", "graine", "mangeoire", "boule", "graisse"],
    "poissons": ["poisson", "aquarium", "aquariophilie", "filtre", "pompe", "nourriture", "flocon", "granule"],
}

def detect_category(name, search_term=""):
    n = name.lower()
    s = search_term.lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in n:
                score += 1
            if kw in s:
                score += 2
        if score:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return "autre"

CATEGORY_LABELS = {
    "croquettes-chien": "Croquettes chien", "croquettes-chat": "Croquettes chat",
    "patees-chien": "Patees chien", "patees-chat": "Patees chat",
    "friandises-chien": "Friandises chien", "friandises-chat": "Friandises chat",
    "litiere": "Litiere", "anti-parasitaires": "Anti-parasitaires",
    "vermifuges": "Vermifuges", "compliments": "Complements",
    "jouets-chien": "Jouets chien", "accessoires-chien": "Accessoires chien",
    "accessoires-chat": "Accessoires chat",
    "rongeurs": "Rongeurs", "oiseaux": "Oiseaux", "poissons": "Poissons",
    "autre": "Autre",
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

        # Detect category from name and search terms
        cat = detect_category(clean_name, items[0].get("search_term", ""))
        cat_label = CATEGORY_LABELS.get(cat, "Autre")

        # Brand: take first real word (skip numbers/short words)
        words = [w for w in normalize(clean_name).split() if len(w) > 1 and not w.isdigit()]
        brand = words[0].title() if words else ""

        # Animal type
        if "chat" in clean_name.lower() or "chaton" in clean_name.lower() or "kitten" in clean_name.lower() or cat in ["croquettes-chat", "patees-chat", "friandises-chat", "accessoires-chat"]:
            animal = "cat"
        elif "chien" in clean_name.lower() or "chiot" in clean_name.lower() or "puppy" in clean_name.lower() or "dog" in clean_name.lower() or "canin" in clean_name.lower() or cat in ["croquettes-chien", "patees-chien", "jouets-chien", "accessoires-chien", "friandises-chien"]:
            animal = "dog"
        elif cat in ["rongeurs"]:
            animal = "rodent"
        elif cat in ["oiseaux"]:
            animal = "bird"
        elif cat in ["poissons"]:
            animal = "fish"
        else:
            animal = "other"

        # Weight
        w = extract_weight(clean_name)
        weight_str = ", ".join(sorted(w)) if w else ""

        products_json.append({
            "name": clean_name,
            "slug": normalize(clean_name).replace(" ", "-"),
            "category": cat,
            "categoryLabel": cat_label,
            "animal": animal,
            "brand": brand,
            "weight": weight_str,
            "best_price": best_price,
            "best_shop": best_shop,
            "image": best_image,
            "description": best_desc,
            "prices": prices,
        })

    # Trier par categorie puis nom
    cat_order = [
        "croquettes-chien", "friandises-chien", "patees-chien", "jouets-chien", "accessoires-chien",
        "croquettes-chat", "patees-chat", "friandises-chat", "litiere", "accessoires-chat",
        "anti-parasitaires", "vermifuges", "compliments",
        "rongeurs", "oiseaux", "poissons", "autre",
    ]
    products_json.sort(key=lambda p: (cat_order.index(p["category"]) if p["category"] in cat_order else 99, normalize(p["name"])))

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
