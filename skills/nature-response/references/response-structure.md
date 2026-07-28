<!-- Modified from Yuan1z0825/nature-skills; see ../../../NOTICE. -->

# Response structure

Use this file when drafting or auditing the output shape of a reviewer response package, revision cover letter, marked manuscript changes, or combined revision correspondence package.

## Task-routed package

Select components from the task-mode matrix in `intake-and-routing.md`; it is
the source of truth for mode-to-output routing. Only `revision-package`
defaults to the full combined package. Within the selected components, use this
order:

1. Response strategy summary and comment-response tracker, when routed.
2. Point-by-point response letter, when routed.
3. Revision cover letter, when routed or required by the target journal.
4. Marked manuscript changes, only when manuscript editing is in scope.
5. LaTeX deliverables, only when requested or required.
6. Manuscript change checklist and missing-information/risk flags, when routed.
7. Chinese confirmation notes when the user writes in Chinese.

## Response strategy summary

Keep this short and editor-readable:

```text
Response strategy summary
- Decision type: Major revision
- Task mode: draft
- Parsed email metadata: manuscript ID and deadline found; required files include response letter and marked manuscript
- Package readiness: draft_with_placeholders
- Overall posture: Cooperative, evidence-forward, non-defensive
- Major risks: missing validation results; unclear replicate definition
- Suggested ordering: address editor first, then Reviewer 1 and Reviewer 2 in full
```

Decision types:

- `minor revision`
- `major revision`
- `revise-and-resubmit`
- `transfer after review`
- `appeal-like case` routed outside the default workflow
- `unclear` when the decision type is not supplied

Task modes:

- `draft`
- `audit`
- `revise`
- `triage-only`
- `cover-letter`
- `revision-package`
- `latex-template`
- `appeal-like`

Derive `Package readiness` from the canonical rules in `action-mapping.md`; do
not infer it from prose polish or restate its semantics here.

## Comment-response tracker

Use a compact table:

```markdown
| ID | Reviewer concern | Type | Severity | Proposed action | Work status | Required input | Expected output | Blocks finalization? |
|---|---|---|---|---|---|---|---|---|
| R1.1 | Missing validation cohort | Evidence / validation | Major | ACCEPT_ANALYSIS | TODO_ANALYSIS | Validation result and location | Results text plus validation table | Yes |
```

Keep reviewer concern text short in the tracker. Preserve the full wording in the letter when available.
Use `E.1`, `E.2`, etc. for editor instructions and list them before reviewer comments.
When the input is a pasted editorial email, use the tracker to preserve all extracted required
revision items rather than only the reviewer comments.
Do not use `Work status` as a synonym for `Proposed action`: the former reports progress and verification, while the latter states the response strategy.
If the table becomes too wide for the requested medium, keep the same fields in a per-item block rather than dropping status, expected output, or blocking state.

## Point-by-point letter anatomy

Use this default structure:

```markdown
Dear Editor and Reviewers,

We thank the editor and reviewers for their careful evaluation of our manuscript.
We have revised the manuscript to address the concerns raised and provide a point-by-point response below.

## Response to Reviewer 1

**Reviewer comment R1.1**
[Full reviewer comment preserved here.]

**Response**
We thank the reviewer for raising this point. [Direct answer.]
To address this concern, we have [specific action]. This change appears in [section/page/line/figure].
[If pasting revised manuscript text, place it after the answer and format it in italics.]

**Revised manuscript text**
*[Paste revised manuscript text here.]*
```

Follow target-journal instructions before local layout conventions. When a
print/PDF response requires reviewer page breaks, configure
`\ReviewerSection{1}`, `\ReviewerSection{2}`, and so on from
`templates/response-to-reviewers.tex`. Ordinary Markdown remains continuous;
insert an explicit page-break marker only when that Markdown is intentionally a
print/PDF source.

## Revision cover letter anatomy

Use the cover letter only when the user asks for it, the journal requires it, or the user asks for a complete revision package. Keep it shorter than the point-by-point response.

```markdown
Dear [Editor name],

Thank you for considering our revised manuscript, "[Manuscript title]" ([Manuscript ID]).
We appreciate the editor's and reviewers' constructive feedback.

In this revision, we have [major revision action 1], [major revision action 2], and [major revision action 3].
These changes address the main concerns regarding [concern/theme 1], [concern/theme 2], and [concern/theme 3].

We provide a detailed point-by-point response to all editor and reviewer comments below / in the accompanying response document.
We believe the revised manuscript is now clearer and better supported, and we hope it will be suitable for further consideration by [Journal name].

Sincerely,
[Corresponding author name]
on behalf of all authors
```

Do not use the cover letter to argue around unresolved reviewer concerns. If a major request remains unresolved, mention that the response letter explains the limitation.

## Marked manuscript changes

When modifying manuscript text, work on a copy of the original manuscript and mark changed passages in red. For LaTeX manuscripts, wrap changed text in `\revised{...}` from `templates/revised-manuscript-redline.tex`. For non-LaTeX outputs, use a clear red-text convention appropriate to the target format and keep a clean version separate from the marked copy.

In the response letter, after the direct answer, paste the revised manuscript text in italics. In LaTeX response files, use `\RevisedExcerpt{...}`.

## LaTeX deliverables

When the user asks for LaTeX, use the templates in `templates/`:

- `templates/cover-letter.tex` for revision cover letters.
- `templates/response-to-reviewers.tex` for point-by-point responses.
- `templates/revised-manuscript-redline.tex` for a red-marked manuscript-copy skeleton.

In `templates/response-to-reviewers.tex`, use `\ReviewerSection{...}` for each
reviewer and configure its section-break macro to match the target journal.

Preserve visible placeholders for unknown manuscript ID, editor name, line numbers, figure panels, dates, or author information. Do not hide missing facts in comments.

## Manuscript change checklist

List manuscript actions, not polite intentions:

```text
Manuscript change checklist
- R1.1: Add validation result summary to Results and cite Fig. 5.
- R1.2: Clarify replicate definition in Methods.
- R2.1: Soften causal claim in Abstract and Discussion.
```

## Missing information / risk flags

Use specific requests:

```text
Missing information / risk flags
- R1.1: Need validation result direction and effect/performance summary before final wording.
- R1.2: Need test name, replicate unit, sample size, and correction method.
- R2.1: No line numbers supplied; using section names for now.
```
