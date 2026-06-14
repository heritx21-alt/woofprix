/**
 * API client WoofPrix.
 * Lit les données depuis /data/products.json, généré chaque nuit par les scrapers.
 * Ne jette jamais d'erreur : retourne des valeurs par défaut si le fichier
 * est manquant, vide, ou en cours de génération.
 */

let cache = null;
let fetchFailed = false;

async function loadAll() {
  if (cache) return cache;
  if (fetchFailed) return null;

  try {
    const res = await fetch('/data/products.json');
    if (!res.ok) {
      console.warn(`API: products.json introuvable (HTTP ${res.status})`);
      fetchFailed = true;
      return null;
    }
    const data = await res.json();
    if (!data || !Array.isArray(data.products)) {
      console.warn('API: products.json vide ou invalide');
      fetchFailed = true;
      return null;
    }
    cache = data;
    return cache;
  } catch (err) {
    console.warn('API: impossible de charger products.json —', err.message);
    fetchFailed = true;
    return null;
  }
}

export function invalidateCache() {
  cache = null;
  fetchFailed = false;
}

export async function getShops() {
  const data = await loadAll();
  return data?.shops || [];
}

export async function getCategories() {
  const data = await loadAll();
  return data?.categories || [];
}

export async function getStats() {
  const data = await loadAll();
  return data?.stats || null;
}

export async function listProducts({ category, animal, search, limit, offset } = {}) {
  const data = await loadAll();
  if (!data) return [];

  let results = data.products;

  if (category) results = results.filter(p => p.category === category);
  if (animal) results = results.filter(p => p.animal === animal);
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(p =>
      p.name.toLowerCase().includes(q) ||
      (p.categoryLabel || '').toLowerCase().includes(q) ||
      (p.animalLabel || '').toLowerCase().includes(q) ||
      (p.description || '').toLowerCase().includes(q)
    );
  }

  const withMeta = results.map(p => {
    const sortedPrices = [...(p.prices || [])].sort((a, b) => a.price - b.price);
    const best = sortedPrices[0];
    const worst = sortedPrices[sortedPrices.length - 1];
    const savings = sortedPrices.length > 1
      ? Math.round((worst.price - best.price) / worst.price * 100)
      : 0;
    return { ...p, prices: sortedPrices, bestPrice: best?.price, savings };
  });

  const start = offset || 0;
  const end = start + (limit || withMeta.length);
  return withMeta.slice(start, end);
}

export async function getProduct(slug) {
  const products = await listProducts();
  return products.find(p => p.slug === slug) || null;
}

/** True si les données sont indisponibles (premier déploiement, JSON pas encore généré) */
export async function isDataAvailable() {
  const data = await loadAll();
  return data !== null && data.products?.length > 0;
}
