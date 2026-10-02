# Decisions

Newest first. Each entry: what was decided and why.

## 2026-10-02 — Keep the folder layout, document it instead

**Decision:** No `src/` folder. Pages stay in the repo root.

**Why:** The site is served straight from the repo, so files are URLs. Moving them would break links and search rankings.

## 2026-09-30 — Add a blog

**Decision:** Publish 10 useful articles and keep adding 1–2 a month.

**Why:** AdSense rejected the site as "low-value content"; a sales page alone is not enough content.

## 2026-09-22 — Tone down the under-construction banner

**Decision:** Keep the banner but make it small and dismissible.

**Why:** A loud "under construction" notice tells AdSense reviewers the site is unfinished.

## 2026-07-11 — Separate Arabic pages

**Decision:** Add `ar/` pages alongside the in-page language toggle.

**Why:** Search engines index a URL in one language; Arabic searches need their own Arabic pages.

## 2026-07-09 — Charge in USD through PayPal

**Decision:** Prices are shown in AED but PayPal is charged the USD equivalent.

**Why:** The PayPal account cannot receive AED; the first attempt charged the wrong currency.

## 2026-07-09 — On-site checkout page

**Decision:** A checkout page collects the order before sending the customer to PayPal.

**Why:** A direct PayPal redirect gave no place to choose products and add-ons or see the total.

## Earlier — Plain static site

**Decision:** No framework, no build step, one file per page.

**Why:** Fast to load, nothing to maintain, and it deploys by a simple git push.
