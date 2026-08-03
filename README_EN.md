<!-- Rewritten from the upstream repository; see NOTICE for attribution. -->

# Nature Skills

[![License](https://img.shields.io/badge/license-Apache--2.0-2ea44f)](LICENSE)
![Skills](https://img.shields.io/badge/skills-11-0ea5e9)
[![Validate](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Mubuky/nature-skills/actions/workflows/validate.yml)
[中文](README.md)

Eleven focused Agent Skills for evidence-grounded research writing, literature
workflows, figures, submission, peer review, and research records. Each skill
is independently installable; detailed policies, rubrics, templates, and
deterministic scripts load only when needed.

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
| Activation-description characters for the final 11 skill names | 7,612 | 5,182 | -32% |
| Total `SKILL.md` lines for the final 11 skill names | 1,479 | 888 | -40% |
| `nature-downloader/SKILL.md` | 623 | 78 | -87% |
| Real-paper practice in `nature-figure` | Third-party project snapshot | 8 project families, 24 render entries, 42 original outputs | Faithful reorganization with regression baselines |

All skills now use two-field frontmatter, aligned names, concise boundaries,
generated `agents/openai.yaml`, self-contained references, five per-skill
activation case types, suite-level negatives, and multi-skill combinations.
High-risk research-integrity, access-control, patent, data, and statistics
constraints remain explicit.

`nature-figure` now preserves the complete Python example gallery from eight
real-paper project families and their original outputs as immutable visual
baselines. The pre-existing volcano, ROC, dot-plot, marginal, and paired
analytical tools remain independent rather than standing in for paper-specific
designs. Registry, hash, isolated-run, and image-difference checks constrain
later refactoring.

See [the design note](docs/context-engineering.md).

## Skill index

| Skill | Primary job |
|---|---|
| [`nature-academic-search`](skills/nature-academic-search/README_EN.md) | Multi-source discovery, bibliography verification, maps, and citation-network audits |
| [`nature-citation`](skills/nature-citation/README_EN.md) | Claim-level supporting literature and reference export |
| [`nature-downloader`](skills/nature-downloader/README_EN.md) | Lawful full-text and supporting-information retrieval |
| [`nature-writing`](skills/nature-writing/README_EN.md) | Evidence-grounded drafting, faithful polishing, LaTeX layout, and initial submission |
| [`nature-reviewer`](skills/nature-reviewer/README_EN.md) | Pre-submission referee simulation |
| [`nature-response`](skills/nature-response/README_EN.md) | Post-decision reviewer-response packages |
| [`nature-data`](skills/nature-data/README_EN.md) | Data/Code Availability, repositories, citations, and FAIR metadata |
| [`nature-statistics`](skills/nature-statistics/README_EN.md) | Manuscript statistical-design and reporting audit |
| [`nature-figure`](skills/nature-figure/README_EN.md) | Submission-grade scientific figures and final-size QA |
| [`nature-paper2ppt`](skills/nature-paper2ppt/README_EN.md) | Complete evidence-led academic PPTX decks |
| [`nature-paper-to-patent`](skills/nature-paper-to-patent/README_EN.md) | Evidence-traceable Chinese patent and disclosure drafts |

### Installation profiles

| Profile | Skills |
|---|---|
| Core (default) | `nature-academic-search`, `nature-citation`, `nature-data`, `nature-figure`, `nature-response`, `nature-reviewer`, `nature-writing` |
| On demand (GitHub non-core) | `nature-downloader`, `nature-statistics`, `nature-paper2ppt`, `nature-paper-to-patent` |

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

From a local clone, the updater defaults to the 7-skill `core` profile; use
`--profile all` for all 11:

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
python3 skills/nature-figure/scripts/check_paper_gallery.py
bash -n scripts/update-codex-skills.sh
python3 scripts/test_update_codex_skills.py
python3 -m unittest discover -s skills/nature-citation/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-paper-to-patent/tests -p 'test_*.py'
python3 -m unittest discover -s skills/nature-downloader/tests/python -p 'test_*.py'
python3 -m unittest discover -s skills/nature-figure/tests -p 'test_*.py'
node --test skills/nature-downloader/tests/unit/*.test.mjs
python3 skills/nature-figure/scripts/validate_figure.py --self-test
```

The 77 labelled cases in `evals/trigger_cases.jsonl` comprise 65 per-skill
cases (including the merged bibliography-verification and faithful-polishing
extensions), six suite-level negatives expected to activate no Nature skill,
and six multi-skill combinations. This corpus checks static schema, labels,
and coverage; it does not measure model activation accuracy. Substantial
changes should also run representative forward tests; quality and evidence
completeness come before context or cost reductions.

## License

The root project is licensed under [Apache License 2.0](LICENSE). Some components
retain separate MIT licences or attribution files. See [NOTICE](NOTICE) for
source revision, derivative status, and third-party material handling.

The real-paper plotting examples in `nature-figure` were reorganized from
[`ChenLiu-1996/figures4papers`](https://github.com/ChenLiu-1996/figures4papers)
at revision `6e9ca1200f4b1445cff68a42be76f7712ec2d4e1`. We thank Chen Liu for
sharing these paper-figure practices. The skill retains 25 Python source files,
29 Python-rendered PNGs, three companion PDFs, and ten hybrid reference images
under its `scripts/assets/references` structure without copying the repository
shell. All 42 upstream outputs remain immutable baselines. Narrow user-approved
source repairs record both upstream and current hashes, and optimized renders
are stored separately under `optimized/`.
