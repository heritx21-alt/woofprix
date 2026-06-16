"""Scraper Direct-Vet (direct-vet.fr) — PrestaShop."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class DirectVetScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="directvet",
            base_url="https://www.direct-vet.fr",
            search_path="/?s=",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".ajax_block_product, .product_block")

        for item in items:
            name_el = item.select_one("h5[itemprop='name'] a, [itemprop='name'] a, h5 a")
            price_el = item.select_one(".price, .product-price, [itemprop='price']")
            link_el = item.select_one("a.product_img_link, a[itemprop='url']")
            img_el = item.select_one("img[src]")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue

            link = link_el.get("href", "") if link_el else ""
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
