# Japanese night-train optional pass links

## Scope and reviewed publication base

Prepared against verified remote main `4819154b3169c03ea36d23e76f02b9e581499015`
in `YZ-Shield-Wei/europe-train`. The connected work GitHub account confirmed the
repository identity, default branch and remote publication instructions.

Only `ja/articles/europe-night-train-guide.html` changes on the public site.
This note and five regression tests accompany it. The existing four official
night-train booking buttons remain the primary entry points and retain their
exact destinations. No new product, script, conversion event, URL parameter,
affiliate account setting or legal acceptance is introduced. No other language
page, canonical, hreflang, archive link, sitemap or historical URL is changed.

The unrelated GA correction was independently deployed in commit
`ce039708494ac07ab0dd547c86d1b316f992902c`. The preparation branch was
fast-forwarded onto that verified latest main before the authorized publication.
All nine Swiss comparison GA changes remain intact. Final integration tests
repeated the checks below; this source note is not deployment evidence.

## Editorial changes

- Add a clearly marked optional advertising section after the existing pass
  reservation guidance, with a Japanese commission disclosure before the links.
- Retain the already-used Japanese Klook short links exactly:
  `https://klook.tpm.li/8Rsd7jNl` and `https://klook.tpm.li/SALNtv2Y`.
  Both have `rel="sponsored noopener"` and an accessible disclosure reference.
- Describe passes as conditional multi-leg options, not night-train tickets,
  sleeper bookings, guaranteed availability or universally cheaper purchases.
  Explain that a single trip may be cheaper with an ordinary ticket.
- Distinguish Interrail's separately paid night-train reservations from mandatory
  reservations included in eligible Trenitalia Pass journeys. Refine the earlier
  general comparison sentence so included charges are not counted twice.
- Explain Trenitalia eligibility and Easy/Comfort accommodation limits without
  promising all private cabins. Link existing Japanese detailed pass guides.
- Preserve old editorial sections and substantive advice. Review the full Japanese
  page, title, metadata, navigation, language labels, source wording and link text.
  Proper product names and the intentional language selector are not untranslated
  editorial copy.

## Rules and link verification, 6 November 2026

Primary sources:

- https://www.interrail.com/en/interrail-passes/what-is-interrail
- https://www.interrail.com/en/terms-conditions/pass-purchase-conditions
- https://help.interrail.com/hc/en-001/articles/11538882203805-What-are-seat-reservations
- https://www.trenitalia.com/en/offers/trenitalia-pass.html

Interrail's current official material permits travellers from around the world;
the draft does not repeat the obsolete Europe-residents-only restriction. It asks
readers to verify country-of-residence, validity, eligibility and service rules.
The 10 September 2026 purchase conditions state reservations are not included.

Trenitalia's current page says the pass is for foreign citizens resident outside
Italy. Easy includes seats and couchettes on Intercity Night; Comfort also covers
the designated T2/double and T3 sleeper services. Eligible reservations are
mandatory and free. All forms of private occupancy are not promised.

Both affiliate buttons were clicked in a browser on 6 November 2026. They reached
the Japanese Klook product pages for Interrail Global Pass (activity 9868) and
Trenitalia Pass (activity 113905), with the existing affiliate identifiers retained
by the short-link redirect. The page itself adds no tracking parameters. No
purchase, login, account change or terms acceptance was attempted.

## Validation, repeated after integrating the GA correction

- Full Python suite: 93 tests pass, including five new affiliate regression tests.
- All existing JavaScript suites pass: conversion behavior, nine-language route
  search and rail-status logic.
- Localized archive structural validation and selected article publication guard
  pass. Site audit retains 1,726 HTML paths, with zero missing local references,
  zero new noindex pages and no deletion/integrity regressions.
- Existing executable scripts match the preparation baseline byte-for-byte.
- CUA browser QA used a supported local-only Sites preview, without Site creation
  or hosting publication. Preview copies suppressed executable scripts to avoid
  polluting analytics; production scripts were not edited.
- Responsive frames at 320, 390, 768 and 1,440 CSS pixels show no horizontal
  overflow (content widths 305, 375, 753 and 1,425 after native scrollbars).
  Affiliate buttons measure 69.6 pixels high on the two phone frames and 45.8
  pixels on the wider frames. Japanese disclosure and cards were visually
  reviewed on phone and desktop layouts.
- Browser tests verify both affiliate destinations, Back navigation, the return
  to official booking links, and the Japanese Trenitalia details link without
  JavaScript. All local destinations and fragments pass automated tests.
- This is preparation, not a claim of conversion improvement or revenue. Existing
  affiliate attribution is retained, but purchases and attribution reporting were
  not tested.

## Publication and rollback

Recheck the current remote main, preserve the independently released GA tag,
review the exact three-file diff, rerun all applicable checks, and create one
commit on that reviewed head followed by a non-forced atomic reference update.
A changed head requires review again. Verify the resulting remote commit, exact
GitHub Pages deployment and production article before reporting success.
Rollback is a normal revert on the latest reviewed main, never a force reset.
