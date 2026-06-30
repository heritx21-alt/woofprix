from typing import Optional
import httpx
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult


class AmazonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="amazon",
            base_url="https://www.amazon.fr",
            search_path="/s?k=",
        )
        # Amazon is aggressive, use shorter timeout
        self.client = httpx.Client(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/125.0.0.0 Safari/537.36",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            follow_redirects=True,
            timeout=3.0,
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        soup = self._fetch(url)
        if not soup:
            return None

        results = []
        items = soup.select('div[data-component-type="s-search-result"]')

        for item in items:
            name_el = item.select_one("h2 a.a-link-normal span")
            price_whole = item.select_one(".a-price-whole")
            price_frac = item.select_one(".a-price-fraction")
            link_el = item.select_one("h2 a.a-link-normal")
            img_el = item.select_one("img.s-image")

            if not name_el:
                continue

            name = name_el.get_text(strip=True)

            price = None
            if price_whole:
                p_text = price_whole.get_text(strip=True).replace(",", ".")
                if price_frac:
                    p_text += "." + price_frac.get_text(strip=True)
                try:
                    price = float(p_text)
                except ValueError:
                    pass

            if not price or price < 0.1:
                continue

            link = link_el.get("href", "") if link_el else ""
            if link and not link.startswith("http"):
                link = self._abs_url(link)
            img = img_el.get("src", "") if img_el else ""

            results.append(ScraperResult(
                product_name=name, price=price, shipping=0,
                url=link, in_stock=True,
                image_url=img, description="",
            ))

        self._wait()
        return results if results else None

    def _make_search_url(self, query: str) -> str:
        from urllib.parse import quote
        q = quote(query)
        return f"{self.base_url}/s?k={q}"

    def close(self):
        self.client.close()
