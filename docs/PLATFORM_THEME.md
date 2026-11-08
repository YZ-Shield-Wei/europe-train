# Platform presentation theme

The November 2026 design handoff's final Direction A is adapted to the existing
static site. It uses warm white, navy, signal yellow, condensed Archivo headings,
square-edged cards, and departure-board route rows. The existing logo and images
remain in use. Prototype-only copy, illustrative times, pass scoring, subscriptions,
React/Babel, and alternative directions B/C are not shipped.

## Scope and maintenance

The seven existing primary CSS URLs now load the self-hosted font declarations,
their byte-identical prior stylesheet in `css/platform-base/`, and either
`platform-home.css` or `platform-content.css`. All CSS asset URLs are absolute.
No new JavaScript, tracking, network service, or build dependency is required.

The root and nine locale homepages move the existing, unchanged planner section
immediately after the hero. This matches the visual and keyboard order. No text,
links, IDs, events, head metadata, analytics, affiliate parameters, or scripts
inside those pages are changed. Other HTML, all JavaScript, sitemap and robots
files are retained. Existing old placeholder/redirect pages are not rewritten.

The design is responsive and retains native selects, details, language menus,
no-JavaScript route links, focus indicators, reduced motion and print behavior.
Do not replace real guide data with the design prototype's sample durations.

## Font provenance

Fonts were obtained from the official Google Fonts service and are served from
this site rather than making visitor requests to Google Fonts. The original
SIL Open Font License files are included in `fonts/`.

- Archivo variable width 62–125%, weight 400–900, Latin and Latin extended:
  https://fonts.google.com/specimen/Archivo
- JetBrains Mono, weight 700, Latin:
  https://fonts.google.com/specimen/JetBrains+Mono
- License sources:
  https://github.com/google/fonts/blob/main/ofl/archivo/OFL.txt
  https://github.com/google/fonts/blob/main/ofl/jetbrainsmono/OFL.txt

Chinese, Japanese and Korean use the existing system-font fallbacks. No large
remote CJK font bundle is introduced.

## Checks

Run `python3 -m unittest discover -s tests -v` and
`bash scripts/sync_articles_index.sh`. The Platform tests cover CSS imports,
self-hosted font files and licenses, and homepage keyboard order.

Browser QA covers all nine homepage languages at 320, 390, 768 and 1440 CSS pixels,
plus guide, Chinese guide, passes, archive, routes, service status and historical
disruption templates. Also check route selection, swap, same-city error, empty
results/reset, region filters, disclosures, language-menu Escape, anchor links,
keyboard focus order and primary affiliate links after changing the theme.
Preview copies block remote analytics/ad scripts; production scripts are preserved.

## Publication and rollback

Baseline before the restyle: `beef797df53c791015f7c56d6a7fc868b19aef1d`.
Publish one reviewed commit using that expected head and a non-forced atomic ref
update. If main changes, inspect the new changes and repeat the relevant checks
before publishing; never substitute the new head without review.

Verify the exact published SHA, its successful Pages deployment, and the live
homepage, CSS/font assets and representative localized pages. A successful Git
update alone is not a verified deployment.

For rollback, revert only the restyle commit on top of the current main, preserving
any later commits. The old CSS is also retained byte-for-byte in platform-base.
Do not force-reset main or use the legacy bulk publisher for this change.
