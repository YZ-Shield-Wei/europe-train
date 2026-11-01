"""Berlin–Munich's localized guide, legacy URLs and homepage entries stay coherent."""
import json,re,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
LANGS=('en','zh','de','fr','es','it','ja','ko','pt')
SLUG='berlin-to-munich-train-guide.html'
ORIGIN='https://europe-train.com/'
class BerlinRoutePilot(unittest.TestCase):
 def test_primary_languages_and_anchors(self):
  for lang in LANGS:
   with self.subTest(lang=lang):
    s=(ROOT/lang/'articles'/SLUG).read_text();url=ORIGIN+lang+'/articles/'+SLUG
    self.assertIn('href="'+url+'"',s)
    self.assertEqual(re.findall(r'<link rel="canonical" href="([^"]+)"',s),[url])
    self.assertEqual(len(re.findall(r'<link rel="alternate"',s)),10)
    for x in ['route','cost','reservation','detail','prepare','change','sources']:
     self.assertEqual(s.count('id="'+x+'"'),1)
    schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1])
    self.assertEqual(schema['mainEntityOfPage'],url)
    self.assertEqual(schema['dateModified'],'2026-11-02')
    self.assertIn('deutschlandticket-kombi-fv-dt',s)
 def test_legacy_aliases_remain_readable_with_primary_canonical(self):
  for lang in ('en','de'):
   primary=(ROOT/lang/'articles'/SLUG).read_text()
   alias=(ROOT/lang/'articles/berlin-to-munich-by-train-complete-guide.html').read_text()
   self.assertEqual(alias,primary)
   self.assertNotIn('http-equiv="refresh"',alias)
 def test_sitemap_uses_primary_not_duplicate_aliases(self):
  ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
  locations=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
  for lang in LANGS:self.assertIn(ORIGIN+lang+'/articles/'+SLUG,locations)
  self.assertFalse(any('berlin-to-munich-by-train-complete-guide.html' in x for x in locations))
 def test_homepage_route_has_guide_and_official_planner(self):
  for lang in ('',)+LANGS:
   s=(ROOT/lang/'index.html').read_text();card=re.search(r'<article class="route-card"[^>]*id="route-berlin-munich".*?</article>',s,re.S)[0]
   target=(lang or 'en')
   self.assertEqual(card.count('/'+target+'/articles/'+SLUG),1)
   self.assertRegex(card,r'https://(?:int|www)\.bahn\.de/')
   self.assertEqual(s.count('https://tpembars.com/NTkyOTk4.js?t=592998'),1)
 def test_no_third_party_loader_added_to_article(self):
  for lang in LANGS:
   s=(ROOT/lang/'articles'/SLUG).read_text()
   self.assertNotIn('tpembars.com',s)
   self.assertEqual(s.count('https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF'),0 if lang=='it' else 1)
if __name__=='__main__':unittest.main()
