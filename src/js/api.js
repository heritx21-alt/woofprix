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

export async function getAnimals() {
  const data = await loadAll();
  if (!data?.products) return [];
  const seen = new Set();
  return data.products.filter(p => {
    if (!p.animal || seen.has(p.animal)) return false;
    seen.add(p.animal);
    return true;
  }).map(p => ({ id: p.animal, label: p.animalLabel }));
}

export async function getFilterOptions() {
  const data = await loadAll();
  if (!data?.products) return { animals: [], categories: [], subcategories: [] };
  const animals = new Set();
  const cats = new Set();
  const subs = new Set();
  for (const p of data.products) {
    if (p.animal) animals.add(JSON.stringify({ id: p.animal, label: p.animalLabel }));
    if (p.category) cats.add(JSON.stringify({ id: p.category, label: p.categoryLabel }));
    if (p.subcategory) subs.add(JSON.stringify({ id: p.subcategory, label: p.subcategoryLabel }));
  }
  return {
    animals: [...animals].map(JSON.parse).sort((a, b) => a.label?.localeCompare(b.label)),
    categories: [...cats].map(JSON.parse).sort((a, b) => a.label?.localeCompare(b.label)),
    subcategories: [...subs].map(JSON.parse).sort((a, b) => a.label?.localeCompare(b.label)),
  };
}

export async function getStats() {
  const data = await loadAll();
  return data?.stats || null;
}

export async function listProducts({ category, subcategory, animal, search, shop, limit, offset } = {}) {
  const data = await loadAll();
  if (!data) return [];

  let results = data.products;

  if (animal) results = results.filter(p => String(p.animal).toLowerCase() === animal.toLowerCase());
  if (category) results = results.filter(p => String(p.category).toLowerCase() === category.toLowerCase());
  if (subcategory) results = results.filter(p => String(p.subcategory).toLowerCase() === subcategory.toLowerCase());
  if (shop) results = results.filter(p => (p.prices || []).some(pr => pr.shop === shop));
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(p =>
      (p.name || '').toLowerCase().includes(q) ||
      (p.brand || '').toLowerCase().includes(q) ||
      (p.categoryLabel || '').toLowerCase().includes(q) ||
      (p.subcategoryLabel || '').toLowerCase().includes(q) ||
      (p.animalLabel || '').toLowerCase().includes(q) ||
      (p.description || '').toLowerCase().includes(q)
    );
  }

  const ANIMAL_EMOJI = { dog: '🐕', cat: '🐈', rodent: '🐹', bird: '🐦', fish: '🐠', other: '🐾' };

  const withMeta = results.map(p => {
    const sortedPrices = [...(p.prices || [])].sort((a, b) => a.price - b.price);
    const best = sortedPrices[0];
    const worst = sortedPrices[sortedPrices.length - 1];
    const savings = sortedPrices.length > 1
      ? Math.round((worst.price - best.price) / worst.price * 100)
      : 0;

    // Normalize for both old and new format
    const animal = p.animal || 'other';
    const animalLabel = p.animalLabel || (animal === 'dog' ? 'Chien' : animal === 'cat' ? 'Chat' : 'Autre');
    const subcategory = p.subcategory || '';
    const subcategoryLabel = p.subcategoryLabel || '';
    const categoryLabel = p.categoryLabel || p.category || '';

    return {
      ...p,
      animal,
      animalLabel,
      subcategory,
      subcategoryLabel,
      categoryLabel,
      prices: sortedPrices,
      bestPrice: best?.price,
      savings
    };
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
