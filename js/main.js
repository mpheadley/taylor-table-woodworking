/* ============================================================
   J.T.'s Table Collection — Main JS
   Hamburger menu, scroll-aware nav.
   No dependencies. No build step.
   ============================================================ */

var header = document.getElementById('site-header');

(function () {
  'use strict';

  const hamburger  = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');

  // ── Scroll-aware nav background (IntersectionObserver) ──────
  // Use IO instead of scroll events: no false triggers from mobile
  // address bar show/hide, no threshold math, no smooth-scroll glitches.

  var heroEl = document.querySelector('.hero');
  if (heroEl) {
    header.classList.add('over-hero');
    new IntersectionObserver(function (entries) {
      header.classList.toggle('scrolled', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(heroEl);
  } else {
    header.classList.add('scrolled');
  }

  // ── Hamburger / Mobile Menu ──────────────────────────────────

  var scrollY = 0;

  function setMenuOpen(open) {
    if (open) {
      // Pin fixed menu to the actual bottom of the header (accounts for
      // the announcement bar height when at the top of the page)
      mobileMenu.style.top = header.getBoundingClientRect().bottom + 'px';
      // iOS Safari: save position, fix body to prevent background scroll
      scrollY = window.scrollY;
      document.body.style.top = '-' + scrollY + 'px';
      document.body.style.position = 'fixed';
      document.body.style.width = '100%';
    } else {
      // Restore body and scroll position
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, scrollY);
    }
    mobileMenu.classList.toggle('open', open);
    hamburger.classList.toggle('open', open);
    header.classList.toggle('menu-open', open);
    hamburger.setAttribute('aria-expanded', open);
    mobileMenu.setAttribute('aria-hidden', !open);
  }

  hamburger.addEventListener('click', function () {
    setMenuOpen(!mobileMenu.classList.contains('open'));
  });

  mobileMenu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () { setMenuOpen(false); });
  });

})();

// ── Sticky mobile CTA ────────────────────────────────────────

(function () {
  const cta  = document.getElementById('mobile-cta');
  const hero = document.querySelector('.hero');
  if (!cta || !hero) return;

  function updateCta() {
    const heroBottom = hero.getBoundingClientRect().bottom;
    if (heroBottom < 0) {
      cta.classList.add('visible');
      cta.setAttribute('aria-hidden', 'false');
    } else {
      cta.classList.remove('visible');
      cta.setAttribute('aria-hidden', 'true');
    }
  }

  window.addEventListener('scroll', updateCta, { passive: true });
  updateCta();
})();

// Footer year
const yearEl = document.getElementById('footer-year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ── Active nav scroll spy ─────────────────────────────────────
(function () {
  var sections = ['features', 'categories', 'customize', 'gallery', 'how-it-works', 'about', 'contact']
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  var navLinks = document.querySelectorAll('.nav-link');

  function updateActiveNav() {
    var navH = header.getBoundingClientRect().height;
    var current = '';
    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top <= navH + 40) current = section.id;
    });
    navLinks.forEach(function (link) {
      var href = link.getAttribute('href').replace('#', '');
      link.classList.toggle('active', href === current);
    });
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();
})();

// ── Scroll-triggered animations ──────────────────────────────
(function () {
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
    observer.observe(el);
  });
})();
