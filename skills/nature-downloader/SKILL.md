---
name: nature-downloader
description: >-
  Implicit use requires an explicit or already-established Nature Portfolio
  context. Lawfully retrieve known academic full text or supporting information
  through OA sources, publisher
  APIs, CNKI, or user-authorized institutional access, and validate downloaded
  artifacts. Within that scope, use for 下载论文、获取全文、CNKI、OA PDF or SI for
  a particular target; collect a missing DOI, title, or URL before retrieval.
  Do not use for discovery, access-control bypass, citation verification, or
  paper analysis.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Literature Downloader

Retrieve a definite paper list through lawful routes. Use
`nature-academic-search` first when the target papers are not yet known.

## Intake

Establish the identifiers, output location, desired format, and whether to fetch
Supporting Information (SI). An explicit SI or main-text-only request is enough;
otherwise ask once for the whole batch before downloading files.

Read [manifest.yaml](manifest.yaml), then load only the references and scripts
matching the selected route.

## Route

1. Normalize DOI/title/URL and identify language and publisher.
2. Chinese literature: use the configured CNKI route.
3. Supported publisher with configured API entitlement: try the API, then lawful
   OA when the API does not yield usable full text.
4. Other English literature: try lawful OA first.
5. Use institutional browser access only with the user's existing authorization.
   Confirm before switching to it after an API-plus-OA failure.
6. For batches, prefer `scripts/batch_download.mjs`; use the focused helper named
   by the manifest for configuration, browser fetching, or verification.

## Non-negotiable boundaries

- Do not bypass paywalls, DRM, access controls, CAPTCHAs, Turnstile, reCAPTCHA,
  OTP, QR approval, passkeys, or identity checks. Keep the tab open and hand
  those steps to the user.
- Do not read, export, log, or request passwords, cookies, browser storage,
  session tokens, OTPs, or recovery codes. Save publisher API keys only through
  the bundled secret-input flow; never echo them.
- Use only a browser session the user has authorized. Do not claim that a fresh
  profile proves missing institutional entitlement.
- Do not invent PDF, SI, resolver, or publisher URLs. Do not turn a failed lawful
  route into an unauthorized-mirror search.
- PDF, HTML, XML, CAJ, archives, and attachments are distinct deliverables.
  Report the format actually obtained.

Load [references/access-safety-and-handoff.md](references/access-safety-and-handoff.md)
before any institutional or browser-authenticated route.

## Validate and record

For every target:

- verify content type and signature (`%PDF` for PDF), non-empty page/content,
  and title or DOI match;
- retain the source URL, access mode, timestamp, format, file hash, SI status,
  and canonical status from `scripts/lib/status-codes.mjs`;
- distinguish success, unavailable-but-readable HTML, no entitlement,
  authentication handoff, ambiguous metadata, and typed failure.

Load
[references/si-format-and-file-validation.md](references/si-format-and-file-validation.md)
when SI or non-PDF formats are involved.

## Completion

Finish when every requested paper has either a validated artifact or an explicit
typed failure, and the batch manifest is complete. Report user action only for
the papers that still require it. Never report a download as successful solely
because a script exited without error.
