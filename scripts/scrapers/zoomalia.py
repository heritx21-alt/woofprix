"""
Scraper Zoomalia (zoomalia.com) — recherche.
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class ZoomaliaScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="zoomalia",
            base_url="https://www.zoomalia.com",
            search_path="/recherche",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = (
            soup.select("div[class*='product'], article.product")
            or soup.select("li.product, .product-item")
        )

        for item in items:
            name_el = (
                item.select_one("a[class*='product']")
                or item.select_one("a[title]")
                or item.select_one("h2 a, h3 a")
            )
            price_el = (
                item.select_one("span.price, div.price, .product-price, .current-price")
                or item.select_one("[data-price]")
            )
            link_el = (
                item.select_one("a[href*='-p-']")
                or item.select_one("a[href*='/produit/']")
                or name_el
            )
            img_el = item.select_one("img")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            link = link_el.get("href", "") if link_el else ""
            link = self._abs_url(link)
            in_stock = True

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=in_stock,
            ))

        self._wait()
        return results if results else None
