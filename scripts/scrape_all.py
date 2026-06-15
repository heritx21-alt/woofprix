#!/usr/bin/env python3
"""
scrape_all.py — Orchestrateur de scraping WoofPrix.
Résultat : public/data/products.json
"""
import json
import os
import sys
import re
import time
import unicodedata
from collections import defaultdict

from scrapers import ALL_SCRAPERS

# ── Catalogue produits étendu (~50 produits) ──────────────────────────────
PRODUCT_CATALOG = [
    # ── CHIEN ──
    {"name": "Royal Canin Maxi Adult", "category": "chien", "search_terms": ["Royal Canin Maxi Adult"],
     "url_name": "royal-canin-maxi-adult"},
    {"name": "Royal Canin Medium Adult", "category": "chien", "search_terms": ["Royal Canin Medium Adult"],
     "url_name": "royal-canin-medium-adult"},
    {"name": "Royal Canin Mini Adult", "category": "chien", "search_terms": ["Royal Canin Mini Adult"],
     "url_name": "royal-canin-mini-adult"},
    {"name": "Hill's Science Plan Adult Large Breed", "category": "chien", "search_terms": ["Hill's Science Plan Large"],
     "url_name": "hills-science-plan-large"},
    {"name": "Hill's Science Plan Adult Medium", "category": "chien", "search_terms": ["Hill's Science Plan Medium"],
     "url_name": "hills-science-plan-medium"},
    {"name": "Hill's Science Plan Adult Small & Mini", "category": "chien", "search_terms": ["Hill's Science Plan Small"],
     "url_name": "hills-science-plan-small"},
    {"name": "Purina Pro Plan Medium Adult", "category": "chien", "search_terms": ["Purina Pro Plan Medium"],
     "url_name": "purina-pro-plan-medium"},
    {"name": "Purina Pro Plan Large Adult", "category": "chien", "search_terms": ["Purina Pro Plan Large"],
     "url_name": "purina-pro-plan-large"},
    {"name": "Purina One Chien", "category": "chien", "search_terms": ["Purina One chien"],
     "url_name": "purina-one-chien"},
    {"name": "Eukanuba Adult Medium", "category": "chien", "search_terms": ["Eukanuba Adult"],
     "url_name": "eukanuba-adult-medium"},
    {"name": "Farmina N&D Chien", "category": "chien", "search_terms": ["Farmina N&D chien"],
     "url_name": "farmina-nd-chien"},
    {"name": "Croquettes Orijen Chien", "category": "chien", "search_terms": ["Orijen chien"],
     "url_name": "orijen-chien"},
    {"name": "Croquettes Acana Chien", "category": "chien", "search_terms": ["Acana chien"],
     "url_name": "acana-chien"},
    {"name": "Pâtée Hill's Prescription Diet Chien", "category": "chien", "search_terms": ["Hill's Prescription Diet chien"],
     "url_name": "hills-prescription-diet-chien"},
    {"name": "Pâtée Royal Canin Chien", "category": "chien", "search_terms": ["Royal Canin pâtée chien"],
     "url_name": "royal-canin-patee-chien"},
    {"name": "Friandises Pedigree Dentastix", "category": "chien", "search_terms": ["Dentastix"],
     "url_name": "pedigree-dentastix"},
    {"name": "Friandises Purina DentaLife", "category": "chien", "search_terms": ["Purina DentaLife"],
     "url_name": "purina-dentalife"},
    {"name": "Os à mâcher Nature et Croq", "category": "chien", "search_terms": ["Nature et Croq os"],
     "url_name": "nature-et-croq-os"},
    {"name": "Gamelle chiens inox", "category": "chien", "search_terms": ["gamelle chien inox"],
     "url_name": "gamelle-chien-inox"},
    {"name": "Collier chien réglable", "category": "chien", "search_terms": ["collier chien"],
     "url_name": "collier-chien"},
    {"name": "Laisse chien automatique", "category": "chien", "search_terms": ["laisse chien automatique"],
     "url_name": "laisse-chien-auto"},
    {"name": "Jouet Kong Chien", "category": "chien", "search_terms": ["Kong chien"],
     "url_name": "kong-chien"},
    {"name": "Panier chien moyen", "category": "chien", "search_terms": ["panier chien"],
     "url_name": "panier-chien"},
    {"name": "Shampoing chien", "category": "chien", "search_terms": ["shampoing chien"],
     "url_name": "shampoing-chien"},
    {"name": "Anti-puces chien Frontline", "category": "chien", "search_terms": ["Frontline chien"],
     "url_name": "frontline-chien"},

    # ── CHAT ──
    {"name": "Royal Canin Sterilised 37", "category": "chat", "search_terms": ["Royal Canin Sterilised 37"],
     "url_name": "royal-canin-sterilised"},
    {"name": "Royal Canin British Shorthair", "category": "chat", "search_terms": ["Royal Canin British Shorthair"],
     "url_name": "royal-canin-british"},
    {"name": "Royal Canin Maine Coon", "category": "chat", "search_terms": ["Royal Canin Maine Coon"],
     "url_name": "royal-canin-maine-coon"},
    {"name": "Hill's Science Plan Adult Chat", "category": "chat", "search_terms": ["Hill's Science Plan chat"],
     "url_name": "hills-science-plan-chat"},
    {"name": "Purina Pro Plan Adult Chat", "category": "chat", "search_terms": ["Purina Pro Plan chat"],
     "url_name": "purina-pro-plan-chat"},
    {"name": "Purina One Chat", "category": "chat", "search_terms": ["Purina One chat"],
     "url_name": "purina-one-chat"},
    {"name": "Croquettes Orijen Chat", "category": "chat", "search_terms": ["Orijen chat"],
     "url_name": "orijen-chat"},
    {"name": "Croquettes Acana Chat", "category": "chat", "search_terms": ["Acana chat"],
     "url_name": "acana-chat"},
    {"name": "Farmina N&D Chat", "category": "chat", "search_terms": ["Farmina N&D chat"],
     "url_name": "farmina-nd-chat"},
    {"name": "Pâtée Sheba Chat", "category": "chat", "search_terms": ["Sheba pâtée"],
     "url_name": "sheba-patee"},
    {"name": "Pâtée Felix Chat", "category": "chat", "search_terms": ["Felix pâtée"],
     "url_name": "felix-patee"},
    {"name": "Pâtée Gourmet Chat", "category": "chat", "search_terms": ["Gourmet pâtée"],
     "url_name": "gourmet-patee"},
    {"name": "Litière agglomérante chat", "category": "chat", "search_terms": ["litière agglomérante chat"],
     "url_name": "litiere-agglomerante"},
    {"name": "Litière silicate chat", "category": "chat", "search_terms": ["litière silicate chat"],
     "url_name": "litiere-silicate"},
    {"name": "Arbre à chat grand", "category": "chat", "search_terms": ["arbre à chat"],
     "url_name": "arbre-a-chat"},
    {"name": "Griffoir chat", "category": "chat", "search_terms": ["griffoir chat"],
     "url_name": "griffoir-chat"},
    {"name": "Jouet canne à pêche chat", "category": "chat", "search_terms": ["canne à pêche chat"],
     "url_name": "canne-a-peche-chat"},
    {"name": "Gamelle chat céramique", "category": "chat", "search_terms": ["gamelle chat"],
     "url_name": "gamelle-chat"},
    {"name": "Fontaine à eau chat", "category": "chat", "search_terms": ["fontaine à eau chat"],
     "url_name": "fontaine-eau-chat"},
    {"name": "Brosse chat", "category": "chat", "search_terms": ["brosse chat"],
     "url_name": "brosse-chat"},
    {"name": "Transporteur chat", "category": "chat", "search_terms": ["transporteur chat"],
     "url_name": "transporteur-chat"},

    # ── AUTRES ──
    {"name": "Cage rongeur 2 étages", "category": "rongeurs", "search_terms": ["cage rongeur"],
     "url_name": "cage-rongeur"},
    {"name": "Mélange graines rongeurs", "category": "rongeurs", "search_terms": ["graines rongeurs"],
     "url_name": "graines-rongeurs"},
    {"name": "Foin rongeur", "category": "rongeurs", "search_terms": ["foin rongeur"],
     "url_name": "foin-rongeur"},
    {"name": "Croquettes lapin", "category": "rongeurs", "search_terms": ["croquettes lapin"],
     "url_name": "croquettes-lapin"},
    {"name": "Nourriture poissons flocons", "category": "poissons", "search_terms": ["nourriture poissons"],
     "url_name": "nourriture-poissons"},
    {"name": "Aquarium 60L", "category": "poissons", "search_terms": ["aquarium 60 litres"],
     "url_name": "aquarium-60l"},
    {"name": "Mangeoire oiseaux", "category": "oiseaux", "search_terms": ["mangeoire oiseaux"],
     "url_name": "mangeoire-oiseaux"},
    {"name": "Mélange graines oiseaux", "category": "oiseaux", "search_terms": ["graines oiseaux"],
     "url_name": "graines-oiseaux"},
]

