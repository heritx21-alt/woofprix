#!/usr/bin/env python3
"""
scrape_all.py — scrap prices for known catalog products, no guessing.
"""
import json, os, sys, re, time, unicodedata, threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

SHOP_NAMES = ["animalis", "truffaut", "produitsveto"]
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
    pattern = re.compile(r"\d+[.,]?\d*\s*(?:kg|g|l|ml|cm|m|batonnets|etages|litres)", re.I)
    for m in pattern.finditer(name):
        tokens.add(m.group(0).strip().lower().replace(" ", ""))
    return tokens


# ─── mapping: old flat catalog categories -> new 3-level hierarchy ──────────
CAT_FLAT_TO_HIERARCHY = {
    "croquettes-chien": ("dog", "food", "croquettes"),
    "croquettes-chat": ("cat", "food", "croquettes"),
    "patees-chien": ("dog", "food", "patees"),
    "patees-chat": ("cat", "food", "patees"),
    "friandises-chien": ("dog", "food", "friandises"),
    "accessoires-chien": ("dog", "accessories", ""),
    "accessoires-chat": ("cat", "accessories", ""),
    "jouets-chien": ("dog", "accessories", "jouets"),
    "anti-parasitaires": ("multi", "health", "anti-parasitaires"),
    "vermifuges": ("multi", "health", "vermifuges"),
    "litiere": ("cat", "health", "litiere"),
    "compliments": ("multi", "health", "compliments"),
    "rongeurs": ("rodent", "food", ""),
    "oiseaux": ("bird", "food", ""),
    "poissons": ("fish", "food", ""),
}

CATEGORY_LABELS = {
    "food": "Alimentation",
    "health": "Soins & Sante",
    "accessories": "Accessoires",
    "other": "Autre",
}

SUBCATEGORY_LABELS = {
    "croquettes": "Croquettes",
    "patees": "Patees",
    "friandises": "Friandises",
    "litiere": "Litiere",
    "anti-parasitaires": "Anti-parasitaires",
    "vermifuges": "Vermifuges",
    "compliments": "Complements",
    "jouets": "Jouets",
    "": "",
}

ANIMAL_LABELS = {
    "dog": "Chien",
    "cat": "Chat",
    "rodent": "Rongeurs",
    "bird": "Oiseaux",
    "fish": "Poissons",
    "other": "Autre",
    "multi": "Multi",
}


def map_catalog_to_hierarchy(cat_flat, cat_animal):
    if cat_flat in CAT_FLAT_TO_HIERARCHY:
        h_animal, h_category, h_subcategory = CAT_FLAT_TO_HIERARCHY[cat_flat]
        if h_animal == "multi":
            h_animal = cat_animal
        if h_animal == "all":
            h_animal = "dog"
    else:
        h_animal = cat_animal
        h_category = "other"
        h_subcategory = ""

    if h_animal == "other":
        h_animal = "dog"
    if h_animal == "all":
        h_animal = "dog"

    return {
        "animal": h_animal if h_animal in ("dog", "cat", "rodent", "bird", "fish") else "other",
        "animalLabel": ANIMAL_LABELS.get(h_animal, "Autre"),
        "category": h_category,
        "categoryLabel": CATEGORY_LABELS.get(h_category, "Autre"),
        "subcategory": h_subcategory,
        "subcategoryLabel": SUBCATEGORY_LABELS.get(h_subcategory, ""),
    }


def clean_name(name):
    clean = name
    for shop_word in ["animalis", "truffaut", "jardiland", "produitsveto"]:
        prefix = shop_word.capitalize() + "- "
        if clean.lower().startswith(shop_word.lower()):
            clean = clean[len(prefix):] if clean.startswith(prefix) else clean
    words = clean.split()
    if len(words) > 2 and words[0].lower() == words[1].lower():
        clean = " ".join(words[1:])
    return clean.strip()


