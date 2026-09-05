/* A ring of coloured particles that orbits the pointer.
   Canvas based, pointer-events:none, and it never touches the native cursor.
   Skipped entirely on touch devices and when reduced motion is requested. */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches) return;

  const COUNT = 170;
  const RADIUS = 88;          // resting radius of the ring
  const JITTER = 9;           // per-particle wobble around that radius
  const EASE = 0.14;          // how quickly the ring catches the pointer
  const PALETTE = [
    '#ff3b30', '#ff9500', '#ffcc00', '#34c759', '#00c7be',
    '#30b0c7', '#007aff', '#5856d6', '#af52de', '#ff2d55', '#ffffff'
  ];

  const cv = document.createElement('canvas');
  cv.setAttribute('aria-hidden', 'true');
  cv.style.cssText =
    'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9999';
  document.body.appendChild(cv);
  const ctx = cv.getContext('2d');

  let w = 0, h = 0, dpr = Math.min(devicePixelRatio || 1, 2);
  function size() {
    w = innerWidth; h = innerHeight;
    cv.width = w * dpr; cv.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  size();
  addEventListener('resize', size, { passive: true });

  const parts = Array.from({ length: COUNT }, (_, i) => ({
    a: (i / COUNT) * Math.PI * 2,                 // angle on the ring
    v: (0.0016 + Math.random() * 0.0075) * (Math.random() < .5 ? -1 : 1),
    r: RADIUS + (Math.random() - .5) * JITTER * 2,
    ph: Math.random() * Math.PI * 2,              // wobble phase
    sz: Math.random() < .18 ? 1.9 : 1.1,
    c: PALETTE[(Math.random() * PALETTE.length) | 0]
  }));

  // Park the ring off screen until the pointer actually moves.
  let tx = -400, ty = -400, cx = -400, cy = -400, seen = false;
  addEventListener('pointermove', e => {
    tx = e.clientX; ty = e.clientY;
    if (!seen) { cx = tx; cy = ty; seen = true; }
  }, { passive: true });
  addEventListener('pointerleave', () => { tx = -400; ty = -400; }, { passive: true });

  let t = 0;
  (function frame() {
    requestAnimationFrame(frame);
    t += 0.016;
    cx += (tx - cx) * EASE;
    cy += (ty - cy) * EASE;

    ctx.clearRect(0, 0, w, h);
    if (!seen) return;

    for (let i = 0; i < parts.length; i++) {
      const p = parts[i];
      p.a += p.v;
      const r = p.r + Math.sin(t * 1.7 + p.ph) * 3.5;
      const x = cx + Math.cos(p.a) * r;
      const y = cy + Math.sin(p.a) * r;
      ctx.fillStyle = p.c;
      ctx.globalAlpha = 0.55 + Math.sin(t * 2.1 + p.ph) * 0.35;
      ctx.fillRect(x, y, p.sz, p.sz);
    }
    ctx.globalAlpha = 1;
  })();
})();
