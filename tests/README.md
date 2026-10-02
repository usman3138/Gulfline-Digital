# Tests

## Automated check

```
node tests/check-site.mjs
```

Run it from the project root before every push. It needs only Node.js and checks that:

- every local link, script, stylesheet and image in every page points to a file that exists
- every URL in `sitemap.xml` has a file
- every page has a `<title>`
- no script or stylesheet is referenced with two different `?v=` numbers
- no private key has been pasted into a page or script

It prints `PASS all checks`, or one `FAIL` line per problem and exits with code 1.

## By hand, before a push

- Open the changed page on desktop width and phone width.
- Switch to Arabic: text is right-to-left, nothing is left in English, the WhatsApp number reads correctly.
- No button is hidden behind the floating WhatsApp button.
- New page or post is in `sitemap.xml` (and `blog/index.html` + `blog/rss.xml` for a post).

## After a push (live site)

- Home, Services, Blog and one article load.
- Checkout: pick a product and an add-on — the AED total and the USD amount update, and "Pay now" opens PayPal with that USD amount. Do not pay.
- WhatsApp button opens a chat.
- `https://gulflinedigital.com/ads.txt` and `/sitemap.xml` load.
- `https://gulflinedigital.com/README.md` returns 403 (project files are blocked by `.htaccess`).
