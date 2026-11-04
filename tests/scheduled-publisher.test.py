"""Run the real publisher against disposable copies; never publish in checkout."""
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        for folder in ('docs/scheduled', 'blog'):
            shutil.copytree(ROOT / folder, self.work / folder,
                            ignore=shutil.ignore_patterns('__pycache__', '.publisher.lock'))
        for name in ('sitemap.xml', 'CHANGELOG.md'):
            shutil.copyfile(ROOT / name, self.work / name)
        self.queue = self.work / 'docs/scheduled'
        self.stamp = self.queue / 'last-published-date.txt'
        self.stamp.unlink(missing_ok=True)
        self.posts = json.loads((self.queue / 'manifest.json').read_text(encoding='utf-8'))
        # Reset fixture to unpublished even after the real series has started.
        for p in self.posts:
            (self.work / 'blog' / (p['slug'] + '.html')).unlink(missing_ok=True)
        for name in ('blog/index.html', 'blog/rss.xml', 'sitemap.xml'):
            path = self.work / name
            text = path.read_text(encoding='utf-8')
            import re
            for p in self.posts:
                slug = re.escape(p['slug'])
                if name.endswith('index.html'):
                    text = re.sub(r'\s*<a class="card" href="/blog/' + slug + r'\.html">[\s\S]*?</a>', '', text)
                    def reset_schema(match):
                        data = json.loads(match[1])
                        if data.get('@type') == 'Blog':
                            data['blogPost'] = [item for item in data.get('blogPost', [])
                                                if item.get('url') != 'https://gulflinedigital.com/blog/' + p['slug'] + '.html']
                        return '<script type="application/ld+json">' + json.dumps(data) + '</script>'
                    text = re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>', reset_schema, text)
                elif name.endswith('rss.xml'):
                    text = re.sub(r'\s*<item>(?:(?!</item>)[\s\S])*?' + slug + r'\.html[\s\S]*?</item>', '', text)
                else:
                    text = re.sub(r'\s*<url>(?:(?!</url>)[\s\S])*?' + slug + r'\.html[\s\S]*?</url>', '', text)
            path.write_text(text, encoding='utf-8')

    def run_day(self, date, ok=True):
        result = subprocess.run([sys.executable, str(self.queue / 'publish.py')],
                                cwd=self.work / 'blog',
                                env={**os.environ, 'TODAY': date},
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def snapshot(self):
        return {str(p.relative_to(self.work)): p.read_bytes()
                for p in self.work.rglob('*') if p.is_file()}

    def published(self):
        return [p for p in self.posts if (self.work / 'blog' / (p['slug'] + '.html')).exists()]

    def test_schedule_retry_and_late_backlog(self):
        self.assertIn('nothing to publish', self.run_day('2026-11-05'))
        self.assertFalse(self.stamp.exists())
        self.assertIn('published ', self.run_day('2026-11-06'))
        self.assertEqual(len(self.published()), 1)
        before = self.snapshot()
        self.assertIn('already published', self.run_day('2026-11-06'))
        self.assertEqual(before, self.snapshot())
        self.assertIn('nothing to publish', self.run_day('2026-11-07'))
        self.assertIn('published ', self.run_day('2026-11-12'))
        self.assertEqual(len(self.published()), 2)
        before = self.snapshot()
        self.run_day('2026-11-12')
        self.assertEqual(before, self.snapshot())
        self.run_day('2026-11-13')
        self.assertEqual(len(self.published()), 3)
        self.assertEqual(self.stamp.read_text().strip(), '2026-11-13')
        late = self.published()[1]
        article = (self.work / 'blog' / (late['slug'] + '.html')).read_text(encoding='utf-8')
        self.assertIn('datetime="2026-11-12"', article)
        for p in self.published():
            url = 'https://gulflinedigital.com/blog/' + p['slug'] + '.html'
            index = (self.work / 'blog/index.html').read_text(encoding='utf-8')
            self.assertEqual(index.count('href="/blog/' + p['slug'] + '.html"'), 1)
            self.assertIn(p['title_ar'], index)
            rss = ET.parse(self.work / 'blog/rss.xml')
            self.assertEqual(sum(i.findtext('link') == url for i in rss.findall('./channel/item')), 1)
            sitemap = ET.parse(self.work / 'sitemap.xml')
            ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            self.assertEqual(sum(i.text == url for i in sitemap.findall('.//s:loc', ns)), 1)

    def test_all_posts_and_exhaustion(self):
        date = dt.date(2027, 1, 1)
        for offset in range(13):
            day = (date + dt.timedelta(days=offset)).isoformat()
            self.assertIn('published ', self.run_day(day))
            self.assertEqual(len(self.published()), offset + 1)
        before = self.snapshot()
        self.assertIn('nothing to publish', self.run_day('2027-02-01'))
        self.assertEqual(before, self.snapshot())
        self.assertEqual(len(list(self.queue.glob('*.html'))), 13, 'Preserve review sources')
        # Validate the fully published static site with the real Node checks.
        # Add unchanged assets after publication so fixtures stay lightweight
        # during the retry snapshots above.
        for folder in ('ar', 'images'):
            shutil.copytree(ROOT / folder, self.work / folder)
        for path in ROOT.iterdir():
            if path.is_file() and path.suffix in ('.html', '.css', '.js'):
                shutil.copyfile(path, self.work / path.name)
        (self.work / 'tests').mkdir()
        for script in ('check-site.mjs', 'check-scheduled.mjs'):
            shutil.copyfile(ROOT / 'tests' / script, self.work / 'tests' / script)
            result = subprocess.run(['node', 'tests/' + script], cwd=self.work,
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_manifest_does_not_write(self):
        self.posts[0]['slug'] = '../escape'
        (self.queue / 'manifest.json').write_text(json.dumps(self.posts), encoding='utf-8')
        before = self.snapshot()
        self.assertIn('Invalid or duplicate slug', self.run_day('2026-12-05', ok=False))
        self.assertEqual(before, self.snapshot())

    def test_missing_source_and_bad_index_fail_before_writes(self):
        source = self.queue / (self.posts[0]['slug'] + '.html')
        saved = source.read_bytes()
        source.unlink()
        before = self.snapshot()
        self.assertIn('Missing article', self.run_day('2026-11-06', ok=False))
        self.assertEqual(before, self.snapshot())
        source.write_bytes(saved)
        index = self.work / 'blog/index.html'
        index.write_text(index.read_text(encoding='utf-8').replace('<!-- scheduled-posts -->', ''), encoding='utf-8')
        before = self.snapshot()
        self.assertIn('insertion marker', self.run_day('2026-11-06', ok=False))
        self.assertEqual(before, self.snapshot())

    def test_lock_and_invalid_date(self):
        lock = self.queue / '.publisher.lock'
        lock.write_text('')
        before = self.snapshot()
        self.assertIn('lock exists', self.run_day('2026-11-06', ok=False))
        self.assertEqual(before, self.snapshot())
        lock.unlink()
        self.assertIn('Publication failed', self.run_day('not-a-date', ok=False))
        self.assertFalse(lock.exists())

    def test_default_clock_uses_dubai_midnight(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('publisher_fixture', self.queue / 'publish.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        test = self
        class Clock(dt.datetime):
            @classmethod
            def now(cls, tz=None):
                test.assertEqual(tz.utcoffset(None), dt.timedelta(hours=4))
                # Dubai is already Friday while UTC is still Thursday.
                return cls(2026, 11, 5, 20, 1, tzinfo=dt.timezone.utc).astimezone(tz)
        with patch.dict(os.environ):
            os.environ.pop('TODAY', None)
            with patch.object(module.dt, 'datetime', Clock):
                module.main()
        self.assertEqual(self.stamp.read_text().strip(), '2026-11-06')
        self.assertEqual(len(self.published()), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
