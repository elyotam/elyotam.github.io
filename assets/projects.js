/* Category filter for the projects grid. Progressive: without JS every card
   simply stays visible, which is the correct fallback for a portfolio. */
(function () {
  var bar = document.querySelector('.filters');
  var grid = document.getElementById('works');
  if (!bar || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.work'));
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function apply(cat) {
    cards.forEach(function (c) {
      var show = cat === 'all' || c.dataset.cat === cat;
      c.hidden = !show;
      if (show && !reduce) {
        // re-run the entrance so a filtered view does not appear pre-loaded
        c.classList.remove('in');
        requestAnimationFrame(function () { c.classList.add('in'); });
      }
    });
  }

  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-f]');
    if (!btn) return;
    bar.querySelectorAll('button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b === btn));
    });
    apply(btn.dataset.f);
    history.replaceState(null, '', btn.dataset.f === 'all' ? location.pathname
                                                           : '#' + btn.dataset.f);
  });

  // deep link: /projects.html#infra opens straight into that category
  var hash = (location.hash || '').replace('#', '');
  var initial = bar.querySelector('button[data-f="' + hash + '"]');
  if (initial) { initial.click(); }
})();
