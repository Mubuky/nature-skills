---
name: nature-polishing
description: >-
  Edit, locally restructure, proofread, or translate a selected existing
  manuscript passage or section into precise publication-ready prose while
  preserving every scientific claim, evidence relationship, numerical value,
  citation, equation, and uncertainty; also fix LaTeX layout when requested.
  Use for 论文润色、局部改写、翻译 or 排版. Do not draft missing content, rebuild
  the scientific argument, or create a full bilingual reader.
---

<!-- MODIFIED IN THIS DERIVATIVE: context routing, fidelity gates, and layout QA policy differ from upstream; see ../../NOTICE (Apache-2.0 section 4(b)). -->

# Nature-Style Academic Polishing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core principles, paper-type playbooks, per-section guidance, language-specific rules, per-journal style).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the polishing logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

### 0. Route layout requests before prose work

If the user asks to fix *placement or typesetting* rather than wording—loose or
sparse pages, stranded headings, float placement, multi-panel arrangement,
page breaks, or Supplementary Information density—read `manifest.yaml` and
`references/latex-layout.md`, then skip the prose axes and prose core.

- When a suitable LaTeX toolchain is available and the task permits compilation,
  compile, render, and inspect the relevant pages before and after the change.
- When rendering is unavailable or the user has supplied source only, perform a
  source-level layout audit, report `visual_qa_not_run`, and never claim that the
  rendered layout passed visual QA.

For prose requests, follow steps 1–5.

### 1. Load the manifest and the prose core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance,
failure-mode diagnosis, and output format that apply to every prose-polishing job.

### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `paper_type` — research / methods / hypothesis / algorithmic / review. Default: research.
- `section` — abstract / intro / results / discussion / conclusion / title / methods. May be multiple. Ask the user if it is ambiguous and matters for the polish.
- `language` — en or zh-to-en. Detect from the draft itself.
- `journal` — nature / nat-comms / generic. Default: generic. If the user names a Nature subjournal, treat it as `nature`.

Keep obvious axis choices internal. Surface an assumption only when it is
material and non-obvious; ask only when the ambiguity would substantially
change the edit.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis only if the user has supplied free-floating prose with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Polish using the loaded material

Apply the loaded fragments in this priority order, matching the `paper type -> section job -> paragraph logic -> claim/evidence/boundary -> sentence polish` rule from `core/failure-modes.md`:

1. Paper-type playbook (architecture, writing order).
2. Section-specific job and failure modes.
3. Journal-specific framing and constraints.
4. Language-specific sentence and paragraph rules (apply last).
5. Core stance throughout; load ethics only when its on-demand condition is met.

Local restructuring may reorder explicit content for clarity, but it must not
add, remove, or reinterpret a scientific claim or evidence relationship. If a
paragraph's problem cannot be fixed inside that boundary, flag it or route the
work to `nature-writing` rather than papering over it.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them only
when their condition in `references.on_demand` is met.

## Completion gate

Before returning a prose edit, verify that:

- every number, unit, statistical symbol, equation, citation, figure/table
  reference, and defined term is preserved unless the user explicitly requested
  a corresponding change;
- claim strength, scope, causality, comparison, and uncertainty have not drifted;
- any unresolved structural problem or missing factual support is reported
  rather than silently repaired; and
- the default response is the polished text plus only material revision notes.
