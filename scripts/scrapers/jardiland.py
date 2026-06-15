"""
Scraper Jardiland (jardiland.com).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class JardilandScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="jardiland",
            base_url="https://www.jardiland.com",
            search_path="/search"
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".product-card, .product-item, article.product")

        for item in items:
            name_el = item.select_one(".product-card-title, .product-name, h3 a, .product-title a")
            price_el = item.select_one(".product-price, .price, .current-price, .a-price")
            link_el = (
                item.select_one("a.product-card-link, a.product-link, a[href*='/p-']")
                or name_el
            )
            img_el = item.select_one("img")

            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            if price_el:
                price = self._parse_price(price_el.get_text(strip=True))
            else:
                price = None
            if not price:
                continue
            link = link_el.get("href", "") if link_el else ""
            link = self._abs_url(link)

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
            ))

        self._wait()
        return results if results else None
