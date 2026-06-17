import { listProducts, invalidateCache } from '../js/api.js';
import { categories, subcategories, getCategory, getSubcategory, animals, getAnimal } from '../data/categories.js';
import { shops } from '../data/shops.js';
import {
  renderHeader, renderFooter,
  renderBreadcrumbs, renderSpinner,
  formatPrice, getShop, renderProductCard
} from './Layout.js';

function renderFilterSidebar(products, activeFilters, onChange, pageType, pageId) {
  const sidebar = document.createElement('aside');
  sidebar.className = 'filter-sidebar';

  function subcatCount(sub) {
    return products.filter(p => p.subcategory === sub.id).length;
  }

  function catCount(cat) {
    return products.filter(p => p.category === cat.id).length;
  }

  function renderSubcatGroup(catId, label) {
    const subs = (subcategories[catId] || []).filter(s => subcatCount(s) > 0);
    if (subs.length === 0) return null;
    const box = document.createElement('div');
    box.className = 'filter-group';
    box.innerHTML = `<h4>${label}</h4>`;
    subs.forEach(s => {
      const cnt = subcatCount(s);
      const item = document.createElement('a');
      item.className = 'filter-link' + (activeFilters.subcategory === s.id ? ' active' : '');
      item.href = '#';
      item.innerHTML = `${s.label} <span class="count">${cnt}</span>`;
      item.addEventListener('click', e => {
        e.preventDefault();
        activeFilters.subcategory = activeFilters.subcategory === s.id ? null : s.id;
        onChange();
      });
      box.appendChild(item);
    });
    return box;
  }

  // 1. Type de produit (subcategories grouped by category)
  if (pageType === 'animal' || pageType === 'all') {
    for (const cat of categories) {
      const box = renderSubcatGroup(cat.id, cat.label);
      if (box) sidebar.appendChild(box);
    }
  } else if (pageType === 'category') {
    const box = renderSubcatGroup(pageId, 'Sous-catégories');
    if (box) sidebar.appendChild(box);
  }

  // 2. Price range
  const priceBox = document.createElement('div');
  priceBox.className = 'filter-group';
  priceBox.innerHTML = '<h4>Prix</h4>';
  const prices = products.map(p => p.bestPrice).filter(p => p != null);
  const minP = prices.length ? Math.floor(Math.min(...prices)) : 0;
  const maxP = prices.length ? Math.ceil(Math.max(...prices)) : 200;
  const row = document.createElement('div');
  row.className = 'price-range-inputs';
  const minIn = document.createElement('input');
  minIn.type = 'number'; minIn.placeholder = String(minP); minIn.min = minP; minIn.max = maxP;
  minIn.value = activeFilters.priceMin || '';
  minIn.addEventListener('change', () => { activeFilters.priceMin = minIn.value ? Number(minIn.value) : null; onChange(); });
  const maxIn = document.createElement('input');
  maxIn.type = 'number'; maxIn.placeholder = String(maxP); maxIn.min = minP; maxIn.max = maxP;
  maxIn.value = activeFilters.priceMax || '';
  maxIn.addEventListener('change', () => { activeFilters.priceMax = maxIn.value ? Number(maxIn.value) : null; onChange(); });
  row.appendChild(minIn);
  row.append(' — ');
  row.appendChild(maxIn);
  priceBox.appendChild(row);
  sidebar.appendChild(priceBox);

  // 3. Shop
  const shopBox = document.createElement('div');
  shopBox.className = 'filter-group';
  shopBox.innerHTML = '<h4>Boutique</h4>';
  const shopIds = [...new Set(products.flatMap(p => (p.prices || []).map(pr => pr.shop)))].sort();
  shopIds.forEach(sid => {
    const shop = getShop(sid);
    const label = document.createElement('label');
    label.className = 'filter-check';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = activeFilters.shops?.includes(sid);
    cb.addEventListener('change', () => {
      const current = activeFilters.shops || [];
      activeFilters.shops = cb.checked ? [...current, sid] : current.filter(x => x !== sid);
      onChange();
    });
    label.appendChild(cb);
    label.append(' ' + (shop?.name || sid));
    shopBox.appendChild(label);
  });
  sidebar.appendChild(shopBox);

  // 4. Brand
  const brandBox = document.createElement('div');
  brandBox.className = 'filter-group';
  brandBox.innerHTML = '<h4>Marque</h4>';
  const brands = [...new Set(products.map(p => p.brand).filter(Boolean))].sort();
  brands.forEach(b => {
    const label = document.createElement('label');
    label.className = 'filter-check';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = activeFilters.brands?.includes(b);
    cb.addEventListener('change', () => {
      const current = activeFilters.brands || [];
      activeFilters.brands = cb.checked ? [...current, b] : current.filter(x => x !== b);
      onChange();
    });
    label.appendChild(cb);
    label.append(' ' + b);
    brandBox.appendChild(label);
  });
  sidebar.appendChild(brandBox);

  // Reset
  const hasFilters = activeFilters.subcategory || activeFilters.brands?.length || activeFilters.shops?.length || activeFilters.priceMin != null || activeFilters.priceMax != null;
  if (hasFilters) {
    const resetBtn = document.createElement('button');
    resetBtn.className = 'filter-reset';
    resetBtn.textContent = 'Réinitialiser';
    resetBtn.addEventListener('click', () => {
      activeFilters.subcategory = null;
      activeFilters.brands = [];
      activeFilters.shops = [];
      activeFilters.priceMin = null;
      activeFilters.priceMax = null;
      onChange();
    });
    sidebar.appendChild(resetBtn);
  }

  return sidebar;
}

