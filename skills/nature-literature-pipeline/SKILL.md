---
name: nature-literature-pipeline
description: >-
  Configure recurring or periodically rerun literature-monitoring pipelines
  that search, score, deduplicate, summarize, deliver, and archive papers.
  Use for 每日/每周文献推送、定时检索、自动文献监控 or research digests.
  Do not use for one-off search, claim-level citation placement, full-text
  downloading alone, or deep analysis of one paper.
---

<!-- Modified from Yuan1z0825/nature-skills; see ../../NOTICE. -->

# Nature Literature Pipeline

Use this workflow only when discovery is recurring, scheduled, or designed to
be rerun with persistent state.
Route a one-off search to `nature-academic-search`.

## Configure

Establish the research scope, inclusion/exclusion criteria, date window,
sources, frequency, candidate and delivery budgets, reading depth, delivery
target, archive target, and authorization for external writes.

Read [manifest.yaml](manifest.yaml). Load only the reference or template needed
for the current stage; weights and counts are configurable, not universal.

## Pipeline

1. **Search** with a saved query and source list; record unavailable sources.
2. **Normalize and deduplicate** by DOI, preprint ID, title/version, and other
   stable identifiers without collapsing distinct versions silently.
3. **Prioritize** using the configured rubric. Treat model scores as ranking
   aids, not truth about quality, novelty, or credibility.
4. **Read** at an explicit level: metadata, abstract, or full text. Every factual
   summary must be traceable to material actually read.
5. **Deliver and archive** only to user-authorized destinations, with provenance,
   source links, dedup decisions, and failure notes.

Use [references/scheduling.md](references/scheduling.md) for deployment rather
than assuming a particular cron product or always-on machine.

## Integrity rules

- Never present metadata-only or abstract-only reading as full-text analysis.
- Do not infer scientific quality from institution, venue, citation count, or
  author prominence alone.
- Preserve preprint, accepted, and version-of-record relationships.
- Do not let a ranking score replace inclusion criteria or human review.
- Do not modify a knowledge base, send messages, or create recurring jobs
  without the user's configured authorization.

## Completion

Each run records query version, run time, sources, candidate/selected counts,
reading level, dedup rules, failed sources, delivery result, and archive paths.
Finish only when every selected paper has a traceable note and every external
side effect has a recorded outcome.
