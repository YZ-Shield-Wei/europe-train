"""Keep optional pass sales distinct from official night-train bookings."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "ja/articles/europe-night-train-guide.html"

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class JapaneseNightTrainAffiliates(unittest.TestCase):
    def setUp(self):
        self.text = ARTICLE.read_text()
        self.tags = Tags(self.text).tags

    def test_exact_existing_links_and_clear_disclosure(self):
        affiliate = [attrs for tag, attrs in self.tags if tag == "a" and urlsplit(attrs.get("href", "")).hostname == "klook.tpm.li"]
        self.assertEqual(len(affiliate), 2)
        self.assertEqual({a["href"] for a in affiliate}, {"https://klook.tpm.li/8Rsd7jNl", "https://klook.tpm.li/SALNtv2Y"})
        for a in affiliate:
            self.assertEqual(set(a["rel"].split()), {"sponsored", "noopener"})
            self.assertEqual(a["aria-describedby"], "pass-affiliate-disclosure")
            self.assertFalse(urlsplit(a["href"]).query)
        self.assertIn("当サイトが紹介料を受け取る場合があります", self.text)
        self.assertIn("割引や最安値を保証するものではありません", self.text)

    def test_pass_purchase_is_not_a_night_train_reservation(self):
        for phrase in ["複数区間を周遊する場合のパス比較（広告）", "片道1回や少ない移動回数では、パスが割安とは限りません", "特定の夜行列車の乗車券や寝台予約を直接購入するページではありません", "パスを買うだけでは希望の列車・ベッド・個室は確保されません", "パス発行元・運行会社の現行ルール"]:
            self.assertIn(phrase, self.text)
        self.assertLess(self.text.index('id="operators"'), self.text.index('id="pass-options"'))
        self.assertIn('href="#operators">夜行列車の公式予約先に戻る', self.text)

    def test_fees_distinguish_interrail_and_trenitalia(self):
        interrail = self.text.split('id="interrail-option"', 1)[1].split('id="trenitalia-option"', 1)[0]
        trenitalia = self.text.split('id="trenitalia-option"', 1)[1].split('</section>', 1)[0]
        self.assertIn("夜行列車の座席・寝台予約はパス代に含まれず", interrail)
        self.assertIn("予約料金はパス代に含まれます", trenitalia)
        self.assertIn("予約は必須", trenitalia)
        self.assertIn("イタリア国外に居住する外国籍", trenitalia)
        self.assertIn("指定の2人用・3人用寝台", trenitalia)
        self.assertNotIn("欧州居住者限定", self.text)

    def test_official_buttons_preserved_and_no_tracking_added(self):
        buttons = [a for t, a in self.tags if t == "a" and a.get("class") == "night-book"]
        self.assertEqual(len(buttons), 4)
        self.assertEqual({urlsplit(a["href"]).hostname for a in buttons}, {"www.nightjet.com", "www.sncf-connect.com", "www.trenitalia.com", "www.europeansleeper.eu"})
        self.assertTrue(all(a.get("rel") == "noopener" for a in buttons))
        for marker in ["data-conversion-", "conversion-events.js", "onclick=", "iframe", "localStorage", "utm_", "sub_id", "tpembars.com"]:
            self.assertNotIn(marker, self.text)
        self.assertEqual(len([1 for tag, _ in self.tags if tag == "script"]), 3)
        self.assertEqual(len([1 for tag, a in self.tags if tag == "script" and "src" in a]), 1)

    def test_japanese_cross_links_and_sources(self):
        for slug in ["interrail-global-pass-travel-days-reservations-guide", "trenitalia-pass-rome-florence-venice-guide"]:
            path = f"ja/articles/{slug}.html"
            self.assertIn(f'href="/{path}"', self.text)
            self.assertTrue((ROOT / path).is_file())
            self.assertIn('lang="ja"', (ROOT / path).read_text())
        self.assertIn('href="https://www.interrail.com/en/interrail-passes/what-is-interrail"', self.text)
        self.assertIn('href="https://www.trenitalia.com/en/offers/trenitalia-pass.html"', self.text)

if __name__ == "__main__":
    unittest.main()
