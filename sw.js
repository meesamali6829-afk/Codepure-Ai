/* Whole AI service worker: keeps the app installable and opens fast.
   Home page: NETWORK FIRST, so every new deploy shows up right away.
   If the network is offline or slower than 3 seconds, the cached copy opens instead.
   Icons: served instantly from cache, refreshed in background.
   Everything else: network first. API and auth are never cached,
   so credits, plans and saved projects are never stale. */
const VERSION = 'whole-ai-v3';          // bumped: clears the old cached home page on every device
const HOME_TIMEOUT_MS = 3000;

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith('/api/')) return;
  if (url.pathname === '/sw.js') return;

  const isHome = req.mode === 'navigate' && url.pathname === '/';
  const isStaticAsset = /\.(png|jpg|jpeg|svg|ico|webp)$/i.test(url.pathname);

  // Home page: always try the network first (fresh deploy), fall back to cache when offline/slow
  if (isHome) {
    event.respondWith(
      caches.open(VERSION).then((cache) => {
        const network = fetch(req, { cache: 'no-cache' }).then((res) => {
          if (res && res.ok) cache.put('/', res.clone());
          return res;
        });
        const timeout = new Promise((resolve) => {
          setTimeout(() => cache.match('/').then((hit) => resolve(hit || null)), HOME_TIMEOUT_MS);
        });
        return Promise.race([network, timeout])
          .then((res) => res || network)
          .catch(() => cache.match('/').then((hit) => hit || Response.error()));
      })
    );
    return;
  }

  // Icons / images: instant from cache, refreshed in background
  if (isStaticAsset) {
    event.respondWith(
      caches.open(VERSION).then((cache) =>
        cache.match(req).then((hit) => {
          const refresh = fetch(req).then((res) => {
            if (res && res.ok) cache.put(req, res.clone());
            return res;
          }).catch(() => hit);
          return hit || refresh;
        })
      )
    );
    return;
  }

  // Everything else: network first
  event.respondWith(
    fetch(req).catch(() => caches.match(req).then((hit) => hit || caches.match('/')))
  );
});
