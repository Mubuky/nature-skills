<!-- MODIFIED IN THIS DERIVATIVE: alignment is now conditional and completion is evidence-gated; see ../../../../NOTICE (Apache-2.0 section 4(b)). -->

# Writing workflow

Run these steps for drafting or restructuring. Planning may remain internal
unless an unresolved assumption requires author alignment.

## 1. Build a one-sentence argument

> In [system/problem], we show [advance] using [approach], supported by [evidence], with [boundary].

Force every section to serve this sentence. If the sentence cannot be written, the paper does not yet have an argument — surface that to the user.

## 1b. Build the Terminology Ledger

Preserve recurring terms, abbreviations, notation, and proper names. For
multi-section work or source terminology drift, load
`../../references/terminology-ledger.md`, record canonical forms, and reuse
them. A short, consistent passage needs only an internal terminology check.

## 2. Choose section architecture

Pick the section structure from the relevant `section/*.md` fragment and, if needed, deeper patterns from `references/article-architecture.md`.

## 3. Map each paragraph to one job

Each paragraph must do exactly one job from: context, gap, approach, result, comparison, mechanism, implication, limitation.

If a paragraph carries two jobs, split it before drafting.

## 3b. Conditional alignment

Proceed directly when the author-provided claim, evidence, boundary, target
section, and requested language are clear. Surface assumptions without waiting
when they are reversible and do not change scientific meaning.

Pause only when a high-leverage ambiguity would materially change the core
contribution, claim strength, leading result, target audience, or deliverable.
In that case show a compact one-sentence argument and ask at most 2–3 targeted
questions. Do not ask for facts the user already supplied.

If the user asks for an outline-first workflow, return the paragraph map before
prose. Do not impose this extra round by default. If the user says the voice is
wrong, request one short author sample only when it would materially improve
calibration; match its style, never its claims.

## 4. Draft from evidence outward

Keep claims near the data that support them. Do not stack claims at the top of a section then leave evidence at the bottom.

## 5. Calibrate verbs to evidence strength

`show` / `demonstrate` need strong direct evidence. `suggest` / `indicate` are for trend-level or indirect evidence. `may` / `could` are for plausible but unverified mechanisms.

## 6. Remove unsupported novelty and universal claims

Sweep for `first`, `unique`, `unprecedented`, `comprehensive`, `complete`, `always`, `never`. Replace with bounded claims or delete.

## 7. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).

For full reverse-outlining, open `references/paragraph-flow.md`.

## 8. Return prose plus notes

Output the draft together with explicit notes on assumptions, missing inputs, and where evidence is needed. See `output-format.md`.

## 9. Revise by targeted edit, not full rewrite

When the user reacts to a draft, localize the mismatch before editing. Preserve
correct passages unless the user requests a full rewrite or the correction
necessarily changes the section architecture.

- Change **only** the paragraphs or claims the user flagged; keep the rest verbatim.
- If a requested fix forces a structural change, state the change and reason;
  ask before applying it only when multiple materially different structures
  remain plausible.
- Keep the Terminology Ledger (step 1b) stable across revisions unless the user changes a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (steps 5-7), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to
  conditional alignment rather than patching prose on a broken premise.

## 10. Completion gate

Before delivery, verify that every substantive claim maps to author-provided
evidence or a visible placeholder; reported numbers, citations, terminology,
and claim strength remain consistent; all requested sections and constraints
are satisfied; and material uncertainties are stated without inventing content.
