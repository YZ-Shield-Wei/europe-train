import unittest,re
from pathlib import Path
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
LANGS=['en','zh','de','fr','es','it','ja','ko','pt']
PAIRS={'london-paris','paris-amsterdam','berlin-munich','rome-florence','zurich-milan','barcelona-madrid','london-amsterdam','paris-barcelona','paris-milan','milan-venice','vienna-budapest'}
class RouteIntegration(unittest.TestCase):
 def test_cards_and_options(self):
  for rel in ['index.html']+[f'{l}/index.html' for l in LANGS]:
   s=(ROOT/rel).read_text(); cards=re.findall(r'<article class="route-card".*?</article>',s,re.S)
   self.assertEqual(len(cards),11,rel)
   self.assertEqual({re.search(r'id="route-([^"]+)"',c)[1] for c in cards},PAIRS,rel)
   for name in ['origin','destination']:
    options=re.search(r'<select id="'+name+r'".*?</select>',s,re.S)[0]
    values=re.findall(r'<option value="([^"]*)"',options)
    self.assertEqual(len(values),len(set(values)),rel)
    for c in cards:
     for endpoint in re.findall(r'data-(?:from|to)="([^"]+)"',c):self.assertIn(endpoint,values,rel)
 def test_internal_links_and_official_entries(self):
  for rel,l in [('index.html','en')]+[(f'{l}/index.html',l) for l in LANGS]:
   s=(ROOT/rel).read_text()
   for c in re.findall(r'<article class="route-card".*?</article>',s,re.S):
    route=re.search(r'id="route-([^"]+)"',c)[1]
    self.assertRegex(c,r'href="https://',route)
    links=re.findall(r'class="route-guide-link" href="([^"]+)"',c)
    expected=0 if route=='barcelona-madrid' and l in ['it','ja','ko','pt'] else 1
    self.assertEqual(len(links),expected,(rel,route))
    for link in links:
     link=unescape(link);self.assertTrue(link.startswith('/'+l+'/articles/'),link)
     self.assertTrue((ROOT/link.lstrip('/')).is_file(),link)
 def test_home_scripts_preserved(self):
  homes={'index.html'}|{f'{l}/index.html' for l in LANGS}
  for rel in homes:
   s=(ROOT/rel).read_text()
   self.assertEqual(s.count('https://tpembars.com/NTkyOTk4.js?t=592998'),1,rel)
   self.assertIn('G-JWY9K5ZRSF',s)
   self.assertIn('conversion-events.js',s)
   helptext=re.search(r'<p class="planner-help".*?</p>',s,re.S)[0]
   self.assertFalse(re.search(r'six |sechs |six |seis |sei |6路|6개|六条',helptext),rel)
 def test_dynamic_counts(self):
  self.assertIn('cards.length',(ROOT/'js/home-travel.js').read_text())
  self.assertIn('cards.length',(ROOT/'js/home-travel-localized.js').read_text())
