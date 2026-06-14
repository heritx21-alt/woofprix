"""Scraper MaxiZoo (maxizoo.fr)."""
from typing import Optional
from .base import BaseScraper, ScraperResult


class MaxiZooScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="maxizoo",
            base_url="https://www.maxizoo.fr",
            search_path="/catalogsearch/result/",
            delay=1.5,
        )

    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        url = f"{self.base_url}{self.search_path}?q={product_name.replace(' ', '+')}"
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        for item in soup.select("li.product-item, .product-item, .item.product"):
            name_el = item.select_one(".product-item-name a, .product.name a, a.product-item-link")
            price_el = item.select_one(".price, .special-price .price, .normal-price .price")
            link_el = item.select_one("a.product-item-link, .product-item-name a")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            link = link_el.get("href", "") if link_el else ""

            if price and price > 0:
                results.append(ScraperResult(
                    product_name=name,
                    price=price,
                    shipping=0,
                    url=link,
                    in_stock=True,
                ))

        self._wait()
        return results if results else None
