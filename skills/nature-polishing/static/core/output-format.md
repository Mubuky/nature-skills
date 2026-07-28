<!-- MODIFIED IN THIS DERIVATIVE: concise default output and a scientific-fidelity gate differ from upstream; see ../../../../NOTICE (Apache-2.0 section 4(b)). -->

# Output format

Default output:

1. The polished text as plain prose, not in a code block.
2. `Revision notes:` only when a structural choice, residual ambiguity, fidelity
   risk, or requested style decision is material. Keep them brief.

If the user asks for side-by-side revision, provide:

- `Original`
- `Polished`
- `Why changed`

If any paragraph's structural problem could not be fixed without inventing content, say so under `Revision notes:` instead of papering over it.

## Fidelity gate

Before returning the edit, compare it with the source and verify:

- numbers, units, statistical symbols, equations, citations, figure/table
  references, and technical terms are unchanged unless explicitly requested;
- subjects, comparators, populations, conditions, temporal scope, negation, and
  modality still match;
- claim strength, causal language, novelty, generality, and uncertainty have
  not drifted; and
- no claim, evidence, mechanism, limitation, or contradiction was silently
  added or removed.

If a desirable edit would fail this gate, preserve the source meaning and flag
the issue instead of silently making the change.
