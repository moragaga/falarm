const CACHE_NAME = 'ada-n1-static-__APP_VERSION__';

const STATIC_ASSETS = [
    '/manifest.webmanifest',
    '/assets/favicon.ico',
    '/assets/img/branding/logos/web-app-manifest-192x192.png',
    '/assets/img/branding/logos/web-app-manifest-512x512.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((error) => {
                console.warn('[WARN] Service worker precache failed:', error);
            })
    );

    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((cacheName) => cacheName !== CACHE_NAME)
                        .map((cacheName) => caches.delete(cacheName))
                );
            })
            .then(() => {
                return self.clients.claim();
            })
    );
});

self.addEventListener('fetch', (event) => {
    const request = event.request;

    if (request.method !== 'GET') {
        return;
    }

    const url = new URL(request.url);

    if (url.origin !== self.location.origin) {
        return;
    }

    if (request.headers.has('range')) {
        return;
    }

    if (
        url.pathname === '/' ||
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/_dash-') ||
        url.pathname.startsWith('/_dash-component-suites/') ||
        url.pathname.includes('_dash-update-component') ||
        url.pathname.startsWith('/apple-touch-icon')
    ) {
        return;
    }

    const isCacheableRequest = (
        url.pathname.startsWith('/assets/') ||
        url.pathname === '/manifest.webmanifest'
    );

    if (!isCacheableRequest) {
        return;
    }

    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }

                return fetch(request)
                    .then((networkResponse) => {
                        if (!networkResponse) {
                            return networkResponse;
                        }

                        if (!networkResponse.ok) {
                            return networkResponse;
                        }

                        if (networkResponse.status === 206) {
                            return networkResponse;
                        }

                        if (networkResponse.type !== 'basic') {
                            return networkResponse;
                        }

                        const responseToCache = networkResponse.clone();

                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                return cache.put(request, responseToCache);
                            })
                            .catch((error) => {
                                console.warn('[WARN] Service worker cache put failed:', error);
                            });

                        return networkResponse;
                    });
            })
            .catch((error) => {
                console.warn('[WARN] Service worker asset fetch failed:', error);

                return fetch(request)
                    .catch(() => {
                        return new Response('', {
                            status: 204,
                            statusText: 'Service Worker fallback'
                        });
                    });
            })
    );
});