function renderActiveFilterChips(activeFilters, onChange) {
  const chips = document.createElement('div');
  chips.className = 'active-filters';
  const all = [];
  if (activeFilters.subcategory) {
    const sub = getSubcategory(activeFilters.subcategory);
    all.push({ label: sub?.label || activeFilters.subcategory, remove: () => { activeFilters.subcategory = null; onChange(); } });
  }
  if (activeFilters.brands) for (const b of activeFilters.brands) all.push({ label: b, remove: () => { activeFilters.brands = activeFilters.brands.filter(x => x !== b); onChange(); } });
  if (activeFilters.shops) for (const s of activeFilters.shops) {
    const shop = getShop(s);
    all.push({ label: shop?.name || s, remove: () => { activeFilters.shops = activeFilters.shops.filter(x => x !== s); onChange(); } });
  }
  if (activeFilters.priceMin != null) all.push({ label: formatPrice(activeFilters.priceMin) + '+', remove: () => { activeFilters.priceMin = null; onChange(); } });
  if (activeFilters.priceMax != null) all.push({ label: '–' + formatPrice(activeFilters.priceMax), remove: () => { activeFilters.priceMax = null; onChange(); } });
  all.forEach(f => {
    const chip = document.createElement('span');
    chip.className = 'filter-chip';
    chip.innerHTML = `${f.label} <span class="chip-remove">&times;</span>`;
    chip.querySelector('.chip-remove').addEventListener('click', f.remove);
    chips.appendChild(chip);
  });
  return chips;
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

function applyFilters(products, filters) {
  let r = products;
  if (filters.subcategory) r = r.filter(p => p.subcategory === filters.subcategory);
  if (filters.brands?.length) r = r.filter(p => p.brand && filters.brands.includes(p.brand));
  if (filters.shops?.length) r = r.filter(p => (p.prices || []).some(pr => filters.shops.includes(pr.shop)));
  if (filters.priceMin != null) r = r.filter(p => p.bestPrice != null && p.bestPrice >= filters.priceMin);
  if (filters.priceMax != null) r = r.filter(p => p.bestPrice != null && p.bestPrice <= filters.priceMax);
  return r;
}

async function renderListing(title, breadcrumbs, products, router, pageType, pageId) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container';
  container.style.paddingTop = '1.25rem';

  container.appendChild(renderBreadcrumbs(breadcrumbs));

  const h1 = document.createElement('h1');
  h1.className = 'section-title';
  h1.textContent = title;
  container.appendChild(h1);

  if (!products) {
    container.appendChild(renderSpinner());
    main.appendChild(container);
    app.appendChild(main);
    app.appendChild(renderFooter());
    return;
  }

  const activeFilters = { subcategory: null, brands: [], shops: [], priceMin: null, priceMax: null };

  function renderAll() {
    while (container.children.length > 3) container.removeChild(container.lastChild);

    const filtered = applyFilters(products, activeFilters);

    const layout = document.createElement('div');
    layout.className = 'listing-layout';

    const sidebar = renderFilterSidebar(products, activeFilters, renderAll, pageType, pageId);
    layout.appendChild(sidebar);

    const content = document.createElement('div');
    content.className = 'listing-content';

    const chips = renderActiveFilterChips(activeFilters, renderAll);
    if (chips.children.length) content.appendChild(chips);

    const countEl = document.createElement('div');
    countEl.className = 'result-count';
    countEl.textContent = `${filtered.length} produits`;
    content.appendChild(countEl);

    const sorted = [...filtered].sort((a, b) => (a.bestPrice || 999) - (b.bestPrice || 999));
    content.appendChild(renderProductGrid(sorted, router));
    layout.appendChild(content);
    container.appendChild(layout);
  }

  renderAll();
  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}

export async function renderCategoryPage(catSlug, router) {
  const cat = getCategory(catSlug);
  const title = cat?.label || catSlug;
  const products = await listProducts({ category: catSlug });
  await renderListing(title, [{ label: 'Accueil', nav: '/' }, { label: title }], products, router, 'category', catSlug);
}

export async function renderAnimalPage(type, router) {
  const animal = getAnimal(type);
  const title = animal ? `${animal.emoji} ${animal.label}` : 'Tous les animaux';
  const products = await listProducts({ animal: type });
  await renderListing(title, [{ label: 'Accueil', nav: '/' }, { label: title }], products, router, 'animal', type);
}

export async function renderAllPage(router) {
  const products = await listProducts({});
  await renderListing('Tous les produits', [{ label: 'Accueil', nav: '/' }, { label: 'Tous les produits' }], products, router, 'all', null);
}
