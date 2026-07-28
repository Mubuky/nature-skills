---
name: nature-ref-verifier
description: >-
  Cross-check an existing bibliography or reference against authoritative
  sources at field level—authors/order, title, venue, year, volume/issue, pages,
  and DOI—and report conflicts or safe corrections. Use for 核对参考文献、
  文献验证、ref check or bibliography cleanup. Do not judge claim support,
  discover literature, download papers, or rewrite citation style alone.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Reference Verifier

Verify metadata already present in a single citation, bibliography, BibTeX file,
or Zotero export. Route claim-to-source support questions to `nature-citation`.

## Workflow

1. Parse each entry without discarding the original text.
2. Resolve any DOI and compare its landing record to the cited work.
3. Query the most authoritative applicable source, then a second source when
   fields conflict or the first source is incomplete.
4. Compare authors/order, title, work type, venue, dates/version, volume, issue,
   pages/article number, DOI, and edition.
5. Classify differences:
   - `Critical`: identifies a different work or makes the citation unusable;
   - `Warning`: credible source/version conflict needs judgment;
   - `Info`: harmless representation or style difference.
6. Return `Verified`, `Check suggested`, `Needs fix`, or `Unverifiable`.

Read [manifest.yaml](manifest.yaml) and load only the source/conflict, pattern,
report, or writeback reference needed for this request. Independent records may
be checked in parallel; final conflict resolution must use one consistent source
hierarchy.

## Evidence rules

- Crossref 404 does not by itself prove a DOI is invalid.
- A search snippet is discovery evidence, not final metadata evidence.
- Prefer the DOI/publisher landing page, official proceedings, repository record,
  or authoritative Chinese database appropriate to the work.
- Preserve online-first versus issue assignment, preprint versus version of
  record, conference versus journal, and edition differences; do not silently
  collapse them.
- Treat accents, transliteration, compound surnames, initials, group authors,
  and historical venue names conservatively.
- Mark a field unverifiable instead of inventing a correction.

## Output and writes

For every proposed change, include the entry ID, field, original value,
suggested value, severity, source URL/identifier, access date, and conflict note.
Do not write to BibTeX, Zotero, or another library without explicit authorization.
Before an authorized writeback, preserve the original and provide a change log.

Finish when each entry has a status, every correction has authoritative evidence,
and unresolved conflicts are visible.
