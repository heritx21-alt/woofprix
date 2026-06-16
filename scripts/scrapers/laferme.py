"""Scraper La Ferme des Animaux (lafermedesanimaux.com) — Next.js."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class LaFermeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="laferme",
            base_url="https://www.lafermedesanimaux.com",
            search_path="/search",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select("a.product")

        for item in items:
            name = item.get_text(strip=True)
            price_el = item.select_one("[class*=price]")
            img_el = item.select_one("img")

            if not name or not price_el:
                continue

            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue

            link = item.get("href", "")
            link = self._abs_url(link)

            img = ""
            if img_el:
                img = img_el.get("src") or img_el.get("data-src") or ""

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
                image_url=img, description="",
            ))

        self._wait()
        return results if results else None
