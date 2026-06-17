from .base import BaseScraper, ScraperResult
from .animalis import AnimalisScraper
from .jardiland import JardilandScraper
from .truffaut import TruffautScraper
from .produitsveto import ProduitsVetoScraper

ALL_SCRAPERS = [
    ("animalis", AnimalisScraper),
    ("jardiland", JardilandScraper),
    ("truffaut", TruffautScraper),
    ("produitsveto", ProduitsVetoScraper),
]
