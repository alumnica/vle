// Chrome's currently missing some useful cache methods,
// this polyfill adds them.
// importScripts('serviceworker-cache-polyfill.js');

// Here comes the install event!
// This only happens once, when the browser sees this
// version of the ServiceWorker for the first time.
self.addEventListener('install', function(event) {
  // We pass a promise to event.waitUntil to signal how
  // long install takes, and if it failed
  event.waitUntil(
    // We open a cache…
    caches.open('simple-sw-v1').then(function(cache) {
      // And add resources to it
      return cache.addAll([
        '/static/webapp/css/app.css',
         '/static/webapp/js/app.js',
         '/static/webapp/fonts/BryantPro-Bold.otf',
         '/static/webapp/fonts/BryantPro-Light.otf',
         '/static/webapp/fonts/BryantPro-Medium.otf',
         '/static/webapp/fonts/BryantPro-Regular.otf',
      ]);
    })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          // Return true if you want to remove this cache,
          // but remember that caches are shared across
          // the whole origin
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

// The fetch event happens for the page request with the
// ServiceWorker's scope, and any request made within that
// page
// self.addEventListener('fetch', function(event) {
//   // Calling event.respondWith means we're in charge
//   // of providing the response. We pass in a promise
//   // that resolves with a response object
//   event.respondWith(
//     // First we look for something in the caches that
//     // matches the request
//     caches.match(event.request).then(function(response) {
//       // If we get something, we return it, otherwise
//       // it's null, and we'll pass the request to
//       // fetch, which will use the network.
//       return response || fetch(event.request);
//     })
//   );
// });