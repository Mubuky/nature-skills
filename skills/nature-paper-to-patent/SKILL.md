---
name: nature-paper-to-patent
description: >-
  Implicit use requires an explicit or already-established Nature Portfolio
  context. Convert papers, code, figures, or inventor notes into
  evidence-traceable Chinese invention-patent
  drafts, claims, technical disclosures, source maps, and claim-aligned figures
  or DOCX. Within that scope, use for 技术交底书、权利要求、论文转专利、专利点挖掘 or
  paper-patent audits. Do not provide legal/patentability opinions, invent
  unsupported features, or replace professional review.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Paper to Chinese Patent

This is an evidence-to-draft workflow, not a legal opinion or filing service.
Do not draft formal claims directly from an abstract or contribution list.

## Route

Read [manifest.yaml](manifest.yaml) and its core files. Detect:

- source format: text PDF, scanned PDF, pasted text, or mixed project;
- task: full draft, claim set, disclosure analysis, technical disclosure,
  disclosure iteration, or paper-patent audit;
- invention type: algorithm/software, apparatus/system, process/material, or mixed.

Load only the selected fragments and condition-matched references.

## Evidence ledger

Assign stable source IDs to paper blocks, equations, figures, code, and
supplementary evidence. Every material claim feature must map to source IDs and
one support state: `explicit`, `inherent`, `needs-confirmation`, or `unsupported`.
Formal claims may not contain `unsupported` features.

Do not infer inventorship, ownership, unpublished implementation, public dates,
prior-art conclusions, legal sufficiency, freedom to operate, infringement, or
patentability. Absence of a search hit is not evidence of novelty.

## Stage gates

1. Build the source map, terminology ledger, feature inventories, and evidence
   ledger.
2. Define the invention concept and boundaries.
3. Follow the selected task and invention fragments.
4. For an application, draft claims first; align specification, embodiments,
   figures, formulas, and abstract to the same terminology and ordered steps.
5. For a disclosure iteration, preserve the previous draft and change record.
6. Populate the structured draft and run the bundled validator/package builder,
   or the disclosure-specific checks for a technical disclosure.

Use `[TO CONFIRM: specific question]` outside formal claims when author facts are
missing. Preserve source-supported formulas as editable Office Math and map the
main flowchart to the principal method claim when those deliverables apply.

## Completion

Resolve validation errors and review warnings against the source. Label an
incomplete package explicitly. Deliver the source map, evidence ledger,
structured draft, requested Chinese documents, validation report, and unresolved
questions.

Every output remains a drafting aid that must be reviewed by the inventors and a
qualified patent professional before filing or legal reliance.
