"""Scraper Produits-Véto (produits-veto.com) — WordPress/WooCommerce."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class ProduitsVetoScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="produitsveto",
            base_url="https://www.produits-veto.com",
            search_path="/?s=",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select("li.product")

        for item in items:
            name_el = item.select_one("h2.woocommerce-loop-product__title")
            price_el = item.select_one(".price")
            link_el = item.select_one("a.woocommerce-loop-product__link")
            img_el = item.select_one("a.woocommerce-loop-product__link img")

            if not name_el or not price_el:
                continue

            name = name_el.get_text(strip=True)

            # WooCommerce price can be range like "46,16€ – 58,00€" — take min
            price_text = price_el.get_text(strip=True).replace("\u2013", "-").replace("\u2014", "-")
            if "-" in price_text:
                price_text = price_text.split("-")[0].strip()
            price = self._parse_price(price_text)
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
