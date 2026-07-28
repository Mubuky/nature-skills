<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# `nature-citation` Skill

[中文说明](README.md)

`nature-citation` splits manuscript passages or scientific claims into citable units and finds supporting references from Nature Portfolio, the Science family, and Cell Press.

## What To Use It For

- Add citations to key claims in an introduction, discussion, or reviewer response.
- Split long passages into stable claim units such as `S001` and `S002`.
- Restrict evidence to Nature, Science, Cell, and their subjournals, or keep only flagship journals.
- Treat metadata matches as candidates; after semantic review, record evidence
  locators and support strength.
- Export only screened selections with traceable evidence for Zotero, EndNote,
  or other reference managers.

## Typical Requests

- "Split this introduction paragraph and add Nature-series citations."
- "Use only CNS and subjournal papers from the last five years to support these claims."
- "These DOIs have been screened and mapped to their claims; validate the
  selection record and export a Zotero-importable file."

## What You Need To Provide

- Passage or claim list; known DOIs can be supplied as candidates for the
  corresponding claims.
- Journal scope, year range, whether reviews are allowed, and whether only flagship journals should be kept.
- Target citation style and export format such as `RIS`, `ENW`, or Zotero `RDF`.

## Outputs

- Claim-segmentation and candidate tables; discovery produces JSON/TSV/Markdown
  review artifacts only.
- A screened claim-to-source map with support grade, evidence locator, check
  time, and contradiction/retraction status.
- A reference-manager file plus screening audit only after the screened-selection
  gate passes.

## Boundaries

- Title or metadata matches remain candidates and never produce insertion
  markers or final reference files.
- Candidate papers are support options, not a guarantee that the final citation is appropriate.
- Blogs, press releases, and search snippets are not used as sole evidence.
- When a paper supports a nearby but not identical claim, the evidence mismatch is stated explicitly.

## Related Skills

- `nature-academic-search`: broader literature search and citation-metric audits.
- `nature-ref-verifier`: verify selected reference metadata.
- `nature-writing`: integrate citation choices back into manuscript argument.
