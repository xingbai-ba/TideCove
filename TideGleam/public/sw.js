// TideCove Service Worker 鈥斺€?璁?PWA 鍙畨瑁?+ 鏂綉鏃惰繕鑳芥墦寮€澹?const CACHE = 'tidecove-v1308';
const SHELL = ['/', '/index.html', '/manifest.json', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL).catch(() => {})).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // API 鍜屼笂浼犳枃浠朵竴寰嬭蛋缃戠粶锛屼笉缂撳瓨
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/uploads/')) return;
  // 鍙鐞嗗悓婧?  if (url.origin !== location.origin) return;

  e.respondWith(
    fetch(req)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(req).then((hit) => hit || caches.match('/index.html')))
  );
});
