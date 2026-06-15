"""
Scraper Animalis (animalis.com).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class AnimalisScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="animalis",
            base_url="https://www.animalis.com",
            search_path="/recherche"
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".product-card, article.product, .product-item, [data-product-id]")

        for item in items:
            name_el = (
                item.select_one(".product-card-title a, .product-name a, h3 a")
                or item.select_one("a[title]")
            )
            price_el = item.select_one(".product-price, .price, .current-price, .price-value")
            link_el = (
                item.select_one("a.product-card-link, .product-card-title a")
                or item.select_one("a[href*='/p-']")
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

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
            ))

        self._wait()
        return results if results else None
