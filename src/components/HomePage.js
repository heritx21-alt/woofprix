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

  /* Featured products */
  const products = await listProducts({ limit: 8 });
  if (products.length > 0) {
    const prodSection = document.createElement('div');
    prodSection.className = 'section';
    const prodTitle = document.createElement('h2');
    prodTitle.className = 'section-title';
    prodTitle.innerHTML = `Produits à la une <span class="count">${products.length} produits</span>`;
    prodSection.appendChild(prodTitle);

    const grid = document.createElement('div');
    grid.className = 'product-grid';
    products.forEach(p => grid.appendChild(renderProductCard(p, router)));
    prodSection.appendChild(grid);
    container.appendChild(prodSection);
  }

  container.appendChild(renderSavingsBanner(router));

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
