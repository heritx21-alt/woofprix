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
        items = soup.select("a.product-info__caption")

        for item in items:
            price_el = item.select_one("[class*=price]")
            a = item
            img_el = item.select_one("img")
            name_el = item

            if not price_el:
                continue

            full_text = name_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True)
            price = self._parse_price(price_text)
            if not price:
                continue

            name = full_text.replace(price_text, "").strip()
            name = name.rsplit("/", 1)[0].strip()

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
