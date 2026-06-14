export const products = [
  {
    id: 'milbemax-chien',
    name: 'Milbemax Chien',
    slug: 'milbemax-chien',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'vermifuges',
    categoryLabel: 'Vermifuge',
    emoji: '💊',
    description: 'Comprimé vermifuge pour chiens contre les vers ronds et plats. Efficace contre les ascaris, ankylostomes, trichures et ténias.',
    image: 'https://img.zooplus.com/1',
    bestPrice: 5.49,
    savings: 42,
    prices: [
      { shop: 'zooplus', price: 5.49, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chiens/vermifuges/milbemax/123456', inStock: true },
      { shop: 'wanimo', price: 6.20, shipping: 3.90, url: 'https://www.wanimo.com/chiens/vermifuges/milbemax.html', inStock: true },
      { shop: 'veterinaire', price: 9.50, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'frontline-combo-chat',
    name: 'Frontline Combo Chat',
    slug: 'frontline-combo-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'antiparasitaires',
    categoryLabel: 'Antiparasitaire',
    emoji: '🐛',
    description: 'Solution antiparasitaire externe pour chats. Protège contre les puces, tiques et poux. Application spot-on facile.',
    image: 'https://img.zooplus.com/2',
    bestPrice: 8.90,
    savings: 38,
    prices: [
      { shop: 'wanimo', price: 8.90, shipping: 3.90, url: 'https://www.wanimo.com/chats/antiparasitaires/frontline-combo.html', inStock: true },
      { shop: 'zooplus', price: 9.40, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/antiparasitaires/frontline/234567', inStock: true },
      { shop: 'veterinaire', price: 14.30, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'royal-canin-adult-10kg',
    name: 'Royal Canin Adult 10kg',
    slug: 'royal-canin-adult-10kg',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'croquettes-chien',
    categoryLabel: 'Croquettes',
    emoji: '🍖',
    description: 'Croquettes pour chien adulte de taille moyenne. Riche en protéines et nutriments essentiels pour une alimentation équilibrée.',
    image: 'https://img.zooplus.com/3',
    bestPrice: 42.90,
    savings: 25,
    prices: [
      { shop: 'zooplus', price: 42.90, shipping: 0, url: 'https://www.zooplus.fr/shop/chiens/croquettes/royal-canin/345678', inStock: true },
      { shop: 'wanimo', price: 46.50, shipping: 3.90, url: 'https://www.wanimo.com/chiens/croquettes/royal-canin-adult.html', inStock: true },
      { shop: 'animigo', price: 57.00, shipping: 0, url: 'https://www.animigo.fr/chiens/croquettes/royal-canin.html', inStock: true }
    ]
  },
  {
    id: 'advocate-chat',
    name: 'Advocate Chat 0,4ml',
    slug: 'advocate-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'antiparasitaires',
    categoryLabel: 'Antiparasitaire',
    emoji: '🐛',
    description: 'Solution spot-on antiparasitaire pour chats. Protège contre les puces, acariens et vers pulmonaires.',
    image: 'https://img.zooplus.com/4',
    bestPrice: 12.90,
    savings: 35,
    prices: [
      { shop: 'zooplus', price: 12.90, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/antiparasitaires/advocate/456789', inStock: true },
      { shop: 'wanimo', price: 14.50, shipping: 3.90, url: 'https://www.wanimo.com/chats/antiparasitaires/advocate-chat.html', inStock: true },
      { shop: 'veterinaire', price: 19.90, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'hill-prescription-dog',
    name: "Hill's Prescription Diet 12kg",
    slug: 'hill-prescription-dog',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'croquettes-chien',
    categoryLabel: 'Croquettes',
    emoji: '🍖',
    description: "Alimentation diététique pour chiens. Formulée pour les troubles digestifs et allergies alimentaires.",
    image: 'https://img.zooplus.com/5',
    bestPrice: 68.50,
    savings: 18,
    prices: [
      { shop: 'zooplus', price: 68.50, shipping: 0, url: 'https://www.zooplus.fr/shop/chiens/croquettes/hills/567890', inStock: true },
      { shop: 'wanimo', price: 72.00, shipping: 3.90, url: 'https://www.wanimo.com/chiens/croquettes/hills-prescription.html', inStock: true },
      { shop: 'maxizoo', price: 79.90, shipping: 0, url: '#', inStock: false }
    ]
  },
  {
    id: 'purina-one-chat',
    name: 'Purina One Chat 1,5kg',
    slug: 'purina-one-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'croquettes-chat',
    categoryLabel: 'Croquettes',
    emoji: '🐟',
    description: 'Croquettes pour chat adulte. Riche en poulet et céréales complètes pour une alimentation saine et équilibrée.',
    image: 'https://img.zooplus.com/6',
    bestPrice: 12.99,
    savings: 22,
    prices: [
      { shop: 'zooplus', price: 12.99, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/croquettes/purina-one/678901', inStock: true },
      { shop: 'wanimo', price: 14.20, shipping: 3.90, url: 'https://www.wanimo.com/chats/croquettes/purina-one.html', inStock: true },
      { shop: 'animigo', price: 16.50, shipping: 0, url: 'https://www.animigo.fr/chats/croquettes/purina-one.html', inStock: true }
    ]
  },
  {
    id: 'drontal-chien',
    name: 'Drontal Chien',
    slug: 'drontal-chien',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'vermifuges',
    categoryLabel: 'Vermifuge',
    emoji: '💊',
    description: 'Comprimé vermifuge large spectre pour chiens. Efficace contre tous les vers digestifs.',
    image: 'https://img.zooplus.com/7',
    bestPrice: 7.90,
    savings: 30,
    prices: [
      { shop: 'zooplus', price: 7.90, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chiens/vermifuges/drontal/789012', inStock: true },
      { shop: 'wanimo', price: 8.80, shipping: 3.90, url: 'https://www.wanimo.com/chiens/vermifuges/drontal-chien.html', inStock: true },
      { shop: 'veterinaire', price: 11.30, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'frolic-chien',
    name: 'Frolic Chien 10kg',
    slug: 'frolic-chien',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'croquettes-chien',
    categoryLabel: 'Croquettes',
    emoji: '🍖',
    description: 'Croquettes complètes pour chien au bœuf. Riches en vitamines et minéraux.',
    image: 'https://img.zooplus.com/8',
    bestPrice: 24.99,
    savings: 15,
    prices: [
      { shop: 'zooplus', price: 24.99, shipping: 0, url: 'https://www.zooplus.fr/shop/chiens/croquettes/frolic/890123', inStock: true },
      { shop: 'wanimo', price: 27.50, shipping: 3.90, url: 'https://www.wanimo.com/chiens/croquettes/frolic.html', inStock: true },
      { shop: 'jardiland', price: 29.90, shipping: 0, url: '#', inStock: false }
    ]
  },
  {
    id: 'whiskas-chat',
    name: 'Whiskas Chat 1,4kg',
    slug: 'whiskas-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'croquettes-chat',
    categoryLabel: 'Croquettes',
    emoji: '🐟',
    description: 'Croquettes pour chat adulte au poulet et aux légumes.',
    image: 'https://img.zooplus.com/9',
    bestPrice: 10.50,
    savings: 20,
    prices: [
      { shop: 'zooplus', price: 10.50, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/croquettes/whiskas/901234', inStock: true },
      { shop: 'animigo', price: 11.99, shipping: 0, url: 'https://www.animigo.fr/chats/croquettes/whiskas.html', inStock: true },
      { shop: 'jardiland', price: 13.40, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'revolution-chat',
    name: 'Revolution Chat 3mg',
    slug: 'revolution-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'antiparasitaires',
    categoryLabel: 'Antiparasitaire',
    emoji: '🐛',
    description: 'Solution spot-on contre puces, tiques, acariens et vers du cœur pour chats.',
    image: 'https://img.zooplus.com/10',
    bestPrice: 15.90,
    savings: 28,
    prices: [
      { shop: 'wanimo', price: 15.90, shipping: 3.90, url: 'https://www.wanimo.com/chats/antiparasitaires/revolution-chat.html', inStock: true },
      { shop: 'zooplus', price: 17.40, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/antiparasitaires/revolution/012345', inStock: true },
      { shop: 'veterinaire', price: 22.10, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'milbemax-chat',
    name: 'Milbemax Chat',
    slug: 'milbemax-chat',
    animal: 'cat',
    animalLabel: 'Chat',
    category: 'vermifuges',
    categoryLabel: 'Vermifuge',
    emoji: '💊',
    description: 'Comprimé vermifuge pour chats contre les vers ronds et plats.',
    image: 'https://img.zooplus.com/11',
    bestPrice: 6.90,
    savings: 32,
    prices: [
      { shop: 'zooplus', price: 6.90, shipping: 4.99, url: 'https://www.zooplus.fr/shop/chats/vermifuges/milbemax/112233', inStock: true },
      { shop: 'wanimo', price: 7.50, shipping: 3.90, url: 'https://www.wanimo.com/chats/vermifuges/milbemax-chat.html', inStock: true },
      { shop: 'veterinaire', price: 10.10, shipping: 0, url: '#', inStock: true }
    ]
  },
  {
    id: 'applaws-chien',
    name: 'Applaws Chien 2kg',
    slug: 'applaws-chien',
    animal: 'dog',
    animalLabel: 'Chien',
    category: 'croquettes-chien',
    categoryLabel: 'Croquettes',
    emoji: '🍖',
    description: 'Croquettes naturelles pour chien, sans céréales, riches en poulet.',
    image: 'https://img.zooplus.com/12',
    bestPrice: 18.90,
    savings: 12,
    prices: [
      { shop: 'wanimo', price: 18.90, shipping: 3.90, url: 'https://www.wanimo.com/chiens/croquettes/applaws.html', inStock: true },
      { shop: 'zooplus', price: 19.50, shipping: 0, url: 'https://www.zooplus.fr/shop/chiens/croquettes/applaws/223344', inStock: true },
      { shop: 'animigo', price: 21.40, shipping: 0, url: '#', inStock: true }
    ]
  }
];

export function getProduct(slug) {
  return products.find(p => p.slug === slug);
}

export function searchProducts(query) {
  const q = query.toLowerCase().trim();
  if (!q) return products;
  return products.filter(p =>
    p.name.toLowerCase().includes(q) ||
    p.categoryLabel.toLowerCase().includes(q) ||
    p.animalLabel.toLowerCase().includes(q) ||
    p.description.toLowerCase().includes(q)
  );
}

export function getProductsByCategory(categorySlug) {
  return products.filter(p => p.category === categorySlug);
}

export function getProductsByAnimal(animal) {
  return products.filter(p => p.animal === animal);
}