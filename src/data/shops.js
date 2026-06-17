export const shops = [
  { id: 'zooplus', name: 'Zooplus', url: 'https://www.zooplus.fr', logo: '🐾', color: '#2D9B6F', affiliate: true, network: 'awin' },
  { id: 'wanimo', name: 'Wanimo', url: 'https://www.wanimo.com', logo: '🐱', color: '#4A90D9', affiliate: true, network: 'netaffiliation' },
  { id: 'pepette', name: 'Pepette', url: 'https://www.pepette.fr', logo: '🐶', color: '#E86C8B', affiliate: true, network: 'awin' },
  { id: 'directvet', name: 'Direct-Vet', url: 'https://www.direct-vet.fr', logo: '💊', color: '#27AE60', affiliate: false, network: null },
  { id: 'cernunos', name: 'Cernunos', url: 'https://www.cernunos.fr', logo: '🌿', color: '#8E44AD', affiliate: false, network: null },
  { id: 'santevet', name: 'Santévet', url: 'https://www.santevet.com', logo: '❤️', color: '#3498DB', affiliate: false, network: null },
  { id: 'amazon', name: 'Amazon', url: 'https://www.amazon.fr', logo: '📦', color: '#FF9900', affiliate: true, network: 'amazon', trackingId: 'retux-21' },
  { id: 'ultrapremium', name: 'Ultra Premium Direct', url: 'https://www.ultrapremiumdirect.com', logo: '⭐', color: '#E74C3C', affiliate: false, network: null },
  { id: 'maxizoo', name: 'MaxiZoo', url: 'https://www.maxizoo.fr', logo: '🦁', color: '#9B59B6', affiliate: false, network: null },
  { id: 'zoomalia', name: 'Zoomalia', url: 'https://www.zoomalia.com', logo: '🦎', color: '#1ABC9C', affiliate: false, network: null },
  { id: 'animalis', name: 'Animalis', url: 'https://www.animalis.com', logo: '🐕', color: '#F39C12', affiliate: false, network: null },
  { id: 'jardiland', name: 'Jardiland', url: 'https://www.jardiland.com', logo: '🌻', color: '#27AE60', affiliate: false, network: null },
  { id: 'truffaut', name: 'Truffaut', url: 'https://www.truffaut.com', logo: '🌸', color: '#2ECC71', affiliate: false, network: null },
  { id: 'laferme', name: 'La Ferme des Animaux', url: 'https://www.lafermedesanimaux.com', logo: '🐓', color: '#E67E22', affiliate: false, network: null },
  { id: 'medor', name: 'Médor & Compagnie', url: 'https://www.medor-et-compagnie.fr', logo: '🦴', color: '#95A5A6', affiliate: false, network: null },
  { id: 'petsonic', name: 'Petsonic', url: 'https://www.petsonic.com', logo: '🐟', color: '#34495E', affiliate: false, network: null },
  { id: 'produitsveto', name: 'Produits-Véto', url: 'https://www.produits-veto.com', logo: '🏥', color: '#16A085', affiliate: false, network: null },
  { id: 'franceveto', name: 'France-Véto', url: 'https://www.france-veto.com', logo: '⚕️', color: '#2980B9', affiliate: false, network: null },
  { id: 'universveto', name: 'Univers-Véto', url: 'https://www.univers-veto.fr', logo: '🔬', color: '#8E44AD', affiliate: false, network: null },
];

export function getAffiliateUrl(shopId, url) {
  const shop = shops.find(s => s.id === shopId);
  if (!shop || !shop.affiliate || !url) return url || '#';

  if (shop.network === 'amazon' && shop.trackingId) {
    const separator = url.includes('?') ? '&' : '?';
    return url + separator + 'tag=' + shop.trackingId;
  }

  return url;
}
