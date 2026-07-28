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

<!-- MODIFIED IN THIS DERIVATIVE: backend persistence, neutral QA, path-safe tooling, and artifact privacy were revised; see ../../NOTICE (Apache-2.0 section 4(b)). -->

# Nature Scientific Figures

Build the visual argument from supplied evidence. A graphical abstract or
schematic remains a draft visual and must not invent mechanisms or results.

## Route

Read [manifest.yaml](manifest.yaml) and its core contract. Select the backend in
this order:

1. explicit user choice;
2. existing source file, project dependencies, or established project backend;
3. saved user preference;
4. ask only when Python and R are both viable and the choice would materially
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
archetype, chart, template adaptation, or export. Prefer the provenance-recorded
chart-atlas/gallery examples or user code; do not copy an external paper figure.

## Build and validate

1. Choose an archetype and a clear hero panel.
2. Map data and statistics before styling. Preserve missingness, sample sizes,
   units, and uncertainty.
3. Use restrained hierarchy, typography, and color; verify grayscale and
   color-vision robustness when distinctions matter.
4. Adapt templates by semantics, never by relabelling incompatible data.
5. Export the required vector/raster products under the task's output directory.
6. Resolve `SKILL_DIR` as the directory containing this `SKILL.md`, load
   [references/qa-contract.md](references/qa-contract.md), run
   `python3 "$SKILL_DIR/scripts/validate_figure.py" SOURCE`, and inspect rendered
   outputs at final size with an appropriate neutral viewer.

## Integrity and completion

Do not invent values, mechanisms, labels, institutional marks, or statistical
significance. Do not hide data or alter analysis to improve appearance. Finish
only when source and exports agree, labels and legends are readable, panel
claims are evidence-supported, and final-size visual QA passes when a rendered
deliverable is in scope and inspectable; otherwise state clearly that visual QA
was not run.
