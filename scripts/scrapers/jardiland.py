"""Scraper Jardiland (jardiland.com) via Playwright (contourne Cloudflare)."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult
from .playwright_base import fetch_html


class JardilandScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="jardiland",
            base_url="https://www.jardiland.com",
            search_path="/search",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        html = fetch_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        results = []
        items = soup.select("article.ds-ens-product-card")

        if not items:
            return None

        for item in items:
            brand_el = item.select_one(".ds-ens-product-card__brand")
            name_el = item.select_one(".ds-ens-product-card__name")
            price_el = item.select_one(".ds-ens-product-card__price")
            img_el = item.select_one(".ds-ens-product-card__visual-box img")

            if not name_el or not price_el:
                continue

            brand = brand_el.get_text(strip=True) if brand_el else ""
            product_name = name_el.get_text(strip=True)
            full_name = f"{brand} {product_name}".strip()
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                continue

            img = ""
            if img_el:
                img = img_el.get("src") or ""
            if not img and img_el:
                img = img_el.get("data-src") or ""

            results.append(ScraperResult(
                product_name=full_name, price=price, shipping=0,
                url=url, in_stock=True,
                image_url=img, description="",
            ))

        return results if results else None
