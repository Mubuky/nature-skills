#!/usr/bin/env python3
# Modified in the context-engineered edition; see repository NOTICE.
"""Validate the static, labelled activation-coverage corpus."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "trigger_cases.jsonl"
SCHEMA = ROOT / "evals" / "trigger_case.schema.json"
PER_SKILL_KINDS = {"direct", "indirect", "incomplete", "negative", "implicit-en"}
GLOBAL_KINDS = {"suite-negative", "multi-skill"}
KINDS = PER_SKILL_KINDS | GLOBAL_KINDS
MIN_GLOBAL_CASES = {"suite-negative": 4, "multi-skill": 4}
ALLOWED_FIELDS = {"id", "skill", "kind", "prompt", "expected"}
CASE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def main() -> int:
    skills = {
        path.name
        for path in (ROOT / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    errors: list[str] = []
    ids: Counter[str] = Counter()
    coverage: dict[str, set[str]] = defaultdict(set)
    kind_counts: Counter[str] = Counter()
    case_count = 0

    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        schema_kinds = set(schema["properties"]["kind"]["enum"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"{SCHEMA.relative_to(ROOT)}: invalid schema metadata: {exc}")
    else:
        if schema_kinds != KINDS:
            errors.append(
                f"{SCHEMA.relative_to(ROOT)}: kind enum does not match validator"
            )

    for line_number, raw in enumerate(CASES.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        case_count += 1
        try:
            case = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(case, dict):
            errors.append(f"line {line_number}: case must be an object")
            continue

        unknown_fields = sorted(set(case) - ALLOWED_FIELDS)
        if unknown_fields:
            errors.append(
                f"line {line_number}: unknown fields {unknown_fields}"
            )

        case_id_value = case.get("id")
        case_id = case_id_value if isinstance(case_id_value, str) else ""
        raw_skill = case.get("skill")
        skill = str(raw_skill) if raw_skill is not None else ""
        kind_value = case.get("kind")
        kind = kind_value if isinstance(kind_value, str) else ""
        expected = case.get("expected")
        prompt_value = case.get("prompt")
        prompt = prompt_value if isinstance(prompt_value, str) else ""

        ids[case_id] += 1
        if case_id and not CASE_ID_RE.fullmatch(case_id):
            errors.append(f"line {line_number}: invalid id {case_id!r}")
        if raw_skill is not None and not isinstance(raw_skill, str):
            errors.append(f"line {line_number}: skill must be a string")
        if kind not in KINDS:
            errors.append(f"line {line_number}: unknown kind {kind!r}")
        else:
            kind_counts[kind] += 1
        if kind in PER_SKILL_KINDS:
            if skill not in skills:
                errors.append(f"line {line_number}: unknown skill {skill!r}")
            coverage[skill].add(kind)
        if not isinstance(prompt_value, str) or not prompt.strip():
            errors.append(f"line {line_number}: prompt must be a non-empty string")
        if not isinstance(expected, list):
            errors.append(f"line {line_number}: expected must be a list")
            expected = []
        elif any(not isinstance(item, str) for item in expected):
            errors.append(f"line {line_number}: expected items must be strings")
        elif len(expected) != len(set(expected)):
            errors.append(f"line {line_number}: expected contains duplicates")
        if any(item not in skills for item in expected):
            errors.append(f"line {line_number}: expected contains unknown skill")

        if kind == "suite-negative":
            if skill:
                errors.append(f"line {line_number}: suite-negative must omit skill")
            if expected != []:
                errors.append(f"line {line_number}: suite-negative must use expected=[]")
            if "$nature-" in prompt:
                errors.append(f"line {line_number}: suite-negative must be implicit")
        elif kind == "multi-skill":
            if skill:
                errors.append(f"line {line_number}: multi-skill must omit skill")
            if len(expected) < 2:
                errors.append(f"line {line_number}: multi-skill needs at least two expected skills")
        elif kind in PER_SKILL_KINDS:
            if not expected:
                errors.append(f"line {line_number}: expected must be non-empty")
            if kind == "negative" and skill in expected:
                errors.append(f"line {line_number}: negative case must route away from {skill}")
            if kind != "negative" and skill not in expected:
                errors.append(f"line {line_number}: expected must include {skill}")
            if kind == "direct" and f"${skill}" not in prompt:
                errors.append(f"line {line_number}: direct case must mention ${skill}")
            if kind == "implicit-en":
                if "$nature-" in prompt:
                    errors.append(f"line {line_number}: implicit-en must not name a skill")
                if not re.search(r"[A-Za-z]{3}", prompt):
                    errors.append(f"line {line_number}: implicit-en needs English text")

    for case_id, count in ids.items():
        if not case_id:
            errors.append("one or more cases have an empty id")
        elif count > 1:
            errors.append(f"duplicate case id {case_id!r}")
    for skill in sorted(skills):
        missing = PER_SKILL_KINDS - coverage[skill]
        if missing:
            errors.append(f"{skill}: missing case kinds {sorted(missing)}")
    for kind, minimum in MIN_GLOBAL_CASES.items():
        if kind_counts[kind] < minimum:
            errors.append(
                f"{kind}: {kind_counts[kind]} cases, expected at least {minimum}"
            )

    if errors:
        print("Trigger-case validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Trigger-case validation passed: {case_count} cases, "
        f"{len(skills)} skills, five per-skill kinds plus suite-level cases. "
        "This is static label/coverage validation, not model activation accuracy."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
