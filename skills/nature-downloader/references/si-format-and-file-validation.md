# Supporting information, formats, and validation

<!-- Modified from Yuan1z0825/nature-skills; see ../../../NOTICE. -->

Load this file when SI, browser-downloaded files, or non-PDF full text is in
scope.

## Supporting Information

- Fetch SI only after an explicit batch-level yes.
- Start from the verified article landing page. Follow only links clearly
  labelled as supplementary/supporting material or returned by a publisher API.
- Do not fabricate filename patterns or treat a guessed URL as evidence.
- Preserve original attachment names when safe and record each attachment's
  source page, format, size, and hash.
- A missing SI file does not invalidate a valid main-text download; record the
  SI result separately.

## Format checks

For PDF:

- response and file begin with `%PDF`;
- page count is non-zero;
- extracted text or rendered pages match title, DOI, authors, or supplement
  identity;
- a login page or HTML error saved with a `.pdf` suffix is a failure.

For HTML/XML:

- content contains the article title or DOI and substantive full text;
- report that the current route yielded HTML/XML, not PDF.

For CAJ or another database-native format:

- report the native format explicitly;
- do not rename it as PDF;
- include the tool needed to open or convert it when known.

For archives and datasets:

- validate the container can be listed;
- preserve file names and checksums;
- never execute downloaded content as part of validation.

## Per-paper manifest

Record:

- normalized identifier and title;
- attempted source URLs and access modes;
- canonical status;
- local relative path and actual format;
- byte size and cryptographic hash;
- retrieval timestamp;
- SI requested/found/downloaded/failed state;
- validation evidence and remaining user action.

Complete the final user response from the manifest, not from console output.
