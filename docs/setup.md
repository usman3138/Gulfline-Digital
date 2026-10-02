# Setup notes

## Machine

- Git
- Any browser. Optional: Node.js for `npx serve .`

## Hosting and deploy

- Hostinger, connected to the GitHub repo `usman3138/Gulfline-Digital`, branch `main`. A push is live within seconds.
- `.htaccess` blocks `.md`, `.env*`, `docs/` and `tests/` on the website. The GitHub repo itself is public, so keep private material out of it.

## PayPal

`checkout.html` builds a `paypal.me` link. The PayPal username, product prices and the AED→USD rate are constants near the bottom of that file.

## Supabase (not switched on)

1. Create a Supabase project.
2. Project Settings → API: copy the project URL and the **anon** key into `supabase-config.js`.
3. Authentication → URL configuration: add `https://gulflinedigital.com`.

Only the anon key belongs in the site. Never use the service_role key here.

## AdSense

- The AdSense script is in the `<head>` of every page; `ads.txt` is in the root.
- Status at 2026-09-28: "Needs attention — low-value content". The blog was added on 2026-09-30 in response.
- Next: submit `sitemap.xml` in Google Search Console, wait 1–2 weeks, then request a review.

## Adding a blog post

1. Copy an existing file in `blog/` and rewrite it (title, description, body, structured data, both dates).
2. Add a WebP photo to `images/`.
3. Add the post to `blog/index.html`, `blog/rss.xml` and `sitemap.xml`.
