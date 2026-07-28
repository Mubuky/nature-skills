<!-- Rewritten from the upstream repository; see NOTICE for attribution. -->

# Nature Skills

[![License](https://img.shields.io/badge/license-Apache--2.0-2ea44f)](LICENSE)
![Skills](https://img.shields.io/badge/skills-15-0ea5e9)
[![Validate](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml)
[中文](README.md)

Fifteen focused Agent Skills for evidence-grounded research writing, paper
reading, literature workflows, figures, submission, peer review, and research
records. Each skill is independently installable; detailed policies, rubrics,
templates, and deterministic scripts load only when needed.

This is an independently maintained derivative of
[`Yuan1z0825/nature-skills`](https://github.com/Yuan1z0825/nature-skills).
It starts from a new Git history and is not a GitHub fork. See
[NOTICE](NOTICE) for the source revision and attribution.

## Context-engineering changes

The design combines the
[OpenAI GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6),
[Anthropic Claude 5 context-engineering guidance](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models),
and [OpenAI Codex skill documentation](https://developers.openai.com/plugins/build/skills).

Compared with the adopted upstream HEAD:

| Metric | Upstream | This repository | Change |
|---|---:|---:|---:|
| Activation-description characters for the retained 15 skills | 10,462 | 5,481 | -48% |
| Total `SKILL.md` lines for the retained 15 skills | 1,970 | 1,113 | -44% |
| `nature-downloader/SKILL.md` | 623 | 78 | -87% |
| `nature-figure` directory | ~34 MB | ~5.8 MB | Unlicensed third-party snapshot removed |

All skills now use two-field frontmatter, aligned names, concise boundaries,
generated `agents/openai.yaml`, self-contained references, five per-skill
activation case types, suite-level negatives, and multi-skill combinations.
High-risk research-integrity, access-control, patent, data, and statistics
constraints remain explicit.

See [the design note](docs/context-engineering.md).

## Skill index

| Skill | Primary job |
|---|---|
| [`nature-academic-search`](skills/nature-academic-search/README_EN.md) | Multi-source discovery, search strategies, maps, and citation-network audits |
| [`nature-citation`](skills/nature-citation/README_EN.md) | Claim-level supporting literature and reference export |
| [`nature-ref-verifier`](skills/nature-ref-verifier/README_EN.md) | Field-level verification of existing bibliography metadata |
| [`nature-downloader`](skills/nature-downloader/README_EN.md) | Lawful full-text and supporting-information retrieval |
| [`nature-reader`](skills/nature-reader/README_EN.md) | Full bilingual, figure-aware, source-anchored paper readers |
| [`nature-paper-card`](skills/nature-paper-card/README_EN.md) | Source-grounded deep-reading cards for one paper |
| [`nature-writing`](skills/nature-writing/README_EN.md) | Evidence-grounded manuscript and initial-submission drafting |
| [`nature-polishing`](skills/nature-polishing/README_EN.md) | Claim-preserving prose editing, translation, and LaTeX layout |
| [`nature-reviewer`](skills/nature-reviewer/README_EN.md) | Pre-submission referee simulation |
| [`nature-response`](skills/nature-response/README_EN.md) | Post-decision reviewer-response packages |
| [`nature-data`](skills/nature-data/README_EN.md) | Data/Code Availability, repositories, citations, and FAIR metadata |
| [`nature-statistics`](skills/nature-statistics/README_EN.md) | Manuscript statistical-design and reporting audit |
| [`nature-figure`](skills/nature-figure/README_EN.md) | Submission-grade scientific figures and final-size QA |
| [`nature-paper2ppt`](skills/nature-paper2ppt/README_EN.md) | Complete evidence-led academic PPTX decks |
| [`nature-paper-to-patent`](skills/nature-paper-to-patent/README_EN.md) | Evidence-traceable Chinese patent and disclosure drafts |

## Install

List skills:

```bash
npx skills add Mubuky/nature-skills --list
```

Install one skill:

```bash
npx skills add Mubuky/nature-skills --global --agent codex \
  --skill nature-writing --yes --copy
```

Install all skills:

```bash
npx skills add Mubuky/nature-skills --global --agent codex \
  --skill '*' --yes --copy
```

From a local clone, the updater defaults to the 11-skill `core` profile; use
`--profile all` for all 15:

```bash
scripts/update-codex-skills.sh --profile core
scripts/update-codex-skills.sh --check --profile core
```

Restart Codex or the host agent after installation. Runtime dependencies such
as Python, R, browser access, MCP servers, or publisher credentials remain
optional and workflow-specific.

## Validate

```bash
python3 scripts/generate_openai_metadata.py
git diff --exit-code -- skills
python3 scripts/validate_context_engineering.py
python3 scripts/validate_trigger_cases.py
python3 scripts/validate-repository.py
python3 scripts/validate-skill-metadata.py
python3 scripts/validate-workflows.py
bash -n scripts/update-codex-skills.sh
python3 scripts/test_update_codex_skills.py
python3 -m unittest discover -s skills/nature-citation/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-paper-to-patent/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-downloader/tests/python -p 'test_*.py'
node --test skills/nature-downloader/tests/unit/*.test.mjs
python3 skills/nature-figure/scripts/validate_figure.py --self-test
```

The 88 labelled cases in `evals/trigger_cases.jsonl` comprise 75 per-skill
cases, six suite-level negatives expected to activate no Nature skill, and
seven multi-skill combinations. This corpus checks static schema, labels, and
coverage; it does not measure model activation accuracy. Substantial changes
should also run representative forward tests; quality and evidence completeness
come before context or cost reductions.

## License

The root project is licensed under [Apache License 2.0](LICENSE). Some components
retain separate MIT licences or attribution files. See [NOTICE](NOTICE) for
source revision, derivative status, and third-party material handling.
