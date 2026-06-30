from .base import BaseScraper, ScraperResult
from .animalis import AnimalisScraper
from .truffaut import TruffautScraper
from .produitsveto import ProduitsVetoScraper
from .amazon import AmazonScraper

ALL_SCRAPERS = [
    ("animalis", AnimalisScraper),
    ("truffaut", TruffautScraper),
    ("produitsveto", ProduitsVetoScraper),
    ("amazon", AmazonScraper),
]
