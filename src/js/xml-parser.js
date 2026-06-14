export class XmlFeedParser {
  constructor() {
    this.feeds = new Map();
    this.lastSync = new Map();
  }

  async parseXmlString(xml) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xml, 'text/xml');
    return doc;
  }

  async fetchFeed(url) {
    try {
      const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`;
      const response = await fetch(proxyUrl);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const xml = await response.text();
      return this.parseXmlString(xml);
    } catch (err) {
      console.warn(`Feed fetch failed for ${url}:`, err.message);
      return null;
    }
  }

  parseProductFeed(doc, shopId) {
    if (!doc) return [];
    const items = doc.querySelectorAll('item, product');
    const products = [];

    items.forEach(item => {
      const title = item.querySelector('title')?.textContent || '';
      const price = parseFloat(
        item.querySelector('price, g:price, sale_price')?.textContent?.replace('EUR', '').replace(',', '.').trim() || '0'
      );
      const url = item.querySelector('link')?.textContent || '';
      const image = item.querySelector('image, g:image_link')?.textContent || '';

      if (title && price > 0) {
        products.push({
          shop: shopId,
          title: title.trim(),
          price,
          url,
          image,
          inStock: true
        });
      }
    });

    return products;
  }

  getMockFeed(shopId) {
    const mockData = {
      zooplus: `
        <rss version="2.0">
          <channel>
            <item><title>Milbemax Chien</title><price>5.49 EUR</price><link>https://www.zooplus.fr/shop/chiens/vermifuges/milbemax/123456</link></item>
            <item><title>Frontline Combo Chat</title><price>9.40 EUR</price><link>https://www.zooplus.fr/shop/chats/antiparasitaires/frontline/234567</link></item>
            <item><title>Royal Canin Adult 10kg</title><price>42.90 EUR</price><link>https://www.zooplus.fr/shop/chiens/croquettes/royal-canin/345678</link></item>
          </channel>
        </rss>`,
      wanimo: `
        <rss version="2.0">
          <channel>
            <item><title>Milbemax Chien</title><price>6.20 EUR</price><link>https://www.wanimo.com/chiens/vermifuges/milbemax.html</link></item>
            <item><title>Frontline Combo Chat</title><price>8.90 EUR</price><link>https://www.wanimo.com/chats/antiparasitaires/frontline-combo.html</link></item>
          </channel>
        </rss>`
    };
    return mockData[shopId] || null;
  }

  async syncFeed(shopId) {
    const now = Date.now();
    const lastSync = this.lastSync.get(shopId) || 0;

    if (now - lastSync < 3600000) {
      return this.feeds.get(shopId);
    }

    const mockXml = this.getMockFeed(shopId);
    if (!mockXml) return [];

    const doc = await this.parseXmlString(mockXml);
    const products = this.parseProductFeed(doc, shopId);

    this.feeds.set(shopId, products);
    this.lastSync.set(shopId, now);

    return products;
  }
}

export const feedParser = new XmlFeedParser();