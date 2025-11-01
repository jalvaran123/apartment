// Service Worker for Apartment PWA
// Version 2.0 - Full offline support with sync

const CACHE_NAME = 'apartment-pwa-v2';
const STATIC_CACHE = 'apartment-static-v2';
const DYNAMIC_CACHE = 'apartment-dynamic-v2';
const API_CACHE = 'apartment-api-v2';

// Assets to cache on install (static assets - cache-first strategy)
const STATIC_ASSETS = [
    '/',
    '/login/',
    '/offline.html',
    '/static/manifest.json'
];

// Install event: Cache static assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing service worker...');
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => {
            console.log('[SW] Caching static assets');
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn('[SW] Some static assets failed to cache:', err);
            });
        }).then(() => {
            return self.skipWaiting(); // Activate immediately
        })
    );
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating service worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (
                        cacheName !== STATIC_CACHE &&
                        cacheName !== DYNAMIC_CACHE &&
                        cacheName !== API_CACHE &&
                        cacheName !== CACHE_NAME
                    ) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            return self.clients.claim(); // Take control of all pages
        })
    );
});

// Helper: Cache-first strategy (for static assets)
async function cacheFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    if (cached) {
        return cached;
    }
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/offline.html');
        }
        throw error;
    }
}

// Helper: Network-first strategy (for API calls)
async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        // Return from cache if network fails
        const cached = await cache.match(request);
        if (cached) {
            return cached;
        }
        throw error;
    }
}

// Helper: Stale-while-revalidate (for HTML pages)
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    
    const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => {
        // If network fails, return cached version
        return cached || caches.match('/offline.html');
    });
    
    return cached || fetchPromise;
}

// Fetch event: Route requests to appropriate strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip chrome-extension and other protocols
    if (!url.protocol.startsWith('http')) {
        return;
    }

    // Static assets (CSS, JS, images, fonts) - Cache First
    if (
        url.pathname.startsWith('/static/') ||
        url.pathname.includes('.css') ||
        url.pathname.includes('.js') ||
        url.pathname.includes('.png') ||
        url.pathname.includes('.jpg') ||
        url.pathname.includes('.jpeg') ||
        url.pathname.includes('.gif') ||
        url.pathname.includes('.svg') ||
        url.pathname.includes('.woff') ||
        url.pathname.includes('.woff2') ||
        url.pathname.includes('.ttf')
    ) {
        event.respondWith(cacheFirst(request, STATIC_CACHE));
        return;
    }

    // API endpoints - Network First
    if (
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/accounts/apartments/sync/') ||
        url.pathname.includes('/auth/')
    ) {
        event.respondWith(networkFirst(request, API_CACHE));
        return;
    }

    // HTML pages - Stale While Revalidate
    if (request.mode === 'navigate' || request.headers.get('accept').includes('text/html')) {
        event.respondWith(staleWhileRevalidate(request, DYNAMIC_CACHE));
        return;
    }

    // Default: Network First for everything else
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-offline-data') {
        event.waitUntil(syncOfflineData());
    }
});

// Sync offline data when connection is restored
async function syncOfflineData() {
    // This will be handled by the client-side code
    // Service worker sends message to clients to trigger sync
    const clients = await self.clients.matchAll();
    clients.forEach((client) => {
        client.postMessage({ type: 'SYNC_OFFLINE_DATA' });
    });
}

// Message handler for cache updates
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(DYNAMIC_CACHE).then((cache) => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});
