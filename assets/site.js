/* Shared behaviour for every page: nav, reveals, cursor spotlight. */
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    nav.addEventListener('click', e => {
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  const boxes = document.querySelectorAll('.reveal');
  if (reduce) {
    boxes.forEach(b => b.classList.add('in'));
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: .08 });
    boxes.forEach((b, i) => {
      b.style.transitionDelay = Math.min(i * 50, 400) + 'ms';
      io.observe(b);
    });
  }

  // decorative only, so it is created here rather than repeated in every page
  document.body.insertAdjacentHTML('beforeend', '<div class="grain" aria-hidden="true"></div>');

  if (!reduce && matchMedia('(hover:hover)').matches) {
    document.querySelectorAll('.box').forEach(b => {
      b.addEventListener('pointermove', e => {
        const r = b.getBoundingClientRect();
        b.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        b.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }
})();
