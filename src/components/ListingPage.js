import { listProducts, getStats, invalidateCache } from '../js/api.js';
import { categories } from '../data/categories.js';
import {
  renderHeader, renderFooter, renderStats,
  renderBreadcrumbs, renderSavingsBanner, renderNoDataMessage,
  renderSpinner, formatPrice, getShop
} from './Layout.js';

function renderProductList(products, router) {
  const grid = document.createElement('div');
  grid.className = 'product-grid';

  if (products.length === 0) {
    grid.innerHTML = `<div class="empty-state"><span class="big-icon">🔍</span><p>Aucun produit trouvé</p></div>`;
    return grid;
  }

  products.forEach(p => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.setAttribute('data-nav', `/product/${p.slug}`);

    const topShops = p.prices.slice(0, 3);
    const moreCount = p.prices.length - 3;
    const savingsHtml = p.savings > 0
      ? `<span class="card-savings">📊 -${p.savings}%</span>`
      : '';

    card.innerHTML = `
      <div class="card-header">
        <span class="card-emoji">${p.emoji || '🐾'}</span>
        <div>
          <div class="card-title">${p.name}</div>
          <div class="card-meta">
            <span>${p.categoryLabel || ''}</span>
            · <span>${p.animal === 'dog' ? '🐕 Chien' : p.animal === 'cat' ? '🐈 Chat' : '🐾 Autre'}</span>
          </div>
        </div>
      </div>
      <div class="card-best">${formatPrice(p.bestPrice)} <small>à partir de</small></div>
      <div class="card-shops">
        ${topShops.map(sp => {
          const shop = getShop(sp.shop);
          const isBest = sp.price === p.bestPrice;
          return `<div class="shop-row">
            <span class="shop-dot" style="background:${shop?.color || '#999'}"></span>
            <span class="shop-name">${shop?.name || sp.shop}</span>
            <span class="shop-price ${isBest ? 'best' : ''}">${formatPrice(sp.price)}</span>
          </div>`;
        }).join('')}
      </div>
      <div class="card-footer">
        ${savingsHtml}
        <span class="card-more">${moreCount > 0 ? `+${moreCount} autres →` : 'Voir les prix →'}</span>
      </div>
    `;
    card.addEventListener('click', () => router.navigate(`/product/${p.slug}`));
    grid.appendChild(card);
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
  const sortedData = [...data].sort((a, b) => a.bestPrice - b.bestPrice);

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
      if (sortOrder === 'asc') sortedData.sort((a, b) => a.bestPrice - b.bestPrice);
      else sortedData.sort((a, b) => b.bestPrice - a.bestPrice);
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
  const sortedData = [...data].sort((a, b) => a.bestPrice - b.bestPrice);

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
      if (sortOrder === 'asc') sortedData.sort((a, b) => a.bestPrice - b.bestPrice);
      else sortedData.sort((a, b) => b.bestPrice - a.bestPrice);
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
