"""The reservation guide retains its URL and includes complete localized troubleshooting."""
import json,re,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
LANGS=('en','zh','de','fr','es','it','ja','ko','pt')
SLUG='seat-reservation-guide.html'
class ReservationDecisionPilot(unittest.TestCase):
 def test_localized_diagnostic_sections(self):
  english=None
  for l in LANGS:
   s=(ROOT/l/'articles'/SLUG).read_text();url='https://europe-train.com/'+l+'/articles/'+SLUG
   sec=re.search(r'<section id="reservation-decision">(.*?)</section>',s,re.S)[1]
   self.assertEqual(len(re.findall('<strong>',sec)),6)
   self.assertIn('href="#reservation-decision"',s)
   self.assertIn('reservierung-sitzplatz',sec)
   self.assertIn('seat-reservations-booking-period',sec)
   self.assertIn('plan-your-trip/reservations',sec)
   if l=='en':english=sec
   else:self.assertNotEqual(sec,english)
   self.assertEqual(re.findall(r'<link rel="canonical" href="([^"]+)"',s),[url])
   self.assertEqual(len(re.findall(r'<link rel="alternate"',s)),10)
   self.assertNotIn('tpembars.com',s)
 def test_schema_matches_visible_content(self):
  for l in LANGS:
   s=(ROOT/l/'articles'/SLUG).read_text()
   schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1])
   self.assertEqual(schema['dateModified'],'2026-11-02')
   self.assertNotIn('datePublished',schema)
   import html
   self.assertEqual(schema['headline'],html.unescape(re.search(r'<h1>(.*?)</h1>',s)[1]))
 def test_sitemap_and_archive(self):
  ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
  entries={u.find('s:loc',ns).text:u for u in ET.parse(ROOT/'sitemap.xml').findall('s:url',ns)}
  for l in LANGS:
   self.assertEqual(entries['https://europe-train.com/'+l+'/articles/'+SLUG].find('s:lastmod',ns).text,'2026-11-02')
   self.assertEqual((ROOT/l/'articles/index.html').read_text().count('href="'+SLUG+'"'),1)
 def test_no_homepage_script_changes(self):
  for l in ('',)+LANGS:
   s=(ROOT/l/'index.html').read_text();self.assertEqual(s.count('https://tpembars.com/NTkyOTk4.js?t=592998'),1)
if __name__=='__main__':unittest.main()
