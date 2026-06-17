import { getProduct, invalidateCache } from '../js/api.js';
import {
  renderHeader, renderFooter, renderBreadcrumbs,
  renderSpinner, formatPrice, getShop
} from './Layout.js';
import { getAffiliateUrl } from '../data/shops.js';

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
  const imgHtml = p.image
    ? `<img class="detail-img" src="${p.image}" alt="${p.name}">`
    : `<span class="detail-emoji">${p.emoji || '🐾'}</span>`;
  header.innerHTML = `
    ${imgHtml}
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

  /* Description */
  if (p.description) {
    const desc = document.createElement('div');
    desc.className = 'detail-desc';
    desc.textContent = p.description;
    container.appendChild(desc);
  }

  /* Price history */
  const historySection = document.createElement('div');
  historySection.className = 'price-history';
  historySection.innerHTML = `<h3>📈 Historique des prix</h3>`;
  const historyContainer = document.createElement('div');
  historyContainer.id = 'historyChart';
  historyContainer.innerHTML = '<div class="history-empty">Chargement...</div>';
  historySection.appendChild(historyContainer);
  container.appendChild(historySection);

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
        if (activeShops.size <= 1) return;
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
              ? `<a href="${getAffiliateUrl(sp.shop, sp.url || shop?.url || '#')}" target="_blank" rel="noopener" class="btn-offer">Voir l'offre →</a>`
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

  /* Load price history asynchronously */
  loadPriceHistory(slug, historyContainer);
}

async function loadPriceHistory(slug, container) {
  try {
    const res = await fetch('/data/price_history.json');
    if (!res.ok) throw new Error('not found');
    const data = await res.json();

    // Find all entries for this product
    const entries = Object.values(data).filter(e => e.product_slug === slug || e.product === slug);
    if (entries.length === 0) { container.innerHTML = '<div class="history-empty">Pas encore d\'historique</div>'; return; }

    // Collect all price points across shops
    const points = [];
    entries.forEach(e => {
      (e.history || []).forEach(h => {
        points.push({ date: h.date, price: h.price, shop: e.shop });
      });
    });

    if (points.length < 2) { container.innerHTML = '<div class="history-empty">Pas assez de données pour un graphique</div>'; return; }

    // Sort by date
    points.sort((a, b) => a.date.localeCompare(b.date));

    // Group by date: average price per day
    const byDate = {};
    points.forEach(p => {
      if (!byDate[p.date]) byDate[p.date] = [];
      byDate[p.date].push(p.price);
    });
    const dates = Object.keys(byDate).sort();
    const avgPrices = dates.map(d => {
      const vals = byDate[d];
      return vals.reduce((s, v) => s + v, 0) / vals.length;
    });

    renderMiniChart(container, dates, avgPrices);
  } catch (e) {
    container.innerHTML = '<div class="history-empty">Historique non disponible</div>';
  }
}

function renderMiniChart(container, labels, values) {
  if (values.length < 2) { container.innerHTML = '<div class="history-empty">Pas assez de données</div>'; return; }

  const w = 600, h = 120, pad = 20;
  const min = Math.min(...values) * 0.95;
  const max = Math.max(...values) * 1.05;
  const range = max - min || 1;

  const xScale = (w - pad * 2) / (values.length - 1 || 1);
  const yScale = (val) => h - pad - ((val - min) / range) * (h - pad * 2);

  let pathD = values.map((v, i) => `${i === 0 ? 'M' : 'L'}${pad + i * xScale},${yScale(v)}`).join(' ');
  let areaD = `${pathD} L${pad + (values.length - 1) * xScale},${h - pad} L${pad},${h - pad} Z`;

  // Date labels (show first, middle, last)
  const labelPositions = [0];
  if (values.length > 2) labelPositions.push(Math.floor(values.length / 2));
  if (values.length > 1) labelPositions.push(values.length - 1);

  container.innerHTML = `
    <svg viewBox="0 0 ${w} ${h}" class="history-chart">
      <defs>
        <linearGradient id="h-gradient" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="var(--accent, #FF6B35)"/>
          <stop offset="100%" stop-color="var(--accent, #FF6B35)" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <path class="h-area" d="${areaD}"/>
      <path class="h-line" d="${pathD}"/>
      ${values.map((v, i) => i === 0 || i === values.length - 1 ? `<circle class="h-dot" cx="${pad + i * xScale}" cy="${yScale(v)}" r="3"/>` : '').join('')}
      ${labelPositions.map(i => `<text class="h-label" x="${pad + i * xScale}" y="${h - 4}">${labels[i]}</text>`).join('')}
      <text class="h-label" x="4" y="${pad + 10}" text-anchor="start">${formatPriceLabel(max)}</text>
      <text class="h-label" x="4" y="${h - pad - 6}" text-anchor="start">${formatPriceLabel(min)}</text>
    </svg>
  `;
}

function formatPriceLabel(val) {
  return val.toFixed(2).replace('.', ',') + '€';
}
