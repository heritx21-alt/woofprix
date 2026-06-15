import { getProduct, invalidateCache } from '../js/api.js';
import {
  renderHeader, renderFooter, renderBreadcrumbs,
  renderSpinner, formatPrice, getShop
} from './Layout.js';

export async function renderProductPage(slug, router) {
  invalidateCache();
  const app = document.getElementById('app');
  app.innerHTML = '';

  app.appendChild(renderHeader(router));

  const main = document.createElement('main');
  main.className = 'fade-in';
  const container = document.createElement('div');
  container.className = 'container product-detail';

  /* Load product */
  const p = await getProduct(slug);

  if (!p) {
    container.innerHTML = `
      <a class="detail-back" data-nav="/">← Retour à l'accueil</a>
      <div class="empty-state">
        <span class="big-icon">😕</span>
        <p>Produit introuvable</p>
      </div>
    `;
    container.querySelector('[data-nav]')?.addEventListener('click', e => {
      e.preventDefault(); router.navigate('/');
    });
    main.appendChild(container);
    app.appendChild(main);
    app.appendChild(renderFooter());
    return;
  }

  /* Breadcrumbs */
  container.appendChild(renderBreadcrumbs([
    { label: 'Accueil', nav: '/' },
    { label: p.categoryLabel || p.category || 'Produit', nav: `/category/${p.category}` },
    { label: p.name }
  ]));

  /* Header */
  const sortedPrices = [...(p.prices || [])].sort((a, b) => a.price - b.price);
  const best = sortedPrices[0]?.price || 0;
  const worst = sortedPrices[sortedPrices.length - 1]?.price || 0;
  const savings = sortedPrices.length > 1 ? Math.round((worst - best) / worst * 100) : 0;

  const header = document.createElement('div');
  header.className = 'detail-header';
  header.innerHTML = `
    <span class="detail-emoji">${p.emoji || '🐾'}</span>
    <div class="detail-info">
      <h1>${p.name}</h1>
      <div class="detail-tags">
        <span class="tag">${p.categoryLabel || p.category}</span>
        <span class="tag">${p.animal === 'dog' ? '🐕 Chien' : p.animal === 'cat' ? '🐈 Chat' : '🐾 Autre'}</span>
      </div>
      ${savings > 0 ? `<span class="detail-savings">📊 Économisez jusqu'à ${savings}%</span>` : ''}
    </div>
  `;
  container.appendChild(header);

  /* Price comparison */
  const pricesTitle = document.createElement('h2');
  pricesTitle.className = 'detail-prices-title';
  pricesTitle.innerHTML = `Comparer les prix <span class="count">${sortedPrices.length} offres</span>`;
  container.appendChild(pricesTitle);

  /* Shop filter */
  const filterBar = document.createElement('div');
  filterBar.className = 'shop-filters';
  let activeShops = new Set(sortedPrices.map(sp => sp.shop));

  sortedPrices.forEach(sp => {
    const shop = getShop(sp.shop);
    const btn = document.createElement('button');
    btn.className = 'shop-filter-btn active';
    btn.dataset.shop = sp.shop;
    btn.innerHTML = `
      <span class="dot" style="background:${shop?.color || '#999'}"></span>
      ${shop?.name || sp.shop}
    `;
    btn.addEventListener('click', () => {
      if (activeShops.has(sp.shop)) {
        if (activeShops.size <= 1) return; // keep at least one
        activeShops.delete(sp.shop);
        btn.classList.remove('active');
      } else {
        activeShops.add(sp.shop);
        btn.classList.add('active');
      }
      updateTable();
    });
    filterBar.appendChild(btn);
  });
  container.appendChild(filterBar);

  /* Comparison table */
  const tableWrap = document.createElement('div');
  tableWrap.className = 'compare-table';

  function updateTable() {
    const filtered = sortedPrices.filter(sp => activeShops.has(sp.shop));
    if (filtered.length === 0) {
      tableWrap.innerHTML = `<div class="empty-state" style="padding:2rem"><p>Aucune boutique sélectionnée</p></div>`;
      return;
    }
    const minPrice = Math.min(...filtered.map(sp => sp.price));

    tableWrap.innerHTML = filtered.map(sp => {
      const shop = getShop(sp.shop);
      const isBest = sp.price === minPrice;
      const diff = minPrice > 0 ? Math.round((sp.price - minPrice) / minPrice * 100) : 0;
      const shippingHtml = sp.shipping === 0 || !sp.shipping
        ? '<span class="free">Gratuite</span>'
        : formatPrice(sp.shipping);

      return `
        <div class="compare-row ${isBest ? 'best-row' : ''}">
          <div class="cp-shop">
            <span class="cp-dot" style="background:${shop?.color || '#999'}"></span>
            <span class="cp-name">${shop?.name || sp.shop}</span>
            ${isBest ? '<span class="cp-badge">Meilleur prix</span>' : ''}
          </div>
          <div class="cp-price">
            <span class="amount">${formatPrice(sp.price)}</span>
            ${diff > 0 ? `<span class="diff">+${diff}%</span>` : ''}
          </div>
          <div class="cp-shipping ${!sp.shipping ? 'free' : ''}">${shippingHtml}</div>
          <div class="cp-action">
            ${sp.in_stock !== false
              ? `<a href="${sp.url || shop?.url || '#'}" target="_blank" rel="noopener" class="btn-offer">Voir l'offre →</a>`
              : `<span class="stock-out">Rupture</span>`
            }
          </div>
        </div>
      `;
    }).join('');
  }

  updateTable();
  container.appendChild(tableWrap);

  /* Affiliation notice */
  const affil = document.createElement('div');
  affil.className = 'affil-notice';
  affil.textContent = 'Les prix et disponibilités sont donnés à titre indicatif. Les liens vers les boutiques peuvent être des liens d\'affiliation.';
  container.appendChild(affil);

  main.appendChild(container);

  /* Navigate handler for breadcrumbs */
  main.querySelectorAll('[data-nav]').forEach(el => {
    if (el.dataset.nav) {
      el.addEventListener('click', e => { e.preventDefault(); router.navigate(el.dataset.nav); });
    }
  });

  app.appendChild(main);
  app.appendChild(renderFooter());
}
