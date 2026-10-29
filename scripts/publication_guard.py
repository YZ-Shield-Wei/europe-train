#!/usr/bin/env python3
"""Read-only checks for the canonical, root-level article publishing surface.

These structural checks are not a translation or factual-accuracy review.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "de", "fr", "es", "it", "ja", "ko", "pt", "zh")
PLACEHOLDERS = re.compile(
    r"(?i:article\s+content\s+coming\s+soon|lorem\s+ipsum)|\[TODO\]|\bTODO\s*:|\bTBD\b"
)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.languages = []
        self.redirect = False
        self.draft = False
        self.text = []
        self.body = False
        self.inside_body = False
        self.body_text = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.languages.append(attrs.get("lang", "").lower().split("-")[0])
        if tag == "body":
            self.body = True
            self.inside_body = True
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "meta":
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.redirect = True
            if (attrs.get("name", "").lower() == "publication-status"
                    and attrs.get("content", "").lower() != "published"):
                self.draft = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.inside_body = False
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.text.append(data)
            if self.inside_body:
                self.body_text.append(data)


def article_paths(root=ROOT):
    return [p.relative_to(root).as_posix() for lang in LANGUAGES
            for p in sorted((root / lang / "articles").glob("*.html"))]


def index_paths():
    return [f"{lang}/articles/index.html" for lang in LANGUAGES]


def prepare_files(paths, root=ROOT):
    """Validate every selected file before returning an immutable content snapshot."""
    root = root.resolve()
    files, errors = {}, []
    for name in sorted(set(paths)):
        path = PurePosixPath(name)
        if (len(path.parts) != 3 or path.parts[0] not in LANGUAGES
                or path.parts[1] != "articles" or path.suffix != ".html"
                or path.as_posix() != name or ".." in path.parts):
            errors.append(f"{name}: only <language>/articles/*.html is allowed")
            continue
        local = root / name
        try:
            if local.resolve(strict=True) != local or not local.is_file():
                raise ValueError("symlinks and non-files are not allowed")
            content = local.read_text(encoding="utf-8")
        except (OSError, ValueError) as error:
            # Do not print arbitrary filesystem or file contents.
            errors.append(f"{name}: cannot read a regular UTF-8 file ({type(error).__name__})")
            continue
        page = Page()
        page.feed(content)
        visible = " ".join(" ".join(page.text).split())
        problems = []
        if page.languages != [path.parts[0]]:
            problems.append("HTML language must match the path")
        if not page.body or not "".join(page.body_text).strip():
            problems.append("missing HTML body/content")
        if page.redirect and path.name == "index.html":
            problems.append("localized article indices must not redirect")
        if page.draft:
            problems.append("publication-status is not published")
        if PLACEHOLDERS.search(visible):
            problems.append("placeholder/draft text")
        if problems:
            errors.append(f"{name}: {', '.join(problems)}")
        else:
            files[name] = content
    if not paths:
        errors.append("no article files selected or found")
    if errors:
        raise ValueError("Publication blocked:\n" + "\n".join(errors))
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indices", action="store_true", help="check all nine existing localized indices")
    parser.add_argument("files", nargs="*", help="explicit repository-relative article paths; default: audit all")
    args = parser.parse_args(argv)
    if args.indices and args.files:
        parser.error("--indices cannot be combined with file paths")
    paths = index_paths() if args.indices else args.files or article_paths()
    try:
        files = prepare_files(paths)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"PASS: {len(files)} files passed structural checks; no files changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
