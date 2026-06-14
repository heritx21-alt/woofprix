"""Scraper Zoomalia (zoomalia.com)."""
from typing import Optional
from .base import BaseScraper, ScraperResult


class ZoomaliaScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="zoomalia",
            base_url="https://www.zoomalia.com",
            search_path="/recherche",
            delay=1.5,
        )

    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        url = f"{self.base_url}{self.search_path}?q={product_name.replace(' ', '+')}"
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        for item in soup.select(".product-miniature, article.product, .product-item, [data-product]"):

            name_el = (item.select_one(".product-title a, h2.product-name a, .product-name a, .product-title")
                       or item.select_one("a.product-name"))
            price_el = (item.select_one(".price, .product-price, .current-price")
                        or item.select_one("[data-price]"))
            link_el = (item.select_one("a.product-name, .product-title a, h2 a")
                       or item.select_one("a[href*='/produit/']"))

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                data_price = price_el.get("data-price") or price_el.get("content")
                if data_price:
                    price = self._parse_price(data_price)
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
