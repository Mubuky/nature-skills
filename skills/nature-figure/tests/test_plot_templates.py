"""Regression tests for the data-driven Nature figure template CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "plot_templates.py"
VALIDATOR = SKILL_DIR / "scripts" / "validate_figure.py"


class PlotTemplateCliTests(unittest.TestCase):
    def run_cli(self, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            expected,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        return completed

    def test_help_exposes_only_the_five_analytical_families(self) -> None:
        completed = self.run_cli("--help")
        for command in ("volcano", "roc", "dotplot", "marginal", "paired"):
            self.assertIn(command, completed.stdout)
        for removed in ("benchmark", "composition", "comparison-matrix", "sweep", "timeline"):
            self.assertNotIn(removed, completed.stdout)

    def test_modular_entry_passes_static_preflight(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(SCRIPT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("[PASS] EDITABLE-TEXT", completed.stdout)
        self.assertIn("0 fail", completed.stdout)

    def test_analytical_demo_families_emit_bundle_and_mark_demo(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            for command in ("volcano", "roc", "dotplot", "marginal", "paired"):
                prefix = directory / command
                self.run_cli(command, "--demo", "--output", str(prefix), "--dpi", "72")
                for suffix in (".svg", ".pdf", ".tiff", ".png", ".qa.json"):
                    path = prefix.with_suffix(suffix)
                    self.assertTrue(path.is_file(), f"missing {path}")
                    self.assertGreater(path.stat().st_size, 20)
                qa = json.loads(prefix.with_suffix(".qa.json").read_text(encoding="utf-8"))
                svg = prefix.with_suffix(".svg").read_text(encoding="utf-8")
                self.assertIs(qa["demo"], True)
                self.assertGreater(qa["rows_plotted"], 0)
                self.assertEqual(qa["excluded_rows"], 0)
                self.assertIn("font-family", svg)

    def test_existing_volcano_command_still_runs(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            prefix = Path(raw_directory) / "volcano"
            self.run_cli("volcano", "--demo", "--output", str(prefix), "--dpi", "72")
            qa = json.loads(prefix.with_suffix(".qa.json").read_text(encoding="utf-8"))
            self.assertEqual(qa["template"], "volcano")
            self.assertIs(qa["demo"], True)

    def test_production_rejects_low_resolution_tiff(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            source = directory / "volcano.csv"
            source.write_text(
                "gene,log2fc,padj\nA,1.2,0.01\nB,-0.3,0.4\n",
                encoding="utf-8",
            )
            completed = self.run_cli(
                "volcano",
                "--input",
                str(source),
                "--output",
                str(directory / "volcano"),
                "--dpi",
                "72",
                expected=2,
            )
            self.assertIn("at least 300", completed.stderr)


if __name__ == "__main__":
    unittest.main()
