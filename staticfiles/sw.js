const CACHE_NAME = 'apartment-app-v1';
const urlsToCache = [
    '/accounts/login/',
    '/static/manifest.json',
    '/static/icon-192x192.png',
    '/static/icon-512x512.png',
    '/static/style.css'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});