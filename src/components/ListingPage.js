import { categories } from '../data/categories.js';
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

async function commonRender(title, emoji, router, fetcher) {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.appendChild(renderNav(router));

  const available = await isDataAvailable();

  if (!available) {
    app.appendChild(renderNoDataMessage());
    app.appendChild(renderFooter());
    return;
  }

  const products = await fetcher();
  const page = buildPage(title, emoji, products, router);
  app.appendChild(page);
  if (products.length > 0) app.appendChild(renderSavingsBanner(router));
  app.appendChild(renderFooter());
}

export function renderCategoryPage(categorySlug, router) {
  const cat = categories.find(c => c.slug === categorySlug);
  const title = cat?.name || 'Catégorie';
  const emoji = cat?.emoji || '📂';
  return commonRender(title, emoji, router, () => listProducts({ category: categorySlug }));
}

export function renderAnimalPage(animal, router) {
  const labels = { dog: ['Chiens', '🐕'], cat: ['Chats', '🐈'] };
  const [title, emoji] = animal === 'all' ? ['Tous les produits', '🐾'] : labels[animal] || ['Animaux', '🐾'];
  const fetcher = animal === 'all'
    ? () => listProducts({ limit: 200 })
    : () => listProducts({ animal });
  return commonRender(title, emoji, router, fetcher);
}

function buildPage(title, emoji, items, router) {
  const page = document.createElement('div');
  page.className = 'search-results fade-in';
  page.innerHTML = `
    <div class="breadcrumb">
      <a data-nav="/">Accueil</a>
      <span class="sep">/</span>
      <span class="current">${emoji} ${title}</span>
    </div>

    <h2>${emoji} ${title} <span class="search-results-count">(${items.length} produit${items.length > 1 ? 's' : ''})</span></h2>

    <div class="products" style="margin-top:1.5rem">
      ${items.length === 0
        ? '<div class="no-results"><span class="big-emoji">📭</span><p>Aucun produit dans cette rubrique pour le moment.</p></div>'
        : items.map(p => productCard(p)).join('')
      }
    </div>
  `;

  page.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', (e) => { e.preventDefault(); router.navigate(el.dataset.nav); });
  });
  page.querySelectorAll('[data-product]').forEach(el => {
    el.addEventListener('click', () => router.navigate(`/product/${el.dataset.product}`));
  });

  return page;
}
