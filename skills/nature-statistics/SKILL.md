---
name: nature-statistics
description: >-
  Implicit use requires an explicit or already-established Nature Portfolio
  context. Plan, audit, or revise manuscript statistical methods and reporting;
  when data and design are
  supplied and computation is requested, run bounded analyses. Cover
  experimental units, n, tests, assumptions, effects, intervals, multiplicity,
  randomization/blinding, and figure legends. Within that scope, use for
  统计审查、p值、样本量、多重比较 or 图注统计. Do not do unsupported reanalysis.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Statistics

Use this skill for statistical reporting and audit. Reanalyse raw data only when
the user explicitly requests computation and supplies the design metadata needed
for a reproducible analysis.

## Core rules

- Identify what was measured, the independent experimental unit, and the unit
  actually analysed. Do not silently promote cells, images, fields, readings,
  runs, or technical replicates into independent `n`.
- Report effect size, uncertainty, sample size, test/model, assumptions, and
  multiplicity alongside significance where applicable.
- Do not invent `n`, p values, confidence intervals, degrees of freedom,
  software versions, correction methods, exclusions, randomization, blinding,
  preregistration, or power calculations.
- Do not make a final test recommendation when design or analysis unit is
  unclear.
- Do not upgrade association to causality or `significant` to important,
  biologically meaningful, or large.

## Route and workflow

Classify the task as audit, rewrite, draft, figure-statistics alignment,
reviewer-response support, or data-backed reanalysis. Read
[manifest.yaml](manifest.yaml), load its minimum reporting sources, then only
the condition-matched failure-mode, figure, or reviewer checklist.

1. Extract groups, endpoints, hierarchy, repeated measures, blocks, missingness,
   exclusions, randomization, and blinding.
2. Define `n` and distinguish biological/experimental, technical, repeated, and
   nested observations.
3. Map each claim to its comparison/model, assumptions, correction, effect,
   uncertainty, and exact p-value policy.
4. Audit Methods, Results, legends, and source-data notes for consistency.
5. Draft conservative ready-to-paste text and list factual gaps as
   `AUTHOR_INPUT_NEEDED`.
6. For reanalysis, treat inputs as read-only, record their hashes, and write
   code, environment, derived outputs, and the decision log to a new output
   directory. Do not overwrite source data, prior results, or manuscript files.

## Output and completion

Return scope and boundary, design/unit readout, severity-ranked issues,
ready-to-paste text, missing author facts, and residual reviewer risk. Finish
when design, analysis unit, `n`, method, effect/uncertainty, multiplicity, and
unresolved facts are explicit.
