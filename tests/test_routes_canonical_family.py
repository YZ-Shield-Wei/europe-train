"""Route directory canonical/language consolidation with exact content preservation."""
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://europe-train.com/'
LANGUAGES = ('en', 'zh', 'de', 'fr', 'es', 'it', 'ja', 'ko', 'pt')
GRAPH = {('zh-CN' if lang == 'zh' else lang): ORIGIN + lang + '/routes.html'
         for lang in LANGUAGES}
GRAPH['x-default'] = GRAPH['en']
BODY_HASHES = {'routes.html': '7103ae12bf48f3435f78a8ca1cc99995e2fe8c61d733a5cb6f643bad0e6d1113', 'en/routes.html': '7103ae12bf48f3435f78a8ca1cc99995e2fe8c61d733a5cb6f643bad0e6d1113', 'zh/routes.html': '1ec56410863d1aec6c985f05696faf03126d18be4f50ff6b035b1999a0d434f6', 'de/routes.html': 'c954261ea9d288646c47e83c7c01ef73fbac6717d37bccf55c031a48847b1f15', 'fr/routes.html': '58f95b2ed1555d826f7988cc111b43e1ea4f38c4d4e454686933ef37bdd1771c', 'es/routes.html': '830342befc50051a0140dc495a7502921f6b7796944df2ba74d3137973a60c76', 'it/routes.html': '3b19554a23952b999f798b7ac44f299ffef9d7c5cf4778fb57704e8619f7cabc', 'ja/routes.html': '68dcbb617537b85397038555868268f30fe3d730c1cb28c616b1fb6f3bc38f97', 'ko/routes.html': 'ff3e15de9dad5101982bc6ed30c750e3eb8914643c1f3c71703123ca63dbe5ca', 'pt/routes.html': '7303f5fabaf0676e100e751e86234486bbc45b31b697fb3724f4cca79f7c550a'}
SCRIPT_HASH = '4fbfb672e54d4b476a142633d9be68f50c28c7a4562c005e14567f81ab778631'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonicals, self.alternates, self.og_urls, self.links = [], [], [], []
        self.lang = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))
        if tag == 'link' and attrs.get('hreflang'):
            self.alternates.append((attrs['hreflang'], attrs.get('href')))
        if tag == 'meta' and attrs.get('property') == 'og:url':
            self.og_urls.append(attrs.get('content'))


class RoutesCanonicalFamily(unittest.TestCase):
    def test_preserved_bodies_scripts_and_languages(self):
        for path, expected in BODY_HASHES.items():
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding='utf-8')
                body = re.search(r'<body\b.*</body>', text, re.S)[0]
                scripts = ''.join(re.findall(r'<script\b.*?</script>', text, re.S))
                self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), expected)
                self.assertEqual(hashlib.sha256(scripts.encode()).hexdigest(), SCRIPT_HASH)
                lang = 'en' if path == 'routes.html' else path.split('/')[0]
                self.assertEqual(Page(text).lang, 'zh-CN' if lang == 'zh' else lang)
                self.assertNotIn('http-equiv="refresh"', text)
                self.assertNotRegex(text, r'<meta[^>]+content="[^"]*noindex')

    def test_canonical_og_and_reciprocal_alternates(self):
        for path in BODY_HASHES:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding='utf-8')
                head = re.search(r'<head>.*?</head>', text, re.S)[0]
                page = Page(head)
                canonical = GRAPH['en'] if path == 'routes.html' else ORIGIN + path
                self.assertEqual(page.canonicals, [canonical])
                self.assertEqual(page.og_urls, [canonical])
                self.assertEqual(len(page.alternates), len(GRAPH))
                self.assertEqual(dict(page.alternates), GRAPH)
                for language, target in page.alternates:
                    target_path = urlsplit(target).path.lstrip('/')
                    target_page = Page((ROOT / target_path).read_text(encoding='utf-8'))
                    self.assertEqual(target_page.canonicals, [target])
                    self.assertEqual(dict(target_page.alternates), GRAPH)
                    if language != 'x-default':
                        self.assertEqual(target_page.lang, language)

    def test_visible_language_links_and_internal_targets(self):
        for path in BODY_HASHES:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding='utf-8')
                nav = re.search(r'<nav class="section-languages".*?</nav>', text, re.S)[0]
                urls = [urljoin(ORIGIN + path, link) for link in Page(nav).links]
                self.assertEqual(len(urls), 9)
                self.assertEqual(set(urls), set(GRAPH.values()))
                for link in Page(text).links:
                    url = urlsplit(urljoin(ORIGIN + path, link))
                    if url.netloc != 'europe-train.com':
                        continue
                    target = unquote(url.path).lstrip('/')
                    if not target or target.endswith('/'):
                        target += 'index.html'
                    self.assertTrue((ROOT / target).is_file(), (path, link))

    def test_sitemap_canonical_family(self):
        text = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        xml = ET.fromstring(text)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
              'x': 'http://www.w3.org/1999/xhtml'}
        entries = xml.findall('sm:url', ns)
        locations = [entry.find('sm:loc', ns).text for entry in entries]
        self.assertEqual(len(locations), len(set(locations)))
        self.assertNotIn(ORIGIN + 'routes.html', locations)
        family = [entry for entry in entries
                  if entry.find('sm:loc', ns).text in set(GRAPH.values())]
        self.assertEqual(len(family), 9)
        for entry in family:
            alternates = entry.findall('x:link', ns)
            self.assertEqual(len(alternates), len(GRAPH))
            self.assertEqual({item.get('hreflang'): item.get('href') for item in alternates}, GRAPH)
            self.assertTrue(all(item.get('rel') == 'alternate' for item in alternates))
            self.assertEqual(entry.find('sm:lastmod', ns).text, '2026-11-05')


if __name__ == '__main__':
    unittest.main()
