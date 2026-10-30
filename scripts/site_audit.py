#!/usr/bin/env python3
"""Read-only structural audit. Does not establish accuracy, translation or rankings."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
# Source partials are not standalone documents. Public build/content/www aliases are audited.
EXCLUDED = {'components', 'templates', 'schema'}
HOSTS = {'europe-train.com', 'www.europe-train.com'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.assets, self.canonical, self.robots = [], [], [], []
        self.h1 = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag == 'link':
            if attrs.get('rel') == 'canonical':
                self.canonical.append(attrs.get('href', ''))
            if attrs.get('rel') == 'stylesheet':
                self.assets.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name', '').lower() == 'robots':
            self.robots.append(attrs.get('content', '').lower())
        if tag == 'h1':
            self.h1 += 1

def local_target(source, href):
    """Resolve local URLs including relative paths, encoded filenames and fragments."""
    url = urlsplit(urljoin('https://europe-train.com/' + source, href))
    if url.scheme not in ('http', 'https') or url.netloc.lower() not in HOSTS:
        return None
    path = posixpath.normpath('/' + unquote(url.path).lstrip('/')).lstrip('/')
    if not path or path == '.':
        return 'index.html'
    if url.path.endswith('/'):
        path += '/index.html'
    return path

def collect(root=ROOT):
    root = Path(root)
    all_html = sorted(p.relative_to(root).as_posix() for p in root.rglob('*.html')
                      if '.git' not in p.relative_to(root).parts)
    pages = [name for name in all_html if name.split('/')[0] not in EXCLUDED]
    missing, www, noindex, no_canonical, referenced = [], [], [], [], Counter()
    for name in pages:
        page = Page()
        page.feed((root / name).read_text(encoding='utf-8'))
        if any('www.europe-train.com' in value for value in page.canonical):
            www.append(name)
        if not page.canonical:
            no_canonical.append(name)
        if any('noindex' in value for value in page.robots):
            noindex.append(name)
        for kind, links in [('link', page.links), ('asset', page.assets)]:
            for href in links:
                target = local_target(name, href)
                if target is None:
                    continue
                referenced[target] += 1
                if not (root / target).is_file():
                    missing.append({'source': name, 'href': href, 'target': target, 'kind': kind})
    missing = sorted({json.dumps(row, sort_keys=True) for row in missing})
    return {'all_html_paths': all_html, 'public_html_paths': pages,
            'missing_references': [json.loads(row) for row in missing],
            'www_canonical_pages': www, 'no_canonical_pages': no_canonical,
            'noindex_pages': noindex,
            'unreferenced_public_pages': [name for name in pages if not referenced[name]]}

def regressions(current, baseline):
    deleted = sorted(set(baseline['all_html_paths']) - set(current['all_html_paths']))
    known_missing = {json.dumps(row, sort_keys=True) for row in baseline['missing_references']}
    new_missing = [row for row in current['missing_references']
                   if json.dumps(row, sort_keys=True) not in known_missing]
    new_noindex = sorted(set(current['noindex_pages']) - set(baseline['noindex_pages']))
    return {'deleted_html_paths': deleted, 'new_missing_references': new_missing,
            'new_noindex_pages': new_noindex}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--baseline', type=Path, default=ROOT / 'docs/site-audit-baseline.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    current = collect(args.root)
    baseline = json.loads(args.baseline.read_text())
    findings = regressions(current, baseline)
    report = {'counts': {key: len(value) for key, value in current.items()},
              'regressions': findings, 'current': current,
              'limits': 'Offline HTML href/src audit, not CSS url(), dynamic API, external links, translation, factual accuracy, visual or live availability verification.'}
    data = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(data)
    print(json.dumps({'counts': report['counts'], 'regressions': findings}, ensure_ascii=False, indent=2))
    return 1 if any(findings.values()) else 0

if __name__ == '__main__':
    raise SystemExit(main())
