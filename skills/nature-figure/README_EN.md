<!-- MODIFIED IN THIS DERIVATIVE: backend, QA, persistence, and artifact-privacy behavior were clarified; see ../../NOTICE (Apache-2.0 section 4(b)). -->

# `nature-figure`

[中文](README.md)

A submission-grade workflow for manuscript figures, supplementary figures,
mechanism schematics, and graphical abstracts. It starts from the scientific
claim and evidence structure, builds or revises Python/R figures, and audits
them at final publication size.

## Use it for

- Creating editable single- or multi-panel figures from data, legends, claims,
  or existing graphics;
- Redesigning Figure 1, method overviews, mechanisms, workflows, and graphical
  abstracts;
- Auditing chart choice, hierarchy, color, typography, labels, statistics, and
  export settings;
- Selecting and faithfully adapting complete Python examples and original
  outputs from eight real-paper project families;
- Using the existing analytical CSV tools for volcano, ROC, marker dot-plot,
  marginal, and paired data;
- Producing SVG/PDF/TIFF/PNG, source-data maps, and pre-submission QA records.

Use `nature-paper2ppt` for a full slide deck and `nature-statistics` for
statistical inference or reporting review.

## Working principles

1. Define the core conclusion, panel roles, evidence hierarchy, and target
   dimensions before selecting a chart.
2. Infer Python or R from an explicit request, existing source, project
   dependencies, or a saved preference. Ask only when the choice materially
   changes the implementation.
3. Use one source file and backend for drawing, layout semantics, and export;
   neutral viewers and validators may inspect the outputs.
4. When adapting a high-quality example, use its original output as the visual
   regression baseline. Preserve project-specific composition, palette,
   typography, line weight, annotations, and export settings.
5. Preserve all observations and requested variables by default. Record every
   exclusion, aggregation, and transformation with before/after counts.
6. Inspect typography, whitespace, alignment, color accessibility, and scaling
   at the target column width and final resolution.

When the user explicitly requests an AI schematic, the host's image-generation
tool may create a concept draft. Generated content must never be presented as
real experimental evidence, quantitative data, or an unverified scientific
structure.

## Inputs and outputs

Useful inputs are raw data or an existing figure, the legend or claim, target
journal and dimensions, export formats, and source-data requirements. If
missing information does not threaten scientific validity, the skill proceeds
with a visible assumption.

Typical outputs include:

- Reproducible plotting source;
- Submission-grade vector and raster exports;
- Panel notes, source-data mapping, and exclusion counts;
- Final-size visual QA and a list of unresolved items.

See [SKILL.md](SKILL.md) for the execution contract. Bundled references cover
chart choice, layout, template adaptation, backend selection, and QA. The
[faithful real-paper gallery](references/paper-pattern-catalog.md) records the
original outputs, approved optimizations, scripts, dependencies, regression
baselines, and unresolved review items; `scripts/validate_figure.py` provides
deterministic static preflight.

## Boundaries

- Do not invent tests, sample sizes, error-bar meanings, conditions, or data.
- Do not silently sample, remove points, or hide adverse results.
- Do not reduce “Nature style” to a fixed palette or decorative template.
- Do not remove a difficult or questionable example merely because it resists
  generalization; retain it and show the issue and candidate repair first.
- Local private templates may be used without embedding private paths or names
  in public artifacts; chat replies may link deliverables created for the task.
