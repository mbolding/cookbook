const CACHE_NAME = 'cookbook-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/assets/css/style.css',
  '/assets/js/theme.js',
  '/assets/js/filter.js',
  '/assets/images/icon-512.svg',
  '/manifest.json'
];

// Dynamically cache all recipe pages
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Pre-cache core assets
      cache.addAll(ASSETS);
      
      // Fetch the recipe list from the directory or assume they follow the pattern
      // In a real build, we'd list them, but for now, we'll cache them as they're visited
      // or we can pre-cache some if we know them.
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request).then((response) => {
        // Cache new recipes as they are visited
        if (event.request.url.includes('/recipes/')) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      });
    }).catch(() => {
      // Fallback for offline if not in cache (e.g., return index.html)
      if (event.request.mode === 'navigate') {
        return caches.match('/index.html');
      }
    })
  );
});
