import { listProducts, getStats, invalidateCache } from '../js/api.js';
import { categories } from '../data/categories.js';
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

  /* Hero search */
  const hero = document.createElement('div');
  hero.className = 'search-hero';
  hero.innerHTML = `
    <h1>Comparez les prix pour <span>votre animal</span></h1>
    <p>Aliments, litières, accessoires — trouvez le meilleur prix parmi 10 boutiques</p>
    <div class="hero-search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="heroSearch" placeholder="Ex: croquettes Royal Canin, litière Catsan..." autocomplete="off">
    </div>
    <div class="search-suggestions">
      <button data-nav="/category/croquettes-chien">🍖 Croquettes chien</button>
      <button data-nav="/category/croquettes-chat">🐟 Croquettes chat</button>
      <button data-nav="/category/litiere">⬜ Litière</button>
      <button data-nav="/category/patees">🥫 Pâtées chat</button>
      <button data-nav="/category/accessoires-chien">🎾 Accessoires</button>
    </div>
  `;

  hero.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', e => {
      e.preventDefault();
      router.navigate(el.dataset.nav);
    });
  });

  const heroInput = hero.querySelector('#heroSearch');
  heroInput?.addEventListener('keydown', e => {
    if (e.key === 'Enter' && heroInput.value.trim()) {
      router.navigate(`/search/${encodeURIComponent(heroInput.value.trim())}`);
    }
  });

  main.appendChild(hero);

  /* Data loading */
  const [stats, products] = await Promise.all([getStats(), listProducts({ limit: 6 })]);

  if (!products || products.length === 0) {
    const shops = (await import('../data/shops.js')).shops;
    main.appendChild(renderNoDataMessage(shops));
    app.appendChild(main);
    app.appendChild(renderFooter());
    return;
  }

  const container = document.createElement('div');
  container.className = 'container';

  /* Stats */
  const statsEl = await renderStats(stats);
  container.appendChild(statsEl);

  /* Categories */
  const catSection = document.createElement('div');
  catSection.className = 'section';
  catSection.innerHTML = `<h2 class="section-title">Catégories populaires</h2>`;
  const catGrid = document.createElement('div');
  catGrid.className = 'cat-grid';
  categories.forEach(c => {
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.setAttribute('data-nav', `/category/${c.slug}`);
    card.innerHTML = `
      <span class="cat-emoji">${c.emoji}</span>
      <div class="cat-info">
        <div class="cat-name">${c.name}</div>
        <div class="cat-count">${c.count} produits</div>
      </div>
    `;
    card.addEventListener('click', () => router.navigate(`/category/${c.slug}`));
    catGrid.appendChild(card);
  });
  catSection.appendChild(catGrid);
  container.appendChild(catSection);

  /* Featured products */
  const prodSection = document.createElement('div');
  prodSection.className = 'section';
  prodSection.innerHTML = `<h2 class="section-title">Produits à la une <span class="count">${products.length} produits</span></h2>`;

  const grid = document.createElement('div');
  grid.className = 'product-grid';

  products.forEach(p => {
    const card = renderProductCard(p, router);
    grid.appendChild(card);
  });

  prodSection.appendChild(grid);
  container.appendChild(prodSection);

  /* Savings banner */
  container.appendChild(renderSavingsBanner(router));

  main.appendChild(container);
  app.appendChild(main);
  app.appendChild(renderFooter());
}
