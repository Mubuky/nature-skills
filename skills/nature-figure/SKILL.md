---
name: nature-figure
description: >-
  Implicit use requires an explicit or already-established Nature Portfolio
  context. Design, revise, audit, and export submission-grade quantitative
  figures and multi-panel layouts
  using Python or R, and route manuscript schematics or graphical abstracts
  through an appropriate visual workflow. Within that scope, use for
  论文配图、科研绘图、Figure 1 or journal-ready SVG/PDF/TIFF. Do not use for
  statistics-only inference, dashboards, slide decks, photo editing, or general
  illustration.
---

<!-- MODIFIED IN THIS DERIVATIVE: backend persistence, faithful paper-example routing, neutral QA, path-safe tooling, and artifact privacy were revised; see ../../NOTICE (Apache-2.0 section 4(b)). -->

# Nature Scientific Figures

Build the visual argument from supplied evidence. A graphical abstract or
schematic remains a draft visual and must not invent mechanisms or results.

## Route

Read [manifest.yaml](manifest.yaml) and its core contract. Select the backend in
this order:

1. explicit user choice;
2. existing source file, project dependencies, or established project backend;
3. saved user preference;
4. a faithful paper-specific Python example or maintained analytical CSV template when it
   is a semantic match and no project constraint conflicts;
5. ask only when Python and R are both viable and the choice would materially
   affect integration or maintainability.

If the user asks you to choose, use
[references/backend-selection.md](references/backend-selection.md) and proceed.
Use one backend as the source of truth for drawing, layout semantics, and
export. Neutral viewers, image/PDF/SVG inspection, and deterministic validators
may perform QA without becoming a second drawing backend. Persist a backend
preference only when the user explicitly asks to make it the future default.

## Figure contract

Before code, define:

- one-sentence conclusion and intended reader;
- evidence chain and role of every panel;
- source-data fields, transformations, statistics, and uncertainty;
- target journal dimensions, formats, fonts, and accessibility;
- likely reviewer misreadings and integrity risks.

Load only the selected backend fragment and the references required by the
archetype, chart, example adaptation, or export. Prefer user code or a
provenance-recorded high-fidelity example over a generic style preset. For a
Python task that benefits from a real-paper precedent, load
[references/paper-pattern-catalog.md](references/paper-pattern-catalog.md),
inspect the original output first, then open only its registered source.

When refactoring a preserved example, treat its bundled PNG/PDF as the golden
output. Keep paper-specific palettes, typography, canvas, layout, drawing order,
annotations, camera, and save settings local. Do not route it through the
shared analytical-template style. Make one structural change at a time and compare the
rerender; retain and show the original when a proposed repair changes pixels or
scientific meaning. Store an approved changed render under `paper-patterns/optimized/`;
never replace its upstream golden.

## Build and validate

1. Choose an archetype and a clear hero panel.
2. Map data and statistics before styling. Preserve missingness, sample sizes,
   units, and uncertainty.
3. Preserve the selected reference's deliberate visual hierarchy and diversity;
   verify readability, grayscale, and color-vision robustness without silently
   flattening its design.
4. Adapt examples and templates by semantics, never by relabelling incompatible
   data. Treat the five analytical CSV commands as utilities, not canonical paper style.
5. Export the required vector/raster products under the task's output directory.
6. Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, load
   [references/qa-contract.md](references/qa-contract.md), run
   `python3 "$SKILL_DIR/scripts/validate_figure.py" SOURCE`, and inspect rendered
   outputs at final size with an appropriate neutral viewer.

## Integrity and completion

Do not invent values, mechanisms, labels, institutional marks, or statistical
significance. Do not hide data or alter analysis to improve appearance. Do not
delete a questionable example merely because it is hard to generalize; preserve
it, record the issue, and request a decision before an output-changing repair.
Finish only when source and exports agree, labels and legends are readable,
panel claims are evidence-supported, and final-size visual QA passes when a
rendered deliverable is in scope and inspectable; otherwise state clearly that
visual QA was not run.
