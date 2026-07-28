#!/usr/bin/env python3
# Modified in the context-engineered edition; see repository NOTICE.
"""Generate Codex/ChatGPT UI metadata for every Nature skill."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

UI = {
    "nature-academic-search": (
        "Nature Academic Search",
        "Discover and map scholarly literature",
        "Use $nature-academic-search to build a reproducible search strategy and evidence table for this research question.",
    ),
    "nature-citation": (
        "Nature Citation Support",
        "Match manuscript claims to verified citations",
        "Use $nature-citation to discover candidate literature, verify claim-level support, and export only the screened references.",
    ),
    "nature-data": (
        "Nature Data Availability",
        "Prepare publication-ready data availability",
        "Use $nature-data to draft and audit a journal-ready Data and Code Availability package for this manuscript.",
    ),
    "nature-downloader": (
        "Nature Literature Downloader",
        "Retrieve lawful full text and supplements",
        "Use $nature-downloader to lawfully retrieve and validate the full text and requested supplements for these known papers.",
    ),
    "nature-figure": (
        "Nature Scientific Figures",
        "Build and audit publication-grade figures",
        "Use $nature-figure to create, revise, or audit this submission-grade scientific figure and validate the available exports.",
    ),
    "nature-paper-card": (
        "Nature Paper Card",
        "Create a grounded deep-reading paper card",
        "Use $nature-paper-card to create a source-grounded deep-reading card for this paper.",
    ),
    "nature-paper-to-patent": (
        "Nature Paper to Patent",
        "Turn research evidence into Chinese patent drafts",
        "Use $nature-paper-to-patent to turn these materials into the requested evidence-traceable Chinese technical disclosure or patent draft.",
    ),
    "nature-paper2ppt": (
        "Nature Paper to PPTX",
        "Build evidence-led academic slide decks",
        "Use $nature-paper2ppt to build a complete academic presentation from this paper and run available structural and rendered visual QA.",
    ),
    "nature-polishing": (
        "Nature Academic Polishing",
        "Polish academic prose without changing claims",
        "Use $nature-polishing to polish this manuscript text while preserving every scientific claim and uncertainty.",
    ),
    "nature-reader": (
        "Nature Bilingual Reader",
        "Create bilingual, source-anchored paper readers",
        "Use $nature-reader to create a bilingual, figure-aware, source-anchored reader for this full paper.",
    ),
    "nature-ref-verifier": (
        "Nature Reference Verifier",
        "Verify every field in existing references",
        "Use $nature-ref-verifier to verify every bibliographic field in this reference list and report safe corrections.",
    ),
    "nature-response": (
        "Nature Reviewer Response",
        "Draft rigorous reviewer-response packages",
        "Use $nature-response to draft a point-by-point response package for this editor decision and reviewer feedback.",
    ),
    "nature-reviewer": (
        "Nature Reviewer",
        "Simulate a rigorous pre-submission peer review",
        "Use $nature-reviewer to simulate a rigorous pre-submission peer review of this manuscript.",
    ),
    "nature-statistics": (
        "Nature Statistics",
        "Audit manuscript statistics and reporting",
        "Use $nature-statistics to audit the statistical methods, results wording, and figure legends in this manuscript.",
    ),
    "nature-writing": (
        "Nature Manuscript Writing",
        "Draft manuscripts and initial submissions",
        "Use $nature-writing to draft or structurally rebuild this manuscript from the supplied evidence and author notes.",
    ),
}


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render(display_name: str, short_description: str, default_prompt: str) -> str:
    return (
        "# MODIFIED IN THIS DERIVATIVE: generated UI metadata; see "
        "../../../NOTICE (Apache-2.0 section 4(b)).\n"
        "interface:\n"
        f"  display_name: {quoted(display_name)}\n"
        f"  short_description: {quoted(short_description)}\n"
        f"  default_prompt: {quoted(default_prompt)}\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )


def main() -> int:
    skill_dirs = {
        path.name: path
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if set(skill_dirs) != set(UI):
        missing = sorted(set(skill_dirs) - set(UI))
        stale = sorted(set(UI) - set(skill_dirs))
        raise SystemExit(f"metadata map mismatch: missing={missing}, stale={stale}")

    for name, values in sorted(UI.items()):
        agents_dir = skill_dirs[name] / "agents"
        agents_dir.mkdir(exist_ok=True)
        (agents_dir / "openai.yaml").write_text(render(*values), encoding="utf-8")

    print(f"Generated metadata for {len(UI)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