def main():
    output_dir = os.path.join("public", "data")
    os.makedirs(output_dir, exist_ok=True)

    db_path = os.path.join(output_dir, "products_db.json")
    catalog = []
    if os.path.exists(db_path):
        catalog = json.load(open(db_path, encoding="utf-8"))
    print(f"  {len(catalog)} produits dans le catalogue")

    if not catalog:
        print("  Catalogue vide, rien a faire.")
        return

    # Phase 1: scrape prices for each catalog product
    print("\n=== PHASE 1: SCRAPING ===")
    load_scrapers()
    if not ALL_SCRAPERS:
        print("  Aucun scraper charge, abandon.")
        return

    catalog_by_term = {}
    for p in catalog:
        term = p["search_terms"][0] if p["search_terms"] else p["name"]
        catalog_by_term[term] = p

    search_terms = list(catalog_by_term.keys())

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
                "search_term": term,
                "product_name": clean_name(best.product_name),
                "price": round(best.price, 2),
                "url": best.url,
                "image_url": best.image_url or "",
                "description": best.description or "",
                "in_stock": best.in_stock,
            })
        scraper.close()
        return raw

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(scrape_scraper, n, c): n for n, c in ALL_SCRAPERS}
        for f in as_completed(futures):
            raw = f.result()
            all_raw.extend(raw)
            name = raw[0]["shop"] if raw else "?"
            print(f"  {name}: {len(raw)} prix trouves")

    print(f"\n  Total: {len(all_raw)} prix bruts")

    # Phase 2: build products from catalog data + scraped prices
    print("\n=== PHASE 2: ASSEMBLAGE ===")

    results_by_term = defaultdict(list)
    for r in all_raw:
        results_by_term[r["search_term"]].append(r)

    products_json = []

    for p in catalog:
        term = p["search_terms"][0] if p["search_terms"] else p["name"]

        hier = map_catalog_to_hierarchy(p["category"], p["animal"])

        prices = []
        for r in sorted(results_by_term.get(term, []), key=lambda x: x["price"]):
            prices.append({
                "shop": r["shop"],
                "price": r["price"],
                "url": r["url"],
                "in_stock": r["in_stock"],
                "image_url": r["image_url"],
                "description": r["description"],
                "source": "scraped",
            })

        best_per_shop = {}
        for pr in prices:
            s = pr["shop"]
            if s not in best_per_shop or pr["price"] < best_per_shop[s]["price"]:
                best_per_shop[s] = pr

        prices_deduped = sorted(best_per_shop.values(), key=lambda x: x["price"])
        best_price = prices_deduped[0]["price"] if prices_deduped else None
        best_shop = prices_deduped[0]["shop"] if prices_deduped else ""

        scraped_names = [r["product_name"] for r in results_by_term.get(term, [])]
        final_name = p["name"]
        if scraped_names:
            candidates = sorted(set(scraped_names), key=lambda x: len(x))
            final_name = candidates[0]

        slug = normalize(final_name).replace(" ", "-")
        if not slug:
            slug = normalize(p["name"]).replace(" ", "-")

        products_json.append({
            "name": final_name,
            "slug": slug,
            "animal": hier["animal"],
            "animalLabel": hier["animalLabel"],
            "category": hier["category"],
            "categoryLabel": hier["categoryLabel"],
            "subcategory": hier["subcategory"],
            "subcategoryLabel": hier["subcategoryLabel"],
            "brand": p["brand"],
            "weight": p["weight"],
            "best_price": best_price,
            "best_shop": best_shop,
            "image": prices_deduped[0]["image_url"] if prices_deduped else "",
            "description": prices_deduped[0]["description"] if prices_deduped else "",
            "prices": prices_deduped,
        })

    animal_order = ["dog", "cat", "rodent", "bird", "fish"]
    cat_order = ["food", "health", "accessories"]
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

    with_prices = [pp for pp in products_json if pp["prices"]]
    print(f"\n  {len(products_json)} produits finaux")
    print(f"  {len(with_prices)} produits AVEC prix")
    print(f"  {len(products_json) - len(with_prices)} produits sans prix")
    print(f"  {sum(len(pp['prices']) for pp in products_json)} prix au total")
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
