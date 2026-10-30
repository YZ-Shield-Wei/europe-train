# Site integrity and preservation gate

Run before publishing any batch:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/site_audit.py --output /tmp/europe-train-site-audit.json
```

The baseline records all 1,585 original HTML file paths at commit
`4b8bc89af0fdaa8257986cb607a4d4b830edbbde`. This includes old copies outside the
main public surface: do not delete them merely because they are duplicated.
The initial baseline treated 1,348 pages outside build/content/www/components/templates/schema
as the primary public surface. The current audit also includes public build/content/www
aliases (see below), checking their literal HTML links and asset URLs.

The gate fails if an original HTML path disappears, a new missing local href/src
reference is introduced, or a page acquires an unreviewed `noindex` directive.
It reports existing failures without blocking every unrelated repair. A passing
gate therefore does **not** mean the old failures are fixed. The initial baseline
contains 227 missing references, 1,322 www canonicals and 30 separately identified
placeholder article pages. No one should reset the baseline to hide a new failure.

Keep the original path even when updating content and presentation. Redirects,
canonical changes or deliberate retirement require a reviewed path-level plan.
Do not interpret broad design permission as permission to discard old articles.
Content corrections are permitted; the gate does not freeze old inaccurate prose.

The check does not validate JavaScript-generated links, CSS `url()` declarations,
fragment targets, HTTP response status, external websites, factual claims,
translation completeness or visual behavior. Those require separate checks.
No Search Console access is implied, and no ranking or indexing guarantee follows
from a pass. Test the exact final GitHub Pages deployment and selected live URLs
before reporting a batch as published.


## Public duplicate-path coverage

The structural audit includes HTML under `build/`, `content/`, and `www/`. These old public URLs remain as same-topic, same-language redirects with clickable fallback links; they are not excluded just because the directories resemble build output. Only source partials in `components/`, `templates/`, and `schema/` are excluded from full-document checks. All original HTML paths remain covered by the deletion guard.
