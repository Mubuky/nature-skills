<!-- Modified from Yuan1z0825/nature-skills; see ../../../NOTICE. -->

# QA checklist

## Grounding checks

- Every substantive evaluation should be traceable to either:
  - `references/editorial criteria and processes.md`, or
  - manuscript facts explicitly supplied by the user.
- No reviewer persona detail should appear beyond allowed `emphasis` labels.
- No technical failing should be invented from domain habit alone when the supplied material does not show it.
- Every substantive concern has a stable concern ID, `claim_pointer`, and `evidence_pointer`.
- Page, line, figure, and table identifiers are supplied or directly verified; otherwise the pointer says `location not provided` or `not assessable from supplied material`.

## Technical coverage checks

- The internal 12-axis matrix was considered without being dumped into the final report.
- Each axis is marked internally as `applicable`, `not applicable`, or `not assessable`; absence of evidence is not silently treated as a defect.
- The technical taxonomy supplements the five source-grounded Nature axes and does not create policy claims or severity statistics.

## Coverage checks

- Confirm the configured number of reviewer reports exists: the
  user-requested count when supplied, otherwise three.
- Confirm reports differ in `emphasis` only.
- Confirm each reviewer still addresses all core axes, even if briefly.
- Confirm a `Cross-review synthesis` section exists.
- Confirm a `Risk / unsupported claims` section exists.

## Boundary checks

- Confirm the output stays in reviewer-assessment mode, not author-response mode.
- Confirm the output does not claim a final editorial decision.
- Confirm broad-interest judgment is expressed cautiously, because the source assigns that final judgment to editors.

## Non-invention checks

- No invented reviewer identity, specialty, institution, or selection history.
- No invented experiments, controls, analyses, line numbers, citations, prior-work details, or figure-specific content absent from the input.
- If evidence is partial, mark `AUTHOR_INPUT_NEEDED` or `Not assessable from provided material`.

## Consistency checks

- Shared manuscript facts should stay consistent across all reviewer reports.
- Divergence across reviewers should reflect weighting differences, not contradictory factual claims.
- Technical failings listed in the synthesis should match issues already raised in at least one individual report.
- Consensus issues were raised by at least two reviewer reports and map to the same underlying issue key.
- Preserve important single-reviewer concerns as weighting differences instead of deleting them.

## Issue-key and synthesis checks

- Normalize concerns to internal issue keys before comparing reviewer reports.
- Reuse one issue key for the same underlying concern; do not split a shared
  concern merely to make reports look different.
- Supported overlap is allowed. Remove redundant prose or let the synthesis
  consolidate it, but never invent diversity or redistribute concerns away
  from the reviewer whose emphasis genuinely activates them.
- Ensure every consensus statement maps to an issue key raised by at least two
  reports. Keep supported single-reviewer issues as differences in emphasis.

## Final release rule

- If the skill cannot produce the configured reviewer package without major
  invention, return a bounded draft review with explicit missing-information
  flags rather than pretending certainty.
