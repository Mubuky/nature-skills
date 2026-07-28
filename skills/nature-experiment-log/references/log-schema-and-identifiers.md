# Experiment-log schema and identifiers

<!-- New in this derivative; see ../../../NOTICE. -->

Adapt the field set to the laboratory while keeping stable semantics.

## Minimum frontmatter

```yaml
experiment_id: ""
date: "YYYY-MM-DD"
title: ""
status: "planned|running|completed|failed|partial"
sample_ids: []
batch_ids: []
operators: []
instruments: []
source_materials: []
unknown_fields: []
```

Add domain fields only when supplied or defined by the laboratory, for example
temperature, atmosphere, electrochemical cell, acquisition software, reagent
lot, model seed, dataset version, or code commit.

## Identifier requirements

An identifier must be unique within the configured store, stable after the
record is created, and separable from a descriptive title. Prefer a laboratory
scheme supplied by the user. If none exists, propose:

```text
EXP-YYYYMMDD-NNN
SAMPLE-<project>-NNN
BATCH-<project>-NNN
```

Check the index before assigning the next sequence. Do not infer semantic
meaning from an identifier unless the naming policy defines it.

## Body structure

1. Objective or question
2. Inputs and provenance
3. Protocol as performed
4. Direct observations and instrument outputs
5. Calculations or transformations
6. Interpretation, visibly labelled
7. Deviations and anomalies
8. Follow-up actions
9. Raw-material links
10. Change log

Use original units beside normalized values when conversion matters. Keep a
correction as a dated append-only note that names the corrected field and
reason.
