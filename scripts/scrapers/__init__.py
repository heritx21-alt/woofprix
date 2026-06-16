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
from .directvet import DirectVetScraper
from .cernunos import CernunosScraper
from .santevet import SantevetScraper
from .ultrapremium import UltraPremiumScraper
from .petsonic import PetsonicScraper

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
    ("directvet", DirectVetScraper),
    ("cernunos", CernunosScraper),
    ("santevet", SantevetScraper),
    ("ultrapremium", UltraPremiumScraper),
    ("petsonic", PetsonicScraper),
]
