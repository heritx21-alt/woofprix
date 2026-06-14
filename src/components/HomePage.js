import { categories } from '../data/categories.js';
import { listProducts, getStats, isDataAvailable, invalidateCache } from '../js/api.js';
import { renderNav, renderFooter, renderStats, renderNoDataMessage, renderSavingsBanner, formatPrice, getShop } from './Layout.js';

function productCard(p) {
  const topPrices = (p.prices || []).slice(0, 3);
  return `
    <div class="product-card fade-in" data-product="${p.slug}">
      <div class="product-top">
        <div class="product-img">${p.emoji || '📦'}</div>
        <div class="product-info">
          <div class="product-name">${p.name}</div>
          <div class="product-animal">${p.animal === 'dog' ? '🐕' : '🐈'} ${p.animalLabel || ''} • ${p.categoryLabel || ''}</div>
        </div>
        ${p.savings ? `<span class="product-badge">−${p.savings}%</span>` : ''}
      </div>
      <div class="price-list">
        ${topPrices.map(pr => {
          const shop = getShop(pr.shop);
          return `
            <div class="price-row">
              <span class="shop-name" style="color:${shop?.color || 'var(--muted)'}">${shop?.name || pr.shop}</span>
              <span class="price-amount ${pr.price === p.bestPrice ? 'best' : ''}">${formatPrice(pr.price)}</span>
            </div>
          `;
        }).join('')}
        ${p.prices && p.prices.length > 3 ? `<div class="price-row"><span class="shop-name" style="color:var(--muted)">+${p.prices.length - 3} autres prix</span></div>` : ''}
      </div>
      <button class="compare-btn" data-product="${p.slug}">Voir tous les prix →</button>
    </div>
  `;
}

export async function renderHomePage(router) {
  const app = document.getElementById('app');
  app.innerHTML = '';
  invalidateCache();

  app.appendChild(renderNav(router));

  const stats = await getStats();
  const available = await isDataAvailable();

  const hero = document.createElement('section');
  hero.className = 'hero';
  hero.innerHTML = `
    <div class="hero-badge">🐾 Comparateur N°1 produits animaux</div>
    <h1>Le meilleur prix pour<br><em>votre animal</em></h1>
    <p>Comparez vermifuges, antiparasitaires et croquettes sur les meilleures animaleries en ligne. Économisez jusqu'à 60% sur les mêmes produits.</p>
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="Ex : Frontline chat, Milbemax, Royal Canin…" autofocus />
      <button class="search-btn" id="searchBtn">Comparer</button>
    </div>
    <div class="search-tags">
      ${['Frontline chat', 'Milbemax chien', 'Royal Canin', 'Advocate chat', 'Croquettes chien'].map(t =>
        `<button class="tag" data-search="${t}">${t}</button>`
      ).join('')}
    </div>
  `;
  app.appendChild(hero);

  const doSearch = () => {
    const q = hero.querySelector('#searchInput');
    if (q && q.value.trim()) router.navigate(`/search/${encodeURIComponent(q.value.trim())}`);
  };
  hero.querySelector('#searchBtn')?.addEventListener('click', doSearch);
  hero.querySelector('#searchInput')?.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSearch(); });
  hero.querySelectorAll('[data-search]').forEach(el => {
    el.addEventListener('click', () => router.navigate(`/search/${encodeURIComponent(el.dataset.search)}`));
  });

  app.appendChild(await renderStats(stats));

  if (!available) {
    app.appendChild(renderNoDataMessage());
    app.appendChild(renderFooter());
    return;
  }

  const catSection = document.createElement('div');
  catSection.className = 'section';
  catSection.innerHTML = `
    <div class="section-header">
      <h2 class="section-title">Catégories populaires</h2>
      <a class="section-link" data-nav="/animal/all">Tout voir →</a>
    </div>
    <div class="categories">
      ${categories.map(c => `
        <a class="cat-card" data-nav="/category/${c.slug}">
          <span class="cat-emoji">${c.emoji}</span>
          <div class="cat-name">${c.name}</div>
          <div class="cat-count">${c.count} produits</div>
        </a>
      `).join('')}
    </div>
  `;
  catSection.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', (e) => { e.preventDefault(); router.navigate(el.dataset.nav); });
  });
  app.appendChild(catSection);

  const prodSection = document.createElement('div');
  prodSection.className = 'section';
  prodSection.innerHTML = `
    <div class="section-header">
      <h2 class="section-title">Produits les plus recherchés</h2>
      <a class="section-link" data-nav="/animal/all">Tout voir →</a>
    </div>
    <div class="products" id="featuredProducts">
      <div class="loading"><div class="spinner"></div></div>
    </div>
  `;
  app.appendChild(prodSection);

  listProducts({ limit: 6 }).then(products => {
    const container = prodSection.querySelector('#featuredProducts');
    if (!container) return;
    if (products.length === 0) {
      container.innerHTML = `
        <div class="no-results">
          <p style="font-size:1rem">Aucun produit disponible pour le moment.</p>
        </div>
      `;
      return;
    }
    container.innerHTML = products.map(p => productCard(p)).join('');
    container.querySelectorAll('[data-product]').forEach(el => {
      el.addEventListener('click', () => router.navigate(`/product/${el.dataset.product}`));
    });
  });

  app.appendChild(renderSavingsBanner(router));
  app.appendChild(renderFooter());
}
