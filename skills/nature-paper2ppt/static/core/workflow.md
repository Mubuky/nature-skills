<!-- Modified from Yuan1z0825/nature-skills; see ../../../../NOTICE. -->

# Workflow

Run these nine steps for any paper-to-deck job. The paper-type fragment loaded for this job sets the narrative arc; this workflow is the shared spine. Deep design, figure, and self-review material lives in the on-demand references named below.

Before step 1, establish task paths:

1. Parse an explicit output directory from the user's request when present.
2. Otherwise set `OUTPUT_DIR` to a task-local `paper2ppt-output/` directory
   beside the source or current task files, never inside `SKILL_DIR`.
3. Use `PPTX_PATH="$OUTPUT_DIR/presentation.pptx"` for one deck. If the user
   asks for parallel language variants, use `presentation_zh.pptx` and
   `presentation_en.pptx`.
4. Resolve `SKILL_DIR` to the installed directory containing `SKILL.md`; use it
   only for bundled references and scripts.

## Step 1. Read and extract source material

Extract, when available: title, authors, journal/preprint server, year, DOI; field and subfield; paper type; central problem and knowledge gap; main claim or thesis; study design, workflow, model, dataset, or experimental system; key methods and controls; main results and quantitative findings; key figures, tables, and figure legends; validation, robustness, ablation, or sensitivity analyses; limitations and unresolved questions; broader scientific, clinical, technical, environmental, or translational meaning.

Do not invent missing numbers, mechanisms, datasets, or figure details. Use a two-pass reading strategy: first capture metadata, abstract, headings, figure legends, and table captions; then read only the result and methods pages needed to support the slides. Start the Terminology Ledger here.

## Step 2. Classify the paper and choose the presentation logic

The router already detected the `paper_type` axis and loaded the matching arc fragment. Confirm the classification against the source, then follow that fragment's arc (`claim-first`, `question-to-evidence`, `problem-to-solution`, `workflow-to-validation`, or `evidence-map`) when ordering slides.

## Step 3. Build the presentation plan

Default length: 12-16 slides for a 15-20 minute report; prefer 10-14 for a quick or unspecified request; expand beyond 16 only for a detailed seminar deck or when the paper genuinely needs the space. Use the default slide structure from the loaded paper-type fragment and adapt it to the paper. Do not force every paper into the same template.

Before authoring, plan the visual rhythm: assign each slide a visual role and a composition type, and avoid repeating the same role/composition too often. For the composition-type catalogue and the rule against single-layout-family decks, open `references/design-and-layout.md`.

## Step 4. Select figures as evidence, not decoration

Prioritize figures that carry the argument: design/workflow, main evidence, validation/robustness, mechanism/model/synthesis, then practical/conceptual implication. Prefer a few readable key panels over many unreadable full figures. For the full selection checklist, open `references/figure-assets.md`.

## Step 5. Extract and prepare figure assets

Extract or render only selected figures, crop dense panels, keep original data
visuals unchanged, save under `$OUTPUT_DIR/assets/figures/`, and record
traceability in `$OUTPUT_DIR/asset_manifest.md`. For a standard 10-14 slide
deck, usually select 4-8 assets. Prefer editable PPT-native tables/charts when
values are explicit. Run the figure-crop self-check before insertion. A crop
that removes panel letters, axes, legends, scale bars, method labels, table
headers, or scientifically necessary annotations is a high-severity defect and
must be re-extracted, expanded, or split into multiple slides before insertion.
Full extraction, crop, and self-check rules are in
`references/figure-assets.md`.

## Step 6. Write slide-by-slide content

For each slide write: a conclusion-style title where possible, slide purpose,
suggested layout, two to four concise bullets, the selected figure/table asset,
caption and interpretation, one core takeaway, and a concise speaker note when
oral explanation helps. Each slide makes one point. In any language, avoid
template slogans and use paper-specific, evidence-grounded wording.

Respect the on-slide text budget: write for the slide, not the manuscript; most explanation belongs in speaker notes. Order each result slide as hero evidence first, then a narrow interpretation rail, then only the minimum labels. The detailed text budget, evidence hierarchy, layout-adaptation, anti-template, archetype, title, and density rules are in `references/design-and-layout.md`.

## Step 7. Build the actual PPTX deck

Create a real `.pptx` as the primary deliverable with `python-pptx` (or a
user-provided template), using 16:9 by default, the selected language for
titles/bullets/captions/notes, source labels on evidence slides, and consistent
typography. Let geometry follow the figure. Align content to a small set of
guides. Prefer shorter text, larger boxes, or another slide over automatic text
shrinking; never deliver expected clipping. Full implementation rules are in
`references/design-and-layout.md`.

Save the reusable, task-specific generator as
`$OUTPUT_DIR/generator/build_presentation.py`. It must rebuild the deck from
task-relative source/assets, avoid secrets and machine-specific absolute paths,
and include a concise dependency/run note when the invocation is not obvious.

## Step 8. Self-review and corrective revision loop

After the first draft, run at least one explicit self-review pass as a
defect-finding step: inspect the PPTX and assets, write a severity-graded defect
list (`high`/`medium`/`low`) with slide numbers, fix every high-severity issue
and every reasonable medium one, regenerate, and update
`$OUTPUT_DIR/qa_report.md`. When a `.pptx` exists, run this before and after
revision:

```bash
python3 "$SKILL_DIR/scripts/audit_pptx_quality.py" "$PPTX_PATH" \
  --report "$OUTPUT_DIR/pptx_audit.md" --fail-on high
```

Copy high/medium findings into the QA report. The full checklist, severity
rules, programmatic PPTX checks, and rendered-preview policy are in
`references/self-review.md`.

## Step 9. Final verification

Reopen the PPTX, check slide count, embedded media count, and speaker-notes
presence when planned, check shape bounds if tooling supports it, create or
inspect a contact sheet from cropped assets, and confirm the structural audit
has no unresolved high-severity findings. Record exactly one canonical QA state
from `static/core/output-and-quality.md`. Do not stop at "PPTX opens" if
self-review found high-severity issues—fix them first, then verify again, and
document any remaining limitation in `$OUTPUT_DIR/qa_report.md`. See
`references/self-review.md`.
