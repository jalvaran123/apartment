const CACHE_NAME = 'apartment-cache-v7';

const urlsToCache = [
    '/',
    '/accounts/login/',
    '/accounts/apartments/',
    '/static/js/db.js',
    '/static/js/main.js',
    '/static/css/style.css',
    '/static/icon-192x192.png',
    '/static/icon-512x512.png',
    '/offline.html'
];

// ✅ INSTALL
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('📦 Caching files...');
            return cache.addAll(urlsToCache);
        })
    );
    self.skipWaiting();
});

// ✅ ACTIVATE
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    return self.clients.claim();
});

// ✅ FETCH — Network first, Cache fallback + Full offline fallback
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            })
            .catch(async () => {
                const cached = await caches.match(event.request);
                if (cached) return cached;

                if (event.request.mode === 'navigate') {
                    return caches.match('/offline.html');
                }
            })
    );
});
