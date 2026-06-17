from .base import BaseScraper, ScraperResult
from .maxizoo import MaxiZooScraper
from .animalis import AnimalisScraper
from .jardiland import JardilandScraper
from .truffaut import TruffautScraper
from .laferme import LaFermeScraper
from .produitsveto import ProduitsVetoScraper
from .directvet import DirectVetScraper
from .cernunos import CernunosScraper

ALL_SCRAPERS = [
    ("maxizoo", MaxiZooScraper),
    ("animalis", AnimalisScraper),
    ("jardiland", JardilandScraper),
    ("truffaut", TruffautScraper),
    ("laferme", LaFermeScraper),
    ("produitsveto", ProduitsVetoScraper),
    ("directvet", DirectVetScraper),
    ("cernunos", CernunosScraper),
]
