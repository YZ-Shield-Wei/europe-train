# Amsterdam–Berlin canonical consolidation — 3 November 2026

Technical SEO maintenance, separate from the ten-theme pilot released on 2 November.
Reviewed baseline main: 7dda8c1b6db57213056967684a05d962dc323b36.

Fifteen existing article URLs contained eight languages with identical article bodies within each language. All were self-canonical, split across three alternate-language families. Fourteen were in the sitemap. This is inconsistent discovery/canonical signaling, not evidence of lost traffic or Google's selected canonical.

Use the existing English complete-guide URL (already first in the English archive and in the sitemap), and the existing short train-guide URLs in zh/de/fr/es/pt/ja/ko as primaries. Preserve all fifteen URLs and exact article body bytes; harmonize canonical, og:url, Article mainEntityOfPage, reciprocal hreflang and language switches. Italian is absent and not advertised. Remove only duplicate archive cards and six noncanonical sitemap entries, leaving 371 sitemap URLs. No tracking, scripts, homepage, prices, editorial content or verification dates change.

Validation: 77 Python tests, three Node suites, nine index structural gates and full article structural gate. Independent diff review passed. Cloud browser narrow-frame checks found no horizontal overflow in eight guides and five changed indices; language-switch and archive-link navigation worked. Publication and exact deployment verification are recorded separately in the maintenance execution record; a commit alone is not proof of deployment or indexing.

Observe this technical change separately from pilot content. Do not attribute subsequent traffic changes to either intervention without comparable data; this site-level discovery change is a potential confounder. No traffic, ranking, conversion or revenue benefit is asserted. No new article was added.
