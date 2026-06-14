import { getProduct, isDataAvailable } from '../js/api.js';
import { renderNav, renderFooter, renderNoDataMessage, formatPrice, getShop } from './Layout.js';

export async function renderProductPage(slug, router) {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.appendChild(renderNav(router));

  const available = await isDataAvailable();

  if (!available) {
    app.appendChild(renderNoDataMessage());
    app.appendChild(renderFooter());
    return;
  }

  const product = await getProduct(slug);

  if (!product) {
    app.innerHTML += `
      <div class="section" style="text-align:center;padding:4rem 2rem">
        <span style="font-size:3rem;display:block;margin-bottom:1rem">😕</span>
        <h2 style="font-family:var(--font-title);margin-bottom:0.5rem">Produit introuvable</h2>
        <p style="color:var(--muted);margin-bottom:1.5rem">Ce produit n'existe pas ou a été retiré.</p>
        <button class="search-btn" onclick="location.hash='/'">Retour à l'accueil</button>
      </div>
    `;
    app.appendChild(renderFooter());
    return;
  }

  const sortedPrices = [...product.prices].sort((a, b) => a.price - b.price);
  const bestPrice = sortedPrices[0];
  const animals = { dog: '🐕 Chien', cat: '🐈 Chat' };

  const savings = sortedPrices.length > 1
    ? Math.round((sortedPrices[sortedPrices.length - 1].price - bestPrice.price) / sortedPrices[sortedPrices.length - 1].price * 100)
    : 0;

  const detail = document.createElement('div');
  detail.className = 'product-detail fade-in';
  detail.innerHTML = `
    <a class="back-link" data-nav="/">← Retour aux produits</a>

    <div class="detail-header">
      <div class="detail-img">${product.emoji || '📦'}</div>
      <div class="detail-info">
        <h1>${product.name}</h1>
        <div class="detail-meta">
          <span class="detail-meta-tag">${animals[product.animal] || product.animalLabel || product.animal}</span>
          <span class="detail-meta-tag">${product.categoryLabel || product.category || ''}</span>
          ${savings > 0 ? `<span class="detail-meta-tag" style="background:var(--green-light);color:var(--green);font-weight:600">Jusqu'à −${savings}%</span>` : ''}
        </div>
        <p class="detail-desc">${product.description || ''}</p>
      </div>
    </div>

    <h2 class="compare-section-title">Comparer les prix</h2>

    <div class="compare-table">
      <div class="compare-table-header">
        <span>Boutique</span>
        <span>Prix</span>
        <span>Livraison</span>
        <span>Action</span>
      </div>
      ${sortedPrices.map((pr, i) => {
        const shop = getShop(pr.shop);
        if (!shop) return '';
        const isBest = i === 0;
        const diff = isBest ? 0 : Math.round((pr.price - bestPrice.price) / bestPrice.price * 100);
        return `
          <div class="compare-row ${isBest ? 'best-row' : ''}">
            <div class="compare-shop">
              <div class="compare-shop-logo" style="background:${shop.color}">${shop.logo}</div>
              <span>${shop.name}</span>
              ${isBest ? '<span class="compare-badge">Meilleur prix</span>' : ''}
            </div>
            <div>
              <div class="compare-price ${isBest ? 'best' : ''}">${formatPrice(pr.price)}</div>
              ${diff > 0 ? `<div style="font-size:0.72rem;color:var(--red)">+${diff}%</div>` : ''}
            </div>
            <div class="compare-shipping ${(pr.shipping || 0) === 0 ? 'free' : ''}">
              ${(pr.shipping || 0) === 0 ? 'Gratuite' : formatPrice(pr.shipping)}
            </div>
            <div class="compare-actions">
              <a href="${pr.url || shop.url}" target="_blank" rel="noopener" class="compare-link">Voir l'offre</a>
              <span class="compare-stock ${pr.in_stock ? 'in-stock' : 'out-of-stock'}">
                ${pr.in_stock ? '✓ En stock' : '✗ Rupture'}
              </span>
            </div>
          </div>
        `;
      }).join('')}
    </div>

    <div class="affiliation-notice">
      <strong>💡 Affiliations :</strong> Les prix affichés incluent les éventuels frais de port. WoofPrix perçoit une commission sur les achats effectués via les liens partenaires, sans frais supplémentaires pour vous.
    </div>
  `;

  detail.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', (e) => { e.preventDefault(); router.navigate(el.dataset.nav); });
  });

  app.appendChild(detail);
  app.appendChild(renderFooter());
}
