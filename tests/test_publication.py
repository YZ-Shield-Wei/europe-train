"""Offline regression tests. No test uses real credentials or GitHub requests."""

import contextlib
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import publication_guard as guard
import push_all_articles_api as publisher

HEAD = "a" * 40
NEW_HEAD = "b" * 40


def page(lang="en", body="A reviewed article with travel information.", head=""):
    return f'<html lang="{lang}"><head><title>Guide</title>{head}</head><body>{body}</body></html>'


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_utf8_and_italian(self):
        self.write("it/articles/guide.html", page("it", "Viaggiare in treno è comodo."))
        result = guard.prepare_files(["it/articles/guide.html"], self.root)
        self.assertIn("è comodo", result["it/articles/guide.html"])
        self.assertIn("it/articles/index.html", guard.index_paths())

    def test_placeholder_entities_and_tags_are_blocked(self):
        for body in ("Article content coming soon...", "Article <b>content</b> coming&nbsp;soon...", "[TODO]"):
            with self.subTest(body=body):
                self.write("en/articles/guide.html", page(body=body))
                with self.assertRaisesRegex(ValueError, "placeholder"):
                    guard.prepare_files(["en/articles/guide.html"], self.root)

    def test_spanish_and_portuguese_todo_is_not_a_draft_marker(self):
        self.write("es/articles/guide.html", page("es", "Todo lo que necesitas para viajar."))
        guard.prepare_files(["es/articles/guide.html"], self.root)

    def test_wrong_language_redirect_empty_body_and_draft_blocked(self):
        cases = [page("de"), page(head='<meta http-equiv="Refresh" content="0; url=/en/articles/">'),
                 page(body=""), page(head='<meta name="publication-status" content="draft">')]
        for content in cases:
            with self.subTest(content=content):
                self.write("en/articles/index.html", content)
                with self.assertRaises(ValueError):
                    guard.prepare_files(["en/articles/index.html"], self.root)

    def test_existing_article_redirect_alias_is_preserved(self):
        self.write("en/articles/tag-guide.html", page(head='<meta http-equiv="refresh" content="0; url=/en/articles/">'))
        guard.prepare_files(["en/articles/tag-guide.html"], self.root)

    def test_wrong_prefix_traversal_and_symlinks_blocked(self):
        self.write("en/articles/guide.html", page())
        for name in ("www/europe-train/en/articles/guide.html", "../en/articles/guide.html",
                     "/en/articles/guide.html", "en/articles/../guide.html", "en/./articles/guide.html"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                guard.prepare_files([name], self.root)
        (self.root / "en/articles/link.html").symlink_to(self.root / "en/articles/guide.html")
        with self.assertRaises(ValueError):
            guard.prepare_files(["en/articles/link.html"], self.root)

    def test_all_selected_files_preflight_before_any_api(self):
        self.write("en/articles/guide.html", page())
        self.write("de/articles/guide.html", page("de", "Article content coming soon..."))
        with patch.object(publisher, "ROOT", self.root), patch.object(publisher, "GitHubAPI") as api:
            with contextlib.redirect_stderr(io.StringIO()):
                result = publisher.main(["--publish", "--expect-head", HEAD,
                                         "en/articles/guide.html", "de/articles/guide.html"])
            self.assertEqual(result, 1)
            api.assert_not_called()

    def test_default_preview_does_not_read_token_or_use_network(self):
        self.write("en/articles/guide.html", page())
        with patch.object(publisher, "ROOT", self.root), patch.object(publisher, "GitHubAPI") as api:
            original_get = publisher.os.environ.get
            def safe_get(key, default=None):
                if key == "GITHUB_TOKEN_EUROPE_TRAIN":
                    raise AssertionError("must not read token")
                return original_get(key, default)
            with patch.object(publisher.os.environ, "get", side_effect=safe_get):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = publisher.main(["en/articles/guide.html"])
            self.assertEqual(result, 0)
            api.assert_not_called()

    def test_publication_requires_paths_and_reviewed_head(self):
        for args in (["--publish"], ["--publish", "en/articles/guide.html"],
                     ["--publish", "--expect-head", HEAD]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    publisher.main(args)

    def test_token_must_come_from_explicit_environment(self):
        self.write("en/articles/guide.html", page())
        with patch.object(publisher, "ROOT", self.root), patch.dict(publisher.os.environ, {}, clear=True):
            with patch.object(publisher, "GitHubAPI") as api:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    result = publisher.main(["--publish", "--expect-head", HEAD, "en/articles/guide.html"])
                self.assertEqual(result, 1)
                api.assert_not_called()


class FakeAPI:
    def __init__(self, existing=None, head=HEAD, fail=None, truncated=False):
        self.calls = []
        self.existing = existing or {}
        self.head = head
        self.fail = fail
        self.truncated = truncated

    def __call__(self, method, path, data=None):
        self.calls.append((method, path, data))
        if self.fail == (method, path):
            raise RuntimeError("simulated denied or uncertain API request")
        if path == "/git/ref/heads/main":
            return {"object": {"sha": self.head}}
        if path == f"/git/commits/{HEAD}":
            return {"tree": {"sha": "old-tree"}}
        if path == "/git/trees/old-tree?recursive=1":
            return {"truncated": self.truncated, "tree": [
                {"path": path, "sha": sha} for path, sha in self.existing.items()]}
        if path == "/git/trees":
            return {"sha": "new-tree"}
        if path == "/git/commits":
            return {"sha": NEW_HEAD}
        if path == "/git/refs/heads/main":
            return {"object": {"sha": NEW_HEAD}}
        raise AssertionError(f"Unexpected request: {method} {path}")


class PublisherTests(unittest.TestCase):
    def test_one_atomic_update_with_correct_root_paths(self):
        api = FakeAPI()
        files = {"en/articles/guide.html": page(), "it/articles/guide.html": page("it")}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(publisher.publish(files, HEAD, api), NEW_HEAD)
        self.assertEqual(publisher.REPO, "YZ-Shield-Wei/europe-train")
        tree = next(data for method, path, data in api.calls if method == "POST" and path == "/git/trees")
        self.assertEqual(tree["base_tree"], "old-tree")
        self.assertEqual([e["path"] for e in tree["tree"]], list(files))
        self.assertEqual(api.calls[-1], ("PATCH", "/git/refs/heads/main", {"sha": NEW_HEAD, "force": False}))
        self.assertEqual(sum(method == "PATCH" for method, _, _ in api.calls), 1)

    def test_existing_unchanged_content_needs_no_write_or_cache(self):
        files = {"en/articles/guide.html": page()}
        api = FakeAPI({name: publisher.blob_sha(body) for name, body in files.items()})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(publisher.publish(files, HEAD, api), HEAD)
        self.assertTrue(all(method == "GET" for method, _, _ in api.calls))

    def test_wrong_head_truncated_tree_and_get_failure_stop_before_writes(self):
        for api in (FakeAPI(head=NEW_HEAD), FakeAPI(truncated=True), FakeAPI(fail=("GET", "/git/ref/heads/main"))):
            with self.subTest(api=api), self.assertRaises(RuntimeError):
                publisher.publish({"en/articles/guide.html": page()}, HEAD, api)
            self.assertTrue(all(method == "GET" for method, _, _ in api.calls))

    def test_failed_commit_does_not_update_branch(self):
        api = FakeAPI(fail=("POST", "/git/commits"))
        with self.assertRaises(RuntimeError):
            publisher.publish({"en/articles/guide.html": page()}, HEAD, api)
        self.assertFalse(any(method == "PATCH" for method, _, _ in api.calls))

    def test_branch_race_is_not_forced_or_retried(self):
        api = FakeAPI(fail=("PATCH", "/git/refs/heads/main"))
        with self.assertRaises(RuntimeError):
            publisher.publish({"en/articles/guide.html": page()}, HEAD, api)
        self.assertEqual(sum(method == "PATCH" for method, _, _ in api.calls), 1)
        self.assertFalse(api.calls[-1][2]["force"])

    def test_credential_bearing_redirects_are_disabled(self):
        self.assertIsNone(publisher.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.example"))


class EntryPointTests(unittest.TestCase):
    def test_indices_preserved_from_arbitrary_working_directory(self):
        root = SCRIPTS.parent
        before = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in guard.index_paths()}
        for script in ("sync_articles_index.sh", "sync_all_sites.sh"):
            result = subprocess.run(["bash", str(SCRIPTS / script)], cwd="/tmp", capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in guard.index_paths()})

    def test_daily_entrypoint_fails_closed_on_isolated_placeholder(self):
        # Keep the regression independent of production articles, which may be repaired.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            for name in ("daily_article_full.sh", "push_all_articles_api.py", "publication_guard.py"):
                (scripts / name).write_bytes((SCRIPTS / name).read_bytes())
            article = root / "en/articles/fixture.html"
            article.parent.mkdir(parents=True)
            article.write_text(page(body="Article content coming soon."), encoding="utf-8")
            result = subprocess.run(["bash", str(scripts / "daily_article_full.sh"),
                                     "en/articles/fixture.html"],
                                    cwd="/tmp", capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("placeholder", result.stderr)

    def test_legacy_generation_and_phrase_translation_disabled(self):
        for script in ("generate_daily_article.py", "translate_article_content.py"):
            result = subprocess.run([sys.executable, str(SCRIPTS / script)], cwd="/tmp", capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("disabled", result.stderr)


if __name__ == "__main__":
    unittest.main()
