<!-- Modified in the context-engineered edition; see repository NOTICE. -->

# Script usage

Use `scripts/nature_citation.py` for Crossref candidate discovery and validated
reference-manager export.

## Candidate discovery

```bash
python3 "$SKILL_DIR/scripts/nature_citation.py" \
  --claim "CLAIM TEXT" \
  --scope nature \
  --from-year 2020 \
  --outdir /tmp/nature-citation \
  --with-artifacts
```

Useful inputs include `--text-file`, repeated `--claim`, `--doi-file`,
`--batch-size`, `--max-segments`, `--rows`, `--per-segment`, `--mailto`, and
`--sleep`. Discovery writes candidate JSON and optional TSV/Markdown review
artifacts. It deliberately does not write insertion text or ENW/RIS/RDF.

## Screened selection schema

```json
{
  "selections": [
    {
      "segment_id": "S001",
      "doi": "10.0000/example",
      "support_grade": "strong",
      "evidence_basis": "full_text",
      "evidence_locator": "Results, paragraph 3; Fig. 2b",
      "evidence_paraphrase": "The experiment directly tests the mapped relation.",
      "checked_url": "https://doi.org/10.0000/example",
      "checked_at": "2026-07-28T12:00:00+08:00",
      "contradiction_status": "none_found",
      "retraction_status": "none_found"
    }
  ]
}
```

Use a short evidence excerpt only when copyright limits allow it; a precise
paraphrase is sufficient. The selection is an auditable decision record, not a
claim that a limited search was exhaustive.

## Final export

Pass `--screened-selection`, choose `--format enw|ris|zotero-rdf`, and provide
an appropriate `--output-file`. The final export has a sibling
`*.screening.json` audit file.
