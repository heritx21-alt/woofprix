export const animals = [
  { id: 'dog', label: 'Chien', emoji: '🐕' },
  { id: 'cat', label: 'Chat', emoji: '🐈' },
  { id: 'rodent', label: 'Rongeurs', emoji: '🐹' },
  { id: 'bird', label: 'Oiseaux', emoji: '🐦' },
  { id: 'fish', label: 'Poissons', emoji: '🐠' },
];

export const categories = [
  { id: 'food', label: 'Alimentation', emoji: '🍖' },
  { id: 'health', label: 'Soins & Santé', emoji: '💊' },
  { id: 'accessories', label: 'Accessoires', emoji: '🎒' },
];

export const subcategories = {
  food: [
    { id: 'croquettes', label: 'Croquettes' },
    { id: 'patees', label: 'Pâtées' },
    { id: 'friandises', label: 'Friandises' },
  ],
  health: [
    { id: 'anti-parasitaires', label: 'Anti-parasitaires' },
    { id: 'vermifuges', label: 'Vermifuges' },
    { id: 'compliments', label: 'Compléments' },
    { id: 'litiere', label: 'Litière' },
  ],
  accessories: [
    { id: 'jouets', label: 'Jouets' },
    { id: 'transport', label: 'Transport' },
    { id: 'gamelles', label: 'Gamelles' },
    { id: 'colliers', label: 'Colliers & Laisses' },
    { id: 'paniers', label: 'Paniers & Couchage' },
    { id: 'toilettage', label: 'Toilettage' },
    { id: 'cages', label: 'Cages & Volières' },
    { id: 'aquarium', label: 'Aquarium' },
  ],
};

export function getAnimal(id) {
  return animals.find(a => a.id === id);
}

export function getCategory(id) {
  return categories.find(c => c.id === id);
}

export function getSubcategory(id) {
  for (const catId of Object.keys(subcategories)) {
    const found = subcategories[catId].find(s => s.id === id);
    if (found) return found;
  }
  return null;
}
