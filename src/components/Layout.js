import { shops } from '../data/shops.js';

export function renderNav(router) {
  const nav = document.createElement('nav');
  nav.innerHTML = `
    <a class="logo" data-nav="/">Woof<span>Prix</span></a>
    <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
    <ul class="nav-links" id="navLinks">
      <li><a data-nav="/animal/dog">🐕 Chiens</a></li>
      <li><a data-nav="/animal/cat">🐈 Chats</a></li>
      <li><a data-nav="/category/vermifuges">💊 Vermifuges</a></li>
      <li><a data-nav="/category/antiparasitaires">🐛 Antiparasitaires</a></li>
      <li><a data-nav="/category/croquettes-chien">🍖 Croquettes</a></li>
    </ul>
  `;

  nav.querySelectorAll('[data-nav]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('navLinks')?.classList.remove('open');
      router.navigate(el.dataset.nav);
    });
  });

  const menuBtn = nav.querySelector('#menuBtn');
  menuBtn?.addEventListener('click', () => {
    document.getElementById('navLinks')?.classList.toggle('open');
  });

  return nav;
}

export function renderFooter() {
  const footer = document.createElement('footer');
  const shopNames = shops.map(s =>
    `<span style="color:${s.color};font-weight:600">${s.name}</span>`
  ).join(' · ');

  footer.innerHTML = `
    <div class="footer-links">
      <a href="#">Mentions légales</a>
      <a href="#">Politique de confidentialité</a>
      <a href="#">Contact</a>
    </div>
    <p>© ${new Date().getFullYear()} WoofPrix – Comparateur de prix pour animaux de compagnie</p>
    <p class="footer-shops">Prix comparés sur : ${shopNames}</p>
  `;
  return footer;
}

export function renderNoDataMessage() {
  const div = document.createElement('div');
  div.className = 'no-results fade-in';
  div.style.padding = '5rem 2rem';
  div.innerHTML = `
    <span class="big-emoji" style="font-size:3.5rem">⏳</span>
    <p style="font-size:1.2rem;font-weight:600;color:var(--ink)">Prix en cours de chargement</p>
    <p style="font-size:0.95rem">Les données de prix seront disponibles après la première exécution du scraping automatique, prévue cette nuit.</p>
    <p style="font-size:0.85rem;color:var(--muted);margin-top:1.5rem">Revenez demain pour comparer les prix sur ${shops.length} sites animaliers !</p>
    <div style="margin-top:2rem;display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center">
      ${shops.slice(0, 12).map(s =>
        `<span class="tag" style="background:${s.color}22;color:${s.color};font-weight:600">${s.logo} ${s.name}</span>`
      ).join('')}
    </div>
  `;
  return div;
}

export async function renderStats(stats) {
  const div = document.createElement('div');
  div.className = 'stats';

  const s = stats || { products_count: 0, shops_count: 0 };

  div.innerHTML = `
    <div class="stat">
      <div class="stat-num">+<span>${s.products_count || 0}</span></div>
      <div class="stat-label">Produits comparés</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>${s.shops_count || shops.length}</span></div>
      <div class="stat-label">Sites partenaires</div>
    </div>
    <div class="stat">
      <div class="stat-num">jusqu'à <span>60%</span></div>
      <div class="stat-label">D'économies possibles</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>100%</span></div>
      <div class="stat-label">Gratuit</div>
    </div>
  `;
  return div;
}

export function renderSavingsBanner(router) {
  const div = document.createElement('div');
  div.className = 'savings-banner fade-in';
  div.innerHTML = `
    <div class="savings-text">
      <h2>Les Français dépensent <span>1 000€/an</span><br>pour leur animal.</h2>
      <p>La moitié pourrait être évitée en comparant les prix.<br>WoofPrix le fait pour vous, gratuitement.</p>
    </div>
    <button class="savings-cta">Commencer à économiser</button>
  `;
  div.querySelector('.savings-cta')?.addEventListener('click', () => {
    router.navigate('/');
  });
  return div;
}

export function formatPrice(price) {
  return Number(price).toFixed(2).replace('.', ',') + ' €';
}

export function getShop(id) {
  return shops.find(s => s.id === id);
}
