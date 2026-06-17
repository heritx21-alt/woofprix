from .base import BaseScraper, ScraperResult
from .animalis import AnimalisScraper
from .truffaut import TruffautScraper
from .produitsveto import ProduitsVetoScraper

ALL_SCRAPERS = [
    ("animalis", AnimalisScraper),
    ("truffaut", TruffautScraper),
    ("produitsveto", ProduitsVetoScraper),
]
