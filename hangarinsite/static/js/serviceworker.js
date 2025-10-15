const CACHE_NAME = 'hangarin-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/styles.min.css',
  '/static/css/styles.css',
  '/static/js/app.min.js',
  '/static/js/sidebarmenu.js',
  '/static/libs/jquery/dist/jquery.min.js',
  '/static/libs/bootstrap/dist/js/bootstrap.bundle.min.js',
  '/static/libs/simplebar/dist/simplebar.js',
  '/static/images/logos/hangarin.png',
  '/static/images/logos/hangarin-logo.svg',
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});