---
name: nature-reviewer
description: >-
  Simulate a pre-submission referee assessment of a supplied full or partial
  manuscript, abstract, or manuscript package, with reports and a synthesis on
  novelty, significance, rigor, evidence, reproducibility, and readability.
  Use for 模拟审稿、投稿前自审 or reviewer report. Do not draft real rebuttals,
  polish prose, or perform a statistics-only reporting audit.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Reviewer

Assess a manuscript before submission. Use `nature-response` after a real editor
decision or reviewer report.

## Contract

Default to three reviewer reports with different emphases plus one synthesis;
follow another requested count or structure when it preserves independent
assessment and synthesis.

Evaluate:

- originality;
- scientific importance;
- interdisciplinary readership;
- technical soundness and reproducibility;
- readability for non-specialists.

Read [manifest.yaml](manifest.yaml). Load the current local source basis and only
the workflow, axes, domain gates, structure, role, or QA references needed at the
current stage.

## Workflow

1. Establish source coverage and extract one shared manuscript fact base.
2. Separate author claims, visible evidence, limitations, external checks, and
   facts not assessable from the supplied material.
3. Build a concern ledger. Each substantive concern needs a stable ID, claim
   pointer, evidence pointer, severity, and resolution test.
4. Draft reviewers from the same facts with different emphases, not invented
   identities or biographies.
5. Synthesize consensus only when multiple reports raise the same underlying
   concern; preserve legitimate weighting differences.
6. Run groundedness, coverage, issue-key consistency, synthesis,
   role-boundary, and non-invention QA.

## Boundaries

- Missing material means `not assessable`, not proof that the authors omitted
  the work.
- Do not invent experiments, controls, citations, figure panels, line numbers,
  reviewer identities, institutions, specialties, or selection history.
- Do not infer field novelty solely from the manuscript's related work.
- Do not make the editor's final decision or guarantee fit to Nature.
- The bundled editorial criteria are a local snapshot. Verify current official
  policy when the user needs policy-level certainty, or state the limitation.

## Completion

Finish when every substantive concern is evidence-anchored, unsupported and
not-assessable claims are labelled, repeated concerns share stable issue keys,
and the synthesis distinguishes supported consensus from differences in
emphasis.
