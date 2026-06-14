"""Scraper Médor & Compagnie (medor-et-compagnie.fr)."""
from typing import Optional
from .base import BaseScraper, ScraperResult


class MedorScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="medor",
            base_url="https://www.medor-et-compagnie.fr",
            search_path="/search",
            delay=1.5,
        )

    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        url = f"{self.base_url}{self.search_path}?q={product_name.replace(' ', '+')}"
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        for item in soup.select(".product-card, .product-item, article, [class*='product']"):

            name_el = item.select_one(".product-card-title a, .product-name a, h3 a, .product-title")
            price_el = item.select_one(".price, .product-price, .current-price, [class*='price']")
            link_el = item.select_one("a.product-card-link, a[href*='/p-'], a[href*='/produit']")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
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
