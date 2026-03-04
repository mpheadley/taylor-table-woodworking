/* ============================================================
   J.T.'s Table Collection — Main JS
   Hamburger menu, scroll-aware nav.
   No dependencies. No build step.
   ============================================================ */

(function () {
  'use strict';

  const header     = document.getElementById('site-header');
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

  function setMenuOpen(open) {
    if (open) {
      // Pin fixed menu to the actual bottom of the header (accounts for
      // the announcement bar height when at the top of the page)
      mobileMenu.style.top = header.getBoundingClientRect().bottom + 'px';
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
