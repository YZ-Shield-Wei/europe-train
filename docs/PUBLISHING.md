# Safe article publication

The canonical repository is `YZ-Shield-Wei/europe-train`, branch `main`.
Public article files live at `<language>/articles/*.html` at the repository root,
**not** under `www/europe-train`, `build`, or `content`.

## What changed

- `daily_article_full.sh` now checks content by default, regardless of working
  directory. It does not generate, translate, silently ignore errors, or publish.
- Both legacy index-sync commands only validate the nine existing language
  indices. They never copy the English redirect at `articles/index.html` over
  localized pages. Italian is included.
- The old generator exits with an error because it only creates placeholders.
  The old phrase-replacement translator also exits with an error: substituting
  a few headings is not a full translation. Neither modifies public content.
- The API publisher only publishes explicitly listed article/index files after
  all pass validation. It uses the correct repository-root paths, an expected
  branch commit, and one non-forced atomic branch update. It no longer trusts
  `.push_cache.json` (which previously recorded even unsuccessful uploads).
- Credentials are read only from `GITHUB_TOKEN_EUROPE_TRAIN` when `--publish`
  is explicitly present. No token file, home-directory file, or hardcoded token
  is used. No credentials are needed for checks or tests.

## Check and review

Requires Python 3.9+ and Bash; no third-party Python packages are needed.

```bash
python3 -m unittest discover -s tests -v
bash scripts/sync_articles_index.sh

# Audit all existing article files. Existing placeholders intentionally fail.
bash scripts/daily_article_full.sh

# Preview only the intended files, with no network requests or writes.
bash scripts/daily_article_full.sh en/articles/how-to-buy-european-train-tickets.html
```

The structural gate checks allowed paths, regular UTF-8 files, matching HTML
language, nonempty body, localized-index redirects, explicit draft metadata, and known placeholder
text. It is **not** proof of factual accuracy, full translation, valid links,
canonical/hreflang correctness, or visual quality. Existing indices passing this
check does not mean their untranslated labels and metadata are repaired.

Before selecting content for publication, review the complete article, source
links, dated prices/timetables, title/meta/alt text, navigation, language labels,
canonical/hreflang URLs, and links from the localized index. Review each language
independently; do not publish an English body relabeled as another language.
Full translated content can still be published directly once it has been reviewed;
this patch disables only the unsafe automatic scaffolding and phrase substitution.

## Explicit publication after validation

Do not add a new unattended daily publishing schedule until the full workflow has
been validated. Existing cron invoking the old no-argument entry point now only
audits and returns a failure if blocked content remains.

Use a trusted checkout of this publisher, review the exact selected files against
the current remote `main`, and supply that reviewed commit's full 40-character SHA
as `--expect-head`. Provision a repository-scoped credential securely in the
execution environment; never put it into a command, repository file, or chat.

```bash
bash scripts/daily_article_full.sh --publish --expect-head REVIEWED_MAIN_SHA \
  en/articles/reviewed-guide.html \
  it/articles/reviewed-guide.html \
  it/articles/index.html
```

If remote `main` changes, publication stops. Fetch/review again; do not blindly
substitute the new SHA. Authentication, API failures, and branch races stop the
operation rather than being ignored. A timeout may leave an uncertain result;
inspect remote `main` before retrying. New Git objects may exist after a failed
attempt, but article files are not partially published by separate commits.

After publishing, verify the exact commit on remote `main`, the GitHub Pages
build/deployment, the selected production URLs and localized index links. A
successful Git branch update alone is not a verified production deployment.
This patch does not change Pages configuration, introduce a deployment workflow,
or add external advertising/affiliate scripts.

## Existing content requiring a separate editorial repair

The audit flags known placeholder pages rather than
deleting or inventing their content. The existing placeholder pages remain on the
live site until a later content/deployment change repairs or deliberately removes
them. Root duplicate trees are also left unchanged to avoid an unreviewed rebuild.
Other historical one-off scripts are not safe publication entry points and have
not been comprehensively audited; use only the documented guarded workflow.
