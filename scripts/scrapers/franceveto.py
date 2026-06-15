"""
Scraper France-Véto (france-veto.com).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class FranceVetoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="franceveto",
            base_url="https://www.france-veto.com",
            search_path="/recherche"
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".product-card, article.product, .product-item, li.product")

        for item in items:
            name_el = item.select_one(".product-name a, h2 a, h3 a, a[title]")
            price_el = item.select_one(".price, .product-price, [data-price]")
            link_el = item.select_one("a[href*='/produit/'], a.product-link") or name_el
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
