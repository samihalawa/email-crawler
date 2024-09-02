#!/bin/bash

# Create directories if they don't exist
mkdir -p static/js
mkdir -p static/icons
mkdir -p templates

# Create service worker file
cat <<EOF > static/js/service-worker.js
const CACHE_NAME = 'offline-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
  // Add more URLs to cache as needed
];

// Install service worker and cache resources
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

// Activate the service worker and remove old caches
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
          cacheNames.map(cacheName => {
             if (!cacheWhitelist.includes(cacheName)) {
                return caches.delete(cacheName);
             }
          })
      );
    })
  );
});

// Fetch resources from cache or network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
EOF

# Create manifest file
cat <<EOF > static/manifest.json
{
  "name": "AutoClient AI",
  "short_name": "AutoClient",
  "description": "Find and engage potential clients with personalized, AI-generated emails.",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
EOF

# Download example icons (replace these with actual icons)
curl -o static/icons/icon-192x192.png https://via.placeholder.com/192
curl -o static/icons/icon-512x512.png https://via.placeholder.com/512

# Add routes in Flask app.py
cat <<EOF >> app.py

from flask import send_from_directory

@app.route('/service-worker.js')
def service_worker():
  return send_from_directory('static/js', 'service-worker.js')

@app.route('/manifest.json')
def manifest():
  return send_from_directory('static', 'manifest.json')
EOF

# Update templates to include the manifest and service worker
find templates -name "*.html" -print0 | xargs -0 sed -i '/<\/head>/i \    <link rel="manifest" href="/manifest.json">\n    <script>\n      if ("serviceWorker" in navigator) {\n        window.addEventListener("load", function() {\n          navigator.serviceWorker.register("/service-worker.js")\n            .then(reg => console.log("Service Worker registered with scope:", reg.scope))\n            .catch(err => console.error("Service Worker registration failed:", err));\n        });\n      }\n    </script>\n'

echo "PWA setup is complete."