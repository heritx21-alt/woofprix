(function(){const a=document.createElement("link").relList;if(a&&a.supports&&a.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))r(s);new MutationObserver(s=>{for(const i of s)if(i.type==="childList")for(const l of i.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&r(l)}).observe(document,{childList:!0,subtree:!0});function t(s){const i={};return s.integrity&&(i.integrity=s.integrity),s.referrerPolicy&&(i.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?i.credentials="include":s.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function r(s){if(s.ep)return;s.ep=!0;const i=t(s);fetch(s.href,i)}})();class R{constructor(a){this.routes=a,this.currentRoute=null,this._resolve=null,window.addEventListener("hashchange",()=>this.resolve())}navigate(a){window.location.hash=a}async resolve(){const a=window.location.hash.slice(1)||"/";let t=!1;for(const r of this.routes){const s=r.path.match(/:(\w+)/g);if(s){const i=r.path.replace(/:\w+/g,"([^/]+)"),l=new RegExp(`^${i}$`),d=a.match(l);if(d){const u={};s.forEach((o,n)=>{u[o.slice(1)]=decodeURIComponent(d[n+1])}),this.currentRoute!==a&&(this.currentRoute=a,await r.handler(u)),t=!0;break}}else if(r.path===a){this.currentRoute!==a&&(this.currentRoute=a,await r.handler({})),t=!0;break}}t||this.routes[0].handler({})}init(){this.resolve()}}const j=[{id:"vermifuges",name:"Vermifuges",slug:"vermifuges",emoji:"💊",count:48,animal:"all"},{id:"antiparasitaires",name:"Antiparasitaires",slug:"antiparasitaires",emoji:"🐛",count:63,animal:"all"},{id:"croquettes-chien",name:"Croquettes chien",slug:"croquettes-chien",emoji:"🍖",count:120,animal:"dog"},{id:"croquettes-chat",name:"Croquettes chat",slug:"croquettes-chat",emoji:"🐟",count:98,animal:"cat"},{id:"patées-boites",name:"Pâtées & boîtes",slug:"patees-boites",emoji:"🥫",count:84,animal:"all"},{id:"soins-hygiene",name:"Soins & hygiène",slug:"soins-hygiene",emoji:"💉",count:56,animal:"all"}];let g=null,w=!1;async function x(){if(g)return g;if(w)return null;try{const e=await fetch("/data/products.json");if(!e.ok)return console.warn(`API: products.json introuvable (HTTP ${e.status})`),w=!0,null;const a=await e.json();return!a||!Array.isArray(a.products)?(console.warn("API: products.json vide ou invalide"),w=!0,null):(g=a,g)}catch(e){return console.warn("API: impossible de charger products.json —",e.message),w=!0,null}}function T(){g=null,w=!1}async function z(){const e=await x();return(e==null?void 0:e.stats)||null}async function f({category:e,animal:a,search:t,limit:r,offset:s}={}){const i=await x();if(!i)return[];let l=i.products;if(e&&(l=l.filter(n=>n.category===e)),a&&(l=l.filter(n=>n.animal===a)),t){const n=t.toLowerCase();l=l.filter(c=>c.name.toLowerCase().includes(n)||(c.categoryLabel||"").toLowerCase().includes(n)||(c.animalLabel||"").toLowerCase().includes(n)||(c.description||"").toLowerCase().includes(n))}const d=l.map(n=>{const c=[...n.prices||[]].sort((M,S)=>M.price-S.price),p=c[0],v=c[c.length-1],y=c.length>1?Math.round((v.price-p.price)/v.price*100):0;return{...n,prices:c,bestPrice:p==null?void 0:p.price,savings:y}}),u=s||0,o=u+(r||d.length);return d.slice(u,o)}async function B(e){return(await f()).find(t=>t.slug===e)||null}async function C(){var a;const e=await x();return e!==null&&((a=e.products)==null?void 0:a.length)>0}const $=[{id:"zooplus",name:"Zooplus",url:"https://www.zooplus.fr",logo:"🛒",color:"#2D9B6F",affiliate:!0,network:"awin"},{id:"wanimo",name:"Wanimo",url:"https://www.wanimo.com",logo:"🛒",color:"#4A90D9",affiliate:!0,network:"netaffiliation"},{id:"pepette",name:"Pepette",url:"https://www.pepette.fr",logo:"🛒",color:"#E86C8B",affiliate:!0,network:"awin"},{id:"directvet",name:"Direct-Vet",url:"https://www.direct-vet.fr",logo:"🛒",color:"#27AE60",affiliate:!1,network:null},{id:"cernunos",name:"Cernunos",url:"https://www.cernunos.fr",logo:"🛒",color:"#8E44AD",affiliate:!1,network:null},{id:"santevet",name:"Santévet",url:"https://www.santevet.com",logo:"🛒",color:"#3498DB",affiliate:!1,network:null},{id:"amazon",name:"Amazon",url:"https://www.amazon.fr",logo:"🛒",color:"#FF9900",affiliate:!0,network:"amazon"},{id:"ultrapremium",name:"Ultra Premium Direct",url:"https://www.ultrapremiumdirect.com",logo:"🛒",color:"#E74C3C",affiliate:!1,network:null},{id:"maxizoo",name:"MaxiZoo",url:"https://www.maxizoo.fr",logo:"🛒",color:"#9B59B6",affiliate:!1,network:null},{id:"zoomalia",name:"Zoomalia",url:"https://www.zoomalia.com",logo:"🛒",color:"#1ABC9C",affiliate:!1,network:null},{id:"animalis",name:"Animalis",url:"https://www.animalis.com",logo:"🛒",color:"#F39C12",affiliate:!1,network:null},{id:"jardiland",name:"Jardiland",url:"https://www.jardiland.com",logo:"🛒",color:"#27AE60",affiliate:!1,network:null},{id:"truffaut",name:"Truffaut",url:"https://www.truffaut.com",logo:"🛒",color:"#2ECC71",affiliate:!1,network:null},{id:"laferme",name:"La Ferme des Animaux",url:"https://www.lafermedesanimaux.com",logo:"🛒",color:"#E67E22",affiliate:!1,network:null},{id:"medor",name:"Médor & Compagnie",url:"https://www.medor-et-compagnie.fr",logo:"🛒",color:"#95A5A6",affiliate:!1,network:null},{id:"petsonic",name:"Petsonic",url:"https://www.petsonic.com",logo:"🛒",color:"#34495E",affiliate:!1,network:null},{id:"produitsveto",name:"Produits-Véto",url:"https://www.produits-veto.com",logo:"🛒",color:"#16A085",affiliate:!1,network:null},{id:"franceveto",name:"France-Véto",url:"https://www.france-veto.com",logo:"🛒",color:"#2980B9",affiliate:!1,network:null},{id:"universveto",name:"Univers-Véto",url:"https://www.univers-veto.fr",logo:"🛒",color:"#8E44AD",affiliate:!1,network:null}];function L(e){const a=document.createElement("nav");a.innerHTML=`
    <a class="logo" data-nav="/">Woof<span>Prix</span></a>
    <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
    <ul class="nav-links" id="navLinks">
      <li><a data-nav="/animal/dog">🐕 Chiens</a></li>
      <li><a data-nav="/animal/cat">🐈 Chats</a></li>
      <li><a data-nav="/category/vermifuges">💊 Vermifuges</a></li>
      <li><a data-nav="/category/antiparasitaires">🐛 Antiparasitaires</a></li>
      <li><a data-nav="/category/croquettes-chien">🍖 Croquettes</a></li>
    </ul>
  `,a.querySelectorAll("[data-nav]").forEach(r=>{r.addEventListener("click",s=>{var i;s.preventDefault(),(i=document.getElementById("navLinks"))==null||i.classList.remove("open"),e.navigate(r.dataset.nav)})});const t=a.querySelector("#menuBtn");return t==null||t.addEventListener("click",()=>{var r;(r=document.getElementById("navLinks"))==null||r.classList.toggle("open")}),a}function m(){const e=document.createElement("footer"),a=$.map(t=>`<span style="color:${t.color};font-weight:600">${t.name}</span>`).join(" · ");return e.innerHTML=`
    <div class="footer-links">
      <a href="#">Mentions légales</a>
      <a href="#">Politique de confidentialité</a>
      <a href="#">Contact</a>
    </div>
    <p>© ${new Date().getFullYear()} WoofPrix – Comparateur de prix pour animaux de compagnie</p>
    <p class="footer-shops">Prix comparés sur : ${a}</p>
  `,e}function E(){const e=document.createElement("div");return e.className="no-results fade-in",e.style.padding="5rem 2rem",e.innerHTML=`
    <span class="big-emoji" style="font-size:3.5rem">⏳</span>
    <p style="font-size:1.2rem;font-weight:600;color:var(--ink)">Prix en cours de chargement</p>
    <p style="font-size:0.95rem">Les données de prix seront disponibles après la première exécution du scraping automatique, prévue cette nuit.</p>
    <p style="font-size:0.85rem;color:var(--muted);margin-top:1.5rem">Revenez demain pour comparer les prix sur ${$.length} sites animaliers !</p>
    <div style="margin-top:2rem;display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center">
      ${$.slice(0,12).map(a=>`<span class="tag" style="background:${a.color}22;color:${a.color};font-weight:600">${a.logo} ${a.name}</span>`).join("")}
    </div>
  `,e}async function H(e){const a=document.createElement("div");a.className="stats";const t=e||{products_count:0,shops_count:0};return a.innerHTML=`
    <div class="stat">
      <div class="stat-num">+<span>${t.products_count||0}</span></div>
      <div class="stat-label">Produits comparés</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>${t.shops_count||$.length}</span></div>
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
  `,a}function P(e){var t;const a=document.createElement("div");return a.className="savings-banner fade-in",a.innerHTML=`
    <div class="savings-text">
      <h2>Les Français dépensent <span>1 000€/an</span><br>pour leur animal.</h2>
      <p>La moitié pourrait être évitée en comparant les prix.<br>WoofPrix le fait pour vous, gratuitement.</p>
    </div>
    <button class="savings-cta">Commencer à économiser</button>
  `,(t=a.querySelector(".savings-cta"))==null||t.addEventListener("click",()=>{e.navigate("/")}),a}function b(e){return Number(e).toFixed(2).replace(".",",")+" €"}function k(e){return $.find(a=>a.id===e)}function I(e){const a=(e.prices||[]).slice(0,3);return`
    <div class="product-card fade-in" data-product="${e.slug}">
      <div class="product-top">
        <div class="product-img">${e.emoji||"📦"}</div>
        <div class="product-info">
          <div class="product-name">${e.name}</div>
          <div class="product-animal">${e.animal==="dog"?"🐕":"🐈"} ${e.animalLabel||""} • ${e.categoryLabel||""}</div>
        </div>
        ${e.savings?`<span class="product-badge">−${e.savings}%</span>`:""}
      </div>
      <div class="price-list">
        ${a.map(t=>{const r=k(t.shop);return`
            <div class="price-row">
              <span class="shop-name" style="color:${(r==null?void 0:r.color)||"var(--muted)"}">${(r==null?void 0:r.name)||t.shop}</span>
              <span class="price-amount ${t.price===e.bestPrice?"best":""}">${b(t.price)}</span>
            </div>
          `}).join("")}
        ${e.prices&&e.prices.length>3?`<div class="price-row"><span class="shop-name" style="color:var(--muted)">+${e.prices.length-3} autres prix</span></div>`:""}
      </div>
      <button class="compare-btn" data-product="${e.slug}">Voir tous les prix →</button>
    </div>
  `}async function A(e){var u,o;const a=document.getElementById("app");a.innerHTML="",T(),a.appendChild(L(e));const t=await z(),r=await C(),s=document.createElement("section");s.className="hero",s.innerHTML=`
    <div class="hero-badge">🐾 Comparateur N°1 produits animaux</div>
    <h1>Le meilleur prix pour<br><em>votre animal</em></h1>
    <p>Comparez vermifuges, antiparasitaires et croquettes sur les meilleures animaleries en ligne. Économisez jusqu'à 60% sur les mêmes produits.</p>
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="Ex : Frontline chat, Milbemax, Royal Canin…" autofocus />
      <button class="search-btn" id="searchBtn">Comparer</button>
    </div>
    <div class="search-tags">
      ${["Frontline chat","Milbemax chien","Royal Canin","Advocate chat","Croquettes chien"].map(n=>`<button class="tag" data-search="${n}">${n}</button>`).join("")}
    </div>
  `,a.appendChild(s);const i=()=>{const n=s.querySelector("#searchInput");n&&n.value.trim()&&e.navigate(`/search/${encodeURIComponent(n.value.trim())}`)};if((u=s.querySelector("#searchBtn"))==null||u.addEventListener("click",i),(o=s.querySelector("#searchInput"))==null||o.addEventListener("keydown",n=>{n.key==="Enter"&&i()}),s.querySelectorAll("[data-search]").forEach(n=>{n.addEventListener("click",()=>e.navigate(`/search/${encodeURIComponent(n.dataset.search)}`))}),a.appendChild(await H(t)),!r){a.appendChild(E()),a.appendChild(m());return}const l=document.createElement("div");l.className="section",l.innerHTML=`
    <div class="section-header">
      <h2 class="section-title">Catégories populaires</h2>
      <a class="section-link" data-nav="/animal/all">Tout voir →</a>
    </div>
    <div class="categories">
      ${j.map(n=>`
        <a class="cat-card" data-nav="/category/${n.slug}">
          <span class="cat-emoji">${n.emoji}</span>
          <div class="cat-name">${n.name}</div>
          <div class="cat-count">${n.count} produits</div>
        </a>
      `).join("")}
    </div>
  `,l.querySelectorAll("[data-nav]").forEach(n=>{n.addEventListener("click",c=>{c.preventDefault(),e.navigate(n.dataset.nav)})}),a.appendChild(l);const d=document.createElement("div");d.className="section",d.innerHTML=`
    <div class="section-header">
      <h2 class="section-title">Produits les plus recherchés</h2>
      <a class="section-link" data-nav="/animal/all">Tout voir →</a>
    </div>
    <div class="products" id="featuredProducts">
      <div class="loading"><div class="spinner"></div></div>
    </div>
  `,a.appendChild(d),f({limit:6}).then(n=>{const c=d.querySelector("#featuredProducts");if(c){if(n.length===0){c.innerHTML=`
        <div class="no-results">
          <p style="font-size:1rem">Aucun produit disponible pour le moment.</p>
        </div>
      `;return}c.innerHTML=n.map(p=>I(p)).join(""),c.querySelectorAll("[data-product]").forEach(p=>{p.addEventListener("click",()=>e.navigate(`/product/${p.dataset.product}`))})}}),a.appendChild(P(e)),a.appendChild(m())}async function D(e,a){const t=document.getElementById("app");if(t.innerHTML="",t.appendChild(L(a)),!await C()){t.appendChild(E()),t.appendChild(m());return}const s=await B(e);if(!s){t.innerHTML+=`
      <div class="section" style="text-align:center;padding:4rem 2rem">
        <span style="font-size:3rem;display:block;margin-bottom:1rem">😕</span>
        <h2 style="font-family:var(--font-title);margin-bottom:0.5rem">Produit introuvable</h2>
        <p style="color:var(--muted);margin-bottom:1.5rem">Ce produit n'existe pas ou a été retiré.</p>
        <button class="search-btn" onclick="location.hash='/'">Retour à l'accueil</button>
      </div>
    `,t.appendChild(m());return}const i=[...s.prices].sort((n,c)=>n.price-c.price),l=i[0],d={dog:"🐕 Chien",cat:"🐈 Chat"},u=i.length>1?Math.round((i[i.length-1].price-l.price)/i[i.length-1].price*100):0,o=document.createElement("div");o.className="product-detail fade-in",o.innerHTML=`
    <a class="back-link" data-nav="/">← Retour aux produits</a>

    <div class="detail-header">
      <div class="detail-img">${s.emoji||"📦"}</div>
      <div class="detail-info">
        <h1>${s.name}</h1>
        <div class="detail-meta">
          <span class="detail-meta-tag">${d[s.animal]||s.animalLabel||s.animal}</span>
          <span class="detail-meta-tag">${s.categoryLabel||s.category||""}</span>
          ${u>0?`<span class="detail-meta-tag" style="background:var(--green-light);color:var(--green);font-weight:600">Jusqu'à −${u}%</span>`:""}
        </div>
        <p class="detail-desc">${s.description||""}</p>
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
      ${i.map((n,c)=>{const p=k(n.shop);if(!p)return"";const v=c===0,y=v?0:Math.round((n.price-l.price)/l.price*100);return`
          <div class="compare-row ${v?"best-row":""}">
            <div class="compare-shop">
              <div class="compare-shop-logo" style="background:${p.color}">${p.logo}</div>
              <span>${p.name}</span>
              ${v?'<span class="compare-badge">Meilleur prix</span>':""}
            </div>
            <div>
              <div class="compare-price ${v?"best":""}">${b(n.price)}</div>
              ${y>0?`<div style="font-size:0.72rem;color:var(--red)">+${y}%</div>`:""}
            </div>
            <div class="compare-shipping ${(n.shipping||0)===0?"free":""}">
              ${(n.shipping||0)===0?"Gratuite":b(n.shipping)}
            </div>
            <div class="compare-actions">
              <a href="${n.url||p.url}" target="_blank" rel="noopener" class="compare-link">Voir l'offre</a>
              <span class="compare-stock ${n.in_stock?"in-stock":"out-of-stock"}">
                ${n.in_stock?"✓ En stock":"✗ Rupture"}
              </span>
            </div>
          </div>
        `}).join("")}
    </div>

    <div class="affiliation-notice">
      <strong>💡 Affiliations :</strong> Les prix affichés incluent les éventuels frais de port. WoofPrix perçoit une commission sur les achats effectués via les liens partenaires, sans frais supplémentaires pour vous.
    </div>
  `,o.querySelectorAll("[data-nav]").forEach(n=>{n.addEventListener("click",c=>{c.preventDefault(),a.navigate(n.dataset.nav)})}),t.appendChild(o),t.appendChild(m())}function N(e){const a=(e.prices||[]).slice(0,3);return`
    <div class="product-card fade-in" data-product="${e.slug}">
      <div class="product-top">
        <div class="product-img">${e.emoji||"📦"}</div>
        <div class="product-info">
          <div class="product-name">${e.name}</div>
          <div class="product-animal">${e.animal==="dog"?"🐕":"🐈"} ${e.animalLabel||""} • ${e.categoryLabel||""}</div>
        </div>
        ${e.savings?`<span class="product-badge">−${e.savings}%</span>`:""}
      </div>
      <div class="price-list">
        ${a.map(t=>{const r=k(t.shop);return`
            <div class="price-row">
              <span class="shop-name" style="color:${(r==null?void 0:r.color)||"var(--muted)"}">${(r==null?void 0:r.name)||t.shop}</span>
              <span class="price-amount ${t.price===e.bestPrice?"best":""}">${b(t.price)}</span>
            </div>
          `}).join("")}
      </div>
      <button class="compare-btn" data-product="${e.slug}">Voir tous les prix →</button>
    </div>
  `}async function F(e,a){const t=document.getElementById("app");if(t.innerHTML="",t.appendChild(L(a)),!await C()){t.appendChild(E()),t.appendChild(m());return}const s=await f({search:e}),i=document.createElement("div");i.className="search-results fade-in";const l=()=>{const o=i.querySelector("#searchResultsInput");o&&o.value.trim()&&a.navigate(`/search/${encodeURIComponent(o.value.trim())}`)};i.innerHTML=`
    <div class="breadcrumb">
      <a data-nav="/">Accueil</a>
      <span class="sep">/</span>
      <span class="current">Résultats pour « ${e} »</span>
    </div>

    <div class="results-bar">
      <h2>Résultats pour « ${e} » <span class="search-results-count">(${s.length} produit${s.length>1?"s":""})</span></h2>
      <div class="search-wrap" style="margin:0 0 0 auto;flex:1;max-width:360px">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchResultsInput" placeholder="Affiner la recherche…" value="${e}" />
        <button class="search-btn" id="searchResultsBtn">Chercher</button>
      </div>
    </div>

    ${s.length===0?`
      <div class="no-results">
        <span class="big-emoji">🔍</span>
        <p>Aucun produit trouvé pour « ${e} »</p>
        <p style="font-size:0.9rem;color:var(--muted)">Essayez : Frontline, Milbemax, Royal Canin, croquettes, vermifuge…</p>
        <div style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center">
          ${["Frontline","Milbemax","Royal Canin","Croquettes","Antiparasitaire"].map(o=>`<button class="tag" data-search="${o}">${o}</button>`).join("")}
        </div>
      </div>
    `:`
      <div class="products">
        ${s.map(o=>N(o)).join("")}
      </div>
    `}
  `,i.querySelectorAll("[data-nav]").forEach(o=>{o.addEventListener("click",n=>{n.preventDefault(),a.navigate(o.dataset.nav)})}),i.querySelectorAll("[data-product]").forEach(o=>{o.addEventListener("click",()=>a.navigate(`/product/${o.dataset.product}`))}),i.querySelectorAll("[data-search]").forEach(o=>{o.addEventListener("click",()=>a.navigate(`/search/${encodeURIComponent(o.dataset.search)}`))});const d=i.querySelector("#searchResultsBtn"),u=i.querySelector("#searchResultsInput");d==null||d.addEventListener("click",l),u==null||u.addEventListener("keydown",o=>{o.key==="Enter"&&l()}),t.appendChild(i),s.length>0&&t.appendChild(P(a)),t.appendChild(m())}function V(e){const a=(e.prices||[]).slice(0,3);return`
    <div class="product-card fade-in" data-product="${e.slug}">
      <div class="product-top">
        <div class="product-img">${e.emoji||"📦"}</div>
        <div class="product-info">
          <div class="product-name">${e.name}</div>
          <div class="product-animal">${e.animal==="dog"?"🐕":"🐈"} ${e.animalLabel||""} • ${e.categoryLabel||""}</div>
        </div>
        ${e.savings?`<span class="product-badge">−${e.savings}%</span>`:""}
      </div>
      <div class="price-list">
        ${a.map(t=>{const r=k(t.shop);return`
            <div class="price-row">
              <span class="shop-name" style="color:${(r==null?void 0:r.color)||"var(--muted)"}">${(r==null?void 0:r.name)||t.shop}</span>
              <span class="price-amount ${t.price===e.bestPrice?"best":""}">${b(t.price)}</span>
            </div>
          `}).join("")}
      </div>
      <button class="compare-btn" data-product="${e.slug}">Voir tous les prix →</button>
    </div>
  `}async function q(e,a,t,r){const s=document.getElementById("app");if(s.innerHTML="",s.appendChild(L(t)),!await C()){s.appendChild(E()),s.appendChild(m());return}const l=await r(),d=U(e,a,l,t);s.appendChild(d),l.length>0&&s.appendChild(P(t)),s.appendChild(m())}function _(e,a){const t=j.find(i=>i.slug===e),r=(t==null?void 0:t.name)||"Catégorie",s=(t==null?void 0:t.emoji)||"📂";return q(r,s,a,()=>f({category:e}))}function O(e,a){const t={dog:["Chiens","🐕"],cat:["Chats","🐈"]},[r,s]=e==="all"?["Tous les produits","🐾"]:t[e]||["Animaux","🐾"];return q(r,s,a,e==="all"?()=>f({limit:200}):()=>f({animal:e}))}function U(e,a,t,r){const s=document.createElement("div");return s.className="search-results fade-in",s.innerHTML=`
    <div class="breadcrumb">
      <a data-nav="/">Accueil</a>
      <span class="sep">/</span>
      <span class="current">${a} ${e}</span>
    </div>

    <h2>${a} ${e} <span class="search-results-count">(${t.length} produit${t.length>1?"s":""})</span></h2>

    <div class="products" style="margin-top:1.5rem">
      ${t.length===0?'<div class="no-results"><span class="big-emoji">📭</span><p>Aucun produit dans cette rubrique pour le moment.</p></div>':t.map(i=>V(i)).join("")}
    </div>
  `,s.querySelectorAll("[data-nav]").forEach(i=>{i.addEventListener("click",l=>{l.preventDefault(),r.navigate(i.dataset.nav)})}),s.querySelectorAll("[data-product]").forEach(i=>{i.addEventListener("click",()=>r.navigate(`/product/${i.dataset.product}`))}),s}const h=new R([{path:"/",handler:()=>A(h)},{path:"/home",handler:()=>A(h)},{path:"/product/:slug",handler:e=>D(e.slug,h)},{path:"/search/:query",handler:e=>F(e.query,h)},{path:"/category/:slug",handler:e=>_(e.slug,h)},{path:"/animal/:type",handler:e=>O(e.type,h)}]);document.addEventListener("DOMContentLoaded",()=>{h.resolve()});
