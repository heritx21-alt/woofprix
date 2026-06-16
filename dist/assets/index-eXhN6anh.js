(function(){const s=document.createElement("link").relList;if(s&&s.supports&&s.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))i(e);new MutationObserver(e=>{for(const n of e)if(n.type==="childList")for(const o of n.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&i(o)}).observe(document,{childList:!0,subtree:!0});function a(e){const n={};return e.integrity&&(n.integrity=e.integrity),e.referrerPolicy&&(n.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?n.credentials="include":e.crossOrigin==="anonymous"?n.credentials="omit":n.credentials="same-origin",n}function i(e){if(e.ep)return;e.ep=!0;const n=a(e);fetch(e.href,n)}})();class ee{constructor(s){this.routes=s,this.currentRoute=null,this._resolve=null,window.addEventListener("hashchange",()=>this.resolve())}navigate(s){window.location.hash=s}async resolve(){const s=window.location.hash.slice(1)||"/";let a=!1;for(const i of this.routes){const e=i.path.match(/:(\w+)/g);if(e){const n=i.path.replace(/:\w+/g,"([^/]+)"),o=new RegExp(`^${n}$`),p=s.match(o);if(p){const l={};e.forEach((r,c)=>{l[r.slice(1)]=decodeURIComponent(p[c+1])}),this.currentRoute!==s&&(this.currentRoute=s,await i.handler(l)),a=!0;break}}else if(i.path===s){this.currentRoute!==s&&(this.currentRoute=s,await i.handler({})),a=!0;break}}a||this.routes[0].handler({})}init(){this.resolve()}}const te="modulepreload",ae=function(t){return"/"+t},J={},D=function(s,a,i){let e=Promise.resolve();if(a&&a.length>0){document.getElementsByTagName("link");const o=document.querySelector("meta[property=csp-nonce]"),p=(o==null?void 0:o.nonce)||(o==null?void 0:o.getAttribute("nonce"));e=Promise.allSettled(a.map(l=>{if(l=ae(l),l in J)return;J[l]=!0;const r=l.endsWith(".css"),c=r?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${l}"]${c}`))return;const u=document.createElement("link");if(u.rel=r?"stylesheet":te,r||(u.as="script"),u.crossOrigin="",u.href=l,p&&u.setAttribute("nonce",p),document.head.appendChild(u),r)return new Promise((v,h)=>{u.addEventListener("load",v),u.addEventListener("error",()=>h(new Error(`Unable to preload CSS for ${l}`)))})}))}function n(o){const p=new Event("vite:preloadError",{cancelable:!0});if(p.payload=o,window.dispatchEvent(p),!p.defaultPrevented)throw o}return e.then(o=>{for(const p of o||[])p.status==="rejected"&&n(p.reason);return s().catch(n)})};let k=null,M=!1;async function Y(){if(k)return k;if(M)return null;try{const t=await fetch("/data/products.json");if(!t.ok)return console.warn(`API: products.json introuvable (HTTP ${t.status})`),M=!0,null;const s=await t.json();return!s||!Array.isArray(s.products)?(console.warn("API: products.json vide ou invalide"),M=!0,null):(k=s,k)}catch(t){return console.warn("API: impossible de charger products.json —",t.message),M=!0,null}}function T(){k=null,M=!1}async function R(){const t=await Y();return(t==null?void 0:t.stats)||null}async function q({category:t,animal:s,search:a,limit:i,offset:e}={}){const n=await Y();if(!n)return[];let o=n.products;if(t&&(o=o.filter(c=>c.category===t)),s&&(o=o.filter(c=>c.animal===s)),a){const c=a.toLowerCase();o=o.filter(u=>u.name.toLowerCase().includes(c)||(u.categoryLabel||"").toLowerCase().includes(c)||(u.animalLabel||"").toLowerCase().includes(c)||(u.description||"").toLowerCase().includes(c))}const p=o.map(c=>{const u=[...c.prices||[]].sort((m,w)=>m.price-w.price),v=u[0],h=u[u.length-1],d=u.length>1?Math.round((h.price-v.price)/h.price*100):0;return{...c,prices:u,bestPrice:v==null?void 0:v.price,savings:d}}),l=e||0,r=l+(i||p.length);return p.slice(l,r)}async function ne(t){return(await q()).find(a=>a.slug===t)||null}const z=[{id:"croquettes-chien",name:"Croquettes chien",slug:"croquettes-chien",emoji:"🍖",count:10,animal:"dog"},{id:"friandises",name:"Friandises",slug:"friandises",emoji:"🦴",count:2,animal:"dog"},{id:"accessoires-chien",name:"Accessoires chien",slug:"accessoires-chien",emoji:"🎾",count:4,animal:"dog"},{id:"croquettes-chat",name:"Croquettes chat",slug:"croquettes-chat",emoji:"🐟",count:8,animal:"cat"},{id:"patees",name:"Pâtées & boîtes",slug:"patees",emoji:"🥫",count:3,animal:"cat"},{id:"litiere",name:"Litière",slug:"litiere",emoji:"⬜",count:2,animal:"cat"},{id:"accessoires-chat",name:"Accessoires chat",slug:"accessoires-chat",emoji:"🧶",count:4,animal:"cat"},{id:"rongeurs",name:"Rongeurs",slug:"rongeurs",emoji:"🐹",count:3,animal:"other"},{id:"oiseaux",name:"Oiseaux",slug:"oiseaux",emoji:"🐦",count:1,animal:"other"},{id:"poissons",name:"Poissons",slug:"poissons",emoji:"🐠",count:1,animal:"other"}],A=[{id:"zooplus",name:"Zooplus",url:"https://www.zooplus.fr",logo:"🐾",color:"#2D9B6F",affiliate:!0,network:"awin"},{id:"wanimo",name:"Wanimo",url:"https://www.wanimo.com",logo:"🐱",color:"#4A90D9",affiliate:!0,network:"netaffiliation"},{id:"pepette",name:"Pepette",url:"https://www.pepette.fr",logo:"🐶",color:"#E86C8B",affiliate:!0,network:"awin"},{id:"directvet",name:"Direct-Vet",url:"https://www.direct-vet.fr",logo:"💊",color:"#27AE60",affiliate:!1,network:null},{id:"cernunos",name:"Cernunos",url:"https://www.cernunos.fr",logo:"🌿",color:"#8E44AD",affiliate:!1,network:null},{id:"santevet",name:"Santévet",url:"https://www.santevet.com",logo:"❤️",color:"#3498DB",affiliate:!1,network:null},{id:"amazon",name:"Amazon",url:"https://www.amazon.fr",logo:"📦",color:"#FF9900",affiliate:!0,network:"amazon"},{id:"ultrapremium",name:"Ultra Premium Direct",url:"https://www.ultrapremiumdirect.com",logo:"⭐",color:"#E74C3C",affiliate:!1,network:null},{id:"maxizoo",name:"MaxiZoo",url:"https://www.maxizoo.fr",logo:"🦁",color:"#9B59B6",affiliate:!1,network:null},{id:"zoomalia",name:"Zoomalia",url:"https://www.zoomalia.com",logo:"🦎",color:"#1ABC9C",affiliate:!1,network:null},{id:"animalis",name:"Animalis",url:"https://www.animalis.com",logo:"🐕",color:"#F39C12",affiliate:!1,network:null},{id:"jardiland",name:"Jardiland",url:"https://www.jardiland.com",logo:"🌻",color:"#27AE60",affiliate:!1,network:null},{id:"truffaut",name:"Truffaut",url:"https://www.truffaut.com",logo:"🌸",color:"#2ECC71",affiliate:!1,network:null},{id:"laferme",name:"La Ferme des Animaux",url:"https://www.lafermedesanimaux.com",logo:"🐓",color:"#E67E22",affiliate:!1,network:null},{id:"medor",name:"Médor & Compagnie",url:"https://www.medor-et-compagnie.fr",logo:"🦴",color:"#95A5A6",affiliate:!1,network:null},{id:"petsonic",name:"Petsonic",url:"https://www.petsonic.com",logo:"🐟",color:"#34495E",affiliate:!1,network:null},{id:"produitsveto",name:"Produits-Véto",url:"https://www.produits-veto.com",logo:"🏥",color:"#16A085",affiliate:!1,network:null},{id:"franceveto",name:"France-Véto",url:"https://www.france-veto.com",logo:"⚕️",color:"#2980B9",affiliate:!1,network:null},{id:"universveto",name:"Univers-Véto",url:"https://www.univers-veto.fr",logo:"🔬",color:"#8E44AD",affiliate:!1,network:null}],F=Object.freeze(Object.defineProperty({__proto__:null,shops:A},Symbol.toStringTag,{value:"Module"}));function H(t,s={}){var e;const a=document.createElement("header");a.className="site-header",a.innerHTML=`
    <div class="header-inner">
      <a class="logo" data-nav="/">Woof<span>Prix</span></a>
      <div class="header-search">
        <span class="search-icon">🔍</span>
        <input type="text" id="headerSearchInput" placeholder="Rechercher un produit..." autocomplete="off">
      </div>
      <button class="menu-btn" id="menuBtn" aria-label="Menu">☰</button>
      <ul class="nav-links" id="navLinks">
        <li><a data-nav="/animal/dog">🐕 Chiens</a></li>
        <li><a data-nav="/animal/cat">🐈 Chats</a></li>
        <li><a data-nav="/animal/all">🐾 Tous</a></li>
      </ul>
    </div>
    <div class="cat-bar show" id="catBar">
      <div class="cat-bar-inner">
        ${z.map(n=>`
          <a class="cat-pill" data-nav="/category/${n.slug}">${n.emoji} ${n.name}</a>
        `).join("")}
      </div>
    </div>
  `,a.querySelectorAll("[data-nav]").forEach(n=>{n.addEventListener("click",o=>{var p;o.preventDefault(),(p=document.getElementById("navLinks"))==null||p.classList.remove("open"),t.navigate(n.dataset.nav)})}),(e=a.querySelector("#menuBtn"))==null||e.addEventListener("click",()=>{var n;(n=document.getElementById("navLinks"))==null||n.classList.toggle("open")});const i=a.querySelector("#headerSearchInput");return i==null||i.addEventListener("keydown",n=>{n.key==="Enter"&&i.value.trim()&&(t.navigate(`/search/${encodeURIComponent(i.value.trim())}`),i.value="")}),a}function L(){const t=document.createElement("footer");t.className="site-footer";const s=A.map(a=>`<span style="color:${a.color}">${a.name}</span>`).join(" · ");return t.innerHTML=`
    <div class="footer-inner">
      <div class="footer-main">
        <div class="footer-col">
          <h4>🐾 WoofPrix</h4>
          <a href="#">Comparateur de prix pour animaux</a>
          <span>Gratuit & indépendant</span>
        </div>
        <div class="footer-col">
          <h4>Animaux</h4>
          <a data-nav="/animal/dog">🐕 Chiens</a>
          <a data-nav="/animal/cat">🐈 Chats</a>
          <a data-nav="/animal/all">🐾 Tous</a>
        </div>
        <div class="footer-col">
          <h4>Informations</h4>
          <a href="#">Mentions légales</a>
          <a href="#">Politique de confidentialité</a>
        </div>
      </div>
      <div class="footer-shops">Prix comparés sur : ${s}</div>
      <div class="footer-copy">
        © ${new Date().getFullYear()} WoofPrix — Comparateur de prix animaliers
      </div>
    </div>
  `,t.querySelectorAll("[data-nav]").forEach(a=>{a.addEventListener("click",i=>{i.preventDefault(),window.dispatchEvent(new CustomEvent("navigate",{detail:a.dataset.nav}))})}),t}function O(t){const s=document.createElement("div");s.className="no-data fade-in";const a=t||A;return s.innerHTML=`
    <span class="big-icon">⏳</span>
    <h2>Prix en cours de chargement</h2>
    <p>Les données seront disponibles après la première exécution du scraping automatique, prévue cette nuit.</p>
    <div class="shop-tags">
      ${a.slice(0,12).map(i=>`<span class="tag" style="background:${i.color}18;color:${i.color}">${i.name}</span>`).join("")}
    </div>
  `,s}async function I(t){const s=document.createElement("div");s.className="stats fade-in";const a=t||{products_count:0,shops_count:0};return s.innerHTML=`
    <div class="stat">
      <div class="stat-num"><span>${a.products_count||0}</span></div>
      <div class="stat-label">Produits comparés</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>${a.shops_count||A.length}</span></div>
      <div class="stat-label">Sites partenaires</div>
    </div>
    <div class="stat">
      <div class="stat-num">jusqu'à <span>60%</span></div>
      <div class="stat-label">D'économies</div>
    </div>
    <div class="stat">
      <div class="stat-num"><span>100%</span></div>
      <div class="stat-label">Gratuit</div>
    </div>
  `,s}function G(t){var a;const s=document.createElement("div");return s.className="savings-banner fade-in",s.innerHTML=`
    <div>
      <h2>Les Français dépensent <span>1 000€/an</span> pour leur animal.</h2>
      <p>La moitié pourrait être économisée en comparant les prix. WoofPrix le fait pour vous, gratuitement.</p>
    </div>
    <button class="savings-cta">Économiser</button>
  `,(a=s.querySelector(".savings-cta"))==null||a.addEventListener("click",()=>{t.navigate("/")}),s}function _(t){const s=document.createElement("nav");return s.className="breadcrumbs",s.innerHTML=t.map((a,i)=>i===t.length-1?`<span>${a.label}</span>`:a.nav?`<a data-nav="${a.nav}">${a.label}</a> <span class="sep">›</span>`:`<span>${a.label}</span> <span class="sep">›</span>`).join(""),s.querySelectorAll("[data-nav]").forEach(a=>{a.addEventListener("click",i=>{i.preventDefault(),window.dispatchEvent(new CustomEvent("navigate",{detail:a.dataset.nav}))})}),s}function j(t){return Number(t).toFixed(2).replace(".",",")+" €"}function B(t){return A.find(s=>s.id===t)}function U(t,s){const a=document.createElement("div");a.className="product-card",a.setAttribute("data-nav",`/product/${t.slug}`);const i=t.prices.slice(0,3),e=t.prices.length-3,n=t.savings>0?`<span class="card-savings">📊 -${t.savings}%</span>`:"",o=t.image?`<img class="card-image" src="${t.image}" alt="${t.name}" loading="lazy">`:`<span class="card-emoji">${t.emoji||"🐾"}</span>`,p=t.description?`<div class="card-desc">${t.description}</div>`:"";return a.innerHTML=`
    <div class="card-header">
      ${o}
      <div>
        <div class="card-title">${t.name}</div>
        ${p}
        <div class="card-meta">
          <span>${t.categoryLabel||""}</span>
          · <span>${t.animal==="dog"?"🐕 Chien":t.animal==="cat"?"🐈 Chat":"🐾 Autre"}</span>
        </div>
      </div>
    </div>
    <div class="card-best">${j(t.bestPrice)} <small>à partir de</small></div>
    <div class="card-shops">
      ${i.map(l=>{const r=B(l.shop),c=l.price===t.bestPrice;return`<div class="shop-row">
          <span class="shop-dot" style="background:${(r==null?void 0:r.color)||"#999"}"></span>
          <span class="shop-name">${(r==null?void 0:r.name)||l.shop}</span>
          <span class="shop-price ${c?"best":""}">${j(l.price)}</span>
        </div>`}).join("")}
    </div>
    <div class="card-footer">
      ${n}
      <span class="card-more">${e>0?`+${e} autres prix →`:"Voir tous les prix →"}</span>
    </div>
  `,a.addEventListener("click",()=>s.navigate(`/product/${t.slug}`)),a}async function K(t){T();const s=document.getElementById("app");s.innerHTML="";const a=H(t);s.appendChild(a);const i=document.createElement("main");i.className="fade-in";const e=document.createElement("div");e.className="search-hero",e.innerHTML=`
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
  `,e.querySelectorAll("[data-nav]").forEach(d=>{d.addEventListener("click",m=>{m.preventDefault(),t.navigate(d.dataset.nav)})});const n=e.querySelector("#heroSearch");n==null||n.addEventListener("keydown",d=>{d.key==="Enter"&&n.value.trim()&&t.navigate(`/search/${encodeURIComponent(n.value.trim())}`)}),i.appendChild(e);const[o,p]=await Promise.all([R(),q({limit:6})]);if(!p||p.length===0){const d=(await D(async()=>{const{shops:m}=await Promise.resolve().then(()=>F);return{shops:m}},void 0)).shops;i.appendChild(O(d)),s.appendChild(i),s.appendChild(L());return}const l=document.createElement("div");l.className="container";const r=await I(o);l.appendChild(r);const c=document.createElement("div");c.className="section",c.innerHTML='<h2 class="section-title">Catégories populaires</h2>';const u=document.createElement("div");u.className="cat-grid",z.forEach(d=>{const m=document.createElement("div");m.className="cat-card",m.setAttribute("data-nav",`/category/${d.slug}`),m.innerHTML=`
      <span class="cat-emoji">${d.emoji}</span>
      <div class="cat-info">
        <div class="cat-name">${d.name}</div>
        <div class="cat-count">${d.count} produits</div>
      </div>
    `,m.addEventListener("click",()=>t.navigate(`/category/${d.slug}`)),u.appendChild(m)}),c.appendChild(u),l.appendChild(c);const v=document.createElement("div");v.className="section",v.innerHTML=`<h2 class="section-title">Produits à la une <span class="count">${p.length} produits</span></h2>`;const h=document.createElement("div");h.className="product-grid",p.forEach(d=>{const m=U(d,t);h.appendChild(m)}),v.appendChild(h),l.appendChild(v),l.appendChild(G(t)),i.appendChild(l),s.appendChild(i),s.appendChild(L())}async function se(t,s){var C,S,V;T();const a=document.getElementById("app");a.innerHTML="",a.appendChild(H(s));const i=document.createElement("main");i.className="fade-in";const e=document.createElement("div");e.className="container product-detail";const n=await ne(t);if(!n){e.innerHTML=`
      <a class="detail-back" data-nav="/">← Retour à l'accueil</a>
      <div class="empty-state">
        <span class="big-icon">😕</span>
        <p>Produit introuvable</p>
      </div>
    `,(C=e.querySelector("[data-nav]"))==null||C.addEventListener("click",f=>{f.preventDefault(),s.navigate("/")}),i.appendChild(e),a.appendChild(i),a.appendChild(L());return}e.appendChild(_([{label:"Accueil",nav:"/"},{label:n.categoryLabel||n.category||"Produit",nav:`/category/${n.category}`},{label:n.name}]));const o=[...n.prices||[]].sort((f,y)=>f.price-y.price),p=((S=o[0])==null?void 0:S.price)||0,l=((V=o[o.length-1])==null?void 0:V.price)||0,r=o.length>1?Math.round((l-p)/l*100):0,c=document.createElement("div");c.className="detail-header";const u=n.image?`<img class="detail-img" src="${n.image}" alt="${n.name}">`:`<span class="detail-emoji">${n.emoji||"🐾"}</span>`;if(c.innerHTML=`
    ${u}
    <div class="detail-info">
      <h1>${n.name}</h1>
      <div class="detail-tags">
        <span class="tag">${n.categoryLabel||n.category}</span>
        <span class="tag">${n.animal==="dog"?"🐕 Chien":n.animal==="cat"?"🐈 Chat":"🐾 Autre"}</span>
      </div>
      ${r>0?`<span class="detail-savings">📊 Économisez jusqu'à ${r}%</span>`:""}
    </div>
  `,e.appendChild(c),n.description){const f=document.createElement("div");f.className="detail-desc",f.textContent=n.description,e.appendChild(f)}const v=document.createElement("div");v.className="price-history",v.innerHTML="<h3>📈 Historique des prix</h3>";const h=document.createElement("div");h.id="historyChart",h.innerHTML='<div class="history-empty">Chargement...</div>',v.appendChild(h),e.appendChild(v);const d=document.createElement("h2");d.className="detail-prices-title",d.innerHTML=`Comparer les prix <span class="count">${o.length} offres</span>`,e.appendChild(d);const m=document.createElement("div");m.className="shop-filters";let w=new Set(o.map(f=>f.shop));o.forEach(f=>{const y=B(f.shop),g=document.createElement("button");g.className="shop-filter-btn active",g.dataset.shop=f.shop,g.innerHTML=`
      <span class="dot" style="background:${(y==null?void 0:y.color)||"#999"}"></span>
      ${(y==null?void 0:y.name)||f.shop}
    `,g.addEventListener("click",()=>{if(w.has(f.shop)){if(w.size<=1)return;w.delete(f.shop),g.classList.remove("active")}else w.add(f.shop),g.classList.add("active");P()}),m.appendChild(g)}),e.appendChild(m);const $=document.createElement("div");$.className="compare-table";function P(){const f=o.filter(g=>w.has(g.shop));if(f.length===0){$.innerHTML='<div class="empty-state" style="padding:2rem"><p>Aucune boutique sélectionnée</p></div>';return}const y=Math.min(...f.map(g=>g.price));$.innerHTML=f.map(g=>{const E=B(g.shop),W=g.price===y,Z=y>0?Math.round((g.price-y)/y*100):0,X=g.shipping===0||!g.shipping?'<span class="free">Gratuite</span>':j(g.shipping);return`
        <div class="compare-row ${W?"best-row":""}">
          <div class="cp-shop">
            <span class="cp-dot" style="background:${(E==null?void 0:E.color)||"#999"}"></span>
            <span class="cp-name">${(E==null?void 0:E.name)||g.shop}</span>
            ${W?'<span class="cp-badge">Meilleur prix</span>':""}
          </div>
          <div class="cp-price">
            <span class="amount">${j(g.price)}</span>
            ${Z>0?`<span class="diff">+${Z}%</span>`:""}
          </div>
          <div class="cp-shipping ${g.shipping?"":"free"}">${X}</div>
          <div class="cp-action">
            ${g.in_stock!==!1?`<a href="${g.url||(E==null?void 0:E.url)||"#"}" target="_blank" rel="noopener" class="btn-offer">Voir l'offre →</a>`:'<span class="stock-out">Rupture</span>'}
          </div>
        </div>
      `}).join("")}P(),e.appendChild($);const b=document.createElement("div");b.className="affil-notice",b.textContent="Les prix et disponibilités sont donnés à titre indicatif. Les liens vers les boutiques peuvent être des liens d'affiliation.",e.appendChild(b),i.appendChild(e),i.querySelectorAll("[data-nav]").forEach(f=>{f.dataset.nav&&f.addEventListener("click",y=>{y.preventDefault(),s.navigate(f.dataset.nav)})}),a.appendChild(i),a.appendChild(L()),ie(t,h)}async function ie(t,s){try{const a=await fetch("/data/price_history.json");if(!a.ok)throw new Error("not found");const i=await a.json(),e=Object.values(i).filter(r=>r.product_slug===t||r.product===t);if(e.length===0){s.innerHTML=`<div class="history-empty">Pas encore d'historique</div>`;return}const n=[];if(e.forEach(r=>{(r.history||[]).forEach(c=>{n.push({date:c.date,price:c.price,shop:r.shop})})}),n.length<2){s.innerHTML='<div class="history-empty">Pas assez de données pour un graphique</div>';return}n.sort((r,c)=>r.date.localeCompare(c.date));const o={};n.forEach(r=>{o[r.date]||(o[r.date]=[]),o[r.date].push(r.price)});const p=Object.keys(o).sort(),l=p.map(r=>{const c=o[r];return c.reduce((u,v)=>u+v,0)/c.length});oe(s,p,l)}catch{s.innerHTML='<div class="history-empty">Historique non disponible</div>'}}function oe(t,s,a){if(a.length<2){t.innerHTML='<div class="history-empty">Pas assez de données</div>';return}const i=600,e=120,n=20,o=Math.min(...a)*.95,p=Math.max(...a)*1.05,l=p-o||1,r=(i-n*2)/(a.length-1||1),c=d=>e-n-(d-o)/l*(e-n*2);let u=a.map((d,m)=>`${m===0?"M":"L"}${n+m*r},${c(d)}`).join(" "),v=`${u} L${n+(a.length-1)*r},${e-n} L${n},${e-n} Z`;const h=[0];a.length>2&&h.push(Math.floor(a.length/2)),a.length>1&&h.push(a.length-1),t.innerHTML=`
    <svg viewBox="0 0 ${i} ${e}" class="history-chart">
      <defs>
        <linearGradient id="h-gradient" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="var(--accent, #FF6B35)"/>
          <stop offset="100%" stop-color="var(--accent, #FF6B35)" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <path class="h-area" d="${v}"/>
      <path class="h-line" d="${u}"/>
      ${a.map((d,m)=>m===0||m===a.length-1?`<circle class="h-dot" cx="${n+m*r}" cy="${c(d)}" r="3"/>`:"").join("")}
      ${h.map(d=>`<text class="h-label" x="${n+d*r}" y="${e-4}">${s[d]}</text>`).join("")}
      <text class="h-label" x="4" y="${n+10}" text-anchor="start">${Q(p)}</text>
      <text class="h-label" x="4" y="${e-n-6}" text-anchor="start">${Q(o)}</text>
    </svg>
  `}function Q(t){return t.toFixed(2).replace(".",",")+"€"}async function re(t,s){T();const a=document.getElementById("app");a.innerHTML="",a.appendChild(H(s));const i=document.createElement("main");i.className="fade-in";const e=document.createElement("div");e.className="container search-page",e.appendChild(_([{label:"Accueil",nav:"/"},{label:`Recherche : "${t}"`}]));const n=document.createElement("div");n.className="search-header",n.innerHTML=`
    <h1>Résultats pour "<span id="searchQuery">${t}</span>"</h1>
    <div class="search-inline">
      <input type="text" id="refineSearch" value="${t}" placeholder="Affiner la recherche..." autocomplete="off">
      <button class="savings-cta" style="padding:0.5rem 1.2rem;border-radius:999px;background:var(--accent);color:var(--white);font-weight:600;font-size:0.9rem;white-space:nowrap">Chercher</button>
    </div>
  `;const o=n.querySelector("#refineSearch"),p=n.querySelector(".savings-cta");p==null||p.addEventListener("click",()=>{o!=null&&o.value.trim()&&s.navigate(`/search/${encodeURIComponent(o.value.trim())}`)}),o==null||o.addEventListener("keydown",r=>{r.key==="Enter"&&o.value.trim()&&s.navigate(`/search/${encodeURIComponent(o.value.trim())}`)}),e.appendChild(n);const l=await q({search:t});if(!l||l.length===0){const r=document.createElement("div");r.className="empty-state fade-in",r.innerHTML=`
      <span class="big-icon">🔍</span>
      <p>Aucun résultat pour "${t}"</p>
      <div class="search-suggestions" style="margin-top:1.5rem;justify-content:center">
        <button data-nav="/category/croquettes-chien">🍖 Croquettes chien</button>
        <button data-nav="/category/croquettes-chat">🐟 Croquettes chat</button>
        <button data-nav="/category/litiere">⬜ Litière</button>
        <button data-nav="/category/patees">🥫 Pâtées</button>
        <button data-nav="/category/accessoires-chien">🎾 Accessoires</button>
        <button data-nav="/animal/all">🐾 Tous les produits</button>
      </div>
    `,r.querySelectorAll("[data-nav]").forEach(c=>{c.addEventListener("click",u=>{u.preventDefault(),s.navigate(c.dataset.nav)})}),e.appendChild(r)}else{const r=document.createElement("div");r.className="controls-bar",r.innerHTML=`<span class="result-count">${l.length} produit${l.length>1?"s":""} trouvé${l.length>1?"s":""}</span>`,e.appendChild(r);const c=document.createElement("div");c.className="product-grid",l.forEach(u=>{c.appendChild(U(u,s))}),e.appendChild(c)}i.appendChild(e),a.appendChild(i),a.appendChild(L())}function N(t,s){const a=document.createElement("div");return a.className="product-grid",t.length===0?(a.innerHTML='<div class="empty-state"><span class="big-icon">🔍</span><p>Aucun produit trouvé</p></div>',a):(t.forEach(i=>{a.appendChild(U(i,s))}),a)}async function ce(t,s){T();const a=document.getElementById("app");a.innerHTML="",a.appendChild(H(s));const i=document.createElement("main");i.className="fade-in";const e=document.createElement("div");e.className="container",e.style.paddingTop="1.25rem";const n=z.find(d=>d.slug===t),o=(n==null?void 0:n.name)||t.replace(/-/g," "),p=(n==null?void 0:n.emoji)||"🐾";e.appendChild(_([{label:"Accueil",nav:"/"},{label:o}]));const l=await q({category:t});if(!l||l.length===0){i.appendChild(e);const d=(await D(async()=>{const{shops:m}=await Promise.resolve().then(()=>F);return{shops:m}},void 0)).shops;e.appendChild(O(d)),a.appendChild(i),a.appendChild(L());return}const r=document.createElement("h1");r.className="section-title",r.innerHTML=`${p} ${o} <span class="count">${l.length} produits</span>`,e.appendChild(r);let c="asc";const u=[...l].sort((d,m)=>d.bestPrice-m.bestPrice);function v(){var $;const d=e.querySelector(".controls-bar");d&&d.remove();const m=e.querySelector(".product-grid");m&&m.remove();const w=document.createElement("div");w.className="controls-bar",w.innerHTML=`
      <span class="result-count">${u.length} produits</span>
      <div class="sort-group">
        <label>Trier par</label>
        <select id="sortSelect">
          <option value="asc" ${c==="asc"?"selected":""}>Prix croissant</option>
          <option value="desc" ${c==="desc"?"selected":""}>Prix décroissant</option>
        </select>
      </div>
    `,($=w.querySelector("#sortSelect"))==null||$.addEventListener("change",P=>{c=P.target.value,c==="asc"?u.sort((C,S)=>C.bestPrice-S.bestPrice):u.sort((C,S)=>S.bestPrice-C.bestPrice);const b=e.querySelector(".product-grid");b&&b.remove(),e.appendChild(N(u,s))}),e.insertBefore(w,e.querySelector(".product-grid")||e.querySelector(".section")),e.appendChild(N(u,s))}v();const h=await R();h&&e.appendChild(await I(h)),e.appendChild(G(s)),i.appendChild(e),a.appendChild(i),a.appendChild(L())}async function le(t,s){T();const a=document.getElementById("app");a.innerHTML="",a.appendChild(H(s));const i=document.createElement("main");i.className="fade-in";const e=document.createElement("div");e.className="container",e.style.paddingTop="1.25rem";const o={dog:"🐕 Chiens",cat:"🐈 Chats",all:"🐾 Tous les animaux"}[t]||"🐾 Animaux";e.appendChild(_([{label:"Accueil",nav:"/"},{label:o}]));const p=await q({animal:t});if(!p||p.length===0){i.appendChild(e);const h=(await D(async()=>{const{shops:d}=await Promise.resolve().then(()=>F);return{shops:d}},void 0)).shops;e.appendChild(O(h)),a.appendChild(i),a.appendChild(L());return}const l=document.createElement("h1");l.className="section-title",l.innerHTML=`${o} <span class="count">${p.length} produits</span>`,e.appendChild(l);let r="asc";const c=[...p].sort((h,d)=>h.bestPrice-d.bestPrice);function u(){var w;const h=e.querySelector(".controls-bar");h&&h.remove();const d=e.querySelector(".product-grid");d&&d.remove();const m=document.createElement("div");m.className="controls-bar",m.innerHTML=`
      <span class="result-count">${c.length} produits</span>
      <div class="sort-group">
        <label>Trier par</label>
        <select id="sortSelectAnimal">
          <option value="asc" ${r==="asc"?"selected":""}>Prix croissant</option>
          <option value="desc" ${r==="desc"?"selected":""}>Prix décroissant</option>
        </select>
      </div>
    `,(w=m.querySelector("#sortSelectAnimal"))==null||w.addEventListener("change",$=>{r=$.target.value,r==="asc"?c.sort((b,C)=>b.bestPrice-C.bestPrice):c.sort((b,C)=>C.bestPrice-b.bestPrice);const P=e.querySelector(".product-grid");P&&P.remove(),e.appendChild(N(c,s))}),e.insertBefore(m,e.querySelector(".product-grid")||e.querySelector(".section")),e.appendChild(N(c,s))}u();const v=await R();v&&e.appendChild(await I(v)),e.appendChild(G(s)),i.appendChild(e),a.appendChild(i),a.appendChild(L())}const x=new ee([{path:"/",handler:()=>K(x)},{path:"/home",handler:()=>K(x)},{path:"/product/:slug",handler:t=>se(t.slug,x)},{path:"/search/:query",handler:t=>re(t.query,x)},{path:"/category/:slug",handler:t=>ce(t.slug,x)},{path:"/animal/:type",handler:t=>le(t.type,x)}]);document.addEventListener("DOMContentLoaded",()=>{x.resolve()});
