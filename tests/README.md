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

## Scheduled publisher and content

```text
node tests/check-scheduled.mjs
python tests/scheduled-publisher.test.py
```

Use Python 3.10+ (standard library only). Tests operate in temporary directories and never publish in this checkout. See [the publisher guide](../docs/scheduled/README.md) for coverage, manifest format, recovery and the editorial calendar. `TODAY` on the real publisher is a writing override, not a preview mode.

### Local evidence — 2026-11-04

- `node tests/check-site.mjs`: PASS all checks (25 existing public pages, 23 sitemap URLs). Staged articles are intentionally excluded from live discovery until their date.
- `node tests/check-scheduled.mjs`: PASS for 13 bilingual queued articles, dates, publication links, metadata, source-review sections, combined body counts, distinct paragraphs and family footer coverage.
- `python tests/scheduled-publisher.test.py`: six tests passed using local Python 3.13.16. Normal Windows `python` alias was unavailable; the installed interpreter was invoked directly.
- Local headless Chrome at 1365×900 and 390×900: home, Arabic home, blog index and all 13 staged articles checked in EN/AR for language/RTL, correct translation visibility, five footer destinations and no horizontal overflow. Arabic mobile article/footer screenshots inspected; diagrams enlarged and new-post CTA contrast corrected. External HTTPS resources were blocked, so this does not verify web fonts, analytics, advertising, remote availability or real ad placement.
- No physical-device test, live checkout/payment, campaign send, production deployment or Actions execution. The legacy blog article bodies were not translated or manually re-reviewed in this work.
- Documentation validation: nine affected Markdown files are nonempty; all 55 local Markdown links resolve. `git diff --check` passed, and the prohibited-brand scan found no mentions in the affected site/content files. The full-publication fixture also passed both Node checks after all 13 articles were published inside its temporary copy.

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
