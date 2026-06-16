import { listProducts, invalidateCache } from '../js/api.js';
import {
  renderHeader, renderFooter, renderBreadcrumbs,
  renderSpinner, formatPrice, getShop, renderProductCard
} from './Layout.js';

export async function renderSearchPage(query, router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';

  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container search-page';

  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: `Recherche : "${query}"` }
  ]));

  /* Search header with inline search */
  const searchHeader = document.createElement('div');
  searchHeader.className = 'search-header';
  searchHeader.innerHTML = `
    <h1>Résultats pour "<span id="searchQuery">${query}</span>"</h1>
    <div class="search-inline">
      <input type="text" id="refineSearch" value="${query}" placeholder="Affiner la recherche..." autocomplete="off">
      <button class="savings-cta" style="padding:0.5rem 1.2rem;border-radius:999px;background:var(--accent);color:var(--white);font-weight:600;font-size:0.9rem;white-space:nowrap">Chercher</button>
    </div>
  `;

  const inlineInput = searchHeader.querySelector('#refineSearch');
  const inlineBtn = searchHeader.querySelector('.savings-cta');
  inlineBtn?.addEventListener('click', () => {
    if (inlineInput?.value.trim()) {
      router.navigate(`/search/${encodeURIComponent(inlineInput.value.trim())}`);
    }
  });
  inlineInput?.addEventListener('keydown', e => {
    if (e.key === 'Enter' && inlineInput.value.trim()) {
      router.navigate(`/search/${encodeURIComponent(inlineInput.value.trim())}`);
    }
  });

  container.appendChild(searchHeader);

  /* Results */
  const products = await listProducts({ search: query });

  if (!products || products.length === 0) {
    const noResults = document.createElement('div');
    noResults.className = 'empty-state fade-in';
    noResults.innerHTML = `
      <span class="big-icon">🔍</span>
      <p>Aucun résultat pour "${query}"</p>
      <div class="search-suggestions" style="margin-top:1.5rem;justify-content:center">
        <button data-nav="/category/croquettes-chien">🍖 Croquettes chien</button>
        <button data-nav="/category/croquettes-chat">🐟 Croquettes chat</button>
        <button data-nav="/category/litiere">⬜ Litière</button>
        <button data-nav="/category/patees">🥫 Pâtées</button>
        <button data-nav="/category/accessoires-chien">🎾 Accessoires</button>
        <button data-nav="/animal/all">🐾 Tous les produits</button>
      </div>
    `;
    noResults.querySelectorAll('[data-nav]').forEach(el => {
      el.addEventListener('click', e => {
        e.preventDefault();
        router.navigate(el.dataset.nav);
      });
    });
    container.appendChild(noResults);
  } else {
    const resultBar = document.createElement('div');
    resultBar.className = 'controls-bar';
    resultBar.innerHTML = `<span class="result-count">${products.length} produit${products.length > 1 ? 's' : ''} trouvé${products.length > 1 ? 's' : ''}</span>`;
    container.appendChild(resultBar);

    const grid = document.createElement('div');
    grid.className = 'product-grid';

    products.forEach(p => {
      grid.appendChild(renderProductCard(p, router));
    });

    container.appendChild(grid);
  }

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
