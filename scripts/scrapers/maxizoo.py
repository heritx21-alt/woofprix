"""
Scraper MaxiZoo (maxizoo.fr).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class MaxiZooScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="maxizoo",
            base_url="https://www.maxizoo.fr",
            search_path="/search",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".product-teaser")

        for item in items:
            name_el = item.select_one("a.pt-header")
            price_el = item.select_one(".p-regular-price-value")
            link_el = name_el

            if not name_el or not price_el:
                continue
            brand = name_el.select_one(".pt-subhead")
            product = name_el.select_one(".pt-head")
            brand_text = brand.get_text(strip=True) if brand else ""
            product_text = product.get_text(strip=True) if product else ""
            name = f"{brand_text} {product_text}".strip()
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
