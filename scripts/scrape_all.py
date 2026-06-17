#!/usr/bin/env python3
"""
scrape_all.py — scrape prices for catalog products, keep catalog names.
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


def product_key(name):
    n = normalize(name)
    w = extract_weight(name)
    tokens = [t for t in n.split() if len(t) > 2]
    brand = tokens[0] if tokens else ""
    weight_str = "".join(sorted(w)) if w else ""
    return f"{brand}__{weight_str}"


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

    # Build product_key -> catalog entry lookup
    cat_by_key = {}
    for p in catalog:
        term = p["search_terms"][0] if p.get("search_terms") else p["name"]
        key = product_key(term)
        if key not in cat_by_key:
            cat_by_key[key] = []
        cat_by_key[key].append(p)

    # Phase 1: scrape prices
    print("\n=== PHASE 1: SCRAPING ===")
    load_scrapers()
    if not ALL_SCRAPERS:
        print("  Aucun scraper charge, abandon.")
        return

    search_terms = [p["search_terms"][0] if p.get("search_terms") else p["name"] for p in catalog]

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

            # Keep results whose product_key matches the search term's product_key
            expected_key = product_key(term)
            for r in results:
                r_key = product_key(r.product_name or "")
                if r_key == expected_key:
                    raw.append({
                        "shop": scraper_name,
                        "search_term": term,
                        "product_name": r.product_name,
                        "price": round(r.price, 2),
                        "url": r.url,
                        "image_url": r.image_url or "",
                        "description": r.description or "",
                        "in_stock": r.in_stock,
                    })
                    break  # one per shop per term
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

    # Phase 2: build products
    print("\n=== PHASE 2: ASSEMBLAGE ===")

    results_by_term = defaultdict(list)
    for r in all_raw:
        results_by_term[r["search_term"]].append(r)

    products_json = []
    used_slugs = set()

    for p in catalog:
        term = p["search_terms"][0] if p.get("search_terms") else p["name"]
        hier = map_catalog_to_hierarchy(p["category"], p["animal"])

        # Get prices, deduplicate per shop
        best_per_shop = {}
        for r in results_by_term.get(term, []):
            s = r["shop"]
            if s not in best_per_shop or r["price"] < best_per_shop[s]["price"]:
                best_per_shop[s] = r

        prices_deduped = sorted(best_per_shop.values(), key=lambda x: x["price"])
        best_price = prices_deduped[0]["price"] if prices_deduped else None
        best_shop = prices_deduped[0]["shop"] if prices_deduped else ""
        best_image = prices_deduped[0]["image_url"] if prices_deduped else ""
        best_desc = prices_deduped[0]["description"] if prices_deduped else ""

        prices_out = []
        for pr in prices_deduped:
            prices_out.append({
                "shop": pr["shop"],
                "price": pr["price"],
                "url": pr["url"],
                "in_stock": pr["in_stock"],
                "image_url": pr["image_url"],
                "description": pr["description"],
                "source": "scraped",
            })

        # Slug from catalog url_name, deduplicated
        slug = p.get("url_name") or normalize(p["name"]).replace(" ", "-")
        slug_base = slug
        n = 2
        while slug in used_slugs:
            slug = slug_base + "-" + str(n)
            n += 1
        used_slugs.add(slug)

        products_json.append({
            "name": p["name"],
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
            "image": best_image,
            "description": best_desc,
            "prices": prices_out,
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
