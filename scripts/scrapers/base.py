"""Classe de base pour tous les scrapers WoofPrix."""
import time
import random
import re
from abc import ABC, abstractmethod
from typing import Optional
import httpx
from bs4 import BeautifulSoup


class ScraperResult:
    def __init__(self, product_name: str, price: float, shipping: float = 0,
                 url: str = "", in_stock: bool = True):
        self.product_name = product_name
        self.price = price
        self.shipping = shipping
        self.url = url
        self.in_stock = in_stock

    def to_dict(self):
        return {
            "product_name": self.product_name,
            "price": round(self.price, 2),
            "shipping": self.shipping,
            "url": self.url,
            "in_stock": self.in_stock,
        }


class BaseScraper(ABC):
    def __init__(self, name: str, base_url: str, search_path: str = "",
                 delay: float = 1.0):
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
            timeout=15.0,
        )

    def _wait(self):
        time.sleep(self.delay + random.uniform(0, 0.5))

    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            print(f"  ⚠ {self.name}: requête échouée pour {url} — {e}")
            return None

    def _parse_price(self, text: str) -> Optional[float]:
        if not text:
            return None
        text = text.replace("\xa0", " ").replace(",", ".").strip()
        match = re.search(r"(\d+[\.\s]?\d*[\.,]?\d*)", text)
        if match:
            raw = match.group(1).replace(" ", "").replace(",", ".")
            try:
                return float(raw)
            except ValueError:
                return None
        return None

    def _make_search_url(self, query: str) -> str:
        from urllib.parse import quote
        q = quote(query)
        if self.search_path:
            sep = "&" if "?" in self.search_path else "?"
            return f"{self.base_url}{self.search_path}{sep}q={q}"
        return f"{self.base_url}/search?q={q}"

    @abstractmethod
    def search_product(self, product_name: str) -> Optional[list[ScraperResult]]:
        ...

    def close(self):
        self.client.close()
