# J.T.'s Table Collection — Project Notes

## Client
- **Business:** J.T.'s Table Collection
- **Owner:** Justin Taylor
- **Phone:** (256) 515-3017
- **Location:** Alabama
- **Hours:** Mon–Sat 8am–8pm
- **Delivery:** Up to 240 miles
- **Founded:** 2017
- **Built by:** Headley Web & SEO

## Stack
Plain HTML/CSS/JS — no framework, no build step.
- `index.html` — single-page site
- `css/style.css` — all styles (currently v=5)
- `js/main.js` — hamburger menu, scroll-aware nav, sticky mobile CTA, footer year, scroll animations, nav scroll spy, body scroll lock (currently v=6)

## Design Tokens (css/style.css :root)
- `--blue: #96a8ab` (J.T.'s signature steel blue)
- `--blue-dark: #434e52` (nav, footer, announcement bar)
- `--blue-light: #bac6c8`
- `--amber: #c4906a` / `--amber-dark: #a8723f` (CTAs, accents)
- `--cream: #f8f5ef` / `--cream-warm: #f0ebe0` (section backgrounds)
- Fonts: Playfair Display (headings), Inter (body) from Google Fonts
- Mobile breakpoint: 900px

## Page Sections (in order)
1. Header / Nav (sticky, transparent over hero on desktop)
2. Hero (full-bleed coffee table photo)
3. Trust Bar
4. Features (4-up grid)
5. Category Showcase (coffee tables, benches, custom projects)
6. Customization (stain/paint, tabletop pattern, leg style)
7. Gallery (masonry columns, 9 photos)
8. Testimonials (3 cards)
9. How It Works (4 steps)
10. About (split layout — photo left, text right)
11. Contact
12. Footer
13. Mobile Sticky CTA bar

## Image Folders
- `images/brand/` — logo (jts-table-collection-logo.webp), bio photo (justin-taylor-bio.webp + 480w)
- `images/gallery/coffee-tables/` — coffee table photos (webp + 480w/960w srcset variants)
- `images/gallery/benches/` — bench photos (webp + 480w srcset)
- `images/gallery/custom/` — custom projects (bunk beds, porch swing, headboard) + srcset
- `images/options/` — stain-paint-color-chart.webp, tabletop-styles-rectangle.webp, tabletop-styles-square.webp, leg-styles-diagram.webp, leg-style-*.webp

## Outstanding TODOs
- [ ] Replace `DOMAIN.com` placeholder in canonical URL, OG tags, and JSON-LD with real domain (not yet live)
- [ ] Fill in starting prices (`$XXX`) for coffee tables and benches in the category cards
- [ ] Replace 3 placeholder testimonials with real customer quotes (from Google/Facebook reviews or texts)
- [ ] Update About bio copy with J.T.'s own words when available
- [ ] Add `sameAs` social profile URLs to JSON-LD once J.T. has social accounts set up
- [ ] Create og-image.webp for Open Graph/Twitter card preview image

## CSS Cache Busting
Bump `?v=N` on stylesheet and script links whenever making CSS/JS changes:
- `css/style.css?v=3` → next change → `?v=4`
- `js/main.js?v=2` → next change → `?v=3`
