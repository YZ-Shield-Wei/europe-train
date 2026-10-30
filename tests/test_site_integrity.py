"""URL preservation and no-new-broken-link gates for the public static site."""
import json
from pathlib import Path
import unittest
from scripts.site_audit import ROOT, collect, local_target, regressions

class SiteIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = collect()
        cls.baseline = json.loads((ROOT / 'docs/site-audit-baseline.json').read_text())
        cls.changes = regressions(cls.current, cls.baseline)

    def test_original_html_urls_preserved(self):
        self.assertEqual(self.changes['deleted_html_paths'], [])

    def test_no_new_missing_html_or_asset_links(self):
        self.assertEqual(self.changes['new_missing_references'], [])

    def test_no_unreviewed_noindex(self):
        self.assertEqual(self.changes['new_noindex_pages'], [])

    def test_public_duplicate_trees_are_not_excluded(self):
        public = set(self.current['public_html_paths'])
        for name in self.current['all_html_paths']:
            if name.startswith(('build/', 'content/', 'www/')):
                self.assertIn(name, public)

    def test_relative_encoded_and_fragment_resolution(self):
        self.assertEqual(local_target('zh/articles/example.html', '../..//css/global.css'), 'css/global.css')
        self.assertEqual(local_target('en/index.html', '/zh/articles/'), 'zh/articles/index.html')
        self.assertEqual(local_target('en/index.html', '#routes'), 'en/index.html')
        self.assertEqual(local_target('index.html', '/en/articles/a%26b.html'), 'en/articles/a&b.html')
        self.assertIsNone(local_target('index.html', 'https://example.org/x'))
        self.assertIsNone(local_target('index.html', 'mailto:test@example.org'))

    def test_regression_gate_detects_deletion_and_new_failure(self):
        baseline = {'all_html_paths': ['x.html'], 'missing_references': [], 'noindex_pages': []}
        current = {'all_html_paths': [], 'missing_references': [{'source': 'x', 'target': 'y'}], 'noindex_pages': ['z.html']}
        result = regressions(current, baseline)
        self.assertEqual(result['deleted_html_paths'], ['x.html'])
        self.assertTrue(result['new_missing_references'])
        self.assertEqual(result['new_noindex_pages'], ['z.html'])

if __name__ == '__main__':
    unittest.main()
