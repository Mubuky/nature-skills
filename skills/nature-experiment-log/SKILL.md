---
name: nature-experiment-log
description: >-
  Turn user-supplied experiment notes, images, or transcripts into structured
  Markdown records with stable experiment/sample IDs, raw-material links,
  anomaly entries, and index updates. Use for 实验日志、实验记录、样品批次、
  归档实验图片 or Feishu-to-vault logging. Do not invent measurements,
  analyse results statistically, monitor literature, or draft manuscript Methods.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Experiment Log

Convert raw observations into a traceable record. Markdown is the default
artifact; Obsidian and Feishu are optional input/storage adapters, not required
dependencies.

## Intake and routing

Identify the supplied text, images, voice transcripts, files, existing record,
target store, and local naming convention. Read [manifest.yaml](manifest.yaml)
and load only the relevant schema, example, or template.

Ask only when an unknown would change sample identity, measurement meaning,
units, timestamp, instrument, protocol step, or storage destination. Otherwise
record the uncertainty explicitly.

## Integrity rules

- Preserve raw material unchanged and link it by a stable relative path or
  immutable identifier. Never silently overwrite it.
- Separate direct observation, instrument output, calculation, interpretation,
  and follow-up action.
- Mark OCR or visual extraction with its source and confidence; do not convert
  a visual estimate into a measured value.
- Use `UNKNOWN` for unresolved facts. Do not guess sample IDs, batch IDs,
  parameters, units, timing, instrument settings, or operators.
- Append anomalies and corrections. Preserve the prior record and change
  history rather than deleting inconvenient outcomes.

## Workflow

1. Inventory and archive the raw inputs.
2. Extract facts with provenance and normalize units without changing values.
3. Resolve or assign experiment and sample/batch identifiers using
   [references/log-schema-and-identifiers.md](references/log-schema-and-identifiers.md).
4. Write the structured log and link every raw artifact.
5. Append anomaly/deviation entries when needed.
6. Update the configured index and any equipment/reagent tracker.
7. Validate YAML, links, identifiers, dates, and required fields.

Use the bundled examples only when they match the experiment family; do not
copy their material-specific device codes or values into unrelated work.

## Output

Return the log path, experiment ID, sample/batch IDs, raw-material location,
index/anomaly updates, and unresolved fields. Finish only when the frontmatter
parses, raw links resolve, the index is updated, and every unknown is visible.
