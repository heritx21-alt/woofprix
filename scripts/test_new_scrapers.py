"""Test new scrapers locally - import directly to avoid playwright."""
import sys, os, httpx, re
from urllib.parse import quote
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrapers"))
from base import BaseScraper, ScraperResult

# Reimplemnt scrapers inline to avoid playwright import issues
class DirectVetScraper(BaseScraper):
    def __init__(self): super().__init__(name="directvet", base_url="https://www.direct-vet.fr", search_path="/?s=")
    def search_product(self, query):
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup: return None
        results = []
        items = soup.select(".ajax_block_product, .product_block")
        for item in items:
            name_el = item.select_one("h5[itemprop='name'] a, [itemprop='name'] a, h5 a")
            price_el = item.select_one(".price, .product-price, [itemprop='price']")
            link_el = item.select_one("a.product_img_link, a[itemprop='url']")
            img_el = item.select_one("img[src]")
            if not name_el or not price_el: continue
            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price: continue
            link = link_el.get("href", "") if link_el else ""
            img = img_el.get("src", "") if img_el else ""
            results.append(ScraperResult(name, price, 0, self._abs_url(link), True, img, ""))
        self._wait()
        return results if results else None

class CernunosScraper(BaseScraper):
    def __init__(self): super().__init__(name="cernunos", base_url="https://www.cernunos.fr", search_path="/?s=")
    def search_product(self, query):
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup: return None
        results = []
        items = soup.select("[class*=product]")
        for item in items:
            price_el = item.select_one(".price, [class*=price]")
            a = item.select_one("a[href*='/products/']")
            img_el = item.select_one("img")
            if not price_el or not a: continue
            name = item.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price: continue
            link = a.get("href", "")
            img = img_el.get("src", "") if img_el else ""
            results.append(ScraperResult(name, price, 0, self._abs_url(link), True, img, ""))
        self._wait()
        return results if results else None

class UltraPremiumScraper(BaseScraper):
    def __init__(self): super().__init__(name="ultrapremium", base_url="https://www.ultrapremiumdirect.com", search_path="/?s=")
    def search_product(self, query):
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup: return None
        results = []
        items = soup.select("a.product-card")
        for item in items:
            price_el = item.select_one(".product-card-infos-price, [class*=price]")
            img_el = item.select_one("img")
            if not price_el: continue
            name = item.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price: continue
            link = item.get("href", "")
            img = img_el.get("src", "") if img_el else ""
            results.append(ScraperResult(name, price, 0, self._abs_url(link), True, img, ""))
        self._wait()
        return results if results else None

class PetsonicScraper(BaseScraper):
    def __init__(self): super().__init__(name="petsonic", base_url="https://www.petsonic.com", search_path="/catalogsearch/result/?q=")
    def search_product(self, query):
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup: return None
        results = []
        items = soup.select(".product-item, li.product, .product")
        for item in items:
            name_el = item.select_one("[class*=name], [class*=title], h2, h3 a")
            price_el = item.select_one(".price, [class*=price]")
            link_el = item.select_one("a[href*='/product/'], a[href*='/produit/'], a[href*='.html']")
            img_el = item.select_one("img")
            if not name_el or not price_el: continue
            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price: continue
            link = link_el.get("href", "") if link_el else ""
            img = img_el.get("src", "") if img_el else ""
            results.append(ScraperResult(name, price, 0, self._abs_url(link), True, img, ""))
        self._wait()
        return results if results else None

scrapers = [
    ("directvet", DirectVetScraper),
    ("cernunos", CernunosScraper),
    ("ultrapremium", UltraPremiumScraper),
    ("petsonic", PetsonicScraper),
]

for name, cls in scrapers:
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    scraper = cls()
    url = scraper._make_search_url("Royal Canin Maxi Adult 15kg")
    print(f"  URL: {url}")
    
    soup = scraper._fetch(url)
    if not soup:
        print(f"  -> BLOQUE")
        continue
    
    print(f"  Body: {len(str(soup))}b")
    title = soup.select_one("title")
    print(f"  Title: {title.get_text(strip=True)[:80] if title else 'none'}")
    
    items = scraper.search_product("Royal Canin Maxi Adult 15kg")
    if items:
        print(f"  -> {len(items)} results!")
        for it in items[:5]:
            print(f"     {it.product_name[:60]:60s} {it.price:.2f}€")
    else:
        print(f"  -> No results")
    
    scraper.close()
