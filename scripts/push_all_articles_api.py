#!/usr/bin/env python3
"""Preview explicitly selected articles; publish only with --publish --expect-head SHA.

No local hash cache, home-directory credentials, or alternate repository targets.
All selected content is validated before a single atomic, non-forced branch update.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from publication_guard import ROOT, article_paths, prepare_files

REPO = "YZ-Shield-Wei/europe-train"
BRANCH = "main"
API_BASE = f"https://api.github.com/repos/{REPO}"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the Authorization header to another URL.


class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.opener = build_opener(NoRedirect())

    def __call__(self, method, path, data=None):
        payload = None if data is None else json.dumps(data).encode("utf-8")
        request = Request(API_BASE + path, data=payload, method=method, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "europe-train-article-publisher",
        })
        try:
            with self.opener.open(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            raise RuntimeError(f"GitHub {method} {path} failed (HTTP {error.code}); stopped.") from None
        except (URLError, TimeoutError, OSError, ValueError):
            raise RuntimeError(
                f"GitHub {method} {path} did not return a confirmed result; "
                "inspect the remote branch before retrying."
            ) from None


def blob_sha(content):
    data = content.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def publish(files, expected_head, api):
    head = api("GET", f"/git/ref/heads/{BRANCH}")["object"]["sha"]
    if head != expected_head:
        raise RuntimeError("Remote main differs from --expect-head; fetch and review before publishing.")
    base_tree = api("GET", f"/git/commits/{head}")["tree"]["sha"]
    tree = api("GET", f"/git/trees/{base_tree}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("Remote tree is truncated; cannot safely compare selected files.")
    current = {entry["path"]: entry["sha"] for entry in tree["tree"]}
    changes = [{"path": path, "mode": "100644", "type": "blob", "content": content}
               for path, content in files.items() if current.get(path) != blob_sha(content)]
    if not changes:
        print("No changes: selected files already match remote main.")
        return head
    tree_sha = api("POST", "/git/trees", {"base_tree": base_tree, "tree": changes})["sha"]
    commit = api("POST", "/git/commits", {
        "message": f"content: publish {len(changes)} validated article files",
        "tree": tree_sha, "parents": [head],
    })["sha"]
    # A racing branch update must fail; no force, retry, or partial per-file commits.
    result = api("PATCH", f"/git/refs/heads/{BRANCH}", {"sha": commit, "force": False})
    if result["object"]["sha"] != commit:
        raise RuntimeError("Branch update was not confirmed; inspect remote main before retrying.")
    print(f"Published {len(changes)} files in commit {commit}. Verify Pages deployment separately.")
    return commit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true", help="explicitly enable remote writes")
    parser.add_argument("--expect-head", help="reviewed 40-character main commit SHA; required to publish")
    parser.add_argument("files", nargs="*", help="explicit <language>/articles/*.html paths")
    args = parser.parse_args(argv)
    if args.publish and (not args.files or not re.fullmatch(r"[0-9a-f]{40}", args.expect_head or "")):
        parser.error("publication requires explicit file paths and --expect-head <reviewed commit SHA>")
    try:
        files = prepare_files(args.files or article_paths(), ROOT)
        print(f"Target: {REPO}:{BRANCH}; paths are relative to repository root.")
        for path in files:
            print(f"  {path}")
        if not args.publish:
            print("CHECK ONLY: no network requests or changes. Translation/fact review is still required.")
            return 0
        token = os.environ.get("GITHUB_TOKEN_EUROPE_TRAIN", "").strip()
        if not token:
            raise ValueError("GITHUB_TOKEN_EUROPE_TRAIN is required for publication; no credential files are read.")
        publish(files, args.expect_head, GitHubAPI(token))
    except (ValueError, RuntimeError, KeyError, TypeError) as error:
        if isinstance(error, (KeyError, TypeError)):
            print("Publication stopped: unexpected GitHub response; inspect remote main before retrying.", file=sys.stderr)
        else:
            print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
