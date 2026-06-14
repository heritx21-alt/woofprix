import { Router } from './js/router.js';
import { renderHomePage } from './components/HomePage.js';
import { renderProductPage } from './components/ProductPage.js';
import { renderSearchPage } from './components/SearchPage.js';
import { renderCategoryPage, renderAnimalPage } from './components/ListingPage.js';

const router = new Router([
  { path: '/', handler: () => renderHomePage(router) },
  { path: '/home', handler: () => renderHomePage(router) },
  { path: '/product/:slug', handler: (params) => renderProductPage(params.slug, router) },
  { path: '/search/:query', handler: (params) => renderSearchPage(params.query, router) },
  { path: '/category/:slug', handler: (params) => renderCategoryPage(params.slug, router) },
  { path: '/animal/:type', handler: (params) => renderAnimalPage(params.type, router) }
]);

document.addEventListener('DOMContentLoaded', () => {
  router.resolve();
});
