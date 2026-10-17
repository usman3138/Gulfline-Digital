# Project guide

Updated 2026-10-11. This guide supplies documentation roles not already covered by the project's existing records. See [the documentation index](DOCUMENTATION_INDEX.md).

## Product requirements

Static bilingual English/Arabic UAE business website with blog, PayPal checkout links and prepared but inactive Supabase sign-in.

Scope: Services and pricing, enquiry/contact, bilingual pages, blog, PayPal checkout and inactive account scaffolding.

Constraints: Work in Projects/Gulfline-Digital, not the old home-directory copy. Preserve URLs and both languages. A push to main publishes automatically; the repository is public.

Existing implementation is not automatic approval for additional features. Update the relevant feature document when behavior changes.

## Roadmap and next work

Current phase: Maintain the existing business website; sign-in activation and SEO/advertising follow-up require separate work.

Next: Choose the next owner-requested content or feature task. Confirm live SEO/advertising status before reporting it; enable Supabase only as separately authorized work.

Pending: Supabase placeholders and sign-in activation remain pending; historic AdSense/SEO status must be rechecked before current claims. No live service was checked in this task.

No new feature schedule or launch date was agreed during documentation adoption.

## UI and user flows

Pages contain their own markup/styles and language pairs; ar/ contains Arabic-first copies. Preserve RTL, matching English/Arabic content, navigation and mobile layouts.

## APIs and integration contracts

There is no first-party server backend or order database. checkout.html opens a PayPal link; Supabase sign-in is documented as inactive until configured. architecture.md describes these integrations.

Record changed routes, request/response formats, storage and error behavior in the relevant architecture/feature documentation. Do not fabricate a network API for a local-only app.

## Security and privacy

The Git repository is public. .htaccess blocking does not make repository contents private. Never include private context or secret keys; service-role keys cannot go in the browser.

This documentation review is not a security audit. Refer to existing policy and feature records for unverified disclosures or release blockers.

## Release workflow

README and setup.md describe Hostinger publishing from main. No app-store workflow applies to this static site. Local edits are not proof of deployed changes.

Application builds, release version changes and publication are outside this documentation-only task.

## Troubleshooting

- Local setup/build failure: consult the setup document mapped in the index and the project README before altering tools or dependencies.
- Behavior differs from a bundle or live service: compare the dated changelog, feature status and release record; local source may be newer.
- Documentation disagrees: use the latest dated feature/release evidence, preserve older history and record the unresolved difference explicitly.

Known follow-up: Supabase placeholders and sign-in activation remain pending; historic AdSense/SEO status must be rechecked before current claims. No live service was checked in this task.

## Documentation maintenance decision — 2026-10-11

Context: the owner requested one documentation standard for all existing and future projects.

Decision: map roles to existing documentation and add a concise memory, status, index and this guide where needed. Preserve existing code layouts and names, including Game House's lowercase memory.md and play-store/ directory.

Reason: future agents need reliable context and verification status without duplicate or speculative documents.

Consequences: README and AGENTS.md point to the index; future changes update the authoritative document for each role. Historical test/release claims remain historical, and new results must be recorded separately.
