"""The Milan–Venice guide is complete and reachable in all supported languages."""
import json,re,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
LANGS=('en','zh','de','fr','es','it','ja','ko','pt')
SLUG='milan-to-venice-train-guide.html'
ORIGIN='https://europe-train.com/'
class MilanVenicePilot(unittest.TestCase):
 def test_complete_localized_articles(self):
  for lang in LANGS:
   with self.subTest(lang=lang):
    s=(ROOT/lang/'articles'/SLUG).read_text();url=ORIGIN+lang+'/articles/'+SLUG
    self.assertEqual(re.findall(r'<link rel="canonical" href="([^"]+)"',s),[url])
    self.assertEqual(len(re.findall(r'<link rel="alternate"',s)),10)
    self.assertNotIn('Roma → Firenze',s)
    self.assertIn('Milano → Venezia',s)
    schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1])
    self.assertEqual(schema['mainEntityOfPage'],url)
    self.assertEqual(schema['datePublished'],'2026-11-02')
    self.assertEqual(schema['dateModified'],'2026-11-02')
    self.assertGreaterEqual(len(re.findall(r'<section id=',s)),7)
    self.assertNotIn('tpembars.com',s)
 def test_hreflang_and_language_switch(self):
  for lang in LANGS:
   s=(ROOT/lang/'articles'/SLUG).read_text()
   for l in LANGS:
    self.assertIn('href="'+ORIGIN+l+'/articles/'+SLUG+'"',s)
    if l!=lang:self.assertIn('href="/'+l+'/articles/'+SLUG+'"',s)
 def test_existing_home_scripts_preserved(self):
  for lang in ('',)+LANGS:
   s=(ROOT/lang/'index.html').read_text()
   self.assertEqual(s.count('https://tpembars.com/NTkyOTk4.js?t=592998'),1)
 def test_archive_and_sitemap(self):
  ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
  locations=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
  for lang in LANGS:
   self.assertEqual(locations.count(ORIGIN+lang+'/articles/'+SLUG),1)
   self.assertEqual((ROOT/lang/'articles/index.html').read_text().count('href="'+SLUG+'"'),1)
if __name__=='__main__':unittest.main()
