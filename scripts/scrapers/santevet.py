"""Scraper Santévet (santevet.com) — WooCommerce AJAX, needs Playwright."""
from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper, ScraperResult
from .playwright_base import fetch_html


class SantevetScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            name="santevet",
            base_url="https://www.santevet.com",
            search_path="/?s=",
        )

    def search_product(self, query: str) -> Optional[list[ScraperResult]]:
        url = self._make_search_url(query)
        html = fetch_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")
        results = []

        # Check if we're on a single product page (redirected from search)
        product_el = soup.select_one("[class*=product], .product")
        cart_el = soup.select_one(".single_add_to_cart_button, .add_to_cart_button")
        price_el = soup.select_one(".price, [class*=price], .amount, .woocommerce-Price-amount")

        if price_el and cart_el:
            name_el = soup.select_one("h1, [class*=product_title]")
            name = name_el.get_text(strip=True) if name_el else ""

            # Get the price from JSON-LD or HTML
            price = self._parse_price(price_el.get_text(strip=True))
            if not price:
                ld = soup.select_one('script[type="application/ld+json"]')
                if ld:
                    import json
                    try:
                        data = json.loads(ld.string)
                        if isinstance(data, dict) and "offers" in data:
                            price = data["offers"].get("price", price)
                    except: pass

            if price:
                link = url
                img_el = soup.select_one(".woocommerce-product-gallery img, [class*=gallery] img, .product img")
                img = img_el.get("src", "") if img_el else ""
                results.append(ScraperResult(
                    product_name=name, price=price, shipping=0,
                    url=link, in_stock=True,
                    image_url=img, description="",
                ))
        else:
            items = soup.select("li.product, .product-item")
            for item in items:
                name_el = item.select_one("h2.woocommerce-loop-product__title, [class*=title]")
                pr_el = item.select_one(".price, .amount")
                link_el = item.select_one("a[href]")
                img_el = item.select_one("img")
                if not name_el or not pr_el:
                    continue
                name = name_el.get_text(strip=True)
                price = self._parse_price(pr_el.get_text(strip=True))
                if not price:
                    continue
                link = link_el.get("href", "") if link_el else ""
                img = img_el.get("src", "") if img_el else ""
                results.append(ScraperResult(
                    product_name=name, price=price, shipping=0,
                    url=link, in_stock=True,
                    image_url=img, description="",
                ))

        return results if results else None
