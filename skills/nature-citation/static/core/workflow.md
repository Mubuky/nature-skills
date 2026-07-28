<!-- Modified in the context-engineered edition; see repository NOTICE. -->

# Workflow

## 1. Segment claims

Split the supplied prose into stable, focused claim units such as `S001`.
Preserve order and wording. Skip connective text unless the user asks to cite
every sentence.

## 2. Discover candidates

Create precise and synonym-expanded queries, then search appropriate scholarly
indexes. `scripts/nature_citation.py` provides a Crossref-based candidate
discovery path:

```bash
python3 "$SKILL_DIR/scripts/nature_citation.py" \
  --text-file manuscript.txt \
  --scope cns \
  --outdir /tmp/nature-citation \
  --with-artifacts
```

Search output is metadata-only. It must be named and presented as candidates,
not references, and must not contain insertion markers or import-ready
ENW/RIS/RDF records.

## 3. Verify identity and journal scope

Confirm title, authors, version, DOI, venue, and current journal-family status.
Strict portfolio scope is exact-match and fails closed for unknown titles; use
the current official journal page when the distinction matters.

## 4. Screen semantic support

Read the abstract or full text. For every selected claim–source pair, record:

- claim/segment ID and DOI or stable candidate key;
- support grade: `strong`, `partial`, or `background`;
- evidence basis: `abstract`, `publisher_page`, or `full_text`;
- exact page/section/figure/table/paragraph locator;
- a bounded excerpt or precise paraphrase;
- checked URL and access time;
- contradiction and retraction status.

`metadata-only` and `contradictory/limiting` items are never inserted as
support. A review can provide context but should not silently replace available
primary evidence for an experimental claim.

## 5. Export screened records

Create a reviewed selection JSON, then run:

```bash
python3 "$SKILL_DIR/scripts/nature_citation.py" \
  --text-file manuscript.txt \
  --scope cns \
  --screened-selection screened-selection.json \
  --format enw \
  --output-file references.enw
```

The script rejects missing locators, metadata-only evidence, unresolved
contradiction/retraction checks, and candidates not found in the discovery run.
Missing bibliographic fields remain absent.

## 6. Report

Return the claim-to-source mapping, support grade and evidence locator, final
reference-manager file if screening passed, retrieval/scope gaps, and any claim
that should be narrowed. Candidate discovery alone is an intermediate result,
not a completed citation task.
