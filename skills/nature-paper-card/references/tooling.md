# Paper Card tooling

<!-- New in this derivative; see ../../../NOTICE. -->

Resolve scripts from the directory containing the loaded `SKILL.md`, never from
the user's working directory.

## Prepare

For a PDF or compatible `nature-reader` source map:

```text
python3 SKILL_DIR/scripts/prepare_paper.py INPUT \
  --output WORKDIR/source_bundle.json
```

Add `--render-dir WORKDIR/rendered-pages` when visual page review is necessary.
Inspect the exit status and bundle validation before choosing `page-grounded`.

If preparation fails, prefer an existing source map or the environment's normal
PDF/OCR capability. Do not create or patch a substitute extraction script during
a Paper Card task. Downgrade the locator mode to the strongest supported mode.

## Audit

For `page-grounded`:

```text
python3 SKILL_DIR/scripts/audit_paper_card.py \
  --card WORKDIR/paper-card.md \
  --bundle WORKDIR/source_bundle.json \
  --locator-mode page-grounded \
  --report WORKDIR/audit-report.json
```

For a fallback mode, omit `--bundle` and pass the exact canonical mode.

Audit errors block delivery. Review warnings with scientific judgment instead
of suppressing them mechanically. If the auditor cannot run, state the failure
and apply its documented checks manually; do not write a replacement auditor.
