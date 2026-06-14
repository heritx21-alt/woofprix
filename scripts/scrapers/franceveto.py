"""Scraper France-Véto (france-veto.com)."""
from typing import Optional
from .base import BaseScraper, ScraperResult


class FranceVetoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="franceveto",
            base_url="https://www.france-veto.com",
            search_path="/recherche",
            delay=1.5,
        )

    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        url = f"{self.base_url}{self.search_path}?q={product_name.replace(' ', '+')}"
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        for item in soup.select(".product-miniature, article.product, .product-item, [data-product-id]"):

            name_el = item.select_one(".product-title a, .product-name a, h3 a, [itemprop='name']")
            price_el = item.select_one(".price, .product-price, [itemprop='price'], .current-price")
            link_el = item.select_one("a.product-name, .product-title a, a[itemprop='url']")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                data_p = price_el.get("content") or price_el.get("data-price")
                if data_p:
                    price = self._parse_price(data_p)
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
