export class Router {
  constructor(routes) {
    this.routes = routes;
    this.currentRoute = null;
    this._resolve = null;
    window.addEventListener('hashchange', () => this.resolve());
  }

  navigate(path) {
    window.location.hash = path;
  }

  async resolve() {
    const hash = window.location.hash.slice(1) || '/';

    let matched = false;
    for (const route of this.routes) {
      const paramMatch = route.path.match(/:(\w+)/g);
      if (paramMatch) {
        const pattern = route.path.replace(/:\w+/g, '([^/]+)');
        const regex = new RegExp(`^${pattern}$`);
        const match = hash.match(regex);
        if (match) {
          const params = {};
          paramMatch.forEach((param, i) => {
            params[param.slice(1)] = decodeURIComponent(match[i + 1]);
          });
          if (this.currentRoute !== hash) {
            this.currentRoute = hash;
            await route.handler(params);
          }
          matched = true;
          break;
        }
      } else if (route.path === hash) {
        if (this.currentRoute !== hash) {
          this.currentRoute = hash;
          await route.handler({});
        }
        matched = true;
        break;
      }
    }

    if (!matched) {
      this.routes[0].handler({});
    }
  }

  init() {
    this.resolve();
  }
}
