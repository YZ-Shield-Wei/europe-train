"""Presentation-only Platform theme wiring and progressive enhancement."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = (
    'home-travel', 'rail-guide', 'rail-archive', 'rail-sections',
    'rail-status', 'disruption-archive', 'rail-legacy-article',
)


class PlatformTheme(unittest.TestCase):
    def test_existing_stylesheet_urls_keep_original_rules_and_theme(self):
        for name in PRIMARY:
            with self.subTest(name=name):
                content = (ROOT / 'css' / (name + '.css')).read_text()
                imports = re.findall(r'@import url\("([^"]+)"\)', content)
                theme = 'platform-home' if name == 'home-travel' else 'platform-content'
                self.assertEqual(imports, [
                    '/css/platform-fonts.css', '/css/platform-base/' + name + '.css',
                    '/css/' + theme + '.css',
                ])
                for path in imports:
                    self.assertTrue((ROOT / path.lstrip('/')).is_file(), path)
                self.assertGreater((ROOT / 'css/platform-base' / (name + '.css')).stat().st_size, 100)

    def test_fonts_are_self_hosted_with_licenses(self):
        content = (ROOT / 'css/platform-fonts.css').read_text()
        self.assertNotIn('https:', content)
        urls = re.findall(r'url\(([^)]+)\)', content)
        self.assertEqual(len(urls), 3)
        for url in urls:
            self.assertTrue(url.startswith('/fonts/'))
            self.assertEqual((ROOT / url.lstrip('/')).read_bytes()[:4], b'wOF2')
        for filename in ['archivo-OFL.txt', 'jetbrainsmono-OFL.txt']:
            self.assertIn('SIL OPEN FONT LICENSE', (ROOT / 'fonts' / filename).read_text())

    def test_homepage_visual_order_matches_keyboard_order(self):
        for path in [ROOT / 'index.html'] + [ROOT / lang / 'index.html' for lang in
                ['en', 'zh', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'ko']]:
            with self.subTest(path=str(path.relative_to(ROOT))):
                html = path.read_text()
                self.assertLess(html.index('class="hero wrap"'), html.index('id="route-planner"'))
                self.assertLess(html.index('id="route-planner"'), html.index('id="buying-guides"'))
                self.assertNotRegex(html, r'tabindex=["\'][1-9]')
                self.assertIn('id="route-form" hidden', html)
                self.assertIn('<noscript>', html)


if __name__ == '__main__':
    unittest.main()
