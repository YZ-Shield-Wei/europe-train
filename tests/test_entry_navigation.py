"""Ticket/pass entry improvements retain local destinations and existing analytics."""
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
LANGS = 'en zh de fr es it ja ko pt'.split()
SUFFIXES = ['tickets.html', 'passes.html', 'guides/ticket-buying-guide.html']

class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class EntryNavigation(unittest.TestCase):
    def test_locale_clusters_and_navigation(self):
        for lang in LANGS:
            for suffix in SUFFIXES:
                with self.subTest(lang=lang, suffix=suffix):
                    path = f'{lang}/{suffix}'
                    text = (ROOT / path).read_text()
                    tags = Markup(text).tags
                    self.assertIn(('html', {'lang': 'zh-CN' if lang == 'zh' else lang}), tags)
                    canon = [a['href'] for t,a in tags if t == 'link' and a.get('rel') == 'canonical']
                    self.assertEqual(canon, ['https://europe-train.com/' + path])
                    alternatives = {a['hreflang']:a['href'] for t,a in tags if t == 'link' and 'hreflang' in a}
                    self.assertEqual(alternatives, {l:f'https://europe-train.com/{l}/{suffix}' for l in LANGS})
                    self.assertEqual(text.count('class="entry-actions"'), 1)
                    for tag,attrs in tags:
                        if tag != 'a': continue
                        href = attrs.get('href', '')
                        if href.startswith('#'):
                            self.assertIn(f'id="{href[1:]}"',text)
                        if href.startswith('/') and not href.startswith('//'):
                            local = ROOT / href.lstrip('/').split('#')[0]
                            self.assertTrue(local.exists() or local.with_suffix('.html').exists(),href)
                    if suffix == 'tickets.html':
                        self.assertIn('href="#booking-directory"',text)
                        self.assertIn('id="booking-directory"',text)
                    if suffix == 'passes.html':
                        self.assertIn('href="#other-pass-guides"',text)
                        self.assertIn('href="#swiss-travel-pass"',text)
                        self.assertEqual(text.count('src="/js/conversion-events.js"'),1)
                    else:
                        self.assertIn(f'href="/{lang}/articles/how-to-buy-european-train-tickets.html"',text)
                        self.assertNotIn('src="/js/conversion-events.js"',text)
    def test_legacy_entry_urls_retained(self):
        for suffix in SUFFIXES:
            text=(ROOT/suffix).read_text()
            self.assertIn(f'rel="canonical" href="https://europe-train.com/{suffix}"',text)
            self.assertIn('class="entry-actions"',text)
            self.assertNotIn('hreflang=',text)
            for tag, attrs in Markup(text).tags:
                href = attrs.get('href', '')
                if tag == 'a' and '#' in href and href.startswith(('#', '/')):
                    target, fragment = href.split('#', 1)
                    target_text = (ROOT / target.lstrip('/')).read_text() if target else text
                    self.assertIn(f'id="{fragment}"', target_text, href)
            lang = 'zh' if suffix.startswith('guides/') else 'en'
            if suffix != 'passes.html':
                self.assertIn(f'href="/{lang}/articles/how-to-buy-european-train-tickets.html"',text)

if __name__ == '__main__': unittest.main()
