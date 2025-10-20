const CACHE_NAME = 'apartment-cache-v5';

// cache only the static stuff and key pages — no fetch() on install!
const urlsToCache = [
    '/',
    '/accounts/login/',
    '/accounts/apartments/',
    '/accounts/apartments/create/',
    '/static/js/db.js',
    '/static/js/main.js',
    '/static/css/style.css',
    '/static/icon-192x192.png',
    '/static/icon-512x512.png'
];

// ✅ INSTALL — just open cache and addAll safely
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 Caching core files...');
                return cache.addAll(urlsToCache);
            })
            .catch(err => console.error('Cache install failed:', err))
    );
    self.skipWaiting();
});

// ✅ ACTIVATE — clear old cache versions
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    console.log('Service Worker active ✅');
    return self.clients.claim();
});

// ✅ FETCH — network-first, then cache fallback
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // clone and cache a copy dynamically
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            })
            .catch(async () => {
                const cached = await caches.match(event.request);
                if (cached) return cached;

                // if HTML request and no cache found, try root fallback
                if (event.request.mode === 'navigate') {
                    return caches.match('/');
                }
            })
    );
});
