# WoofPrix 🐾

Comparateur de prix pour produits animaliers français. Scraping automatique chaque nuit des plus grandes animaleries en ligne.

**Stack :** Frontend statique Vite (HTML/CSS/JS pur) + scrapers Python (BeautifulSoup/httpx) en GitHub Actions.

## Installation et lancement en local

### Prérequis

- Node.js 18+
- Python 3.12+

### Frontend

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement (http://localhost:5173)
npm run dev

# Build production (génère dist/)
npm run build

# Prévisualiser le build
npm run preview
```

### Scrapers

```bash
# Installer les dépendances Python
pip install -r scripts/requirements.txt

# Lancer le scraping manuellement (génère public/data/products.json)
python scripts/scrape_all.py
```

Le JSON généré est automatiquement copié dans `dist/` par Vite au build. En dev, il est servi directement depuis `public/data/products.json`.

### Fallback

Si aucun JSON n'existe encore (premier déploiement), le frontend affiche "Prix en cours de chargement, revenez demain" au lieu de planter — les scrapers tourneront la nuit suivante dans GitHub Actions.

## Déploiement sur Vercel

### 1. Créer un compte Vercel

Rendez-vous sur [vercel.com](https://vercel.com) et connectez-vous avec GitHub.

### 2. Créer le repo GitHub

```bash
# Depuis le dossier du projet
git init
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/woofprix.git
git branch -M main
git push -u origin main
```

### 3. Importer le projet Vercel

1. Cliquez sur **"Add New..." > "Project"** dans Vercel
2. Choisissez le repo `woofprix`
3. **Ne changez rien** — le `vercel.json` est déjà configuré :

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

4. Cliquez sur **"Deploy"**

Le site est en ligne en ~30 secondes. Chaque `git push` déclenche un redéploiement automatique.

### 4. Lier le scraping automatique

Après le push initial, activez GitHub Actions dans votre repo :

1. Allez dans **Settings > Actions > General**
2. Assurez-vous que `Allow all actions and reusable workflows` est coché
3. Le workflow `.github/workflows/scrape.yml` s'exécutera chaque nuit à 3h UTC

Le workflow :
- Installe Python 3.12 + pip
- Lance `python scripts/scrape_all.py` (scrape 9 sites, génère `products.json`)
- Commit et push le nouveau JSON si des prix ont changé
- Le push sur `main` déclenche le redéploiement Vercel automatiquement

## Configuration des secrets GitHub

Le workflow GitHub Actions a besoin de permissions pour push. Deux options :

### Option A : `GITHUB_TOKEN` (automatique)

Le fichier `.github/workflows/scrape.yml` déclare `permissions: contents: write`, ce qui donne automatiquement au `GITHUB_TOKEN` le droit de push. **Aucune configuration supplémentaire n'est nécessaire.**

### Option B : Vercel Deploy Hook (optionnel)

Si vous voulez déclencher le redéploiement Vercel **immédiatement** après le scraping (au lieu d'attendre le prochain cycle) :

1. Allez dans **Vercel > Dashboard > Settings > Git > Deploy Hooks**
2. Créez un hook, donnez-lui un nom (ex: "post-scrape")
3. Copiez l'URL générée
4. Dans GitHub, allez dans **Settings > Secrets and Variables > Actions**
5. Ajoutez un **New repository secret** :
   - **Name :** `VERCEL_DEPLOY_HOOK`
   - **Secret :** l'URL du hook

Si ce secret n'est pas configuré, le redéploiement se fait quand même via le push GitHub (Vercel écoute les pushes sur `main` par défaut).

## Tester les scrapers en local

```bash
# Test rapide — scrapage de tous les produits sur tous les sites
cd scripts
pip install -r requirements.txt
python scrape_all.py

# Résultat attendu dans la console :
#   🔍 [milbemax-chien] Milbemax Chien
#     → maxizoo… ✓ 15.99€
#     → zoomalia… ✓ 12.50€
#     → animalis… ∅
#     …
#   ✅ Scraping terminé :
#      13 produits
#      XX prix
#      XX sites avec données
#      → public/data/products.json
```

### Tester un scraper spécifique

```bash
python -c "
from scrapers.maxizoo import MaxiZooScraper
s = MaxiZooScraper()
results = s.search_product('Frontline Combo Chat')
for r in results:
    print(f'{r.product_name}: {r.price:.2f}€ (stock: {r.in_stock})')
s.close()
"
```

### Ajouter un nouveau scraper

1. Créez `scripts/scrapers/votresite.py` qui hérite de `BaseScraper`
2. Implémentez `search_product(product_name)` → retourne `list[ScraperResult]`
3. Ajoutez le scraper dans la liste de `scrape_all.py`
4. Ajoutez le shop dans `SHOPS`, `SHOP_URL_PATTERNS` et éventuellement `FALLBACK_PRICES`

Structure du catalogue de produits (13 produits de référence dans `PRODUCT_CATALOG`) :

```python
PRODUCT_CATALOG = [
    {"id": "milbemax-chien", "name": "Milbemax Chien", "slug": "milbemax-chien",
     "animal": "dog", "animal_label": "Chien", "category": "vermifuges",
     "category_label": "Vermifuge", "emoji": "💊",
     "search_terms": ["Milbemax", "Milbemax chien"]},
    # ... 12 autres produits
]
```

### Matching flou

Le scoring utilise un ratio de mots correspondants entre le résultat scrappé et les `search_terms` :

```python
def score_match(result_name, search_terms):
    # +10 si un terme complet est dans le nom
    # +0..5 selon le ratio de mots correspondants
```

Un score ≥ 5 est considéré comme une correspondance valide.

## Ajouter les liens d'affiliation

### Awin (Zooplus, Pepette)

```python
# Une fois votre compte Awin validé :
# 1. Récupérez votre ID programme Awin
# 2. Remplacez l'URL dans le scraper ou dans scrape_all.py :
AFFILIATE_AWIN_ID = "VOTRE_ID"

def build_affiliate_url(base_url):
    return f"https://www.awin1.com/cread.php?awinmid={AFFILIATE_AWIN_ID}&p={base_url}"
```

### Netaffiliation (Wanimo)

```python
# Une fois votre compte Netaffiliation validé :
AFFILIATE_NETAF_ID = "VOTRE_ID"

def build_netaffiliation_url(base_url):
    return f"https://www.netaffiliation.com/link?id={AFFILIATE_NETAF_ID}&url={base_url}"
```

### Amazon Partenaires

```python
# Une fois votre compte Amazon Partenaires validé :
AFFILIATE_AMAZON_TAG = "votre-tag-21"

def build_amazon_url(product_url):
    sep = "&" if "?" in product_url else "?"
    return f"{product_url}{sep}tag={AFFILIATE_AMAZON_TAG}"
```

### Où insérer les URLs affiliées

Dans `scripts/scrape_all.py`, la fonction `build_url()` construit les URLs des produits. C'est là qu'il faut ajouter la logique d'affiliation :

```python
# Dans build_url(), après avoir construit l'URL de base :
if shop_id == "zooplus" and AFFILIATE_AWIN_ID:
    return f"https://www.awin1.com/cread.php?awinmid={AFFILIATE_AWIN_ID}&p={url}"
```

Le frontend affiche déjà les badges "Affiliation" dans `src/data/shops.js` pour les shops marqués `affiliate: true` — aucun changement frontend nécessaire.

## Architecture du projet

```
woofprix/
├── .github/workflows/
│   └── scrape.yml              # Scraping automatique chaque nuit
├── public/
│   └── data/
│       └── products.json        # Données générées par les scrapers
├── scripts/
│   ├── requirements.txt         # Dépendances Python
│   ├── scrape_all.py            # Orchestrateur principal
│   └── scrapers/
│       ├── base.py              # Classe BaseScraper (httpx + BS4)
│       ├── maxizoo.py           # Scrapers individuels (9 sites)
│       ├── zoomalia.py
│       └── ...
├── src/
│   ├── main.js                  # Point d'entrée + routes
│   ├── js/
│   │   ├── api.js               # Client API (fetch products.json)
│   │   └── router.js            # Routeur SPA hash-based
│   ├── components/
│   │   ├── HomePage.js          # Page d'accueil
│   │   ├── SearchPage.js        # Résultats de recherche
│   │   ├── ProductPage.js       # Tableau comparatif
│   │   ├── ListingPage.js       # Listing par catégorie/animal
│   │   └── Layout.js            # Nav, footer, helpers UI
│   ├── data/
│   │   ├── shops.js             # 19 shops (couleurs, logos, affiliation)
│   │   └── categories.js        # Catégories avec compteurs statiques
│   └── styles/
│       └── main.css             # Design responsive complet
├── index.html                   # HTML racine
├── vercel.json                  # Config déploiement Vercel
├── vite.config.js               # Config Vite
└── package.json
```

## Sites supportés

| Site | URL | Affiliation |
|---|---|---|
| Zooplus | zooplus.fr | Awin |
| Wanimo | wanimo.com | Netaffiliation |
| Amazon | amazon.fr | Amazon Partenaires |
| Pepette | pepette.fr | Awin |
| MaxiZoo | maxizoo.fr | Direct |
| Zoomalia | zoomalia.com | Direct |
| Animalis | animalis.com | Direct |
| Jardiland | jardiland.com | Direct |
| Truffaut | truffaut.com | Direct |
| La Ferme des Animaux | lafermedesanimaux.com | Direct |
| Médor & Compagnie | medor-et-compagnie.fr | Direct |
| Produits-Véto | produits-veto.com | Direct |
| France-Véto | france-veto.com | Direct |
| Santévet | santevet.com | Direct |
| Direct-Vet | direct-vet.fr | Direct |
| Cernunos | cernunos.fr | Direct |
| Ultra Premium Direct | ultrapremiumdirect.com | Direct |
| Petsonic | petsonic.com | Direct |
| Univers-Véto | univers-veto.fr | Direct |

## Workflow complet (data → déploiement)

```
GitHub Actions (3h UTC)
    ↓
python scrape_all.py
    ↓
public/data/products.json  ← généré
    ↓
Commit + push sur main
    ↓
Vercel détecte le push
    ↓
npm run build (Vite copie public/ dans dist/)
    ↓
Site mis à jour en ligne 🚀
```

Sans intervention manuelle : chaque matin, les prix sont à jour.

## Génération du sitemap SEO

Pour générer un `sitemap.xml` à partir des données scrappées :

```bash
python -c "
import json
with open('public/data/products.json') as f:
    data = json.load(f)

base = 'https://woofprix.vercel.app'
urls = [f'<url><loc>{base}/</loc></url>']
for p in data['products']:
    urls.append(f'<url><loc>{base}/#/product/{p[\"slug\"]}</loc></url>')

sitemap = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
sitemap += '<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">'
sitemap += ''.join(urls) + '</urlset>'

with open('public/sitemap.xml', 'w') as f:
    f.write(sitemap)
print('✓ sitemap.xml généré')
"
```

## Licence

MIT
