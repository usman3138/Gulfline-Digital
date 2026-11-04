"""Publish one due bilingual article per Dubai day. Run from any directory.

TODAY=YYYY-MM-DD is a test/recovery override; normal runs use Dubai time.
All inputs are validated and outputs prepared before any publication writes.
The workflow serializes runs; this script also rejects concurrent local runs.
"""
import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import sys
from email.utils import format_datetime
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / 'docs/scheduled'
BASE = 'https://gulflinedigital.com'
DUBAI = dt.timezone(dt.timedelta(hours=4))


def read(path):
    return path.read_text(encoding='utf-8')


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(value, encoding='utf-8', newline='\n')
    temporary.replace(path)


def publish(today):
    stamp = QUEUE / 'last-published-date.txt'
    if stamp.exists() and read(stamp).strip() >= today.isoformat():
        print('already published for', today)
        return
    manifest = json.loads(read(QUEUE / 'manifest.json'))
    seen = set()
    for post in manifest:
        slug = post['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or slug in seen:
            raise ValueError('Invalid or duplicate slug: ' + slug)
        seen.add(slug)
        dt.date.fromisoformat(post['date'])
        for key in ('title', 'title_ar', 'description', 'description_ar', 'category', 'category_ar'):
            if not isinstance(post[key], str) or not post[key].strip():
                raise ValueError('Missing metadata: ' + key)
        if not (QUEUE / (slug + '.html')).exists() and not (ROOT / 'blog' / (slug + '.html')).exists():
            raise ValueError('Missing article: ' + slug)
    due = sorted((p for p in manifest if p['date'] <= today.isoformat()
                  and not (ROOT / 'blog' / (p['slug'] + '.html')).exists()),
                 key=lambda p: (p['date'], p['slug']))
    if not due:
        print('nothing to publish for', today)
        return
    p = due[0]
    slug = p['slug'] + '.html'
    url = BASE + '/blog/' + slug
    source = read(QUEUE / slug)
    if 'data-lang="en"' not in source or 'data-lang="ar"' not in source or url not in source:
        raise ValueError('Article must be bilingual with its canonical URL')
    # Late runs retain their planned date in the manifest, but use the actual
    # Dubai publication date in article metadata, RSS, sitemap and changelog.
    actual = today.isoformat()
    source = source.replace(p['date'], actual)
    source = re.sub(r'("dateModified":\s*")[^"]+', lambda m: m[1] + actual, source)
    source = re.sub(r'(<meta property="article:modified_time" content=")[^"]+', lambda m: m[1] + actual, source)
    esc = html.escape
    pair = lambda en, ar: f'<span data-lang="en">{esc(en)}</span><span data-lang="ar" lang="ar">{esc(ar)}</span>'
    card = f'''\n    <a class="card" href="/blog/{slug}">
      <div class="card-body">
        <span class="tag">{pair(p['category'], p['category_ar'])}</span>
        <h2>{pair(p['title'], p['title_ar'])}</h2>
        <p>{pair(p['description'], p['description_ar'])}</p>
        <span class="more">{pair('Read article →', 'اقرأ المقال ←')}</span>
      </div>
    </a>'''
    index_path = ROOT / 'blog/index.html'
    index = read(index_path)
    marker = '<!-- scheduled-posts -->'
    if index.count(marker) != 1:
        raise ValueError('Expected one blog card insertion marker')
    if '/blog/' + slug in index:
        raise ValueError('Article already indexed; inspect incomplete publication')
    index = index.replace(marker, marker + card, 1)
    # Include new article in the existing Blog JSON-LD list as well.
    pattern = r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)'
    def update_schema(match):
        data = json.loads(match[2])
        if data.get('@type') == 'Blog':
            data.setdefault('blogPost', []).insert(0, {
                '@type': 'BlogPosting', 'headline': p['title'], 'url': url,
                'datePublished': actual, 'inLanguage': ['en', 'ar']})
        return match[1] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n' + match[3]
    index = re.sub(pattern, update_schema, index)
    pub = format_datetime(dt.datetime.combine(today, dt.time(8, 17), DUBAI))
    rss_path = ROOT / 'blog/rss.xml'
    rss = read(rss_path)
    item = (f'\n  <item><title>{esc(p["title"])}</title><link>{url}</link>'
            f'<guid isPermaLink="true">{url}</guid><pubDate>{pub}</pubDate>'
            f'<category>{esc(p["category"])}</category><description>{esc(p["description"])}</description></item>\n')
    if url in rss:
        raise ValueError('Article already in feed')
    if '<lastBuildDate>' in rss:
        rss = re.sub(r'<lastBuildDate>[^<]*</lastBuildDate>', f'<lastBuildDate>{pub}</lastBuildDate>', rss)
        rss = rss.replace('</lastBuildDate>', '</lastBuildDate>' + item, 1)
    else:
        rss = rss.replace('<language>en</language>', f'<language>en</language>\n  <lastBuildDate>{pub}</lastBuildDate>' + item, 1)
    if item not in rss:
        raise ValueError('Feed insertion failed')
    sitemap_path = ROOT / 'sitemap.xml'
    sitemap = read(sitemap_path)
    if url in sitemap:
        raise ValueError('Article already in sitemap')
    sitemap = sitemap.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>{actual}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n</urlset>')
    ET.fromstring(rss)
    ET.fromstring(sitemap)
    log_path = ROOT / 'CHANGELOG.md'
    log = read(log_path)
    heading = '# Changelog\n\n'
    if heading not in log:
        raise ValueError('Changelog heading missing')
    log = log.replace(heading, heading + f'- {actual} - Published `blog/{slug}` (scheduled {p["date"]}); updated bilingual blog card, RSS and sitemap. Sources reviewed on the article.\n', 1)
    # Publish derived files before the post and day stamp. A partial filesystem
    # failure fails closed on the next run rather than duplicating listings.
    for path, value in ((index_path, index), (rss_path, rss), (sitemap_path, sitemap), (log_path, log)):
        write(path, value)
    write(ROOT / 'blog' / slug, source)
    write(stamp, actual + '\n')
    # Keep staging source for review and recovery; blog/ existence is the ledger.
    print('published', slug, 'on', actual)


def main():
    today = dt.date.fromisoformat(os.environ.get('TODAY') or dt.datetime.now(DUBAI).date().isoformat())
    lock = QUEUE / '.publisher.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError('Publisher lock exists; another run or interrupted run needs inspection')
    try:
        os.close(fd)
        publish(today)
    finally:
        lock.unlink()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, RuntimeError, OSError) as error:
        print('Publication failed:', error, file=sys.stderr)
        sys.exit(1)
