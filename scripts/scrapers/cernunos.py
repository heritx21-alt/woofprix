"""Scraper Cernunos (cernunos.fr) — Shopify."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class CernunosScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="cernunos",
            base_url="https://www.cernunos.fr",
            search_path="/search?q=",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select("[class*=product]")

        for item in items:
            price_el = item.select_one(".price, [class*=price]")
            a = item.select_one("a[href*='/products/']")
            img_el = item.select_one("img")

            if not price_el or not a:
                continue

            name = item.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue

            link = a.get("href", "")
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
