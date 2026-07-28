<!-- Modified in the context-engineered edition; see repository NOTICE. -->

# Workflow 7: Bibliography Verification

**Purpose:** Verify metadata already present in citations, BibTeX/RIS files, or
reference-manager exports. This workflow checks work identity and bibliographic
fields; use `nature-citation` instead when the question is whether a source
supports a manuscript claim.

## Procedure

1. Parse every entry without discarding its original text or citation key.
2. Resolve any DOI and compare the resolved work with the cited title and
   authors. A registry `not_found` result alone does not prove invalidity.
3. Check the most work-specific authoritative record, then a second source when
   fields conflict or the first source is incomplete:
   1. DOI resolver and publisher/version-of-record page;
   2. official proceedings, repository, standards body, patent office, or
      institutional record;
   3. an appropriate registry such as Crossref, DataCite, PubMed, arXiv, IEEE
      Xplore, CNKI, or Wanfang;
   4. a curated index or library catalogue;
   5. general web search for discovery only, followed by stronger confirmation.
   Record which authoritative source controls each disputed field.
4. Compare work type, author identity and order, title, venue, dates and
   version, volume, issue, pages or article number, DOI, and edition.
5. Classify each difference:
   - `Critical` — likely different work or unusable identifier;
   - `Warning` — credible version/source conflict requiring judgment;
   - `Info` — harmless representation or citation-style difference.
6. Assign each entry `Verified`, `Check suggested`, `Needs fix`, or
   `Unverifiable`.

## Conflict rules

- Treat anomaly patterns as investigation signals, not automatic fixes. First
  establish the cited manifestation and target citation style.
- Preserve legitimate differences between preprint, accepted manuscript,
  conference paper, online-first article, version of record, issue assignment,
  translated record, dataset/report revision, and book or standard edition.
- Do not infer a year from DOI digits or automatically prefer online, event,
  proceedings, or issue dates.
- Treat accents, transliteration, initials, surname particles, compound
  surnames, group authors, and historical venue names conservatively.
  Normalize their presentation only when the target style permits it; preserve
  verified identity and author order.
- Distinguish page ranges from article numbers. Do not modernize a venue or
  silently replace a preprint identifier with a journal DOI.
- A DOI resolving to a different title and author set is a likely critical
  mismatch, but verify both works before suggesting a replacement.
- For software, products, reports, theses, standards, and manuals, verify the
  issuing body, edition/version, stable identifier or URL, and release date.
- Mark a field unverifiable instead of inventing a correction.

## Report and writeback

Return one summary status per entry and one row per proposed field change:

```text
entry_id
status
severity
field
original_value
suggested_value
source_url_or_identifier
accessed_at
version_or_conflict_note
confidence
```

Include counts by status without allowing the aggregate to hide
`Unverifiable` entries.

Do not edit BibTeX, RIS, Zotero, or another library without explicit
authorization for the exact library/export, entry set, and fields. Before an
authorized writeback, create a timestamped backup or sibling corrected export,
limit changes to the approved entries and fields, keep citation keys unless
requested otherwise, and emit a machine-readable change log. For Zotero, use a
supported authenticated API or export/import route; never edit
`zotero.sqlite` directly. If only a read-only endpoint is available, return a
patch report rather than claiming the library was updated.
