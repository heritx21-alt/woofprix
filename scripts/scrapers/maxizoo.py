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
            search_path="/catalogsearch/result/",
            delay=1.5,
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select("li.product-item, .item.product")

        for item in items:
            name_el = item.select_one(".product-item-name a, a.product-item-link")
            price_el = item.select_one(".price, .special-price .price, .normal-price .price")
            link_el = item.select_one("a.product-item-link, .product-item-name a")
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
