# Provider routing and configuration

<!-- Modified from Yuan1z0825/nature-skills; see ../../../NOTICE. -->

Load this file when selecting or configuring a retrieval provider.

## Required input

Normalize at least one stable identifier: DOI, PMID, exact title, or canonical
article URL. Resolve ambiguous metadata before any file request.

## Routing order

```text
Chinese article or explicit CNKI source
  -> configured CNKI route

English article from a supported publisher with configured entitlement
  -> publisher API
  -> lawful article-level OA
  -> confirmed institutional browser route

Other English article
  -> lawful article-level OA
  -> confirmed institutional browser route
```

Lawful OA includes publisher OA pages, PubMed Central, Unpaywall-resolved copies,
arXiv, and repositories that actually expose the requested article. A related
title or search snippet is not a full-text source.

## Configuration

- Library configuration: `scripts/configure_school.py`
- Publisher credentials: `scripts/configure_credentials.py`
- Batch orchestration: `scripts/batch_download.mjs`
- Browser-context PDF transfer: `scripts/browser_pdf_downloader.mjs`
- PDF text check: `scripts/extract_pdf_text.py`

Configure lazily: library settings only for CNKI or institutional routes, and a
publisher credential only when that provider is selected. Start from the actual
library resource/database URL the user uses; do not guess institution domains
from the school name.

Provider configuration and network access are optional capabilities. When a
dependency is unavailable, report the missing capability and continue with any
remaining lawful route rather than silently changing the target or format.

## Route evidence

The manifest must show every attempted route in order, its result, and why the
next route was selected. A successful publisher API fetch may record OA as not
checked; do not label the item non-OA merely because OA resolution was skipped.
