"""Integrity checks for preserved paper examples and golden outputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .registry import EXAMPLES


SKILL_DIR = Path(__file__).resolve().parents[2]
MANIFEST_PATH = SKILL_DIR / "assets" / "paper-patterns" / "manifest.json"


def sha256(path: Path, *, normalize_text: bool = False) -> str:
    """Hash a file, optionally making text hashes independent of line endings."""
    content = path.read_bytes()
    if normalize_text:
        content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_gallery(path: Path = MANIFEST_PATH) -> list[str]:
    manifest = load_manifest(path)
    errors: list[str] = []

    entries = manifest.get("entries")
    source_files = manifest.get("source_files")
    if not isinstance(entries, list) or not isinstance(source_files, list):
        return ["manifest must contain entries and source_files arrays"]

    source_paths = {
        entry.get("path")
        for entry in source_files
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }

    for entry in [*entries, *source_files]:
        relative = entry.get("path")
        expected_hash = entry.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected_hash, str):
            errors.append("manifest entry is missing path or sha256")
            continue
        candidate = SKILL_DIR / relative
        if not candidate.is_file():
            errors.append(f"missing preserved file: {relative}")
        elif sha256(candidate, normalize_text=relative in source_paths) != expected_hash:
            errors.append(f"preserved file changed: {relative}")

    for entry in entries:
        if entry.get("mode") != "optimized-output":
            continue
        baseline = entry.get("baseline_path")
        if not isinstance(baseline, str) or not (SKILL_DIR / baseline).is_file():
            errors.append(f"optimized output has no preserved baseline: {entry.get('path')}")

    for entry in source_files:
        if "curation" not in entry:
            continue
        upstream_hash = entry.get("upstream_sha256")
        if not isinstance(upstream_hash, str):
            errors.append(f"curated source is missing upstream_sha256: {entry.get('path')}")

    registered_assets = {
        f"assets/paper-patterns/python/{example.project}/{name}"
        for example in EXAMPLES
        for name in example.outputs
    }
    manifest_python_assets = {
        str(entry["path"])
        for entry in entries
        if entry.get("mode") == "python-output"
    }
    if registered_assets != manifest_python_assets:
        missing = sorted(registered_assets - manifest_python_assets)
        extra = sorted(manifest_python_assets - registered_assets)
        if missing:
            errors.append("registry outputs missing from manifest: " + ", ".join(missing))
        if extra:
            errors.append("manifest outputs missing from registry: " + ", ".join(extra))

    registered_scripts = {f"scripts/paper_examples/{example.script}" for example in EXAMPLES}
    manifest_scripts = {str(entry["path"]) for entry in source_files}
    missing_scripts = sorted(registered_scripts - manifest_scripts)
    if missing_scripts:
        errors.append("registered scripts missing from manifest: " + ", ".join(missing_scripts))

    return errors
