from .base import BaseScraper, ScraperResult
from .maxizoo import MaxiZooScraper
from .animalis import AnimalisScraper
from .jardiland import JardilandScraper
from .truffaut import TruffautScraper
from .produitsveto import ProduitsVetoScraper
from .directvet import DirectVetScraper

ALL_SCRAPERS = [
    ("maxizoo", MaxiZooScraper),
    ("animalis", AnimalisScraper),
    ("jardiland", JardilandScraper),
    ("truffaut", TruffautScraper),
    ("produitsveto", ProduitsVetoScraper),
    ("directvet", DirectVetScraper),
]
