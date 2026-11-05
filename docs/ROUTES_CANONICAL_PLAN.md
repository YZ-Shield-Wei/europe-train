# Route-directory canonical consolidation

Technical review: 5 November 2026. Reviewed remote main:
`d9c131a3accb1da54c0820601c57441ddc6bf14c`.

## Path-level decision

- Keep `/routes.html` and all nine localized `/<language>/routes.html` URLs
  available with their full existing bodies. No redirect, noindex, deletion,
  translation, price, timetable or other editorial change is included.
- Use `/en/routes.html` as the English canonical, including from the root alias.
  The two English bodies are byte-identical. The current public site has 57
  links to `/en/routes.html` and no links to `/routes.html` outside reusable
  components/templates. The existing visible language navigation already uses
  the nine localized URLs.
- Keep the other eight localized pages self-canonical. All ten documents get
  the same reciprocal HTML alternate set: en, zh-CN, de, fr, es, it, ja, ko,
  pt, and x-default. Both en and x-default select `/en/routes.html`. The root
  alias is not an alternate target. Each document's og:url matches its canonical.
- Replace only the root routes sitemap block with the nine canonical route
  entries and matching alternate sets. Date these changed technical entries
  2026-11-05; preserve all unrelated sitemap bytes and editorial review dates.

## Preservation and review

All ten complete bodies were read. Each localized page contains substantive
content in its declared language. Existing internal links resolve to real
files. The production root page and all nine language pages were opened and
their visible language navigation exercised before the change.

`tests/test_routes_canonical_family.py` records body and script hashes from the
reviewed main, checks canonical/og:url/alternate reciprocity, declared languages,
visible language links and sitemap consistency. A separate pre-publication
byte comparison verifies that all unrelated sitemap entries stay unchanged;
this is deliberately not a permanent test freezing future article additions.
The existing site-integrity gate remains unchanged. No stylesheet, brand asset,
homepage, affiliate link, analytics parameter or third-party script is changed.
The original ten homepage Travelpayouts Drive copies remain untouched.

Source components and the disruption template retain nine links to the working
root alias. `update_navigation.py` consumes those components and could reproduce
alias links if run. This separate source-navigation debt is not repaired here;
do not run that broad updater as part of this change.

## Publication and rollback

The article-only publisher in PUBLISHING.md does not accept route-directory or
sitemap files. For this reviewed non-article patch, use the connected GitHub
Git-data tools: one tree based on the reviewed main tree, one child commit,
and one non-forced main update with expected_sha equal to the reviewed head.
Include only the ten route HTML files, sitemap, this plan and the focused test.
If main changes, stop and review the new head rather than replacing the lease.
Do not change or bypass the article publisher's allowed-path validation.

Afterward verify the exact commit's Pages deployment and all ten production
pages. A successful branch update alone is not a verified live publication.
To roll back, make a new commit restoring only this patch's files from the
reviewed base, after checking current main for later edits. Keep the same
expected-head protection and recheck Pages and live URLs. Never force-reset main.

## Technical sources

Google Search Central, checked 5 November 2026:
- [Canonical URL consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Localized page variants](https://developers.google.com/search/docs/specialty/international/localized-versions)

These changes make site signals consistent. They do not prove indexation or
promise a ranking or traffic improvement.
