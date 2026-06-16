"""
Scraper Animalis (animalis.com).
"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class AnimalisScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="animalis",
            base_url="https://www.animalis.com",
            search_path="/recherche"
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select(".isk-product-card")

        for item in items:
            name_el = item.select_one("a.isk-product-card__headline-link")
            price_el = item.select_one(".isk-product-card__price")
            img_el = item.select_one("img[src]")
            desc_el = item.select_one(".isk-product-card__headline-link")

            if not name_el or not price_el:
                continue
            name = name_el.get_text(strip=True)
            price = self._parse_price(price_el.get("data-min-price", price_el.get_text(strip=True)))
            if not price:
                continue
            link = name_el.get("href", "")
            link = self._abs_url(link)
            img = img_el.get("src", "") if img_el else ""
            desc = desc_el.get_text(strip=True) if desc_el else ""

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
                image_url=img, description=desc,
            ))

        self._wait()
        return results if results else None
