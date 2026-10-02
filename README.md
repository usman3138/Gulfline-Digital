# Gulfline Digital

Website for Gulfline Digital — websites built for tutors, trainers, and freelancers across the UAE.

**Live site:** [gulflinedigital.com](https://gulflinedigital.com)

## About

Gulfline Digital offers fast, affordable, custom-coded websites (no templates) for solo professionals — tutors, trainers, coaches, and freelancers — who need a credible online presence without agency overhead.

- Custom-designed, up to 5 pages
- Mobile-first, fast-loading
- WhatsApp click-to-chat built in
- Basic on-page SEO
- Delivered in 7 business days
- Bilingual: English / Arabic (with RTL support)

## Tech Stack

Static site — no build step, no dependencies.

- HTML5 / CSS3 / vanilla JavaScript, each page is one self-contained file
- Fonts: Space Grotesk, Inter, Noto Kufi Arabic (Google Fonts)
- No frameworks, no bundler — deploys as-is

## Project Structure

There is no `src/` folder: the site is served straight from the repo root, so files are URLs and must not be moved.

```
index.html              → home page (English + Arabic toggle)
about.html, services.html, contact.html, privacy.html, terms.html
checkout.html           → order form, pays through PayPal
account.html            → sign-in page (Supabase, not switched on yet)
ar/                     → Arabic-first copies of the main pages
blog/                   → 10 articles, index.html and rss.xml
images/                 → photos (WebP)
auth-nav.js             → shows "Sign out" in the menu when signed in
supabase-config.js      → Supabase project URL and public key (placeholders)
construction-banner.js  → dismissible notice banner
sitemap.xml, robots.txt, ads.txt, og-image.png
docs/                   → architecture, decisions, setup notes
tests/                  → manual check list
```

## Deployment

Hosted on Hostinger. Deployment is connected via Git — pushing to `main` auto-deploys to production within seconds.

```bash
git add .
git commit -m "your change description"
git push origin main
```

## Local Development

No build tools required. Open `index.html` in a browser, or run `npx serve .` so links between pages work.

## Docs

- `docs/architecture.md` — how the pages fit together
- `docs/decisions.md` — decisions made and why
- `docs/setup.md` — hosting, PayPal, Supabase, AdSense
- `tests/README.md` — what to check before and after a push
- `CHANGELOG.md` — one line per change
- `CLAUDE.md` — working rules for Claude

## Contact

- WhatsApp: +971 56 881 4848
- Website: [gulflinedigital.com](https://gulflinedigital.com)

---
© Gulfline Digital. All rights reserved.
