import { listProducts, getStats, invalidateCache } from '../js/api.js';
import { categories, subcategories, getCategory, getSubcategory, animals, getAnimal } from '../data/categories.js';
import {
  renderHeader, renderFooter, renderStats,
  renderBreadcrumbs, renderSavingsBanner, renderNoDataMessage,
  renderSpinner, formatPrice, getShop, renderProductCard
} from './Layout.js';

function renderSubcategoryTabs(activeSub, onSelect, subs) {
  const bar = document.createElement('div');
  bar.className = 'subcat-bar';
  const allBtn = document.createElement('button');
  allBtn.className = 'subcat-tab' + (!activeSub ? ' active' : '');
  allBtn.textContent = 'Tout';
  allBtn.addEventListener('click', () => onSelect(null));
  bar.appendChild(allBtn);

  subs.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'subcat-tab' + (activeSub === s.id ? ' active' : '');
    btn.textContent = s.label;
    btn.addEventListener('click', () => onSelect(s.id));
    bar.appendChild(btn);
  });
  return bar;
}

function renderAnimalTabs(activeAnimal, onSelect) {
  const bar = document.createElement('div');
  bar.className = 'subcat-bar';
  const allBtn = document.createElement('button');
  allBtn.className = 'subcat-tab' + (!activeAnimal ? ' active' : '');
  allBtn.textContent = 'Tous';
  allBtn.addEventListener('click', () => onSelect(null));
  bar.appendChild(allBtn);

  animals.forEach(a => {
    const btn = document.createElement('button');
    btn.className = 'subcat-tab' + (activeAnimal === a.id ? ' active' : '');
    btn.textContent = a.emoji + ' ' + a.label;
    btn.addEventListener('click', () => onSelect(a.id));
    bar.appendChild(btn);
  });
  return bar;
}

function renderProductGrid(products, router) {
  const grid = document.createElement('div');
  grid.className = 'product-grid';
  if (products.length === 0) {
    grid.innerHTML = `<div class="empty-state"><span class="big-icon">🔍</span><p>Aucun produit trouvé</p></div>`;
    return grid;
  }
  products.forEach(p => grid.appendChild(renderProductCard(p, router)));
  return grid;
}

export async function renderCategoryPage(catSlug, router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container';
  container.style.paddingTop = '1.25rem';

  const cat = getCategory(catSlug);
  const subs = subcategories[catSlug] || [];
  const title = cat?.label || catSlug;

  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: title }
  ]));

  const h1 = document.createElement('h1');
  h1.className = 'section-title';
  h1.innerHTML = `${cat?.emoji || '📦'} ${title}`;
  container.appendChild(h1);

  let activeSub = null;
  let products = await listProducts({ category: catSlug });
  let filtered = products;

  function updateDisplay() {
    const existingBar = container.querySelector('.subcat-bar');
    if (existingBar) existingBar.remove();
    const existingControls = container.querySelector('.controls-bar');
    if (existingControls) existingControls.remove();
    const existingGrid = container.querySelector('.product-grid');
    if (existingGrid) existingGrid.remove();

    filtered = activeSub ? products.filter(p => p.subcategory === activeSub) : products;

    const bar = renderSubcategoryTabs(activeSub, (subId) => {
      activeSub = subId;
      updateDisplay();
    }, subs);
    container.insertBefore(bar, container.querySelector('.section') || null);

    const countEl = document.createElement('div');
    countEl.className = 'result-count';
    countEl.textContent = `${filtered.length} produits`;
    container.appendChild(countEl);

    const sorted = [...filtered].sort((a, b) => (a.bestPrice || 999) - (b.bestPrice || 999));
    container.appendChild(renderProductGrid(sorted, router));
  }

  updateDisplay();

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

  const animal = getAnimal(type);
  const title = animal ? `${animal.emoji} ${animal.label}` : 'Tous les animaux';

  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: title }
  ]));

  const h1 = document.createElement('h1');
  h1.className = 'section-title';
  h1.innerHTML = `${title}`;
  container.appendChild(h1);

  let products = await listProducts({ animal: type });
  let activeCat = null;
  let filtered = products;

  function updateDisplay() {
    const existingBar = container.querySelector('.subcat-bar');
    if (existingBar) existingBar.remove();
    const existingControls = container.querySelector('.controls-bar');
    if (existingControls) existingControls.remove();
    const existingGrid = container.querySelector('.product-grid');
    if (existingGrid) existingGrid.remove();

    filtered = activeCat ? products.filter(p => p.category === activeCat) : products;

    const bar = document.createElement('div');
    bar.className = 'subcat-bar';
    const allBtn = document.createElement('button');
    allBtn.className = 'subcat-tab' + (!activeCat ? ' active' : '');
    allBtn.textContent = 'Tout';
    allBtn.addEventListener('click', () => { activeCat = null; updateDisplay(); });
    bar.appendChild(allBtn);

    categories.forEach(c => {
      const btn = document.createElement('button');
      btn.className = 'subcat-tab' + (activeCat === c.id ? ' active' : '');
      btn.textContent = c.emoji + ' ' + c.label;
      btn.addEventListener('click', () => { activeCat = c.id; updateDisplay(); });
      bar.appendChild(btn);
    });
    container.insertBefore(bar, container.querySelector('.section') || null);

    const countEl = document.createElement('div');
    countEl.className = 'result-count';
    countEl.textContent = `${filtered.length} produits`;
    container.appendChild(countEl);

    const sorted = [...filtered].sort((a, b) => (a.bestPrice || 999) - (b.bestPrice || 999));
    container.appendChild(renderProductGrid(sorted, router));
  }

  updateDisplay();

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
