---
name: nature-paper-card
description: >-
  Create a source-grounded deep-reading card for one paper, tracing its question,
  method modules, formulas, figures/tables, experiment-to-claim evidence,
  limitations, critical connections, and testable ideas. Use for Paper Card、
  单篇精读卡、证据链 or 论文深度分析. Do not use for bilingual translation,
  formal peer review, batch monitoring, slides, or manuscript drafting.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Paper Card

Build one evidence-grounded analytical card. Use `nature-reader` for a complete
bilingual reconstruction and `nature-reviewer` for a referee report.

## Route

Read [manifest.yaml](manifest.yaml) and its core files. Determine source coverage
and one primary paper-type lens; add at most one secondary lens when it carries
independent evidence.

Use one locator mode:

- `page-grounded`: reliable PDF pages and structural locators;
- `structure-grounded`: figures, tables, equations, sections, or stable blocks;
- `source-limited`: abstract, metadata, or supplied excerpt only.

For PDF or an existing source map, follow
[references/tooling.md](references/tooling.md) and use the bundled preparation
script. Do not fabricate page locators when preparation fails.

## Build

1. Prepare the source and terminology ledger.
2. Inventory claims, methods, main figures/tables/equations, experiments,
   reported results, limitations, and stable source pointers.
3. Build a claim-evidence matrix before prose.
4. Load only the selected paper-type fragments and the condition-matched
   provenance, card-schema, or idea-gate reference.
5. Write Sections 01–16, using `Not applicable` or `Not assessable` rather than
   filling gaps.
6. Run the bundled auditor and review the evidence scientifically.

## Integrity

- Separate paper statements, externally verified facts, agent analysis,
  user judgments, and hypotheses.
- Trace every major number, baseline, sample size, figure, table, and conclusion
  to the supplied source.
- Label field-history or novelty claims `paper-framed` or `unverified` until an
  external check supports them.
- Proposed ideas are hypotheses, not novelty or feasibility guarantees.
- Auditor success checks structure and traceability; it does not prove the
  scientific interpretation.

## Completion

Deliver `paper-card.md` plus the preparation/audit artifacts required by the
locator mode. Finish when all required sections exist, no audit error remains,
major evidence is locatable, and every unresolved source gap is explicit.
