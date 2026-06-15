from .base import BaseScraper, ScraperResult
from .zoomalia import ZoomaliaScraper
from .maxizoo import MaxiZooScraper
from .animalis import AnimalisScraper
from .jardiland import JardilandScraper
from .truffaut import TruffautScraper
from .laferme import LaFermeScraper
from .medor import MedorScraper
from .produitsveto import ProduitsVetoScraper
from .franceveto import FranceVetoScraper
from .universveto import UniversVetoScraper

ALL_SCRAPERS = [
    ("zoomalia", ZoomaliaScraper),
    ("maxizoo", MaxiZooScraper),
    ("animalis", AnimalisScraper),
    ("jardiland", JardilandScraper),
    ("truffaut", TruffautScraper),
    ("laferme", LaFermeScraper),
    ("medor", MedorScraper),
    ("produitsveto", ProduitsVetoScraper),
    ("franceveto", FranceVetoScraper),
    ("universveto", UniversVetoScraper),
]
