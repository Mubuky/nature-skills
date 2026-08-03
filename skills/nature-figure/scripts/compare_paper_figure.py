#!/usr/bin/env python3
"""Compare a rerendered raster figure with a preserved golden image."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


def load_rgba(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return image.convert("RGBA")


def compare_images(reference_path: Path, candidate_path: Path) -> dict[str, object]:
    reference = load_rgba(reference_path)
    candidate = load_rgba(candidate_path)
    result: dict[str, object] = {
        "reference": reference_path.name,
        "candidate": candidate_path.name,
        "reference_size": list(reference.size),
        "candidate_size": list(candidate.size),
        "same_size": reference.size == candidate.size,
        "exact": False,
    }
    if reference.size != candidate.size:
        return result

    reference_array = np.asarray(reference, dtype=np.int16)
    candidate_array = np.asarray(candidate, dtype=np.int16)
    absolute = np.abs(reference_array - candidate_array)
    changed_pixels = np.any(absolute != 0, axis=2)
    result.update(
        exact=bool(not np.any(changed_pixels)),
        mae=float(absolute.mean() / 255.0),
        max_channel_difference=int(absolute.max()),
        changed_pixel_fraction=float(changed_pixels.mean()),
    )
    return result


def write_diagnostics(reference_path: Path, candidate_path: Path, diff_path: Path | None, overlay_path: Path | None) -> None:
    reference = load_rgba(reference_path)
    candidate = load_rgba(candidate_path)
    if reference.size != candidate.size:
        raise ValueError("diagnostic images require matching dimensions")
    if diff_path is not None:
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        ImageChops.difference(reference, candidate).save(diff_path)
    if overlay_path is not None:
        overlay_path.parent.mkdir(parents=True, exist_ok=True)
        Image.blend(reference, candidate, 0.5).save(overlay_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--require-exact", action="store_true")
    parser.add_argument("--diff-output", type=Path)
    parser.add_argument("--overlay-output", type=Path)
    args = parser.parse_args()

    result = compare_images(args.reference, args.candidate)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.diff_output is not None or args.overlay_output is not None:
        write_diagnostics(args.reference, args.candidate, args.diff_output, args.overlay_output)
    return 1 if args.require_exact and not result["exact"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
