#!/usr/bin/env python3
"""Verify upstream paper outputs, curated sources, and optimized variants."""

from __future__ import annotations

from paper_examples.gallery import MANIFEST_PATH, load_manifest, verify_gallery


def main() -> int:
    errors = verify_gallery()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    manifest = load_manifest()
    golden_count = sum(
        entry.get("mode") in {"hybrid-reference", "python-output"}
        for entry in manifest["entries"]
    )
    optimized_count = sum(
        entry.get("mode") == "optimized-output"
        for entry in manifest["entries"]
    )
    print(
        f"verified {golden_count} upstream golden outputs, "
        f"{optimized_count} optimized output{'s' if optimized_count != 1 else ''}, and "
        f"{len(manifest['source_files'])} curated source files from {MANIFEST_PATH.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
