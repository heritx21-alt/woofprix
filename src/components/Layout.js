import { shops } from '../data/shops.js';
import { categories } from '../data/categories.js';

export function renderHeader(router, opts = {}) {
  const header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML = `
    <div class="header-inner">
      <a class="logo" data-nav="/">Woof<span>Prix</span></a>
      <div class="header-search">
        <span class="search-icon">🔍</span>
        <input type="text" id="headerSearchInput" placeholder="Rechercher un produit..." autocomplete="off">
      </div>
      <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
      <ul class="nav-links" id="navLinks">
        <li><a data-nav="/favorites">❤️ Ma sélection</a></li>
        <li><a data-nav="/alerts">🔔 Alerte prix</a></li>
      </ul>
    </div>
    <div class="cat-bar show" id="catBar">
      <div class="cat-bar-inner">
        ${categories.map(c => `
          <a class="cat-pill" data-nav="/category/${c.slug}">${c.emoji} ${c.name}</a>
        `).join('')}
      </div>
    </div>
  `;

  header.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      document.getElementById('navLinks')?.classList.remove('open');
      router.navigate(el.dataset.nav);
    });
  });

  header.querySelector('#menuBtn')?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  const searchInput = header.querySelector('#headerSearchInput');
  searchInput?.addEventListener('keydown', e => {
    if (e.key === 'Enter' && searchInput.value.trim()) {
      router.navigate(`/search/${encodeURIComponent(searchInput.value.trim())}`);
      searchInput.value = '';
    }
  });

  return header;
}

export function renderCatBar() {
  const bar = document.createElement('div');
  bar.className = 'cat-bar show';
  bar.innerHTML = `
    <div class="cat-bar-inner">
      ${categories.map(c => `
        <a class="cat-pill" data-nav="/category/${c.slug}">${c.emoji} ${c.name}</a>
      `).join('')}
    </div>
  `;
  return bar;
}

export function renderFooter() {
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  const shopChunks = shops.map(s =>
    `<span style="color:${s.color}">${s.name}</span>`
  ).join(' · ');

  footer.innerHTML = `
    <div class="footer-inner">
      <div class="footer-main">
        <div class="footer-col">
          <h4>🐾 WoofPrix</h4>
          <a href="#">Comparateur de prix pour animaux</a>
          <span>Gratuit & indépendant</span>
        </div>
        <div class="footer-col">
          <h4>Liens</h4>
          <a data-nav="/favorites">❤️ Ma sélection</a>
          <a data-nav="/alerts">🔔 Alerte prix</a>
          <a data-nav="/">🐾 Tous les produits</a>
        </div>
        <div class="footer-col">
          <h4>Informations</h4>
          <a href="#">Mentions légales</a>
          <a href="#">Politique de confidentialité</a>
        </div>
      </div>
      <div class="footer-shops">Prix comparés sur : ${shopChunks}</div>
      <div class="footer-copy">
        © ${new Date().getFullYear()} WoofPrix — Comparateur de prix animaliers
      </div>
    </div>
  `;

  footer.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      window.dispatchEvent(new CustomEvent('navigate', { detail: el.dataset.nav }));
    });
  });

  return footer;
}

export function renderNoDataMessage(shopsList) {
  const div = document.createElement('div');
  div.className = 'no-data fade-in';
  const list = shopsList || shops;
  div.innerHTML = `
    <span class="big-icon">⏳</span>
    <h2>Prix en cours de chargement</h2>
    <p>Les données seront disponibles après la première exécution du scraping automatique, prévue cette nuit.</p>
    <div class="shop-tags">
      ${list.slice(0, 12).map(s =>
        `<span class="tag" style="background:${s.color}18;color:${s.color}">${s.name}</span>`
      ).join('')}
    </div>
  `;
  return div;
}

