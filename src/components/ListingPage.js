import { listProducts, getStats, invalidateCache } from '../js/api.js';
import { categories } from '../data/categories.js';
import {
  renderHeader, renderFooter, renderStats,
  renderBreadcrumbs, renderSavingsBanner, renderNoDataMessage,
  renderSpinner, formatPrice, getShop, renderProductCard
} from './Layout.js';

function renderProductList(products, router) {
  const grid = document.createElement('div');
  grid.className = 'product-grid';

  if (products.length === 0) {
    grid.innerHTML = `<div class="empty-state"><span class="big-icon">🔍</span><p>Aucun produit trouvé</p></div>`;
    return grid;
  }

  products.forEach(p => {
    grid.appendChild(renderProductCard(p, router));
  });

  return grid;
}

export async function renderCategoryPage(slug, router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';

  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container';
  container.style.paddingTop = '1.25rem';

  const cat = categories.find(c => c.slug === slug);
  const title = cat?.name || slug.replace(/-/g, ' ');
  const emoji = cat?.emoji || '🐾';

  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: title }
  ]));

  const data = await listProducts({ category: slug });
  if (!data || data.length === 0) {
    main.appendChild(container);
    const shops = (await import('../data/shops.js')).shops;
    container.appendChild(renderNoDataMessage(shops));
    app.appendChild(main);
    app.appendChild(renderFooter());
    return;
  }

  const h1 = document.createElement('h1');
  h1.className = 'section-title';
  h1.innerHTML = `${emoji} ${title} <span class="count">${data.length} produits</span>`;
  container.appendChild(h1);

  /* Sort controls */
  let sortOrder = 'asc';
  function sortByPrice(arr, order) {
    return arr.sort((a, b) => {
      if (a.bestPrice == null) return 1;
      if (b.bestPrice == null) return -1;
      return order === 'asc' ? a.bestPrice - b.bestPrice : b.bestPrice - a.bestPrice;
    });
  }
  const sortedData = sortByPrice([...data], 'asc');

  function renderWithSort() {
    const existingControls = container.querySelector('.controls-bar');
    if (existingControls) existingControls.remove();
    const existingGrid = container.querySelector('.product-grid');
    if (existingGrid) existingGrid.remove();

    const controls = document.createElement('div');
    controls.className = 'controls-bar';
    controls.innerHTML = `
      <span class="result-count">${sortedData.length} produits</span>
      <div class="sort-group">
        <label>Trier par</label>
        <select id="sortSelect">
          <option value="asc" ${sortOrder === 'asc' ? 'selected' : ''}>Prix croissant</option>
          <option value="desc" ${sortOrder === 'desc' ? 'selected' : ''}>Prix décroissant</option>
        </select>
      </div>
    `;
    controls.querySelector('#sortSelect')?.addEventListener('change', e => {
      sortOrder = e.target.value;
      sortByPrice(sortedData, sortOrder);
      const oldGrid = container.querySelector('.product-grid');
      if (oldGrid) oldGrid.remove();
      container.appendChild(renderProductList(sortedData, router));
    });

    container.insertBefore(controls, container.querySelector('.product-grid') || container.querySelector('.section'));
    container.appendChild(renderProductList(sortedData, router));
  }

  renderWithSort();

  const stats = await getStats();
  if (stats) container.appendChild(await renderStats(stats));
  container.appendChild(renderSavingsBanner(router));

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}

export async function renderAnimalPage(type, router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';

  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container';
  container.style.paddingTop = '1.25rem';

  const animalMap = { dog: '🐕 Chiens', cat: '🐈 Chats', all: '🐾 Tous les animaux' };
  const title = animalMap[type] || '🐾 Animaux';

  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: title }
  ]));

  const data = await listProducts({ animal: type });
  if (!data || data.length === 0) {
    main.appendChild(container);
    const shops = (await import('../data/shops.js')).shops;
    container.appendChild(renderNoDataMessage(shops));
    app.appendChild(main);
    app.appendChild(renderFooter());
    return;
  }

  const h1 = document.createElement('h1');
  h1.className = 'section-title';
  h1.innerHTML = `${title} <span class="count">${data.length} produits</span>`;
  container.appendChild(h1);

  let sortOrder = 'asc';
  const sortedData = sortByPrice([...data], 'asc');

  function renderWithSort() {
    const existingControls = container.querySelector('.controls-bar');
    if (existingControls) existingControls.remove();
    const existingGrid = container.querySelector('.product-grid');
    if (existingGrid) existingGrid.remove();

    const controls = document.createElement('div');
    controls.className = 'controls-bar';
    controls.innerHTML = `
      <span class="result-count">${sortedData.length} produits</span>
      <div class="sort-group">
        <label>Trier par</label>
        <select id="sortSelectAnimal">
          <option value="asc" ${sortOrder === 'asc' ? 'selected' : ''}>Prix croissant</option>
          <option value="desc" ${sortOrder === 'desc' ? 'selected' : ''}>Prix décroissant</option>
        </select>
      </div>
    `;
    controls.querySelector('#sortSelectAnimal')?.addEventListener('change', e => {
      sortOrder = e.target.value;
      sortByPrice(sortedData, sortOrder);
      const oldGrid = container.querySelector('.product-grid');
      if (oldGrid) oldGrid.remove();
      container.appendChild(renderProductList(sortedData, router));
    });

    container.insertBefore(controls, container.querySelector('.product-grid') || container.querySelector('.section'));
    container.appendChild(renderProductList(sortedData, router));
  }

  renderWithSort();

  const stats = await getStats();
  if (stats) container.appendChild(await renderStats(stats));
  container.appendChild(renderSavingsBanner(router));

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
