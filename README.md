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
blog/                   → published articles, index.html and rss.xml
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

## Documentation standard

Read [AGENTS.md](AGENTS.md), [MEMORY.md](MEMORY.md) and [current status](docs/PROJECT_STATUS.md) before work. The [documentation index](docs/DOCUMENTATION_INDEX.md) maps every applicable shared documentation role to its existing or newly added document. The [project guide](docs/PROJECT_GUIDE.md) records scope, pending work and documentation adoption; historical records remain in place.

## Scheduled articles

Thirteen English/Arabic articles are staged in `docs/scheduled/` for Monday/Wednesday/Friday dates from 6 November to 4 December 2026. They are not published yet. The [publisher guide and schedule](docs/scheduled/README.md) explains the manifest, Dubai day limit, retries, review and recovery. The workflow will publish only after the manager pushes this change and GitHub Actions runs successfully; pushes to main publish the website automatically.

Run `node tests/check-site.mjs`, `node tests/check-scheduled.mjs` and `python tests/scheduled-publisher.test.py` before review. Python 3.10+ and Node.js are sufficient; there is no application build. Do not run the publisher in the checkout to preview future articles: its `TODAY` override writes publication files. Use a disposable copy for previews.

The same bilingual “Our apps and sites” footer fragment appears on all 25 existing pages and all staged posts. `family.css` styles it; `site-language.js` supplies language switching on the blog index and new posts. Both languages of each new article share one URL, preserving the requested `data-lang` convention.
