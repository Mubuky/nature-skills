#!/usr/bin/env python3
# Modified in the context-engineered edition; see repository NOTICE.
"""Validate lean, discoverable, self-contained Nature skills and Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ALLOWED_FRONTMATTER = {"name", "description"}
MIN_DESCRIPTION = 80
MAX_DESCRIPTION = 600
MAX_ROUTER_LINES = 180
INLINE_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REFERENCE_LINK_RE = re.compile(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)")
HTML_LINK_RE = re.compile(r"""(?i)\b(?:href|src)\s*=\s*["']([^"']+)["']""")
EXTERNAL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
TEMPLATE_MARKERS = ("{", "}", "[", "]", "*", "$(", "${", "...", "TO_CONFIRM", "TO CONFIRM")
IGNORED_MARKDOWN_DIRS = {".git", "node_modules", ".venv", "venv"}


def load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    try:
        raw = text.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def without_code(text: str) -> str:
    """Remove fenced and inline code so examples are not mistaken for links."""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in {"```", "~~~"}:
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence is None:
            kept.append(re.sub(r"`[^`\n]*`", "", line))
    return "\n".join(kept)


def markdown_destinations(path: Path) -> list[str]:
    text = without_code(path.read_text(encoding="utf-8", errors="replace"))
    destinations = (
        INLINE_LINK_RE.findall(text)
        + REFERENCE_LINK_RE.findall(text)
        + HTML_LINK_RE.findall(text)
    )
    return list(dict.fromkeys(item.strip() for item in destinations if item.strip()))


def is_template_destination(raw: str) -> bool:
    upper = raw.upper()
    return any(marker in raw or marker in upper for marker in TEMPLATE_MARKERS)


def local_links(path: Path) -> list[tuple[str, Path]]:
    targets: list[tuple[str, Path]] = []
    for raw in markdown_destinations(path):
        raw = raw[1:-1].strip() if raw.startswith("<") and raw.endswith(">") else raw
        if not raw or raw.startswith(("#", "/")) or EXTERNAL_SCHEME_RE.match(raw):
            continue
        if is_template_destination(raw):
            continue
        relative = unquote(raw.split("#", 1)[0].split("?", 1)[0])
        if relative:
            targets.append((raw, (path.parent / relative).resolve()))
    return targets


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())

    for skill_dir in skill_dirs:
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        try:
            frontmatter = load_frontmatter(skill_md)
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{name}/SKILL.md: {exc}")
            continue

        keys = set(frontmatter)
        if keys != ALLOWED_FRONTMATTER:
            errors.append(
                f"{name}/SKILL.md: frontmatter keys {sorted(keys)}; "
                f"expected {sorted(ALLOWED_FRONTMATTER)}"
            )
        if frontmatter.get("name") != name:
            errors.append(
                f"{name}/SKILL.md: name {frontmatter.get('name')!r} "
                "does not match the directory"
            )

        description = str(frontmatter.get("description", "")).strip()
        if not MIN_DESCRIPTION <= len(description) <= MAX_DESCRIPTION:
            errors.append(
                f"{name}/SKILL.md: description length {len(description)} "
                f"outside {MIN_DESCRIPTION}..{MAX_DESCRIPTION}"
            )

        line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_ROUTER_LINES:
            errors.append(
                f"{name}/SKILL.md: {line_count} lines exceeds {MAX_ROUTER_LINES}"
            )

        for raw, target in local_links(skill_md):
            try:
                target.relative_to(skill_dir.resolve())
            except ValueError:
                errors.append(
                    f"{name}/SKILL.md: local link escapes skill directory: {raw}"
                )

        manifest = skill_dir / "manifest.yaml"
        try:
            manifest_data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"{name}/manifest.yaml: {exc}")
        else:
            if not isinstance(manifest_data, dict) or manifest_data.get("name") != name:
                errors.append(f"{name}/manifest.yaml: name does not match directory")

        metadata = skill_dir / "agents" / "openai.yaml"
        try:
            metadata_data = yaml.safe_load(metadata.read_text(encoding="utf-8"))
            interface = metadata_data["interface"]
            policy = metadata_data["policy"]
        except (OSError, UnicodeError, yaml.YAMLError, KeyError, TypeError) as exc:
            errors.append(f"{name}/agents/openai.yaml: invalid metadata: {exc}")
        else:
            short = str(interface.get("short_description", ""))
            prompt = str(interface.get("default_prompt", ""))
            if not 25 <= len(short) <= 64:
                errors.append(
                    f"{name}/agents/openai.yaml: short_description length "
                    f"{len(short)} outside 25..64"
                )
            if f"${name}" not in prompt:
                errors.append(
                    f"{name}/agents/openai.yaml: default_prompt must mention ${name}"
                )
            if policy.get("allow_implicit_invocation") is not True:
                errors.append(
                    f"{name}/agents/openai.yaml: implicit invocation must be explicit"
                )

        for reference in skill_dir.rglob("*.md"):
            if reference == skill_md:
                continue
            lines = len(reference.read_text(encoding="utf-8", errors="replace").splitlines())
            if lines > 500:
                warnings.append(
                    f"{reference.relative_to(ROOT)}: {lines} lines; consider splitting"
                )

    checked_links = 0
    markdown_files = sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in IGNORED_MARKDOWN_DIRS for part in path.relative_to(ROOT).parts)
    )
    for markdown in markdown_files:
        for raw, target in local_links(markdown):
            checked_links += 1
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"{markdown.relative_to(ROOT)}: local link escapes repository: {raw}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{markdown.relative_to(ROOT)}: broken local link: {raw}"
                )

    if errors:
        print("Context-engineering validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Context-engineering validation passed: "
        f"{len(skill_dirs)} skills, {len(markdown_files)} Markdown files, "
        f"{checked_links} local links."
    )
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
