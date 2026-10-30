"""Reusable snippets must not reintroduce repaired factual/schema defects."""
import html,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SourceTemplates(unittest.TestCase):
 def test_faq_schema_matches_visible_reviewed_answers(self):
  snippet=(ROOT/'schema/faq-schema.html').read_text();data=json.loads(re.search(r'<script[^>]*>(.*?)</script>',snippet,re.S)[1]);visible=(ROOT/'zh/faq.html').read_text();sections=re.findall(r'<section class="faq-item".*?</section>',visible,re.S)
  clean=lambda value:html.unescape(re.sub('<[^>]+>','',value)).strip()
  answers=[(clean(re.search('<h2>(.*?)</h2>',s,re.S)[1]),clean(re.search('<p>(.*?)</p>',s,re.S)[1])) for s in sections]
  self.assertEqual(len(answers),10);self.assertEqual([(i['name'],i['acceptedAnswer']['text']) for i in data['mainEntity']],answers);self.assertNotIn('261/2004',snippet)
 def test_disruption_template_is_historical_and_json_valid(self):
  template=(ROOT/'templates/disruption-detail.html').read_text();blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',template,re.S);self.assertEqual(len(blocks),2);schemas=[json.loads(b) for b in blocks];self.assertEqual(schemas[1]['@type'],'Article');self.assertIn('Historical disruption record — not live status',template)
  for forbidden in ['currently','current status','www.europe-train.com']:self.assertNotIn(forbidden,template)
  for token in ['lang','id','title','status','status_color','description','description_short','operator_name','country','published_at','published_at_formatted','disruption_type','severity','start_time_formatted','affected_stations','source_url','#if affected_stations','#each affected_stations','this','/each','/if','#if source_url']:self.assertIn('{{'+token+'}}',template)
if __name__=='__main__':unittest.main()
