"""Scraper Jardiland (jardiland.com)."""
from typing import Optional
from .base import BaseScraper, ScraperResult


class JardilandScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="jardiland",
            base_url="https://www.jardiland.com",
            search_path="/search",
            delay=1.5,
        )

    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        url = f"{self.base_url}{self.search_path}?q={product_name.replace(' ', '+')}"
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        for item in soup.select(".product-card, .product-item, article.product, [data-product-id]"):

            name_el = item.select_one(".product-card-title, .product-name, h3 a, .product-title a")
            price_el = item.select_one(".product-price, .price, .current-price, .a-price")
            link_el = item.select_one("a.product-card-link, a.product-link, a[href*='/p-']")

            if not name_el and link_el:
                name_el = link_el

            if not name_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True)) if price_el else None
            link = link_el.get("href", "") if link_el else ""
            if link and not link.startswith("http"):
                link = f"{self.base_url}{link}"

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
