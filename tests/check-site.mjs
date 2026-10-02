// Static checks for the website. No dependencies.
// Run from the project root:  node tests/check-site.mjs
//
// Checks:
//   1. every local link, script, stylesheet and image in every HTML page points to a file that exists
//   2. every URL in sitemap.xml has a file
//   3. every page has a <title>
//   4. a local script or stylesheet is not referenced with two different ?v= numbers
//   5. no private key has been pasted into a page or script
// Exit code 0 = all passed, 1 = something failed.

import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname, relative, sep, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SKIP_DIRS = new Set(['.git', 'node_modules', '.wrangler', 'docs', 'tests']);
const SECRETS = [/sk-or-v1-[a-f0-9]{20,}/, /sk-ant-[A-Za-z0-9_-]{20,}/, /service_role/, /-----BEGIN [A-Z ]*PRIVATE KEY-----/];

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name) || name.startsWith('cf-worker')) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}

const rel = p => relative(ROOT, p).split(sep).join('/');
const files = walk(ROOT);
const pages = files.filter(f => f.endsWith('.html'));
const errors = [];
const versions = new Map();   // "js/layout.js" -> Map(version -> first page that uses it)

function targetExists(fromFile, link) {
  let path = link.split('#')[0].split('?')[0];
  if (!path) return true;
  try { path = decodeURIComponent(path); } catch { /* keep as is */ }
  let full = path.startsWith('/') ? join(ROOT, path) : join(dirname(fromFile), path);
  if (existsSync(full) && statSync(full).isDirectory()) full = join(full, 'index.html');
  return existsSync(full) ? full : false;
}

for (const page of pages) {
  const html = readFileSync(page, 'utf8');
  if (!/<title>[^<]+<\/title>/i.test(html)) errors.push(`${rel(page)}: no <title>`);

  // Only look at the markup: skip <script> bodies, where links are often built from pieces.
  const markup = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, m => m.slice(0, m.indexOf('>') + 1));
  for (const m of markup.matchAll(/\b(?:href|src)\s*=\s*"([^"]*)"/gi)) {
    const link = m[1].trim();
    if (!link || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(link)) continue;   // external, mailto:, tel:, data:, #anchor
    if (/[${}<>'+\s]/.test(link)) continue;                                // template or built in code
    const found = targetExists(page, link);
    if (!found) { errors.push(`${rel(page)}: broken link "${link}"`); continue; }
    const v = /\.(?:js|css)\?v=([\w.]+)/.exec(link);
    if (v) {
      const key = rel(found);
      if (!versions.has(key)) versions.set(key, new Map());
      if (!versions.get(key).has(v[1])) versions.get(key).set(v[1], rel(page));
    }
  }
}

for (const [file, seen] of versions) {
  if (seen.size > 1) {
    errors.push(`${file}: referenced with ${seen.size} different versions — ` +
      [...seen].map(([ver, page]) => `v=${ver} (e.g. ${page})`).join(', '));
  }
}

let sitemapCount = 0;
const sitemap = join(ROOT, 'sitemap.xml');
if (existsSync(sitemap)) {
  for (const m of readFileSync(sitemap, 'utf8').matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) {
    sitemapCount++;
    const path = new URL(m[1]).pathname;
    if (!targetExists(sitemap, path)) errors.push(`sitemap.xml: no file for ${m[1]}`);
  }
} else {
  errors.push('sitemap.xml is missing');
}

for (const f of files.filter(f => /\.(?:html|js|json|xml|txt)$/.test(f))) {
  const text = readFileSync(f, 'utf8');
  for (const re of SECRETS) if (re.test(text)) errors.push(`${rel(f)}: looks like a private key (${re.source})`);
}

console.log(`${pages.length} pages, ${sitemapCount} sitemap URLs, ${versions.size} versioned files checked`);
if (errors.length) {
  for (const e of errors) console.log('FAIL ' + e);
  console.log(`\n${errors.length} problem(s)`);
  process.exit(1);
}
console.log('PASS all checks');
