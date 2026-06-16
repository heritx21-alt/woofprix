"""
Scraper Truffaut (truffaut.com).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class TruffautScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="truffaut",
            base_url="https://www.truffaut.com",
            search_path="/catalogsearch/result/",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select("li.product-item")

        for item in items:
            name_el = item.select_one("h2.product-name")
            price_el = item.select_one(".price")
            link_el = item.select_one("a.product.product-item-photo")
            img_el = item.select_one("img[src]")
            desc_el = item.select_one("h3.product-brand")

            if not name_el or not price_el:
                continue
            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue
            link = link_el.get("href", "") if link_el else ""
            link = self._abs_url(link)
            img = img_el.get("src", "") if img_el else ""
            brand = desc_el.get_text(strip=True) if desc_el else ""

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
                image_url=img, description=brand,
            ))

        self._wait()
        return results if results else None
