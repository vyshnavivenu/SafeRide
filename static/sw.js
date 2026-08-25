/**
 * SafeRide PWA Service Worker (v1.0.0)
 * Provides offline dead-zone fallback protection and caching for passenger emergency safety.
 */

const CACHE_NAME = 'saferide-pwa-v1';
const OFFLINE_URL = '/offline/';

const PRECACHE_ASSETS = [
  '/',
  '/offline/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/static/img/icon-192.svg',
  '/static/img/icon-512.svg',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap'
];

// Install Event: Pre-cache emergency assets and offline page
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline emergency assets');
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[ServiceWorker] Some pre-cache assets failed:', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate Event: Clean up outdated caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Event: Network-First for HTML navigations, Cache-First for static assets, with Offline Fallback
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests and API POSTs (e.g. SOS dispatch)
  if (event.request.method !== 'GET') {
    return;
  }

  const url = new URL(event.request.url);

  // HTML page navigation: Network-First with Offline Fallback
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          // Cache successful page navigations
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        })
        .catch(async () => {
          // Network failed (e.g. transit dead zone): Serve cached page or offline emergency page
          const cache = await caches.open(CACHE_NAME);
          const cachedResponse = await cache.match(event.request);
          if (cachedResponse) {
            return cachedResponse;
          }
          const offlineFallback = await cache.match(OFFLINE_URL);
          if (offlineFallback) {
            return offlineFallback;
          }
          return new Response(
            `<!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>SafeRide - Offline Dead Zone</title>
              <style>
                body { background: #090D16; color: #FFF; font-family: sans-serif; text-align: center; padding: 40px 20px; }
                .btn { display: inline-block; background: #DC2626; color: #FFF; padding: 14px 28px; border-radius: 50px; text-decoration: none; font-weight: bold; margin-top: 20px; }
              </style>
            </head>
            <body>
              <h1>⚠️ No Internet Connection</h1>
              <p>You have entered a network dead zone. Emergency hotlines remain active:</p>
              <p><a href="tel:112" class="btn">🚨 CALL POLICE (112)</a></p>
              <p><a href="tel:1091" class="btn" style="background:#F59E0B;color:#000;">📞 WOMEN HELPLINE (1091)</a></p>
            </body>
            </html>`,
            { headers: { 'Content-Type': 'text/html' } }
          );
        })
    );
    return;
  }

  // Static Assets (CSS, JS, Fonts, Images): Cache-First Strategy
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && event.request.url.startsWith('http')) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Silent fallback for non-critical assets
          return new Response('', { status: 408, statusText: 'Offline' });
        });
    })
  );
});
