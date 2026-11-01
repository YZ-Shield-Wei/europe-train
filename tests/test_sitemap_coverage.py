"""Canonical articles linked by localized indices must be sitemap entries."""
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unicodedata
import unittest
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://europe-train.com/'
LANGUAGES = ('en', 'zh', 'de', 'fr', 'es', 'it', 'ja', 'ko', 'pt')
NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


def normalized_url(value, base=ORIGIN):
    """Compare Unicode and percent-encoded paths without conflating queries."""
    url = urlsplit(urljoin(base, value))
    path = unicodedata.normalize('NFC', unquote(url.path))
    return urlunsplit((url.scheme.lower(), url.netloc.lower(), path, url.query, ''))


class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links, self.canonicals = [], []
        self.noindex = self.redirect = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta':
            if attrs.get('http-equiv', '').lower() == 'refresh':
                self.redirect = True
            if attrs.get('name', '').lower() in ('robots', 'googlebot'):
                self.noindex |= 'noindex' in attrs.get('content', '').lower()


def indexed_canonical_articles(root):
    expected = set()
    for lang in LANGUAGES:
        index_url = ORIGIN + lang + '/articles/index.html'
        index = Metadata((root / lang / 'articles/index.html').read_text(encoding='utf-8'))
        for link in index.links:
            target = normalized_url(link, index_url)
            url = urlsplit(target)
            if url.netloc != 'europe-train.com' or url.query:
                continue
            path = url.path.lstrip('/')
            if not path.startswith(lang + '/articles/') or not path.endswith('.html') or path.endswith('/index.html'):
                continue
            page = Metadata((root / path).read_text(encoding='utf-8'))
            # Legacy aliases and intentional redirects belong to the canonical URL,
            # not additional sitemap entries. noindex pages are likewise excluded.
            if page.redirect or page.noindex:
                continue
            if len(page.canonicals) == 1 and normalized_url(page.canonicals[0], target) == target:
                expected.add(target)
    return expected


class SitemapCoverage(unittest.TestCase):
    def test_canonical_index_linked_articles_are_in_sitemap(self):
        entries = ET.parse(ROOT / 'sitemap.xml').findall('sm:url/sm:loc', NS)
        locations = [normalized_url(entry.text) for entry in entries]
        self.assertEqual(len(locations), len(set(locations)), 'Duplicate sitemap URLs')
        expected = indexed_canonical_articles(ROOT)
        self.assertTrue(expected, 'No canonical articles discovered')
        self.assertEqual(sorted(expected - set(locations)), [], 'Canonical index-linked articles missing from sitemap')

    def test_intentional_redirects_noindex_and_aliases_are_excluded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for lang in LANGUAGES:
                folder = root / lang / 'articles'
                folder.mkdir(parents=True)
                (folder / 'index.html').write_text('', encoding='utf-8')
            folder = root / 'it/articles'
            names = ('real', 'redirect', 'noindex', 'alias')
            (folder / 'index.html').write_text(''.join(
                f'<a href="{name}.html">Article</a>' for name in names), encoding='utf-8')
            for name in names:
                canonical = 'real' if name == 'alias' else name
                markup = f'<link rel="canonical" href="{ORIGIN}it/articles/{canonical}.html">'
                if name == 'redirect':
                    markup += '<meta http-equiv="refresh" content="0;url=real.html">'
                if name == 'noindex':
                    markup += '<meta name="robots" content="noindex,follow">'
                (folder / f'{name}.html').write_text(markup, encoding='utf-8')
            self.assertEqual(indexed_canonical_articles(root), {ORIGIN + 'it/articles/real.html'})

    def test_unicode_percent_encoding_and_fragments(self):
        self.assertEqual(normalized_url('/fr/articles/caf%C3%A9.html#top'), normalized_url('/fr/articles/cafe\u0301.html'))
        self.assertEqual(normalized_url('a%26b.html', ORIGIN + 'en/articles/index.html'), ORIGIN + 'en/articles/a&b.html')
        self.assertNotEqual(normalized_url('/a.html?x=1'), normalized_url('/a.html?x=2'))


if __name__ == '__main__':
    unittest.main()
