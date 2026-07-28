---
name: nature-writing
description: >-
  Plan, draft, or structurally rebuild manuscript sections and initial-
  submission materials from author-provided evidence, claims, figures, or notes.
  Use for 基于作者证据从零起草论文、撰写/重构摘要/引言/方法/结果/讨论、论文结构、
  投稿信、标题页 or 作者贡献. Do not use for language-only polishing, proposals,
  post-review responses, citation search, or specialist data/statistics text.
---

<!-- MODIFIED IN THIS DERIVATIVE: evidence boundaries, non-blocking routing, progressive disclosure, and completion gates were revised; see ../../NOTICE (Apache-2.0 section 4(b)). -->

# Nature-Style Scientific Writing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core stance + workflow, paper-type playbooks, per-section drafting guidance, initial-submission guidance, language-specific rules, per-journal style).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the drafting logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`task`, `paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, writing workflow, and output format that apply to every drafting job.

### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `task` — manuscript / submission-package. Use `submission-package` for first-submission materials, never for revision correspondence.
- `paper_type` — research / methods / hypothesis / algorithmic / review. Default: research.
- `section` — abstract / intro / related-work / method / experiments / discussion / conclusion / title. May be multiple. Ask the user if it is ambiguous and matters for the draft.
- `language` — en or zh-to-en. Detect from the user's notes themselves.
- `journal` — nature / nat-comms / generic. Default: generic. Route Nature
  Communications explicitly to `nat-comms`; route other Nature subjournals to
  `nature`.

Keep obvious axis choices internal. Surface one short assumption only when a
non-obvious choice affects the draft; do not pause unless that ambiguity would
materially change the scientific argument or deliverable.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis when the task is `submission-package` or when the user explicitly asks for a free-floating argument paragraph with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Draft using the loaded material

Apply the loaded fragments in this priority order:

1. Core stance + intake (`static/core/stance.md`) — surface missing claim /
   evidence / boundary before drafting.
2. Paper-type playbook — argument chain, drafting order.
3. Section-specific drafting rules and structure.
4. Task-specific submission rules when `task=submission-package`.
5. Journal-specific framing and constraints.
6. Language-specific sentence and paragraph rules (apply last).

For `task=manuscript`, run `static/core/workflow.md` end-to-end. Planning may
remain internal when the author-provided claim, evidence, and boundary are
clear.

For `task=submission-package`, follow `static/fragments/task/submission-package.md` and `references/submission-package.md` instead. Build the deliverable matrix and readiness audit; do not force manuscript paragraph architecture onto administrative submission materials.

If evidence is missing but a useful bounded scaffold is possible, write a
placeholder and list it under `Assumptions or missing inputs:`. Ask at most a
few targeted questions only when an unresolved choice would materially alter
the scientific argument, claim strength, or requested deliverable.

### 5. Reach for references only when needed

The files under `references/` are deep references and the example library, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user asks for a concrete example or template → `references/examples/index.md`.
- A section's draft has structural problems that the section fragment alone does not explain → the matching `references/<section>.md`.
- The user needs a broad-audience `Nature` abstract opening or asks about a `summary paragraph` → `references/nature-summary-paragraph.md`.
- The user asks "does this paragraph flow?" → `references/paragraph-flow.md`.
- The user asks for a self-review or rejection-risk audit → `references/paper-review.md`.
- The user requests a complete first-submission package, templates, or a submission-readiness audit → `references/submission-package.md`.

## Submission boundary

- `nature-writing` owns **initial submission** materials prepared before peer review.
- `nature-response` owns revision cover letters, rebuttals, point-by-point responses, marked manuscripts, appeals, and other post-decision correspondence.
- Route graphical abstracts and TOC graphics to `nature-figure`; route simulated pre-submission peer review to `nature-reviewer`.

## Completion

Finish only when the requested sections or submission materials exist; every
substantive claim is supported by author-provided evidence or visibly marked as
an assumption or placeholder; numbers, citations, terminology, and claim
strength are consistent; no reference or result was invented; and material
missing inputs are reported without padding the response with process notes.
