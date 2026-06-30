import { listProducts, getStats, getFilterOptions, invalidateCache } from '../js/api.js';
import { animals, categories, subcategories } from '../data/categories.js';
import {
  renderHeader, renderFooter, renderStats,
  renderSavingsBanner, renderNoDataMessage, renderSpinner,
  renderBreadcrumbs, formatPrice, getShop,
  renderProductCard
} from './Layout.js';

export async function renderHomePage(router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';

  const header = renderHeader(router);
  app.appendChild(header);

  const main = document.createElement('main');
  main.className = 'fade-in';

  const container = document.createElement('div');
  container.className = 'container';
  container.style.paddingTop = '1.25rem';

  /* Hero section: Anti-parasitaires en avant */
  const hero = document.createElement('div');
  hero.className = 'hero-section fade-in';
  hero.innerHTML = `
    <div class="hero-badge">💊 SOINS & SANTÉ</div>
    <h1 class="hero-title">Anti-parasitaires<br><span class="hero-highlight">Comparez les prix</span></h1>
    <p class="hero-desc">Frontline, Advantage, Seresto, Scalibor… Trouvez le meilleur prix pour protéger votre animal.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" data-nav="/category/health">Voir tous les soins →</a>
      <a class="hero-btn secondary" data-nav="/search/anti-puces">🔍 Chercher un produit</a>
    </div>
  `;
  hero.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', e => { e.preventDefault(); router.navigate(el.dataset.nav); });
  });
  container.appendChild(hero);

  /* Stats */
  const stats = await getStats();
  if (stats) {
    const statsEl = await renderStats(stats);
    container.appendChild(statsEl);
  }

  /* Browse by Animal */
  const animalSection = document.createElement('div');
  animalSection.className = 'section';
  const animalTitle = document.createElement('h2');
  animalTitle.className = 'section-title';
  animalTitle.textContent = 'Choisissez votre animal';
  animalSection.appendChild(animalTitle);

  const animalGrid = document.createElement('div');
  animalGrid.className = 'cat-grid';
  animals.forEach(a => {
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.setAttribute('data-nav', `/animal/${a.id}`);
    card.innerHTML = `
      <span class="cat-emoji">${a.emoji}</span>
      <div class="cat-info">
        <div class="cat-name">${a.label}</div>
      </div>
    `;
    card.addEventListener('click', () => router.navigate(`/animal/${a.id}`));
    animalGrid.appendChild(card);
  });
  animalSection.appendChild(animalGrid);
  container.appendChild(animalSection);

  /* Featured: Anti-parasitaires en vedette */
  const allProducts = await listProducts({ limit: 200 });
  const antiPara = allProducts.filter(p =>
    p.subcategory === 'anti-parasitaires' && p.prices && p.prices.length > 0
  );
  if (antiPara.length > 0) {
    const featSection = document.createElement('div');
    featSection.className = 'section';
    const featTitle = document.createElement('h2');
    featTitle.className = 'section-title';
    featTitle.innerHTML = `💊 Anti-parasitaires <span class="count">${antiPara.length} produits</span>`;
    featSection.appendChild(featTitle);

    const subTags = document.createElement('div');
    subTags.className = 'sub-tags';
    const types = [...new Set(antiPara.map(p => p.productType).filter(Boolean))];
    const typeLabels = { 'spot-on': '💧 Spot-on', 'collier': '📿 Colliers', 'spray': '🧴 Sprays' };
    types.forEach(t => {
      const tag = document.createElement('a');
      tag.className = 'sub-tag';
      tag.setAttribute('data-nav', `/search/${t === 'spot-on' ? 'pipettes' : t === 'collier' ? 'collier anti-puces' : 'spray anti-puces'}`);
      tag.textContent = typeLabels[t] || t;
      tag.addEventListener('click', e => { e.preventDefault(); router.navigate(tag.dataset.nav); });
      subTags.appendChild(tag);
    });
    featSection.appendChild(subTags);

    const grid = document.createElement('div');
    grid.className = 'product-grid';
    const sorted = [...antiPara].sort((a, b) => (a.bestPrice || 999) - (b.bestPrice || 999));
    sorted.slice(0, 12).forEach(p => grid.appendChild(renderProductCard(p, router)));
    featSection.appendChild(grid);

    const more = document.createElement('div');
    more.className = 'center-link';
    more.innerHTML = '<a data-nav="/category/health">Tous les anti-parasitaires →</a>';
    more.querySelector('a').addEventListener('click', e => { e.preventDefault(); router.navigate('/category/health'); });
    featSection.appendChild(more);

    container.appendChild(featSection);
  }

  /* Categories overview */
  const catSection = document.createElement('div');
  catSection.className = 'section';
  const catTitle = document.createElement('h2');
  catTitle.className = 'section-title';
  catTitle.textContent = 'Toutes les catégories';
  catSection.appendChild(catTitle);

  const catGrid = document.createElement('div');
  catGrid.className = 'cat-grid';

  categories.forEach(c => {
    const subList = subcategories[c.id] || [];
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.innerHTML = `
      <span class="cat-emoji">${c.emoji}</span>
      <div class="cat-info">
        <div class="cat-name">${c.label}</div>
        <div class="cat-count">${subList.length} sous-catégories</div>
      </div>
    `;
    card.addEventListener('click', () => router.navigate(`/category/${c.id}`));
    catGrid.appendChild(card);
  });
  catSection.appendChild(catGrid);
  container.appendChild(catSection);

  /* Products with multiple shops */
  const multiShop = allProducts.filter(p => p.prices && p.prices.length >= 2);
  if (multiShop.length > 0) {
    const compSection = document.createElement('div');
    compSection.className = 'section';
    const compTitle = document.createElement('h2');
    compTitle.className = 'section-title';
    compTitle.innerHTML = `🏆 Top comparés <span class="count">${multiShop.length} produits</span>`;
    compSection.appendChild(compTitle);

    const grid = document.createElement('div');
    grid.className = 'product-grid';
    const sortedComp = [...multiShop].sort((a, b) => (a.bestPrice || 999) - (b.bestPrice || 999));
    sortedComp.slice(0, 8).forEach(p => grid.appendChild(renderProductCard(p, router)));
    compSection.appendChild(grid);
    container.appendChild(compSection);
  }

  container.appendChild(renderSavingsBanner(router));

  /* All products link */
  const allLink = document.createElement('div');
  allLink.className = 'center-link';
  allLink.innerHTML = '<a data-nav="/all">Voir tous les produits →</a>';
  allLink.querySelector('a').addEventListener('click', e => {
    e.preventDefault();
    router.navigate('/all');
  });
  container.appendChild(allLink);

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
