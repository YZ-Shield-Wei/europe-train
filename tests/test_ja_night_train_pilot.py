"""Focused preservation and booking-path gates for the Japanese night-train pilot."""
import json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
PATH='ja/articles/europe-night-train-guide.html'
class Tags(HTMLParser):
 def __init__(self,s):
  super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class JapaneseNightTrainPilot(unittest.TestCase):
 def setUp(self):
  self.s=(ROOT/PATH).read_text();self.tags=Tags(self.s).tags
 def test_existing_sections_and_actionable_booking_links(self):
  ids=[a['id'] for _,a in self.tags if 'id' in a]
  self.assertEqual(len(ids),len(set(ids)))
  for ident in ['topic-'+str(n) for n in range(4)]+['check-'+str(n) for n in range(4)]+['sources','operators','total-price','pass-booking','booking-help']:
   self.assertIn(ident,ids)
  links=[a for t,a in self.tags if t=='a' and a.get('class')=='night-book']
  self.assertEqual(len(links),4)
  self.assertEqual({urlsplit(a['href']).hostname for a in links},{'www.nightjet.com','www.sncf-connect.com','www.trenitalia.com','www.europeansleeper.eu'})
  self.assertTrue(all(not urlsplit(a['href']).query for a in links))
 def test_local_links_and_fragments(self):
  for t,a in self.tags:
   if t!='a' or 'href' not in a:continue
   u=urlsplit(a['href'])
   if u.scheme or u.netloc:continue
   p=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (ROOT/PATH).parent/u.path if u.path else ROOT/PATH
   if p.is_dir():p=p/'index.html'
   self.assertTrue(p.is_file(),str(p))
   if u.fragment:self.assertIn(unquote(u.fragment),[attrs.get('id') for _,attrs in Tags(p.read_text()).tags])
 def test_canonical_hreflang_and_schema(self):
  canonical='https://europe-train.com/'+PATH
  self.assertEqual([a['href'] for t,a in self.tags if t=='link' and a.get('rel')=='canonical'],[canonical])
  alts={a['hreflang']:a['href'] for t,a in self.tags if t=='link' and a.get('rel')=='alternate'}
  self.assertEqual(set(alts),{'en','zh-CN','de','fr','es','pt','ja','ko','x-default'})
  # Italian night-train translation does not exist: do not invent an hreflang URL.
  for lang,url in alts.items():
   s=(ROOT/urlsplit(url).path.lstrip('/')).read_text()
   self.assertIn('hreflang="ja" href="'+canonical+'"',s)
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.s,re.S)[1])
  self.assertEqual(schema['dateModified'],'2026-11-06')
  self.assertEqual(schema['inLanguage'],'ja')
  self.assertEqual(schema['headline'],re.search(r'<h1>(.*?)</h1>',self.s)[1])
  self.assertIn('2026年11月6日',self.s)
 def test_no_new_tracking_or_affiliate_instrumentation(self):
  scripts=[a for t,a in self.tags if t=='script']
  self.assertEqual(len(scripts),3)
  self.assertEqual([a['src'] for a in scripts if 'src' in a],['https://www.googletagmanager.com/gtag/js?id=G-JWY9K5ZRSF'])
  for marker in ['tpembars.com','data-conversion-','onclick=','iframe','localStorage','utm_','sub_id']:
   self.assertNotIn(marker,self.s)
  for lang in ['', 'en','zh','de','fr','es','it','ja','ko','pt']:
   self.assertEqual((ROOT/lang/'index.html').read_text().count('https://tpembars.com/NTkyOTk4.js?t=592998'),1)
 def test_archive_and_sitemap(self):
  s=(ROOT/'ja/articles/index.html').read_text()
  self.assertEqual(s.count('href="europe-night-train-guide.html"'),1)
  self.assertIn('href="night-trains-europe-guide.html"',s)
  ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
  items={e.find('s:loc',ns).text:e for e in ET.parse(ROOT/'sitemap.xml').findall('s:url',ns)}
  self.assertEqual(items['https://europe-train.com/'+PATH].find('s:lastmod',ns).text,'2026-11-06')
if __name__=='__main__':unittest.main()
