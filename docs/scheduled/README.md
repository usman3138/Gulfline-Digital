# Scheduled bilingual articles

Implemented locally 2026-11-04. Nothing in this queue has been published by this task. The manager reviews and pushes; pushing main publishes the site. GitHub Actions publication and Hostinger delivery still need live verification after that push.

## Editorial scope

Thirteen original English/Arabic pages use `blog/website-cost-uae.html` as the HTML/design template, preserving analytics, AdSense, navigation, footer, WhatsApp and the construction banner. Each has a complete paired `data-lang` body, worked example, original accessible inline SVG and a primary-source list reviewed 4 November 2026. Examples are explicitly hypothetical, not customer results. No new photographs or purported screenshots are used. Existing article slugs and bodies were checked for topic overlap; these posts focus on narrower operating decisions.

Body counts are **1,036–1,084 words per bilingual page**, excluding navigation, diagrams, source lists and footer. The manifest records English and Arabic counts separately (English 601–638, Arabic 410–465); the 900–1,500 requirement is applied to the combined bilingual page, not separately to each translation. The Arabic versions express the same guidance idiomatically, rather than mirroring English word counts. Read both versions during editorial review. This calendar is the owner's explicit exception to the usual low-frequency blog guidance.

EasyToolbox destinations were checked in `E:/Projects/Easytoolbox/pages/`: `qr-code-generator.html`, `word-counter.html`, `percentage-calculator.html`. No invoice generator or SEO helper was invented. Related-site/app links are normal links in a modest shared footer; articles use tool or money-tracking links only in relevant passages. Each staged post has the same family footer as the existing pages.

## Calendar

5 November is Thursday; 5 December is Saturday. The 13 Monday/Wednesday/Friday dates within the requested inclusive window are:

| Dubai date | Article / staged filename |
|---|---|
| Fri 2026-11-06 | [Home-visit tutor Business Profile eligibility](google-business-profile-home-visit-eligibility.html) |
| Mon 2026-11-09 | [Permission-first WhatsApp follow-up](whatsapp-marketing-permission-workflow.html) |
| Wed 2026-11-11 | [Online-service licence launch checklist](uae-online-service-licence-launch-checklist.html) |
| Fri 2026-11-13 | [Domain and hosting handover](domain-hosting-handover-owner-checklist.html) |
| Mon 2026-11-16 | [Low-traffic website speed experiments](pagespeed-lab-field-data-small-site.html) |
| Wed 2026-11-18 | [Arabic service-page search intent](arabic-service-page-search-intent.html) |
| Fri 2026-11-20 | [Payment-link reconciliation](uae-payment-link-reconciliation.html) |
| Mon 2026-11-23 | [Service pricing-page copy](service-page-pricing-copy-workshop.html) |
| Wed 2026-11-25 | [Fair client review requests](client-review-request-without-incentives.html) |
| Fri 2026-11-27 | [Monthly Search Console review](search-console-service-page-monthly-review.html) |
| Mon 2026-11-30 | [Printed QR campaign measurement](qr-code-offline-campaign-test.html) |
| Wed 2026-12-02 | [Booking deposit confirmation](booking-deposit-confirmation-workflow.html) |
| Fri 2026-12-04 | [Redesign while preserving URLs](website-redesign-preserve-urls-checklist.html) |

## Publication contract

- Run `python docs/scheduled/publish.py` from any directory. Python 3.10+; standard library only.
- The normal clock is Dubai (UTC+4). `TODAY=YYYY-MM-DD` overrides it for disposable test fixtures or deliberate recovery. It is not a dry-run flag.
- Select the earliest due unpublished post, ordered by date then slug. Future entries remain staged. Missed dates catch up at most one per subsequent day, including weekends; the manifest retains planned dates and published metadata records the actual day.
- Validate manifest metadata, slugs, sources' existence, insertion marker and XML before any publication writes. Preserve staging HTML. Existence in `blog/` is the per-post publication ledger; `last-published-date.txt` is the daily guard. Same-day retries and earlier-date overrides make no changes after a successful run.
- Add a native `.card`/`.card-body` entry below `<!-- scheduled-posts -->`, with English and Arabic title/category/description/read link, and add the post to the existing Blog JSON-LD. Update `blog/rss.xml`, `sitemap.xml` and `CHANGELOG.md` without altering existing URLs.
- The workflow has one concurrency group and runs at Dubai 08:17, 12:17 and 16:17. It executes publisher regression tests, the publisher and both Node checks before saving publication outputs. Default branch Actions/write permissions and repository scheduling must allow this; not verified locally. A manual dispatch obeys the same day guard.
- Workflow commit/push commands are future requested automation. No git commit or push was run while creating it. The workflow stages an explicit publication path list, not unrelated repository edits. A rejected push fails rather than force-pushing.

## Validation

```text
node tests/check-site.mjs
node tests/check-scheduled.mjs
python tests/scheduled-publisher.test.py
```

The Python suite uses temporary copies and does not publish into this checkout. It covers future dates, scheduled dates, Dubai midnight versus UTC, retry byte equality, overdue backlog, actual dates, all 13 publications, exhaustion, XML entries, bilingual cards, invalid input, missing source/marker and locking. It resets previously published fixture entries so tests remain useful after the series starts. The staging check also validates publication-relative links, source/review sections, original paragraph uniqueness, article word counts, required scripts, metadata and shared footer equality across all pages.

For preview, serve a disposable copy with each staged file at its eventual `/blog/` path. `docs/` is intentionally blocked by the live `.htaccess`; staging is not public-site publication, though repository files remain public. Do not add staged URLs to the live RSS/index/sitemap early. Both languages share each article URL; a working toggle does not establish a separately indexed Arabic URL.

## Failure and recovery

Writes use a temporary sibling and replacement per output, not a multi-file transaction. An interrupted process can leave some outputs updated, a `.tmp` sibling or a `.publisher.lock`. If any duplicate listing is detected, the next run fails closed. Do not delete the date stamp or lock to force another article out.

Inspect the failed Actions log and repository diff. When a run fails before commit, its disposable runner changes have not been pushed. For an interrupted local run, restore incomplete publication outputs from the last reviewed state, preserving unrelated work; remove only confirmed stale temporary/lock files, then rerun the checks in a disposable copy. If publication was already saved, verify the HTML, index, RSS, sitemap, changelog and stamp together before choosing any recovery. A successful local test does not prove that a workflow push deployed on Hostinger.

After the first manager-approved push, check the Actions run, published article, EN/AR toggle, index card, RSS item, sitemap entry, footer and live docs/tests access restrictions. Recheck official policy sources before relying on the articles at a later date. No live payment, messaging campaign, account integration or AdSense approval was tested here.
