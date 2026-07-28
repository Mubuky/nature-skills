<!-- Modified from Yuan1z0825/nature-skills; see ../../../../NOTICE. -->

# Workflow and output format

## Accepted inputs

The skill may receive: pasted editorial decision or revision-invitation email; editor decision letter; reviewer comments; previous response draft; manuscript change notes; tracked-change summary; line or page numbers; figure, table, and supplement list; author notes in Chinese or English; journal name and article type; manuscript title; author list; manuscript ID; original manuscript text or LaTeX source; requested cover-letter or LaTeX output format.

If reviewer boundaries or comment segmentation are ambiguous, flag the ambiguity instead of inventing reviewer structure.

## Workflow

1. Identify task mode and input readiness: `draft`, `audit`, `revise`, `triage-only`, `cover-letter`, `revision-package`, `latex-template`, or `appeal-like`.
2. If the input is a pasted journal email, automatically extract manuscript title, manuscript ID, journal, decision type, editor instructions, reviewer-report boundaries, required revision files, deadline, and portal-specific constraints before drafting.
3. Identify decision type: minor revision, major revision, revise-and-resubmit, transfer after review, or unclear.
4. Extract editor instructions first and assign IDs such as `E.1`, then split reviewer comments with IDs such as `R1.1`, `R1.2`, and `R2.1`.
5. Classify each item by category, severity, action label, work status, required
   input, expected output, finalization-blocking state, package readiness, and
   risk using the canonical definitions in
   `../../references/action-mapping.md`.
6. Create a response strategy summary before drafting prose.
7. Draft responses using preserved reviewer comments unless the mode is `triage-only`, `cover-letter`, or `appeal-like`.
8. For `cover-letter` or `revision-package`, draft a concise editor-facing cover letter that summarizes revision scope and points to the point-by-point response without duplicating it.
9. Map each claimed change to manuscript location, figure, table, supplement, citation, or explicit placeholder.
10. If editing manuscript text, create or instruct use of a backed-up manuscript copy and mark changed text in red. For LaTeX, use `\revised{...}` from `templates/revised-manuscript-redline.tex`.
11. If pasting revised manuscript text after a response, format it in italics. For LaTeX response files, use `\RevisedExcerpt{...}` from `templates/response-to-reviewers.tex`.
12. Follow the target journal's correspondence format first. Add reviewer
    page breaks only when the journal, user, or print/PDF destination calls for
    them; ordinary Markdown is continuous by default. In LaTeX, the
    `\ReviewerSection{...}` macro may be configured for the required break.
13. If the user requests LaTeX, use `templates/cover-letter.tex`, `templates/response-to-reviewers.tex`, and/or `templates/revised-manuscript-redline.tex`; preserve visible placeholders for missing facts.
14. Apply the verification-evidence and work-status rules from
    `../../references/action-mapping.md`; do not redefine or loosen them in
    response prose.
15. Flag missing author input rather than fabricating details.
16. Run QA on the components selected by task mode for completeness, per-item
    status calibration, blocking-state consistency, traceability, factuality,
    tone, unresolved risk, applicable change marking, italic revised excerpts,
    medium-specific formatting, and visible placeholders.
17. Derive package readiness from the item statuses using
    `../../references/action-mapping.md`, the single source of truth for work
    status and readiness semantics.

## Output by task mode

Use the task-mode matrix in `../../references/intake-and-routing.md`; do not
emit every possible component by default.

- Only `revision-package` defaults to the combined strategy, tracker,
  point-by-point response, cover letter, change checklist, and visible
  placeholders/risk flags.
- `draft`, `audit`, `revise`, `triage-only`, `cover-letter`, and
  `latex-template` return only their routed components.
- Marked manuscript files are included only when manuscript editing is in
  scope. LaTeX files are included only when requested or required by the target
  journal.
- Use `../../references/response-structure.md` for the anatomy and ordering of
  whichever components were selected.