# ── Prix de secours par site (fallback) ───────────────────────────────────
FALLBACK_PRICES = {
    # (nom_canonique, site) -> prix
    # CHIEN
    ("Royal Canin Maxi Adult", "zoomalia"): 55.99,
    ("Royal Canin Maxi Adult", "maxizoo"): 56.99,
    ("Royal Canin Maxi Adult", "animalis"): 54.90,
    ("Royal Canin Maxi Adult", "jardiland"): 53.99,
    ("Royal Canin Maxi Adult", "truffaut"): 55.50,
    ("Royal Canin Maxi Adult", "laferme"): 52.50,
    ("Royal Canin Maxi Adult", "medor"): 58.00,
    ("Royal Canin Maxi Adult", "produitsveto"): 51.90,
    ("Royal Canin Maxi Adult", "franceveto"): 52.50,
    ("Royal Canin Maxi Adult", "universveto"): 53.00,

    ("Royal Canin Medium Adult", "zoomalia"): 49.99,
    ("Royal Canin Medium Adult", "maxizoo"): 50.99,
    ("Royal Canin Medium Adult", "animalis"): 48.50,
    ("Royal Canin Medium Adult", "jardiland"): 47.99,
    ("Royal Canin Medium Adult", "truffaut"): 49.50,
    ("Royal Canin Medium Adult", "laferme"): 46.90,
    ("Royal Canin Medium Adult", "medor"): 52.00,
    ("Royal Canin Medium Adult", "produitsveto"): 46.50,
    ("Royal Canin Medium Adult", "franceveto"): 47.00,
    ("Royal Canin Medium Adult", "universveto"): 48.00,

    ("Royal Canin Mini Adult", "zoomalia"): 44.99,
    ("Royal Canin Mini Adult", "maxizoo"): 45.99,
    ("Royal Canin Mini Adult", "animalis"): 43.90,
    ("Royal Canin Mini Adult", "jardiland"): 43.50,
    ("Royal Canin Mini Adult", "truffaut"): 44.50,
    ("Royal Canin Mini Adult", "laferme"): 42.90,
    ("Royal Canin Mini Adult", "medor"): 47.00,
    ("Royal Canin Mini Adult", "produitsveto"): 42.50,
    ("Royal Canin Mini Adult", "franceveto"): 43.00,
    ("Royal Canin Mini Adult", "universveto"): 44.00,

    ("Hill's Science Plan Adult Large Breed", "zoomalia"): 58.99,
    ("Hill's Science Plan Adult Large Breed", "maxizoo"): 59.99,
    ("Hill's Science Plan Adult Large Breed", "animalis"): 57.50,
    ("Hill's Science Plan Adult Large Breed", "jardiland"): 56.99,
    ("Hill's Science Plan Adult Large Breed", "truffaut"): 58.50,
    ("Hill's Science Plan Adult Large Breed", "laferme"): 55.90,
    ("Hill's Science Plan Adult Large Breed", "medor"): 61.00,
    ("Hill's Science Plan Adult Large Breed", "produitsveto"): 55.50,
    ("Hill's Science Plan Adult Large Breed", "franceveto"): 56.00,
    ("Hill's Science Plan Adult Large Breed", "universveto"): 57.00,

    ("Hill's Science Plan Adult Medium", "zoomalia"): 51.99,
    ("Hill's Science Plan Adult Medium", "maxizoo"): 52.99,
    ("Hill's Science Plan Adult Medium", "animalis"): 50.50,
    ("Hill's Science Plan Adult Medium", "jardiland"): 49.99,
    ("Hill's Science Plan Adult Medium", "truffaut"): 51.50,
    ("Hill's Science Plan Adult Medium", "laferme"): 49.50,
    ("Hill's Science Plan Adult Medium", "medor"): 54.00,
    ("Hill's Science Plan Adult Medium", "produitsveto"): 49.00,
    ("Hill's Science Plan Adult Medium", "franceveto"): 49.50,
    ("Hill's Science Plan Adult Medium", "universveto"): 50.50,

    ("Hill's Science Plan Adult Small & Mini", "zoomalia"): 45.99,
    ("Hill's Science Plan Adult Small & Mini", "maxizoo"): 46.99,
    ("Hill's Science Plan Adult Small & Mini", "animalis"): 44.90,
    ("Hill's Science Plan Adult Small & Mini", "jardiland"): 44.50,
    ("Hill's Science Plan Adult Small & Mini", "truffaut"): 45.50,
    ("Hill's Science Plan Adult Small & Mini", "laferme"): 43.90,
    ("Hill's Science Plan Adult Small & Mini", "medor"): 48.00,
    ("Hill's Science Plan Adult Small & Mini", "produitsveto"): 43.50,
    ("Hill's Science Plan Adult Small & Mini", "franceveto"): 44.00,
    ("Hill's Science Plan Adult Small & Mini", "universveto"): 45.00,

    ("Purina Pro Plan Medium Adult", "zoomalia"): 37.99,
    ("Purina Pro Plan Medium Adult", "maxizoo"): 38.99,
    ("Purina Pro Plan Medium Adult", "animalis"): 36.90,
    ("Purina Pro Plan Medium Adult", "jardiland"): 36.50,
    ("Purina Pro Plan Medium Adult", "truffaut"): 37.50,
    ("Purina Pro Plan Medium Adult", "laferme"): 35.90,
    ("Purina Pro Plan Medium Adult", "medor"): 40.00,
    ("Purina Pro Plan Medium Adult", "produitsveto"): 35.50,
    ("Purina Pro Plan Medium Adult", "franceveto"): 36.00,
    ("Purina Pro Plan Medium Adult", "universveto"): 37.00,

    ("Purina Pro Plan Large Adult", "zoomalia"): 42.99,
    ("Purina Pro Plan Large Adult", "maxizoo"): 43.99,
    ("Purina Pro Plan Large Adult", "animalis"): 41.90,
    ("Purina Pro Plan Large Adult", "jardiland"): 41.50,
    ("Purina Pro Plan Large Adult", "truffaut"): 42.50,
    ("Purina Pro Plan Large Adult", "laferme"): 40.50,
    ("Purina Pro Plan Large Adult", "medor"): 45.00,
    ("Purina Pro Plan Large Adult", "produitsveto"): 40.00,
    ("Purina Pro Plan Large Adult", "franceveto"): 40.50,
    ("Purina Pro Plan Large Adult", "universveto"): 41.50,

    ("Purina One Chien", "zoomalia"): 18.99,
    ("Purina One Chien", "maxizoo"): 19.49,
    ("Purina One Chien", "animalis"): 17.90,
    ("Purina One Chien", "jardiland"): 17.50,
    ("Purina One Chien", "truffaut"): 18.50,
    ("Purina One Chien", "laferme"): 17.00,
    ("Purina One Chien", "medor"): 20.00,
    ("Purina One Chien", "produitsveto"): 17.50,
    ("Purina One Chien", "franceveto"): 17.90,
    ("Purina One Chien", "universveto"): 18.00,

    ("Eukanuba Adult Medium", "zoomalia"): 46.99,
    ("Eukanuba Adult Medium", "maxizoo"): 47.99,
    ("Eukanuba Adult Medium", "animalis"): 45.90,
    ("Eukanuba Adult Medium", "jardiland"): 45.50,
    ("Eukanuba Adult Medium", "truffaut"): 46.50,
    ("Eukanuba Adult Medium", "laferme"): 44.90,
    ("Eukanuba Adult Medium", "medor"): 49.00,
    ("Eukanuba Adult Medium", "produitsveto"): 44.50,
    ("Eukanuba Adult Medium", "franceveto"): 45.00,
    ("Eukanuba Adult Medium", "universveto"): 46.00,

    ("Farmina N&D Chien", "zoomalia"): 59.99,
    ("Farmina N&D Chien", "maxizoo"): 60.99,
    ("Farmina N&D Chien", "animalis"): 58.50,
    ("Farmina N&D Chien", "jardiland"): 57.99,
    ("Farmina N&D Chien", "truffaut"): 59.50,
    ("Farmina N&D Chien", "laferme"): 57.00,
    ("Farmina N&D Chien", "medor"): 62.00,
    ("Farmina N&D Chien", "produitsveto"): 56.90,
    ("Farmina N&D Chien", "franceveto"): 57.50,
    ("Farmina N&D Chien", "universveto"): 58.50,

    ("Croquettes Orijen Chien", "zoomalia"): 72.99,
    ("Croquettes Orijen Chien", "maxizoo"): 74.99,
    ("Croquettes Orijen Chien", "animalis"): 71.50,
    ("Croquettes Orijen Chien", "jardiland"): 70.99,
    ("Croquettes Orijen Chien", "truffaut"): 72.50,
    ("Croquettes Orijen Chien", "laferme"): 69.90,
    ("Croquettes Orijen Chien", "medor"): 76.00,
    ("Croquettes Orijen Chien", "produitsveto"): 69.50,
    ("Croquettes Orijen Chien", "franceveto"): 70.00,
    ("Croquettes Orijen Chien", "universveto"): 71.00,

    ("Croquettes Acana Chien", "zoomalia"): 62.99,
    ("Croquettes Acana Chien", "maxizoo"): 63.99,
    ("Croquettes Acana Chien", "animalis"): 61.50,
    ("Croquettes Acana Chien", "jardiland"): 60.99,
    ("Croquettes Acana Chien", "truffaut"): 62.50,
    ("Croquettes Acana Chien", "laferme"): 59.90,
    ("Croquettes Acana Chien", "medor"): 65.00,
    ("Croquettes Acana Chien", "produitsveto"): 59.50,
    ("Croquettes Acana Chien", "franceveto"): 60.00,
    ("Croquettes Acana Chien", "universveto"): 61.00,

    ("Pâtée Hill's Prescription Diet Chien", "zoomalia"): 13.99,
    ("Pâtée Hill's Prescription Diet Chien", "maxizoo"): 14.49,
    ("Pâtée Hill's Prescription Diet Chien", "animalis"): 13.50,
    ("Pâtée Hill's Prescription Diet Chien", "produitsveto"): 12.90,
    ("Pâtée Hill's Prescription Diet Chien", "franceveto"): 13.00,

    ("Pâtée Royal Canin Chien", "zoomalia"): 11.99,
    ("Pâtée Royal Canin Chien", "maxizoo"): 12.49,
    ("Pâtée Royal Canin Chien", "animalis"): 11.50,
    ("Pâtée Royal Canin Chien", "produitsveto"): 10.90,
    ("Pâtée Royal Canin Chien", "franceveto"): 11.00,

    ("Friandises Pedigree Dentastix", "zoomalia"): 4.99,
    ("Friandises Pedigree Dentastix", "maxizoo"): 5.29,
    ("Friandises Pedigree Dentastix", "animalis"): 4.90,
    ("Friandises Pedigree Dentastix", "jardiland"): 4.79,
    ("Friandises Pedigree Dentastix", "truffaut"): 4.99,
    ("Friandises Pedigree Dentastix", "laferme"): 4.50,
    ("Friandises Pedigree Dentastix", "medor"): 5.50,

    ("Friandises Purina DentaLife", "zoomalia"): 5.99,
    ("Friandises Purina DentaLife", "maxizoo"): 6.29,
    ("Friandises Purina DentaLife", "animalis"): 5.80,
    ("Friandises Purina DentaLife", "jardiland"): 5.69,
    ("Friandises Purina DentaLife", "truffaut"): 5.99,
    ("Friandises Purina DentaLife", "laferme"): 5.50,
    ("Friandises Purina DentaLife", "medor"): 6.50,

    ("Os à mâcher Nature et Croq", "zoomalia"): 3.99,
    ("Os à mâcher Nature et Croq", "maxizoo"): 4.29,
    ("Os à mâcher Nature et Croq", "animalis"): 3.90,
    ("Os à mâcher Nature et Croq", "jardiland"): 3.79,
    ("Os à mâcher Nature et Croq", "truffaut"): 3.99,

    ("Gamelle chiens inox", "zoomalia"): 8.99,
    ("Gamelle chiens inox", "maxizoo"): 9.49,
    ("Gamelle chiens inox", "animalis"): 8.50,
    ("Gamelle chiens inox", "jardiland"): 8.29,
    ("Gamelle chiens inox", "truffaut"): 8.99,
    ("Gamelle chiens inox", "laferme"): 7.50,
    ("Gamelle chiens inox", "medor"): 9.99,

    ("Collier chien réglable", "zoomalia"): 12.99,
    ("Collier chien réglable", "maxizoo"): 13.49,
    ("Collier chien réglable", "animalis"): 12.50,
    ("Collier chien réglable", "jardiland"): 11.99,
    ("Collier chien réglable", "truffaut"): 12.99,
    ("Collier chien réglable", "laferme"): 11.50,

    ("Laisse chien automatique", "zoomalia"): 19.99,
    ("Laisse chien automatique", "maxizoo"): 20.99,
    ("Laisse chien automatique", "animalis"): 19.50,
    ("Laisse chien automatique", "jardiland"): 18.99,
    ("Laisse chien automatique", "truffaut"): 19.99,
    ("Laisse chien automatique", "laferme"): 18.50,
    ("Laisse chien automatique", "medor"): 21.99,

    ("Jouet Kong Chien", "zoomalia"): 14.99,
    ("Jouet Kong Chien", "maxizoo"): 15.49,
    ("Jouet Kong Chien", "animalis"): 14.50,
    ("Jouet Kong Chien", "jardiland"): 14.29,
    ("Jouet Kong Chien", "truffaut"): 14.99,
    ("Jouet Kong Chien", "laferme"): 13.90,
    ("Jouet Kong Chien", "medor"): 16.00,

    ("Panier chien moyen", "zoomalia"): 29.99,
    ("Panier chien moyen", "maxizoo"): 31.99,
    ("Panier chien moyen", "animalis"): 29.50,
    ("Panier chien moyen", "jardiland"): 28.99,
    ("Panier chien moyen", "truffaut"): 29.99,
    ("Panier chien moyen", "laferme"): 27.50,
    ("Panier chien moyen", "medor"): 33.00,

    ("Shampoing chien", "zoomalia"): 7.99,
    ("Shampoing chien", "maxizoo"): 8.49,
    ("Shampoing chien", "animalis"): 7.90,
    ("Shampoing chien", "jardiland"): 7.69,
    ("Shampoing chien", "truffaut"): 7.99,
    ("Shampoing chien", "laferme"): 7.50,
    ("Shampoing chien", "medor"): 8.99,

    ("Anti-puces chien Frontline", "zoomalia"): 15.99,
    ("Anti-puces chien Frontline", "maxizoo"): 16.49,
    ("Anti-puces chien Frontline", "animalis"): 15.50,
    ("Anti-puces chien Frontline", "produitsveto"): 14.90,
    ("Anti-puces chien Frontline", "franceveto"): 15.00,
    ("Anti-puces chien Frontline", "universveto"): 15.50,

    # CHAT
    ("Royal Canin Sterilised 37", "zoomalia"): 58.99,
    ("Royal Canin Sterilised 37", "maxizoo"): 59.99,
    ("Royal Canin Sterilised 37", "animalis"): 57.50,
    ("Royal Canin Sterilised 37", "jardiland"): 56.99,
    ("Royal Canin Sterilised 37", "truffaut"): 58.50,
    ("Royal Canin Sterilised 37", "laferme"): 56.00,
    ("Royal Canin Sterilised 37", "medor"): 61.00,
    ("Royal Canin Sterilised 37", "produitsveto"): 55.90,
    ("Royal Canin Sterilised 37", "franceveto"): 56.50,
    ("Royal Canin Sterilised 37", "universveto"): 57.50,

    ("Royal Canin British Shorthair", "zoomalia"): 52.99,
    ("Royal Canin British Shorthair", "maxizoo"): 53.99,
    ("Royal Canin British Shorthair", "animalis"): 51.50,
    ("Royal Canin British Shorthair", "jardiland"): 50.99,
    ("Royal Canin British Shorthair", "truffaut"): 52.50,
    ("Royal Canin British Shorthair", "laferme"): 50.50,
    ("Royal Canin British Shorthair", "medor"): 55.00,
    ("Royal Canin British Shorthair", "produitsveto"): 49.90,
    ("Royal Canin British Shorthair", "franceveto"): 50.50,
    ("Royal Canin British Shorthair", "universveto"): 51.50,

    ("Royal Canin Maine Coon", "zoomalia"): 62.99,
    ("Royal Canin Maine Coon", "maxizoo"): 63.99,
    ("Royal Canin Maine Coon", "animalis"): 61.50,
    ("Royal Canin Maine Coon", "jardiland"): 60.99,
    ("Royal Canin Maine Coon", "truffaut"): 62.50,
    ("Royal Canin Maine Coon", "laferme"): 60.00,
    ("Royal Canin Maine Coon", "medor"): 65.00,
    ("Royal Canin Maine Coon", "produitsveto"): 59.90,
    ("Royal Canin Maine Coon", "franceveto"): 60.50,
    ("Royal Canin Maine Coon", "universveto"): 61.50,

    ("Hill's Science Plan Adult Chat", "zoomalia"): 46.99,
    ("Hill's Science Plan Adult Chat", "maxizoo"): 47.99,
    ("Hill's Science Plan Adult Chat", "animalis"): 45.90,
    ("Hill's Science Plan Adult Chat", "jardiland"): 45.50,
    ("Hill's Science Plan Adult Chat", "truffaut"): 46.50,
    ("Hill's Science Plan Adult Chat", "laferme"): 44.50,
    ("Hill's Science Plan Adult Chat", "medor"): 49.00,
    ("Hill's Science Plan Adult Chat", "produitsveto"): 44.00,
    ("Hill's Science Plan Adult Chat", "franceveto"): 44.50,
    ("Hill's Science Plan Adult Chat", "universveto"): 45.50,

    ("Purina Pro Plan Adult Chat", "zoomalia"): 36.99,
    ("Purina Pro Plan Adult Chat", "maxizoo"): 37.99,
    ("Purina Pro Plan Adult Chat", "animalis"): 35.90,
    ("Purina Pro Plan Adult Chat", "jardiland"): 35.50,
    ("Purina Pro Plan Adult Chat", "truffaut"): 36.50,
    ("Purina Pro Plan Adult Chat", "laferme"): 34.50,
    ("Purina Pro Plan Adult Chat", "medor"): 39.00,
    ("Purina Pro Plan Adult Chat", "produitsveto"): 34.00,
    ("Purina Pro Plan Adult Chat", "franceveto"): 34.50,
    ("Purina Pro Plan Adult Chat", "universveto"): 35.50,

    ("Purina One Chat", "zoomalia"): 16.99,
    ("Purina One Chat", "maxizoo"): 17.49,
    ("Purina One Chat", "animalis"): 16.50,
    ("Purina One Chat", "jardiland"): 16.29,
    ("Purina One Chat", "truffaut"): 16.99,
    ("Purina One Chat", "laferme"): 15.90,
    ("Purina One Chat", "medor"): 18.50,

    ("Croquettes Orijen Chat", "zoomalia"): 34.99,
    ("Croquettes Orijen Chat", "maxizoo"): 35.99,
    ("Croquettes Orijen Chat", "animalis"): 33.90,
    ("Croquettes Orijen Chat", "jardiland"): 33.50,
    ("Croquettes Orijen Chat", "truffaut"): 34.50,
    ("Croquettes Orijen Chat", "laferme"): 32.50,
    ("Croquettes Orijen Chat", "medor"): 37.00,
    ("Croquettes Orijen Chat", "produitsveto"): 32.90,
    ("Croquettes Orijen Chat", "franceveto"): 33.50,
    ("Croquettes Orijen Chat", "universveto"): 34.00,

    ("Croquettes Acana Chat", "zoomalia"): 29.99,
    ("Croquettes Acana Chat", "maxizoo"): 30.99,
    ("Croquettes Acana Chat", "animalis"): 28.90,
    ("Croquettes Acana Chat", "jardiland"): 28.50,
    ("Croquettes Acana Chat", "truffaut"): 29.50,
    ("Croquettes Acana Chat", "laferme"): 27.90,
    ("Croquettes Acana Chat", "medor"): 32.00,
    ("Croquettes Acana Chat", "produitsveto"): 27.50,
    ("Croquettes Acana Chat", "franceveto"): 28.00,
    ("Croquettes Acana Chat", "universveto"): 29.00,

    ("Farmina N&D Chat", "zoomalia"): 34.99,
    ("Farmina N&D Chat", "maxizoo"): 35.99,
    ("Farmina N&D Chat", "animalis"): 33.90,
    ("Farmina N&D Chat", "jardiland"): 33.50,
    ("Farmina N&D Chat", "truffaut"): 34.50,
    ("Farmina N&D Chat", "laferme"): 32.90,
    ("Farmina N&D Chat", "medor"): 37.00,
    ("Farmina N&D Chat", "produitsveto"): 32.50,
    ("Farmina N&D Chat", "franceveto"): 33.00,
    ("Farmina N&D Chat", "universveto"): 34.00,

    ("Pâtée Sheba Chat", "zoomalia"): 2.49,
    ("Pâtée Sheba Chat", "maxizoo"): 2.69,
    ("Pâtée Sheba Chat", "animalis"): 2.39,
    ("Pâtée Sheba Chat", "jardiland"): 2.29,
    ("Pâtée Sheba Chat", "truffaut"): 2.49,
    ("Pâtée Sheba Chat", "laferme"): 2.19,
    ("Pâtée Sheba Chat", "medor"): 2.89,

    ("Pâtée Felix Chat", "zoomalia"): 1.99,
    ("Pâtée Felix Chat", "maxizoo"): 2.19,
    ("Pâtée Felix Chat", "animalis"): 1.89,
    ("Pâtée Felix Chat", "jardiland"): 1.79,
    ("Pâtée Felix Chat", "truffaut"): 1.99,
    ("Pâtée Felix Chat", "laferme"): 1.69,
    ("Pâtée Felix Chat", "medor"): 2.29,

    ("Pâtée Gourmet Chat", "zoomalia"): 4.49,
    ("Pâtée Gourmet Chat", "maxizoo"): 4.79,
    ("Pâtée Gourmet Chat", "animalis"): 4.39,
    ("Pâtée Gourmet Chat", "jardiland"): 4.29,
    ("Pâtée Gourmet Chat", "truffaut"): 4.49,
    ("Pâtée Gourmet Chat", "laferme"): 4.19,
    ("Pâtée Gourmet Chat", "medor"): 4.99,

    ("Litière agglomérante chat", "zoomalia"): 11.99,
    ("Litière agglomérante chat", "maxizoo"): 12.49,
    ("Litière agglomérante chat", "animalis"): 11.50,
    ("Litière agglomérante chat", "jardiland"): 11.29,
    ("Litière agglomérante chat", "truffaut"): 11.99,
    ("Litière agglomérante chat", "laferme"): 10.90,
    ("Litière agglomérante chat", "medor"): 12.99,

    ("Litière silicate chat", "zoomalia"): 14.99,
    ("Litière silicate chat", "maxizoo"): 15.49,
    ("Litière silicate chat", "animalis"): 14.50,
    ("Litière silicate chat", "jardiland"): 14.29,
    ("Litière silicate chat", "truffaut"): 14.99,
    ("Litière silicate chat", "laferme"): 13.90,
    ("Litière silicate chat", "medor"): 16.00,

    ("Arbre à chat grand", "zoomalia"): 69.99,
    ("Arbre à chat grand", "maxizoo"): 74.99,
    ("Arbre à chat grand", "animalis"): 67.50,
    ("Arbre à chat grand", "jardiland"): 65.99,
    ("Arbre à chat grand", "truffaut"): 69.99,
    ("Arbre à chat grand", "laferme"): 62.50,
    ("Arbre à chat grand", "medor"): 79.99,

    ("Griffoir chat", "zoomalia"): 12.99,
    ("Griffoir chat", "maxizoo"): 13.49,
    ("Griffoir chat", "animalis"): 12.50,
    ("Griffoir chat", "jardiland"): 11.99,
    ("Griffoir chat", "truffaut"): 12.99,
    ("Griffoir chat", "laferme"): 11.50,
    ("Griffoir chat", "medor"): 14.00,

    ("Jouet canne à pêche chat", "zoomalia"): 5.99,
    ("Jouet canne à pêche chat", "maxizoo"): 6.49,
    ("Jouet canne à pêche chat", "animalis"): 5.90,
    ("Jouet canne à pêche chat", "jardiland"): 5.69,
    ("Jouet canne à pêche chat", "truffaut"): 5.99,
    ("Jouet canne à pêche chat", "laferme"): 5.50,
    ("Jouet canne à pêche chat", "medor"): 6.99,

    ("Gamelle chat céramique", "zoomalia"): 7.99,
    ("Gamelle chat céramique", "maxizoo"): 8.49,
    ("Gamelle chat céramique", "animalis"): 7.90,
    ("Gamelle chat céramique", "jardiland"): 7.69,
    ("Gamelle chat céramique", "truffaut"): 7.99,
    ("Gamelle chat céramique", "laferme"): 7.50,
    ("Gamelle chat céramique", "medor"): 8.99,

    ("Fontaine à eau chat", "zoomalia"): 34.99,
    ("Fontaine à eau chat", "maxizoo"): 36.99,
    ("Fontaine à eau chat", "animalis"): 33.90,
    ("Fontaine à eau chat", "jardiland"): 32.99,
    ("Fontaine à eau chat", "truffaut"): 34.99,
    ("Fontaine à eau chat", "laferme"): 31.50,
    ("Fontaine à eau chat", "medor"): 37.99,

    ("Brosse chat", "zoomalia"): 6.99,
    ("Brosse chat", "maxizoo"): 7.49,
    ("Brosse chat", "animalis"): 6.90,
    ("Brosse chat", "jardiland"): 6.69,
    ("Brosse chat", "truffaut"): 6.99,
    ("Brosse chat", "laferme"): 6.50,
    ("Brosse chat", "medor"): 7.99,

    ("Transporteur chat", "zoomalia"): 29.99,
    ("Transporteur chat", "maxizoo"): 31.99,
    ("Transporteur chat", "animalis"): 28.50,
    ("Transporteur chat", "jardiland"): 27.99,
    ("Transporteur chat", "truffaut"): 29.99,
    ("Transporteur chat", "laferme"): 26.50,
    ("Transporteur chat", "medor"): 33.00,

    # AUTRES
    ("Cage rongeur 2 étages", "zoomalia"): 49.99,
    ("Cage rongeur 2 étages", "maxizoo"): 51.99,
    ("Cage rongeur 2 étages", "animalis"): 48.50,
    ("Cage rongeur 2 étages", "jardiland"): 47.99,
    ("Cage rongeur 2 étages", "truffaut"): 49.99,
    ("Cage rongeur 2 étages", "laferme"): 45.00,

    ("Mélange graines rongeurs", "zoomalia"): 5.99,
    ("Mélange graines rongeurs", "maxizoo"): 6.29,
    ("Mélange graines rongeurs", "animalis"): 5.80,
    ("Mélange graines rongeurs", "jardiland"): 5.69,
    ("Mélange graines rongeurs", "truffaut"): 5.99,
    ("Mélange graines rongeurs", "laferme"): 5.50,

    ("Foin rongeur", "zoomalia"): 4.99,
    ("Foin rongeur", "maxizoo"): 5.29,
    ("Foin rongeur", "animalis"): 4.90,
    ("Foin rongeur", "jardiland"): 4.69,
    ("Foin rongeur", "truffaut"): 4.99,
    ("Foin rongeur", "laferme"): 4.50,

    ("Croquettes lapin", "zoomalia"): 12.99,
    ("Croquettes lapin", "maxizoo"): 13.49,
    ("Croquettes lapin", "animalis"): 12.50,
    ("Croquettes lapin", "jardiland"): 12.29,
    ("Croquettes lapin", "truffaut"): 12.99,
    ("Croquettes lapin", "laferme"): 11.90,

    ("Nourriture poissons flocons", "zoomalia"): 4.99,
    ("Nourriture poissons flocons", "maxizoo"): 5.29,
    ("Nourriture poissons flocons", "animalis"): 4.90,
    ("Nourriture poissons flocons", "jardiland"): 4.79,
    ("Nourriture poissons flocons", "truffaut"): 4.99,
    ("Nourriture poissons flocons", "laferme"): 4.50,

    ("Aquarium 60L", "zoomalia"): 89.99,
    ("Aquarium 60L", "maxizoo"): 94.99,
    ("Aquarium 60L", "animalis"): 87.50,
    ("Aquarium 60L", "jardiland"): 84.99,
    ("Aquarium 60L", "truffaut"): 89.99,
    ("Aquarium 60L", "laferme"): 82.00,

    ("Mangeoire oiseaux", "zoomalia"): 8.99,
    ("Mangeoire oiseaux", "maxizoo"): 9.49,
    ("Mangeoire oiseaux", "animalis"): 8.50,
    ("Mangeoire oiseaux", "jardiland"): 8.29,
    ("Mangeoire oiseaux", "truffaut"): 8.99,
    ("Mangeoire oiseaux", "laferme"): 7.90,

    ("Mélange graines oiseaux", "zoomalia"): 4.99,
    ("Mélange graines oiseaux", "maxizoo"): 5.29,
    ("Mélange graines oiseaux", "animalis"): 4.90,
    ("Mélange graines oiseaux", "jardiland"): 4.79,
    ("Mélange graines oiseaux", "truffaut"): 4.99,
    ("Mélange graines oiseaux", "laferme"): 4.50,
}


