const CACHE_NAME = 'apartment-cache-v6';

const urlsToCache = [
    '/',
    '/accounts/login/',
    '/accounts/apartments/',
    '/static/js/db.js',
    '/static/js/main.js',
    '/static/css/style.css',
    '/static/icon-192x192.png',
    '/static/icon-512x512.png'
];

// ✅ INSTALL — safely cache files
self.addEventListener('install', event => {
    event.waitUntil(
        (async () => {
            const cache = await caches.open(CACHE_NAME);
            console.log('📦 Caching core files...');
            const results = await Promise.allSettled(
                urlsToCache.map(url => cache.add(url))
            );
            const failed = results.filter(r => r.status === 'rejected');
            if (failed.length > 0) {
                console.warn('⚠️ Some files failed to cache:', failed.map(f => f.reason?.url || 'unknown'));
            }
            console.log('✅ Cache install completed');
        })().catch(err => console.error('Cache install failed:', err))
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
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            })
            .catch(async () => {
                const cached = await caches.match(event.request);
                if (cached) return cached;
                if (event.request.mode === 'navigate') {
                    return caches.match('/');
                }
            })
    );
});
