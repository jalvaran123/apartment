const CACHE_NAME = 'apartment-cache-v1';
const OFFLINE_URL = '/offline.html';

// Update with your actual asset paths
const ASSETS_TO_CACHE = [
    '/',
    '/offline.html',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/icon-192x192.png',
    '/static/icon-512x512.png',
    '/static/manifest.json'
];

// Install event: cache core assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate event: clear old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event: serve from cache, fallback to network, then offline page
self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request)
                .then(networkResponse => {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                })
                .catch(() => caches.match(OFFLINE_URL));
        })
    );
});
