/* Whole AI service worker: keeps the app installable and opens fast.
   Home page + icons: served instantly from cache, refreshed in background.
   Everything else: network first. API and auth are never cached,
   so credits, plans and saved projects are never stale. */
const VERSION = 'whole-ai-v2';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith('/api/')) return;

  const isHome = req.mode === 'navigate' && url.pathname === '/';
  const isStaticAsset = /\.(png|jpg|jpeg|svg|ico|webp)$/i.test(url.pathname);

  if (isHome || isStaticAsset) {
    event.respondWith(
      caches.open(VERSION).then((cache) =>
        cache.match(isHome ? '/' : req).then((hit) => {
          const refresh = fetch(req).then((res) => {
            if (res && res.ok) cache.put(isHome ? '/' : req, res.clone());
            return res;
          }).catch(() => hit);
          return hit || refresh;
        })
      )
    );
    return;
  }

  event.respondWith(
    fetch(req).catch(() => caches.match(req).then((hit) => hit || caches.match('/')))
  );
});
