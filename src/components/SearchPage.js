import { listProducts, isDataAvailable } from '../js/api.js';
import { renderNav, renderFooter, renderSavingsBanner, renderNoDataMessage, formatPrice, getShop } from './Layout.js';

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
      </div>
      <button class="compare-btn" data-product="${p.slug}">Voir tous les prix →</button>
    </div>
  `;
}

export async function renderSearchPage(query, router) {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.appendChild(renderNav(router));

  const available = await isDataAvailable();

  if (!available) {
    app.appendChild(renderNoDataMessage());
    app.appendChild(renderFooter());
    return;
  }

  const results = await listProducts({ search: query });

  const page = document.createElement('div');
  page.className = 'search-results fade-in';

  const doSearch = () => {
    const inp = page.querySelector('#searchResultsInput');
    if (inp && inp.value.trim()) router.navigate(`/search/${encodeURIComponent(inp.value.trim())}`);
  };

  page.innerHTML = `
    <div class="breadcrumb">
      <a data-nav="/">Accueil</a>
      <span class="sep">/</span>
      <span class="current">Résultats pour « ${query} »</span>
    </div>

    <div class="results-bar">
      <h2>Résultats pour « ${query} » <span class="search-results-count">(${results.length} produit${results.length > 1 ? 's' : ''})</span></h2>
      <div class="search-wrap" style="margin:0 0 0 auto;flex:1;max-width:360px">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchResultsInput" placeholder="Affiner la recherche…" value="${query}" />
        <button class="search-btn" id="searchResultsBtn">Chercher</button>
      </div>
    </div>

    ${results.length === 0 ? `
      <div class="no-results">
        <span class="big-emoji">🔍</span>
        <p>Aucun produit trouvé pour « ${query} »</p>
        <p style="font-size:0.9rem;color:var(--muted)">Essayez : Frontline, Milbemax, Royal Canin, croquettes, vermifuge…</p>
        <div style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center">
          ${['Frontline', 'Milbemax', 'Royal Canin', 'Croquettes', 'Antiparasitaire'].map(t =>
            `<button class="tag" data-search="${t}">${t}</button>`
          ).join('')}
        </div>
      </div>
    ` : `
      <div class="products">
        ${results.map(p => productCard(p)).join('')}
      </div>
    `}
  `;

  page.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', (e) => { e.preventDefault(); router.navigate(el.dataset.nav); });
  });
  page.querySelectorAll('[data-product]').forEach(el => {
    el.addEventListener('click', () => router.navigate(`/product/${el.dataset.product}`));
  });
  page.querySelectorAll('[data-search]').forEach(el => {
    el.addEventListener('click', () => router.navigate(`/search/${encodeURIComponent(el.dataset.search)}`));
  });

  const searchBtn = page.querySelector('#searchResultsBtn');
  const searchInput = page.querySelector('#searchResultsInput');
  searchBtn?.addEventListener('click', doSearch);
  searchInput?.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSearch(); });

  app.appendChild(page);

  if (results.length > 0) {
    app.appendChild(renderSavingsBanner(router));
  }

  app.appendChild(renderFooter());
}
