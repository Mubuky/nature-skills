---
name: nature-proposal-writer
description: >-
  Compose, revise, or QA evidence-backed research proposals, grant plans,
  opening reports, and structured review proposals using scoped claims,
  argument maps, section contracts, and staged validation. Use for 科研 proposal、
  基金申请、开题报告、研究方案、基金/开题中的综述与研究框架 or proposal QA.
  Do not use for a standard manuscript section, language-only polish, mock
  review, or rebuttal.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Proposal Writer

Build proposal-style scientific arguments. Route ordinary manuscript drafting
to `nature-writing`.

## Invariants

- Establish evidence and hard constraints before prose.
- Establish the argument before sections and a contract before each section.
- Lock the requested scope before optimizing completeness.
- Preserve claim strength: do not turn a hypothesis, plan, or `may` into a fact,
  result, feasibility proof, or `proves`.
- Stop or lower commitments when evidence blockers remain; do not hide them with
  fluent language or rubric scores.

Never invent data, citations, preliminary results, feasibility evidence,
resources, approvals, or expected outcomes.

## Route

Read [manifest.yaml](manifest.yaml), then load only the matching mode:

- `compose`: topic, direction, or rough idea;
- `revise`: existing proposal text;
- `hybrid`: preserve a draft while adding or rebuilding modules;
- `qa`: evaluate an artifact without silently rewriting it.

Infer the mode when safe. Ask only when the choice would materially change scope
or overwrite intent.

## Workflow

1. Create or repair the scope, research canon, evidence table, argument map,
   section contracts, and style/terminology guide.
2. Run the selected mode workflow.
3. Draft within the allowed claims and supplied evidence.
4. For QA, use [references/qa-pipeline.md](references/qa-pipeline.md); a hard
   evidence blocker overrides a numeric score.
5. Preserve the prior draft and record substantive revisions.
6. Validate claims, citations, numbering, reproducibility, and package state.

Load specialist, stopping, reduced-commitment, export, or handoff references
only when their manifest condition is met.

## Output and completion

Return the primary artifact/path, current state or score, unresolved risks, and
one recommended next action. Finish only when scope is stable, each central
claim has evidence or an explicit placeholder, section contracts are respected,
and blockers are visible.