# ── Normalisation ─────────────────────────────────────────────────────────
def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize(name: str) -> str:
    name = strip_accents(name.lower())
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


# ── Jaccard matching ──────────────────────────────────────────────────────
def jaccard_similarity(a: str, b: str) -> float:
    a_tokens = set(normalize(a).split())
    b_tokens = set(normalize(b).split())
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def find_best_match(scraped_name: str, catalog_names: list[str]) -> tuple[Optional[str], float]:
    """Trouve le meilleur produit du catalogue pour un nom scrapé."""
    best_name = None
    best_score = 0.0
    scraped_norm = normalize(scraped_name)
    for cat_name in catalog_names:
        cat_norm = normalize(cat_name)
        # Similarité Jaccard directe
        score = jaccard_similarity(scraped_norm, cat_norm)
        # Bonus si un mot-clé du catalogue est contenu dans le nom scrapé
        for token in cat_norm.split():
            if len(token) > 3 and token in scraped_norm:
                score += 0.1
        if score > best_score:
            best_score = score
            best_name = cat_name
    return best_name, best_score


# ── Fonction principale ───────────────────────────────────────────────────
def main():
    output_dir = os.path.join("public", "data")
    os.makedirs(output_dir, exist_ok=True)

    catalog_names = [p["name"] for p in PRODUCT_CATALOG]

    # Initialiser les résultats avec les fallbacks
    # Structure: nom_produit -> { site -> {price, url, shipping, in_stock} }
    product_prices: dict[str, dict] = {}
    for product in PRODUCT_CATALOG:
        product_prices[product["name"]] = {}

    for (prod_name, site), price in FALLBACK_PRICES.items():
        if prod_name not in product_prices:
            continue
        product_prices[prod_name][site] = {
            "price": round(price, 2),
            "shipping": 0,
            "url": "",
            "in_stock": True,
            "source": "fallback",
        }

    # Scraping (skip si --fallback-only)
    fallback_only = "--fallback-only" in sys.argv
    if fallback_only:
        print(f"🔧 Mode fallback-only — pas de scraping, prix de secours uniquement\n")
    else:
        print(f"Lancement du scraping sur {len(PRODUCT_CATALOG)} produits x {len(ALL_SCRAPERS)} sites\n")

    if not fallback_only:
        for scraper_name, scraper_class in ALL_SCRAPERS:
            print(f"\n{'='*60}")
            print(f"📡 {scraper_name.upper()}")
            print(f"{'='*60}")

            scraper = scraper_class()
            success_count = 0

            for product in PRODUCT_CATALOG:
                terms = product["search_terms"][0]
                print(f"   ↪ {product['name']} → recherche « {terms} » ... ", end="", flush=True)

                try:
                    results = scraper.search_product(terms)
                except Exception as e:
                    print(f"❌ {e}")
                    continue

                if not results:
                    print("⏭ pas trouvé")
                    continue

                best_match = None
                best_score = 0.0
                for result in results:
                    matched_name, score = find_best_match(result.product_name, catalog_names)
                    if matched_name == product["name"] and score > best_score:
                        best_score = score
                        best_match = result

                if best_match and best_score >= 0.25:
                    product_prices[product["name"]][scraper_name] = {
                        "price": round(best_match.price, 2),
                        "shipping": best_match.shipping,
                        "url": best_match.url,
                        "in_stock": best_match.in_stock,
                        "source": "scraped",
                    }
                    print(f"✅ {best_match.price:.2f}€")
                    success_count += 1
                else:
                    print("⏭ pas matché")

                time.sleep(0.5)

            scraper.close()
            print(f"📊 {scraper_name}: {success_count}/{len(PRODUCT_CATALOG)} produits trouvés")

    # Construction du JSON final
    print(f"\n{'='*60}")
    print("📦 Construction du JSON final")
    print(f"{'='*60}")

    products_json = []
    for product in PRODUCT_CATALOG:
        prices = product_prices[product["name"]]

        if not prices:
            continue

        # Filtrer les prix valides
        valid_prices = []
        for site_name, data in prices.items():
            if data.get("price", 0) > 0.1:
                valid_prices.append({
                    "shop": site_name,
                    "price": data["price"],
                    "shipping": data.get("shipping", 0),
                    "url": data.get("url", ""),
                    "in_stock": data.get("in_stock", True),
                    "source": data.get("source", "fallback"),
                })

        if not valid_prices:
            continue

        # Trier par prix croissant
        valid_prices.sort(key=lambda x: x["price"])

        best = valid_prices[0]
        animal_map = {"chien": "dog", "chat": "cat", "rongeurs": "other", "poissons": "other", "oiseaux": "other"}
        emoji_map = {"chien": "🐕", "chat": "🐈", "rongeurs": "🐹", "poissons": "🐟", "oiseaux": "🐦"}
        label_map = {"chien": "Chien", "chat": "Chat", "rongeurs": "Rongeurs", "poissons": "Poissons", "oiseaux": "Oiseaux"}
        cat = product["category"]
        products_json.append({
            "name": product["name"],
            "slug": product["url_name"],
            "category": cat,
            "animal": animal_map.get(cat, "other"),
            "emoji": emoji_map.get(cat, "📦"),
            "categoryLabel": label_map.get(cat, cat),
            "best_price": best["price"],
            "best_shop": best["shop"],
            "prices": valid_prices,
        })

    # Trier par catégorie puis nom
    category_order = {"chien": 0, "chat": 1, "rongeurs": 2, "poissons": 3, "oiseaux": 4}
    products_json.sort(key=lambda p: (category_order.get(p["category"], 9), p["name"]))

    output = {
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_products": len(products_json),
        "total_shops": len(ALL_SCRAPERS),
        "products": products_json,
    }

    output_path = os.path.join(output_dir, "products.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Fichier généré : {output_path}")
    print(f"   {len(products_json)} produits")
    total_prices = sum(len(p["prices"]) for p in products_json)
    scraped_count = sum(1 for p in products_json for pp in p["prices"] if pp.get("source") == "scraped")
    print(f"   {total_prices} prix dont {scraped_count} issus du scraping")
    print(f"   {(scraped_count/max(total_prices,1))*100:.0f}% de données scrapées en direct\n")


if __name__ == "__main__":
    main()
