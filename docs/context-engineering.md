<!-- Modified from the upstream repository structure; see ../NOTICE. -->

# Context-engineering design

This suite keeps the scientific depth of the source project while reducing the
context loaded before and during a task. The design is model-neutral: it uses
durable workflow contracts rather than model slugs, reasoning modes, or
provider-specific prompting tricks.

## Sources and interpretation

The architecture follows three primary references:

- [OpenAI GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6):
  state each instruction once, keep prompts and tool descriptions lean, define
  autonomy boundaries compactly, use outcome-focused prompts, and measure final
  quality before counting token or call reductions.
- [Anthropic's context-engineering guidance for Claude 5](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models):
  remove overlapping constraints, let capable agents use judgment outside
  high-risk boundaries, prefer expressive interfaces to example piles, and use
  progressive disclosure for skills, tools, verification, and references.
- [OpenAI's Codex skill documentation](https://developers.openai.com/plugins/build/skills):
  make each skill a focused workflow, use concise activation metadata, and put
  detailed policies, schemas, assets, and deterministic processing in adjacent
  resources.

The first two references describe current model behavior. Their numeric
performance claims and model-specific features are not encoded as permanent
skill rules. Only the cross-model engineering principles are retained.

## Runtime layers

Each installable directory has four layers:

1. `SKILL.md` is a short router and contract. It states the trigger boundary,
   required inputs, routing decisions, scientific red lines, output, and
   completion test.
2. `manifest.yaml` maps detected task axes to exact files. It is the routing
   source of truth; the router does not repeat every branch.
3. `static/` and `references/` contain stable domain knowledge, schemas,
   rubrics, examples, and deeper workflows. The router says exactly when to
   load each item.
4. `scripts/`, `templates/`, and `assets/` provide deterministic checks and
   high-fidelity artifacts when prose alone is less reliable.

Each skill is self-contained. A small set of shared scientific-writing
principles is materialized inside the skills that need it, avoiding a fragile
cross-directory runtime dependency.

## Authoring rules

- Frontmatter contains only `name` and `description`, as required by the Agent
  Skills format. Release metadata belongs in Git tags and repository history.
- The directory name, frontmatter name, manifest name, and UI metadata agree.
- Descriptions lead with the user goal, include only useful trigger language,
  and name an adjacent workflow when a negative boundary prevents ambiguity.
- A router states an instruction once. Details already expressed by a script,
  manifest, schema, or reference are linked, not copied.
- Hard requirements are reserved for research integrity, evidence provenance,
  privacy, irreversible actions, secret handling, legal access, and strict
  deliverable schemas. Style and implementation choices are expressed as
  criteria so the agent can adapt to the source material.
- Ask only when missing information would change scientific validity,
  authorization, an irreversible action, or the requested deliverable.
  Otherwise proceed with a visible assumption.
- Use deterministic code for parsing, validation, conversion, counting, and
  consistency checks. Keep evidence weighting, scientific interpretation, and
  final review under model judgment.
- Parallel work is optional and only appropriate for independent evidence or
  QA branches. Final scientific synthesis remains a single explicit gate.

## Context budgets

Repository validation enforces:

- no extra `SKILL.md` frontmatter keys;
- a bounded activation description;
- a bounded router length;
- complete `agents/openai.yaml` invocation metadata;
- valid local routes and links;
- labelled direct, indirect, incomplete, negative, and English implicit
  per-skill cases, plus suite-level negatives and multi-skill combinations.

These are static schema and coverage guardrails, not model activation accuracy
or quality proxies. A shorter router is accepted only if representative forward
tests still satisfy its evidence and deliverable contract.

## Evaluation loop

For a substantial change:

1. Re-run the same activation and workflow cases.
2. Compare activation precision, completion, evidence coverage, unsupported
   claims, required artifacts, and unresolved caveats.
3. Compare loaded context and execution cost only after quality passes.
4. Change one coherent instruction or resource group at a time when diagnosing
   regressions.
5. Retain examples only when they encode a real product requirement or repair a
   measured failure.

See `evals/` for the suite-level trigger set and forward-test rubric.
