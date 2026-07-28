# `nature-writing` Skill

[中文说明](README.md)

`nature-writing` drafts or rebuilds Nature-style manuscript sections, faithfully
polishes existing prose, handles LaTeX layout, and prepares initial-submission
packages from author-provided claims, figures, results, notes, or Chinese
drafts.

## What To Use It For

- Build titles, abstracts, introductions, result narratives, discussions, conclusions, or significance paragraphs.
- Organize claim-evidence narrative from figures and data.
- Turn Chinese research notes into English manuscript paragraphs.
- Build the background, gap, question, and contribution chain for an Introduction.
- Reorder Results or Discussion at the section level rather than only polishing sentences.
- Polish, proofread, or translate existing text without changing claims,
  evidence, numbers, citations, or uncertainty.
- Diagnose LaTeX floats, sparse pages, stranded headings, and multi-panel layout.
- Prepare an initial cover letter, title page, highlights, author contributions, availability statements, and other declarations.
- Organize reviewer suggestions, a deliverable matrix, and a pre-submission completeness audit.

## Typical Requests

- "Write a Nature-style abstract from these figures and results."
- "Rebuild the logic of this introduction; do not only polish the sentences."
- "Turn these Chinese results into an English Results narrative."
- "Polish this English paragraph without changing any scientific claim or number."
- "Fix the sparse pages and float layout in this Supplementary Information."
- "Prepare an initial cover letter and complete submission package from this manuscript."

## What You Need To Provide

- Core claim, figures, key results, experimental facts, and target reader.
- Target section, length, language, and terminology that must be preserved.
- For polishing, the source and allowed edit scope; for layout, the LaTeX source
  and any available compiled artifact.
- Confirmed references, limitations, and conclusions that must not be added.

## Outputs

- Section outline, claim-evidence map, or ready-to-paste prose.
- Revision suggestions for novelty, significance, evidence chain, and reader path.
- Fidelity-preserving prose with only material revision notes, or a LaTeX layout
  diagnosis with its validation state.
- Facts, references, or figure notes requiring author confirmation.
- Initial-submission materials, editable LaTeX templates, a missing-input checklist, and a `ready / ready_with_author_checks / blocked` status.

## Boundaries

- The skill does not invent experimental results, statistical significance, mechanism explanations, or references.
- Polishing and layout use on-demand special routes that skip the full drafting
  workflow; problems outside the local fidelity boundary are flagged or offered
  as a separate drafting pass.
- If claim support requires literature search first, use `nature-citation` or `nature-academic-search`.
- This skill handles first submission; use `nature-response` for revision cover letters, rebuttals, and point-by-point responses.

## Related Skills

- `nature-citation`: match supporting references for claims.
- `nature-figure`: align figure conclusions and panel design with manuscript narrative.
- `nature-response`: revision cover letters, responses to reviewers, and revision correspondence.
- `nature-reviewer`: simulated review before submission.
