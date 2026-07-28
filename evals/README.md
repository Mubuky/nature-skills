<!-- Modified in the context-engineered edition; see ../NOTICE. -->

# Static routing coverage

`trigger_cases.jsonl` is a labelled routing-coverage corpus, not a record of
model predictions. Its 88 cases contain:

- 75 per-skill cases: `direct`, `indirect`, `incomplete`, `negative`, and
  `implicit-en` for each of the 15 skills;
- 6 `suite-negative` cases with `expected: []`;
- 7 `multi-skill` cases with two or more expected skills.

Each JSONL object follows
[`trigger_case.schema.json`](trigger_case.schema.json): it has a unique `id`, a
`kind`, a non-empty `prompt`, and an `expected` list. Per-skill cases also
require `skill`; suite-level negatives and multi-skill cases omit it. `expected`
is a static intended-routing label: it does not imply that any model or agent
produced that route.

`scripts/validate_trigger_cases.py` checks this schema, label validity,
uniqueness, and minimum coverage. It does not execute a model and therefore must
not be reported as activation accuracy, precision, recall, or benchmark
performance.

For workflow forward tests, evaluate:

1. correct skill and reference routing;
2. completion of the requested artifact;
3. evidence provenance and unsupported-claim rate;
4. preservation of scientific uncertainty and user data;
5. required validation and final-artifact inspection;
6. unnecessary questions, tools, and loaded context;
7. clear blockers, caveats, and next action.

Quality gates come before context or cost reductions. Compare a changed router
against the same cases and source artifacts. Record context size and execution
cost only after both outputs pass the scientific and deliverable contract.
