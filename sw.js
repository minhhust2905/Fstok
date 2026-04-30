const CACHE_NAME = 'bfstock-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/assets/js/script.js',
  '/manifest.json',
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap'
];

// Cài đặt SW: Lưu trữ các tài nguyên cốt lõi
self.addEventListener('install', event => {
  self.skipWaiting(); // Ép kích hoạt SW mới ngay lập tức
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

// Kích hoạt SW: Xóa cache cũ nếu đổi CACHE_NAME
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
});

// Fetch: Chiến lược Stale-While-Revalidate
self.addEventListener('fetch', event => {
  // Không cache các request API (ví dụ calls proxy worker)
  if (event.request.url.includes('bfstock-proxy')) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(cache => {
      return cache.match(event.request).then(cachedResponse => {
        const fetchPromise = fetch(event.request).then(networkResponse => {
          // Lưu bản mới vào cache để dùng cho lần sau
          if (networkResponse && networkResponse.status === 200) {
            cache.put(event.request, networkResponse.clone());
          }
          return networkResponse;
        }).catch(() => {
          // Xử lý lỗi mất mạng tĩnh tại đây nếu cần
        });

        // Trả về cache ngay lập tức nếu có, đồng thời fetch ngầm bản mới
        return cachedResponse || fetchPromise;
      });
    })
  );
});
