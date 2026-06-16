"""Scraper Petsonic (petsonic.com) — PrestaShop."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class PetsonicScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="petsonic",
            base_url="https://www.petsonic.com",
            search_path="/catalogsearch/result/?q=",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".product-item, li.product, .product")

        for item in items:
            name_el = item.select_one("[class*=name], [class*=title], h2, h3 a")
            price_el = item.select_one(".price, [class*=price]")
            link_el = item.select_one("a[href*='/product/'], a[href*='/produit/'], a[href*='.html']")
            img_el = item.select_one("img")

            if not name_el or not price_el:
                continue
            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            link = link_el.get("href", "") if link_el else ""
            link = self._abs_url(link)
            img = img_el.get("src", "") if img_el else ""
            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True, image_url=img, description="",
            ))

        self._wait()
        return results if results else None
