# Gulfline Digital project instructions

Read and follow CLAUDE.md for the established project constraints.

## Shared documentation protocol — 2026-10-11

Follow the [shared project standard](C:/Users/Usman/AGENTS.md) for this project. Find The Change adopts it explicitly even though it is outside the shared directory.

- Before changes, read this file, CLAUDE.md, README.md, MEMORY.md, docs/PROJECT_STATUS.md, docs/DOCUMENTATION_INDEX.md, and the relevant architecture/feature documents.
- Use docs/DOCUMENTATION_INDEX.md to map documentation roles to existing files. Keep existing names and paths; do not create duplicate versions or empty boilerplate.
- After meaningful work, update affected docs, CHANGELOG.md, current status and MEMORY.md; retain Game House's additional change.md record when working there.
- Keep memory concise with dated context, decisions, blockers and next steps. Do not store secrets or private conversation history.
- Separate planned, implemented, built, locally tested, device-tested, deployed and released claims. Record only checks actually performed and preserve historical results as historical.
- New modules/features must follow the existing structure and extend the relevant docs. New projects under the shared directory establish the same applicable documentation roles at creation.
- Documentation-only edits require documentation validation, not application builds. For code changes use the project commands below and the relevant tests/README.md.
- Do not commit, push, deploy or upload as part of documentation maintenance. AAB builds and release version changes require an explicit release request; verify the highest uploaded code before another store upload.

Project constraints: Work in Projects/Gulfline-Digital, not the old home-directory copy. Preserve URLs and both languages. A push to main publishes automatically; the repository is public.

Validation commands: node tests/check-site.mjs before a push; bilingual/mobile/manual checks are in ../tests/README.md.
