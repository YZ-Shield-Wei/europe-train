# Japanese night-train booking-path pilot

## Baseline and scope

Reviewed main: `1ea051b151b196ddb10d7a7cc79987a917b724c6`.
Production HTML matched that revision on 6 November 2026. Search-result caches
still showed an older page, so they were not treated as the page baseline.

Only the existing Japanese article, its existing archive card, and its sitemap
last-modified date change on the public site. This log and a focused regression
test accompany the change. No new public article, locale, product or redirect.
The original article had eight useful advice sections and four source links but
no dedicated operator booking choices, no explicit per-person versus whole-room
comparison, and no operator-specific pass reservation steps.

## Hypothesis and changes

Making the next step specific to the operator and accommodation may help readers
reach a suitable official booking search with fewer misunderstandings. This is a
usability hypothesis, not measured conversion or revenue growth.

- Add a three-step entry panel and four clearly labelled official booking links.
- Distinguish SNCF first-class couchettes from private occupancy; Nightjet Mini
  Cabins from sleeper rooms; Trenitalia Comfort couchettes from Relax cabins;
  and European Sleeper shared from private Classic accommodation.
- Explain total group cost, included versus additional reservations, pass cost,
  cancellation conditions and date rollover without fixed fare/timetable claims.
- Link to existing Japanese troubleshooting and reservation guidance.
- Preserve every existing body paragraph and section ID, all old URLs, canonical
  and reciprocal eight-language hreflang set plus x-default. No Italian night-
  train translation exists; an unsupported Italian alternate was not added.
- Preserve all executable scripts byte-for-byte. The page does not load the
  site's conversion-events script, so this pilot adds no script, custom event,
  tracking field, affiliate setting or URL parameter. Ten homepage Travelpayouts
  scripts remain unchanged, one per approved homepage.

## Official sources checked on 6 November 2026

- Nightjet booking: https://www.nightjet.com/en/ticket-buchen
- Rome services: https://www.nightjet.com/en/reiseziele/italien/rom
- Couchettes and Mini Cabin: https://www.nightjet.com/en/komfortkategorien/liegewagen
- Private occupancy: https://www.nightjet.com/en/komfortkategorien/ganzes-abteil-buchen
- Pass reservations: https://www.nightjet.com/en/buchung/tarifinformationen/interrail-eurail-paesse
- SNCF night service: https://www.sncf-connect.com/intercites/intercites-nuit
- Paris–Nice: https://www.sncf-connect.com/intercites/trajet/paris/nice
- SNCF English equipment guide: https://www.sncf-connect.com/en-en/intercites/intercites-night
- Trenitalia services/search: https://www.trenitalia.com/it/intercity-notte.html
- Trenitalia accommodation: https://www.trenitalia.com/it/intercity-notte/comfort-a-bordo.html
- European Sleeper: https://www.europeansleeper.eu/
- Timetable: https://www.europeansleeper.eu/timetable
- Classic accommodation: https://www.europeansleeper.eu/travel-class-classic
- Pass instructions: https://www.europeansleeper.eu/interrail
- SNCF pass booking: https://www.interrail.com/en/plan-your-trip/tips-and-tricks/trains-europe/night-trains/intercites-de-nuit
- Trenitalia pass booking: https://www.interrail.com/en/plan-your-trip/tips-and-tricks/trains-europe/night-trains/intercity-notte

European Sleeper's FAQ and pass page conflict on private-compartment pass use.
The article explicitly asks readers to check booking conditions and contact the
operator before payment if unclear. It does not resolve the conflict by guessing.
No short-lived Trenitalia promotional occupancy rule is reproduced.

All 17 distinct external article URLs were checked: 14 returned HTTP 200; the
three SNCF URLs returned HTTP 403 to the direct automated fetch. Their official
content was available through the web research tool and independently reviewed.
No challenge or access restriction was bypassed. This is not a guarantee that
every visitor or every operator booking transaction will work.

## Pre-publication checks

- Full Python suite: 88 tests pass (83 baseline plus five focused tests).
- All existing JavaScript regression suites pass, including nine-language route
  search, conversion-event behavior and rail-status logic.
- Localized-index validation and explicitly selected article publication gate pass.
- Site audit: 1,726 HTML paths retained; no missing local references, new noindex
  pages, deleted URLs or integrity regressions.
- Existing article paragraphs and executable scripts preserved byte-for-byte.
- Internal fragments, schema headline/date/language, reciprocal hreflang,
  canonical, archive link, sitemap date and homepage script count checked.
- Supported Sites local-only preview used for browser QA; no Site registration
  or hosted preview publication. Mobile viewport frames at 320, 390, 768 and
  1,440 CSS pixels have no horizontal overflow; booking links are at least
  45.8 CSS pixels high. Japanese copy and visible cards reviewed at mobile
  widths and desktop. All booking links are normal HTML anchors, independent
  of JavaScript. Nightjet CTA opens the official connection-search form.
- Nightjet's external single-page booking app adds its own history states;
  browser Back did not immediately return to the guide. No claim is made that
  this third-party behavior was fixed.

## Release and rollback

Publication must recheck remote main against the reviewed SHA, create one commit
on that parent, and use a non-forced compare-and-swap branch update. A changed
head requires review before rebuilding. Existing connected GitHub tooling may
provide the authenticated atomic operations without creating or copying a token.
The HTML content must still pass the documented publication guard before writing.
Record the resulting commit, exact Pages run and production verification in the
release report. A branch update alone is not proof of deployment.

Rollback is a normal revert of this single pilot commit on the latest reviewed
main, never a forced branch reset. Recheck Pages and the affected live URLs after
rollback.

## Observation plan

No analytics report was available for this task, so there is no numerical
click-through or booking baseline and no performance claim. Review the existing
Japanese page traffic and only already-configured outbound events if accessible;
confirm their availability first. Compare equivalent periods and traffic sources,
and separate changes in exposure from changes in visitor behavior. Outbound
clicks are not completed bookings or affiliate revenue. Do not add tracking to
fill measurement gaps without separate authorization.
