/* Towards Intelligence — shared page behaviour: theme switch, mobile menu, scroll reveal,
   active section tracking (nav links + page dots), and hash jumps on load. */
(function () {
  var root = document.documentElement;
  var KEY = 'ti-theme';

  /* ---------- Theme switch ---------- */
  var btn = document.getElementById('themeToggle');
  function sync() {
    if (btn) btn.setAttribute('aria-checked', root.getAttribute('data-theme') === 'dark' ? 'true' : 'false');
  }
  sync();
  if (btn) btn.addEventListener('click', function () {
    var n = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n);
    try { localStorage.setItem(KEY, n); } catch (e) {}
    sync();
  });
  /* Follow system changes until the user picks a theme explicitly */
  if (window.matchMedia) {
    var mq = matchMedia('(prefers-color-scheme: dark)');
    var onChange = function (e) {
      var saved; try { saved = localStorage.getItem(KEY); } catch (err) {}
      if (!saved) { root.setAttribute('data-theme', e.matches ? 'dark' : 'light'); sync(); }
    };
    mq.addEventListener ? mq.addEventListener('change', onChange) : mq.addListener(onChange);
  }

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector('.nav-hamburger');
  var menu = document.querySelector('.mobile-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('open');
      menu.classList.toggle('open');
      document.body.style.overflow = menu.classList.contains('open') ? 'hidden' : '';
    });
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        burger.classList.remove('open');
        menu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ---------- Scroll reveal ---------- */
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Active section: nav links + page dots ---------- */
  var sections = document.querySelectorAll('[data-track]');
  if (sections.length) {
    var dots = document.querySelectorAll('.page-dot');
    var navLinks = document.querySelectorAll('.nav .links a');
    var update = function () {
      var current = '';
      sections.forEach(function (s) {
        if (s.getBoundingClientRect().top <= window.innerHeight * 0.4) current = s.id;
      });
      if (!current) return;
      dots.forEach(function (d) { d.classList.toggle('active', d.dataset.section === current); });
      navLinks.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + current); });
    };
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ---------- Hash jump once layout settles (e.g. ../index.html#data-intelligence) ---------- */
  if (location.hash) {
    history.scrollRestoration = 'manual';
    window.addEventListener('load', function () {
      setTimeout(function () {
        var t = document.getElementById(location.hash.slice(1));
        if (t) t.scrollIntoView({ behavior: 'instant', block: 'start' });
      }, 0);
    });
  }
})();