export async function renderStats(stats) {
  const div = document.createElement('div');
  div.className = 'stats fade-in';
  const s = stats || { products_count: 0, shops_count: 0 };
  div.innerHTML = `
    <div class="stat">
      <div class="stat-num"><span>${s.products_count || 0}</span></div>
      <div class="stat-label">Produits comparés</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>${s.shops_count || shops.length}</span></div>
      <div class="stat-label">Sites partenaires</div>
    </div>
    <div class="stat">
      <div class="stat-num">jusqu'à <span>60%</span></div>
      <div class="stat-label">D'économies</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>100%</span></div>
      <div class="stat-label">Gratuit</div>
    </div>
  `;
  return div;
}

export function renderSavingsBanner(router) {
  const div = document.createElement('div');
  div.className = 'savings-banner fade-in';
  div.innerHTML = `
    <div>
      <h2>Les Français dépensent <span>1 000€/an</span> pour leur animal.</h2>
      <p>La moitié pourrait être économisée en comparant les prix. WoofPrix le fait pour vous, gratuitement.</p>
    </div>
    <button class="savings-cta">Économiser</button>
  `;
  div.querySelector('.savings-cta')?.addEventListener('click', () => {
    router.navigate('/');
  });
  return div;
}

export function renderSpinner() {
  const div = document.createElement('div');
  div.className = 'spinner-wrap';
  div.innerHTML = '<div class="spinner"></div>';
  return div;
}

export function renderBreadcrumbs(items) {
  const div = document.createElement('nav');
  div.className = 'breadcrumbs';
  div.innerHTML = items.map((item, i) => {
    if (i === items.length - 1) return `<span>${item.label}</span>`;
    if (item.nav) return `<a data-nav="${item.nav}">${item.label}</a> <span class="sep">›</span>`;
    return `<span>${item.label}</span> <span class="sep">›</span>`;
  }).join('');

  div.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      window.dispatchEvent(new CustomEvent('navigate', { detail: el.dataset.nav }));
    });
  });

  return div;
}

export function formatPrice(price) {
  if (price == null || isNaN(price)) return '—';
  return Number(price).toFixed(2).replace('.', ',') + ' €';
}

export function getShop(id) {
  return shops.find(s => s.id === id);
}

/** Render a single product card (shared across all list views) */
export function renderProductCard(p, router) {
  const card = document.createElement('div');
  card.className = 'product-card';
  card.setAttribute('data-nav', `/product/${p.slug}`);

  const hasPrices = p.prices && p.prices.length > 0;
  const topShops = hasPrices ? p.prices.slice(0, 3) : [];
  const moreCount = hasPrices ? p.prices.length - 3 : 0;
  const savingsHtml = p.savings > 0
    ? `<span class="card-savings">📊 -${p.savings}%</span>`
    : '';
  const imgHtml = p.image
    ? `<img class="card-image" src="${p.image}" alt="${p.name}" loading="lazy">`
    : `<span class="card-emoji">${p.emoji || '🐾'}</span>`;

  card.innerHTML = `
    <div class="card-header">
      ${imgHtml}
      <div>
        <div class="card-title">${p.name}</div>
        <div class="card-meta">
          <span>${p.categoryLabel || ''}</span>
          · <span>${p.animal === 'dog' ? '🐕 Chien' : p.animal === 'cat' ? '🐈 Chat' : '🐾 Autre'}</span>
        </div>
      </div>
    </div>
    <div class="card-best">${hasPrices ? formatPrice(p.bestPrice) + ' <small>à partir de</small>' : '<span style="font-size:0.85rem;font-weight:400;color:var(--ink-lighter)">Prix inconnus</span>'}</div>
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
      ${!hasPrices ? '<div class="shop-row" style="color:var(--ink-lighter);font-size:0.78rem;justify-content:center;padding:0.5rem">⏳ Prix non disponibles — scraping en cours</div>' : ''}
    </div>
    <div class="card-footer">
      ${savingsHtml}
      <span class="card-more">${moreCount > 0 ? `+${moreCount} autres prix →` : 'Voir tous les prix →'}</span>
    </div>
  `;
  card.addEventListener('click', () => router.navigate(`/product/${p.slug}`));
  return card;
}
