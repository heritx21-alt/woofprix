"""Base scraper using Playwright (sync) for shops blocked by Cloudflare/security systems."""
import time
from typing import Optional
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BROWSER = None
CONTEXT = None
PLAY = None


def _ensure_browser():
    global BROWSER, CONTEXT, PLAY
    if BROWSER is None:
        PLAY = sync_playwright().start()
        BROWSER = PLAY.chromium.launch(headless=True)
        CONTEXT = BROWSER.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            locale="fr-FR",
            viewport={"width": 1280, "height": 720},
        )
    return BROWSER, CONTEXT


def fetch_html(url: str, timeout: int = 15000) -> Optional[str]:
    """Fetch a page with Playwright and return the rendered HTML."""
    _, context = _ensure_browser()
    try:
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=timeout)
        time.sleep(1)
        html = page.content()
        page.close()
        return html
    except Exception as e:
        print(f"    Playwright error: {e}")
        return None


def close():
    global BROWSER, CONTEXT, PLAY
    if PLAY:
        PLAY.stop()
    BROWSER = None
    CONTEXT = None
    PLAY = None
