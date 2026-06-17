import { Router } from './js/router.js';
import { renderHomePage } from './components/HomePage.js';
import { renderProductPage } from './components/ProductPage.js';
import { renderSearchPage } from './components/SearchPage.js';
import { renderCategoryPage, renderAnimalPage, renderAllPage } from './components/ListingPage.js';
import { renderHeader, renderFooter } from './components/Layout.js';

function renderPlaceholder(router, title, emoji) {
  const main = document.getElementById('app');
  main.innerHTML = '';
  main.appendChild(renderHeader(router));
  const div = document.createElement('div');
  div.className = 'container';
  div.innerHTML = `<div class="no-data fade-in" style="padding:4rem 1.25rem;text-align:center">
    <span style="font-size:4rem;display:block;margin-bottom:0.75rem">${emoji}</span>
    <h2 style="margin-bottom:0.5rem">${title}</h2>
    <p style="color:var(--ink-lighter);font-size:0.9rem">Fonctionnalité à venir.</p>
  </div>`;
  main.appendChild(div);
  main.appendChild(renderFooter());
}

const router = new Router([
  { path: '/', handler: () => renderHomePage(router) },
  { path: '/home', handler: () => renderHomePage(router) },
  { path: '/product/:slug', handler: (params) => renderProductPage(params.slug, router) },
  { path: '/search/:query', handler: (params) => renderSearchPage(params.query, router) },
  { path: '/category/:slug', handler: (params) => renderCategoryPage(params.slug, router) },
  { path: '/animal/:type', handler: (params) => renderAnimalPage(params.type, router) },
  { path: '/all', handler: () => renderAllPage(router) },
  { path: '/favorites', handler: () => renderPlaceholder(router, 'Ma sélection', '❤️') },
  { path: '/alerts', handler: () => renderPlaceholder(router, 'Alertes prix', '🔔') }
]);

document.addEventListener('DOMContentLoaded', () => {
  router.resolve();
});
