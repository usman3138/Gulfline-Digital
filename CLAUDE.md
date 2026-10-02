# CLAUDE.md — Gulfline Digital

## What this project is

The live website gulflinedigital.com: a bilingual (English/Arabic) static site selling small-business websites in the UAE, with a blog. Read `README.md` and `docs/architecture.md` first.

## Rules

- **This repo is the live site.** A push to `main` publishes to Hostinger within seconds. Never commit or push unless the user asks.
- **Everything in this repo is public.** The GitHub repo is public, so every file can be read there. On the website, `.htaccess` blocks only `.md`, `.env*`, `docs/` and `tests/`. Never put secrets, passwords or private notes in any file.
- **Run `node tests/check-site.mjs` before every push**; it must print `PASS all checks`.
- **Do not move or rename pages or folders.** Files are URLs; `sitemap.xml`, hreflang tags and search results point at them.
- **Every page is bilingual.** When text changes, change both the `data-lang="en"` and `data-lang="ar"` versions, and the matching page in `ar/` if there is one.
- **New page or blog post:** add it to `sitemap.xml`; a blog post also goes in `blog/index.html` and `blog/rss.xml`. Use an existing `blog/*.html` file as the template — the script that generated the first 10 posts is not in this repo.
- **Keep on every page:** the AdSense script in `<head>`, the WhatsApp button, `construction-banner.js`.
- **AdSense:** the site was rejected as "low-value content". Add only real, useful, fact-checked articles (1–2 a month); no filler pages.
- **Images:** WebP, in `images/`, and only photos that are free to use (the blog photos are CC0).
- **Prices** are shown in AED; PayPal charges the USD equivalent (see `checkout.html`). Change both together.
- After every change add one dated line to `CHANGELOG.md`.
- Keep explanations short and in plain English.

## Where things are

- Home: `index.html`. Arabic-first pages: `ar/`.
- Order and payment: `checkout.html` (products, prices, PayPal link).
- Sign-in: `account.html`, `auth-nav.js`, `supabase-config.js` (placeholders — sign-in is off until real values are filled in).
- Blog: `blog/`.
- Notice banner: `construction-banner.js`.

`C:\Users\Usman\Gulfline-Digital` is an old copy of this repo. Work only in `C:\Users\Usman\Projects\Gulfline-Digital`.
