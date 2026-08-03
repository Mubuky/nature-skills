#!/usr/bin/env python3
"""Render an isolated, paper-specific example without restyling it."""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from paper_examples.registry import EXAMPLES, PaperExample, get_example


SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SCRIPT_DIR / "paper_examples"

MODULE_NAMES = {
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "scipy": "scipy",
    "seaborn": "seaborn",
    "python-dateutil": "dateutil",
}

LATEX_COMMANDS = ("latex", "dvipng", "kpsewhich")
LATEX_PACKAGES = ("helvet.sty",)


def _font_available(family: str) -> bool:
    from matplotlib import font_manager

    try:
        font_manager.findfont(
            font_manager.FontProperties(family=family),
            fallback_to_default=False,
        )
    except ValueError:
        return False
    return True


def _requires_system_font(example: PaperExample) -> bool:
    """Return whether Matplotlib must resolve the family from local fonts."""
    return example.font_family is not None and "latex" not in example.requirements


def _tex_package_available(filename: str) -> bool:
    """Return whether the active TeX distribution resolves a required file."""
    kpsewhich = shutil.which("kpsewhich")
    if kpsewhich is None:
        return False
    try:
        result = subprocess.run(
            [kpsewhich, filename],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and bool(result.stdout.strip())


def missing_requirements(example: PaperExample) -> list[str]:
    missing: list[str] = []
    for requirement in example.requirements:
        if requirement == "latex":
            for command in LATEX_COMMANDS:
                if shutil.which(command) is None:
                    missing.append(command)
            if "kpsewhich" not in missing:
                for package in LATEX_PACKAGES:
                    if not _tex_package_available(package):
                        missing.append(f"tex-package:{package}")
            continue
        module = MODULE_NAMES[requirement]
        if importlib.util.find_spec(module) is None:
            missing.append(requirement)
    if (
        _requires_system_font(example)
        and "matplotlib" not in missing
        and not _font_available(example.font_family)
    ):
        missing.append(f"font:{example.font_family}")
    return missing


def render(example: PaperExample, output_dir: Path, *, force: bool) -> list[Path]:
    missing = missing_requirements(example)
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"{example.key} requires missing runtime dependencies: {joined}")

    targets = [output_dir / name for name in example.outputs]
    existing = [path for path in targets if path.exists()]
    if existing and not force:
        joined = ", ".join(path.name for path in existing)
        raise FileExistsError(f"refusing to overwrite existing output(s): {joined}; pass --force")

    script = SOURCE_DIR / example.script
    if not script.is_file():
        raise FileNotFoundError(f"registered source is missing: {script}")

    with tempfile.TemporaryDirectory(prefix=f"nature-figure-{example.key}-") as temporary:
        workdir = Path(temporary)
        generated_dir = workdir / "figures"
        generated_dir.mkdir()
        environment = os.environ.copy()
        environment.setdefault("MPLBACKEND", "Agg")
        subprocess.run([sys.executable, str(script)], cwd=workdir, env=environment, check=True)

        missing_outputs = [name for name in example.outputs if not (generated_dir / name).is_file()]
        if missing_outputs:
            joined = ", ".join(missing_outputs)
            raise RuntimeError(f"{example.key} completed without expected output(s): {joined}")

        output_dir.mkdir(parents=True, exist_ok=True)
        for name, target in zip(example.outputs, targets):
            shutil.copy2(generated_dir / name, target)

    return targets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render a preserved paper-specific example in an isolated subprocess."
    )
    parser.add_argument("example", nargs="?", help="example key; use --list to inspect choices")
    parser.add_argument("--output-dir", type=Path, default=Path("figures"))
    parser.add_argument("--force", action="store_true", help="replace existing named outputs")
    parser.add_argument("--list", action="store_true", help="list examples, outputs, and dependencies")
    return parser


def list_examples() -> None:
    for example in EXAMPLES:
        outputs = ",".join(example.outputs)
        runtime = list(example.requirements)
        if _requires_system_font(example):
            runtime.append(f"font:{example.font_family}")
        requirements = ",".join(runtime)
        if example.visual_qa_pending:
            status = "curated-pending-visual-qa"
        elif example.review_notes:
            status = "review"
        elif example.curation_notes:
            status = "curated"
        else:
            status = "faithful"
        print(f"{example.key}\t{example.visual_family}\t{outputs}\t{requirements}\t{status}")


def main() -> int:
    args = build_parser().parse_args()
    if args.list:
        list_examples()
        return 0
    if not args.example:
        raise SystemExit("provide an example key or use --list")
    try:
        example = get_example(args.example)
        outputs = render(example, args.output_dir, force=args.force)
    except (FileExistsError, FileNotFoundError, KeyError, RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
