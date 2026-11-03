"""Amsterdam–Berlin technical canonical consolidation; all legacy bodies retained."""
import unittest,re,json,hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://europe-train.com/'
PLAN={'primary': {'en': 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html', 'zh': 'zh/articles/amsterdam-to-berlin-train-guide.html', 'de': 'de/articles/amsterdam-to-berlin-train-guide.html', 'fr': 'fr/articles/amsterdam-to-berlin-train-guide.html', 'es': 'es/articles/amsterdam-to-berlin-train-guide.html', 'pt': 'pt/articles/amsterdam-to-berlin-train-guide.html', 'ja': 'ja/articles/amsterdam-to-berlin-train-guide.html', 'ko': 'ko/articles/amsterdam-to-berlin-train-guide.html'}, 'aliases': {'articles/amsterdam-to-berlin-train-guide.html': 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html', 'de/articles/amsterdam-to-berlin-by-train-complete-guide.html': 'de/articles/amsterdam-to-berlin-train-guide.html', 'de/articles/amsterdam-to-berlin-by-train-the-perfect-route.html': 'de/articles/amsterdam-to-berlin-train-guide.html', 'de/articles/amsterdam-to-berlin-train-guide.html': 'de/articles/amsterdam-to-berlin-train-guide.html', 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html': 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html', 'en/articles/amsterdam-to-berlin-by-train-the-perfect-route.html': 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html', 'es/articles/amsterdam-to-berlin-by-train-complete-guide.html': 'es/articles/amsterdam-to-berlin-train-guide.html', 'es/articles/amsterdam-to-berlin-train-guide.html': 'es/articles/amsterdam-to-berlin-train-guide.html', 'fr/articles/amsterdam-to-berlin-by-train-complete-guide.html': 'fr/articles/amsterdam-to-berlin-train-guide.html', 'fr/articles/amsterdam-to-berlin-train-guide.html': 'fr/articles/amsterdam-to-berlin-train-guide.html', 'ja/articles/amsterdam-to-berlin-train-guide.html': 'ja/articles/amsterdam-to-berlin-train-guide.html', 'ko/articles/amsterdam-to-berlin-train-guide.html': 'ko/articles/amsterdam-to-berlin-train-guide.html', 'pt/articles/amsterdam-to-berlin-train-guide.html': 'pt/articles/amsterdam-to-berlin-train-guide.html', 'zh/articles/amsterdam-to-berlin-by-train-complete-guide.html': 'zh/articles/amsterdam-to-berlin-train-guide.html', 'zh/articles/amsterdam-to-berlin-train-guide.html': 'zh/articles/amsterdam-to-berlin-train-guide.html'}, 'body_sha256': {'articles/amsterdam-to-berlin-train-guide.html': '79aa3a814744830553bb5c4c6033f4f1e8e059061fb62353382557dc1b75bdc9', 'de/articles/amsterdam-to-berlin-by-train-complete-guide.html': '8a6d3682902bf7d77154ed7ff6094de39d5d5553e7bb2acd37351aa9be473e54', 'de/articles/amsterdam-to-berlin-by-train-the-perfect-route.html': '8a6d3682902bf7d77154ed7ff6094de39d5d5553e7bb2acd37351aa9be473e54', 'de/articles/amsterdam-to-berlin-train-guide.html': '8a6d3682902bf7d77154ed7ff6094de39d5d5553e7bb2acd37351aa9be473e54', 'en/articles/amsterdam-to-berlin-by-train-complete-guide.html': '79aa3a814744830553bb5c4c6033f4f1e8e059061fb62353382557dc1b75bdc9', 'en/articles/amsterdam-to-berlin-by-train-the-perfect-route.html': '79aa3a814744830553bb5c4c6033f4f1e8e059061fb62353382557dc1b75bdc9', 'es/articles/amsterdam-to-berlin-by-train-complete-guide.html': '31a6f787ccff98b4c0cf18114a14685b6847ac58c9bdc280d1bb608a4f182cd7', 'es/articles/amsterdam-to-berlin-train-guide.html': '31a6f787ccff98b4c0cf18114a14685b6847ac58c9bdc280d1bb608a4f182cd7', 'fr/articles/amsterdam-to-berlin-by-train-complete-guide.html': '54b5d27f9c8def3ecad4a1ddc964523078de26f718a4af74d0ffc987851062c0', 'fr/articles/amsterdam-to-berlin-train-guide.html': '54b5d27f9c8def3ecad4a1ddc964523078de26f718a4af74d0ffc987851062c0', 'ja/articles/amsterdam-to-berlin-train-guide.html': '58e94a0423fd3df465beabddeaf23059e2aac160e7567b507a8b69a42010b9bf', 'ko/articles/amsterdam-to-berlin-train-guide.html': '839c1acb00bb9cea341c3fe6beb70276a8bab6ca2b636571730f29d6342a6c19', 'pt/articles/amsterdam-to-berlin-train-guide.html': 'bcdcae238ad7433e32a7e92093775ae85d38bea83cd56a221d87cffee2865562', 'zh/articles/amsterdam-to-berlin-by-train-complete-guide.html': '0e9dd4851941135367460f42f083f2804b7587d34545517ca4aa1f03029708b0', 'zh/articles/amsterdam-to-berlin-train-guide.html': '0e9dd4851941135367460f42f083f2804b7587d34545517ca4aa1f03029708b0'}}
class AmsterdamCanonicalFamily(unittest.TestCase):
 def test_retained_files_and_exact_article_bodies(self):
  for path,digest in PLAN['body_sha256'].items():
   with self.subTest(path=path):
    s=(ROOT/path).read_text()
    self.assertEqual(hashlib.sha256(re.search(r'<article class="guide-body">.*?</article>',s,re.S)[0].encode()).hexdigest(),digest)
    self.assertNotIn('http-equiv="refresh"',s)
 def test_canonical_graph_schema_and_language_navigation(self):
  graph={('zh-CN' if lang=='zh' else lang):ORIGIN+path for lang,path in PLAN['primary'].items()}
  graph['x-default']=ORIGIN+PLAN['primary']['en']
  for path,primary in PLAN['aliases'].items():
   with self.subTest(path=path):
    s=(ROOT/path).read_text();url=ORIGIN+primary
    self.assertEqual(re.findall(r'<link rel="canonical" href="([^"]+)"',s),[url])
    self.assertEqual(dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',s)),graph)
    self.assertEqual(len(re.findall(r'<link rel="alternate"',s)),9)
    self.assertIn('<meta property="og:url" content="'+url+'">',s)
    schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1])
    self.assertEqual(schema['mainEntityOfPage'],url)
    nav=re.search(r'<nav class="article-languages".*?</nav>',s,re.S)[0]
    self.assertEqual(nav.count('<a '),7);self.assertEqual(nav.count('aria-current="page"'),1)
    for target in re.findall(r'href="([^"]+)"',nav):self.assertIn(target[1:],PLAN['primary'].values())
    self.assertNotIn('hreflang="it"',s)
 def test_sitemap_and_unique_archive_entries(self):
  urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('{*}url/{*}loc')]
  family=[u for u in urls if 'amsterdam' in u and 'berlin' in u]
  self.assertEqual(set(family),{ORIGIN+p for p in PLAN['primary'].values()});self.assertEqual(len(family),8)
  for lang,path in PLAN['primary'].items():
   s=(ROOT/lang/'articles/index.html').read_text()
   links=re.findall(r'href="([^"]*amsterdam[^"<>]*berlin[^"<>]*)"',s)
   self.assertEqual(links,[path.split('/')[-1]])
if __name__=='__main__':unittest.main()
