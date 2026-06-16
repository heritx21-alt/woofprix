"""
Base scraper — version recherche par mot-clé.
Chaque scraper définit un chemin de recherche et des sélecteurs CSS.
"""
import time
import random
import re
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import quote, urljoin

import httpx
from bs4 import BeautifulSoup


class ScraperResult:
    def __init__(self, product_name: str, price: float, shipping: float = 0,
                 url: str = "", in_stock: bool = True,
                 image_url: str = "", description: str = ""):
        self.product_name = product_name
        self.price = price
        self.shipping = shipping
        self.url = url
        self.in_stock = in_stock
        self.image_url = image_url
        self.description = description

    def to_dict(self):
        return {
            "product_name": self.product_name,
            "price": round(self.price, 2),
            "shipping": self.shipping,
            "url": self.url,
            "in_stock": self.in_stock,
            "image_url": self.image_url,
            "description": self.description,
        }


class BaseScraper(ABC):
    def __init__(self, name: str, base_url: str,
                 search_path: str = "/recherche",
                 delay: float = 0.1):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.search_path = search_path
        self.delay = delay
        self.client = httpx.Client(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/125.0.0.0 Safari/537.36",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            follow_redirects=True,
            timeout=5.0,
        )

    def _wait(self):
        time.sleep(self.delay + random.uniform(0, 0.5))

    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        try:
            resp = self.client.get(url, timeout=4.0)
            if resp.status_code in (403, 429, 503):
                print(f"⚠ bloqué ({resp.status_code})")
                return None
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            print(f"⚠ {e}")
            return None

    def _parse_price(self, text: Optional[str]) -> Optional[float]:
        if not text:
            return None
        text = text.replace("\xa0", " ").replace(",", ".").strip()
        match = re.search(r"(\d+[\.\s]?\d*[\.,]?\d*)", text)
        if match:
            raw = match.group(1).replace(" ", "").replace(",", ".")
            try:
                val = float(raw)
                return val if val > 0.1 else None
            except ValueError:
                return None
        return None

    def _make_search_url(self, query: str) -> str:
        q = quote(query)
        sp = self.search_path
        if "?" in sp and sp.endswith("="):
            return f"{self.base_url}{sp}{q}"
        sep = "&" if "?" in sp else "?"
        return f"{self.base_url}{sp}{sep}q={q}"

    def _abs_url(self, href: str) -> str:
        if not href:
            return ""
        if href.startswith("http"):
            return href
        return urljoin(self.base_url, href)

    @abstractmethod
    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        """
        Cherche un produit sur le site et retourne les résultats.
        """
        ...

    def close(self):
        self.client.close()
