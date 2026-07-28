<!-- Rewritten from the upstream tutorial; see ../NOTICE for attribution. -->

# `nature-paper-card` quick tutorial

This tutorial turns one paper into a source-grounded, reviewable Sections 01–16
Paper Card. It is not a summary template: acceptance depends on whether claims,
evidence, and source locators remain mutually traceable.

## 1. Prepare the input

Prefer the paper PDF or a source-map JSON produced by `nature-reader`. Also state:

- the output language and directory;
- methods, experiments, or conclusions that need special scrutiny;
- whether external retrieval is allowed for background verification.

An abstract or partial text can start the workflow, but the output must use
`source-limited` mode and mark unseen content as `Not assessable`.

## 2. Invoke the skill

```text
Use nature-paper-card to deep-read this paper and generate an English Paper Card.
Focus on method modules, decisive experiments, conclusion boundaries,
and testable follow-up ideas.
```

Provide an exact path or accessible link when the input is outside the current
working directory.

## 3. Select a locator mode

| Mode | Use when | Locator contract |
|---|---|---|
| `page-grounded` | PDF page indices are reliable | Record the PDF page plus figure, table, equation, or section |
| `structure-grounded` | HTML/XML or page indices are unstable | Use section, paragraph, figure, table, or equation identifiers |
| `source-limited` | Only an abstract or excerpt is available | State the source boundary and do not infer unseen content |

The mode describes source traceability, not paper quality.

## 4. Standard artifacts

- `paper-card.md`: fixed Sections 01–16;
- `source_bundle.json`: normalized source and locator data;
- `audit-report.json`: structure, locator, and evidence-grounding audit;
- `rendered-pages/`: optional PDF pages for visual inspection.

The workflow builds an evidence inventory and claim–evidence matrix before the
card. External facts, Agent analysis, and research hypotheses must remain
distinct from statements made by the paper's authors.

## 5. Reproducible local checks

These paths are relative to the repository root. An Agent may instead resolve
the scripts from the installed Skill directory.

```bash
python3 skills/nature-paper-card/scripts/prepare_paper.py paper.pdf \
  --output source_bundle.json

python3 skills/nature-paper-card/scripts/audit_paper_card.py \
  --card paper-card.md \
  --bundle source_bundle.json \
  --locator-mode page-grounded \
  --report audit-report.json
```

For input without reliable PDF pagination, change `--locator-mode` to
`structure-grounded` or `source-limited`.

## 6. Acceptance checklist

- All Sections 01–16 are present, with no invented Sections 17 or 18.
- Central conclusions resolve to specific figures, tables, equations,
  experiments, or source excerpts.
- The card invents no unseen experiment, page number, or mechanism.
- Author claims, external facts, Agent analysis, and hypotheses are distinct.
- Follow-up ideas are falsifiable, actionable, and tied to an evidence origin.
- Audit failures are corrected and any residual limitations are explicit.
