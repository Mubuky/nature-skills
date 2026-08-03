from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from compare_paper_figure import compare_images  # noqa: E402
from paper_examples.gallery import load_manifest, verify_gallery  # noqa: E402
from paper_examples.registry import EXAMPLES, get_example  # noqa: E402
from render_paper_example import missing_requirements  # noqa: E402


class PaperExampleTests(unittest.TestCase):
    def test_preserved_gallery_hashes_and_registry(self) -> None:
        self.assertEqual(verify_gallery(), [])
        manifest = load_manifest()
        self.assertEqual(len(EXAMPLES), 24)
        self.assertEqual(len(manifest["entries"]), 45)
        self.assertEqual(
            sum(entry["mode"] in {"hybrid-reference", "python-output"} for entry in manifest["entries"]),
            42,
        )
        self.assertEqual(
            sum(entry["mode"] == "optimized-output" for entry in manifest["entries"]),
            3,
        )
        self.assertEqual(len(manifest["source_files"]), 25)
        self.assertTrue(get_example("vigil-radar").review_notes)
        self.assertFalse(get_example("ophthal-trend").visual_qa_pending)
        curated_sources = {
            entry["path"]
            for entry in manifest["source_files"]
            if "curation" in entry
        }
        self.assertEqual(
            curated_sources,
            {
                "scripts/paper_examples/cflows/diffusion_swiss_roll.py",
                "scripts/paper_examples/immunostruct/plot_bars.py",
                "scripts/paper_examples/immunostruct/raw_data.py",
                "scripts/paper_examples/ophthal_review/plot_trend.py",
                "scripts/paper_examples/vigil/plot_ablation.py",
            },
        )
        for entry in manifest["source_files"]:
            if "curation" in entry:
                self.assertIn("upstream_sha256", entry)

    def test_exact_comparator(self) -> None:
        candidate = SKILL_DIR / "assets" / "paper-patterns" / "python" / "rnagenscape" / "manifold.png"
        result = compare_images(candidate, candidate)
        self.assertTrue(result["exact"])
        self.assertEqual(result["changed_pixel_fraction"], 0.0)

    def test_curated_ophthal_records_localized_latex_pixel_qa(self) -> None:
        manifest = load_manifest()
        entry = next(
            item
            for item in manifest["entries"]
            if item["path"] == "assets/paper-patterns/optimized/ophthal-review/trend_by_month.png"
        )
        self.assertEqual(entry["render_environment"]["font_package"], "helvet")
        self.assertEqual(entry["render_environment"]["dvipng"], "1.18")
        self.assertTrue(entry["verification"]["two_independent_renders_exact"])
        reference = entry["verification"]["same_environment_reference"]
        self.assertEqual(reference["kind"], "upstream-source-rerender")
        self.assertFalse(reference["stored_in_repository"])
        self.assertEqual(
            reference["render_sha256"],
            "84e5a64ca2feb7ba3c60cc0454ab772a74dbb63b781d71bfce6f69a1397c96f1",
        )
        self.assertEqual(
            entry["verification"]["same_environment_changed_outside_expected_annotation_regions"],
            0,
        )

    def test_runner_rejects_silent_font_fallback(self) -> None:
        with (
            patch("render_paper_example.importlib.util.find_spec", return_value=object()),
            patch("render_paper_example._font_available", return_value=False),
        ):
            missing = missing_requirements(get_example("brainteaser-rewriting"))
            self.assertIn("font:Helvetica", missing)
            no_font_requirement = missing_requirements(get_example("rnagenscape-manifold"))
            self.assertNotIn("font:Helvetica", no_font_requirement)

    def test_runner_leaves_latex_font_resolution_to_tex(self) -> None:
        with (
            patch("render_paper_example.importlib.util.find_spec", return_value=object()),
            patch("render_paper_example.shutil.which", side_effect=lambda command: command),
            patch("render_paper_example._tex_package_available", return_value=True),
            patch("render_paper_example._font_available") as font_available,
        ):
            missing = missing_requirements(get_example("ophthal-trend"))

        self.assertEqual(missing, [])
        font_available.assert_not_called()

    def test_runner_requires_complete_latex_helvet_toolchain(self) -> None:
        available_commands = {
            "latex": "latex",
            "dvipng": None,
            "kpsewhich": "kpsewhich",
        }
        with (
            patch("render_paper_example.importlib.util.find_spec", return_value=object()),
            patch(
                "render_paper_example.shutil.which",
                side_effect=lambda command: available_commands.get(command, command),
            ),
            patch("render_paper_example._tex_package_available", return_value=False),
        ):
            missing = missing_requirements(get_example("ophthal-trend"))

        self.assertIn("dvipng", missing)
        self.assertIn("tex-package:helvet.sty", missing)

    def test_runner_matches_real_golden_pixels(self) -> None:
        if importlib.util.find_spec("matplotlib") is None or importlib.util.find_spec("numpy") is None:
            self.skipTest("matplotlib/numpy are optional runtime dependencies")
        with tempfile.TemporaryDirectory() as temporary:
            command = [
                sys.executable,
                str(SCRIPTS_DIR / "render_paper_example.py"),
                "rnagenscape-manifold",
                "--output-dir",
                temporary,
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            candidate = Path(temporary) / "manifold.png"
            golden = SKILL_DIR / "assets" / "paper-patterns" / "python" / "rnagenscape" / "manifold.png"
            self.assertTrue(candidate.is_file())
            comparison = compare_images(golden, candidate)
            self.assertTrue(comparison["exact"], comparison)
            self.assertEqual(comparison["changed_pixel_fraction"], 0.0)

    def test_curated_swiss_roll_matches_optimized_pixels(self) -> None:
        required = ("matplotlib", "numpy", "scipy")
        if any(importlib.util.find_spec(module) is None for module in required):
            self.skipTest("matplotlib/numpy/scipy are optional runtime dependencies")
        with tempfile.TemporaryDirectory() as temporary:
            command = [
                sys.executable,
                str(SCRIPTS_DIR / "render_paper_example.py"),
                "cflows-diffusion-swiss-roll",
                "--output-dir",
                temporary,
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            candidate = Path(temporary) / "diffusion_swiss_roll.png"
            optimized = (
                SKILL_DIR
                / "assets"
                / "paper-patterns"
                / "optimized"
                / "cflows"
                / "diffusion_swiss_roll.png"
            )
            comparison = compare_images(optimized, candidate)
            self.assertTrue(comparison["exact"], comparison)

    def test_curated_vigil_matches_environment_specific_optimized_pixels(self) -> None:
        required = ("matplotlib", "numpy")
        if any(importlib.util.find_spec(module) is None for module in required):
            self.skipTest("matplotlib/numpy are optional runtime dependencies")

        import matplotlib
        from matplotlib import ft2font

        if matplotlib.__version__ != "3.10.8" or ft2font.__freetype_version__ != "2.6.1":
            self.skipTest("optimized VIGIL raster records Matplotlib 3.10.8 and FreeType 2.6.1")

        with tempfile.TemporaryDirectory() as temporary:
            workdir = Path(temporary)
            (workdir / "figures").mkdir()
            environment = os.environ.copy()
            environment["MPLBACKEND"] = "Agg"
            script = SCRIPTS_DIR / "paper_examples" / "vigil" / "plot_ablation.py"
            subprocess.run(
                [sys.executable, "-B", str(script)],
                cwd=workdir,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
            candidate = workdir / "figures" / "ablation_curves.png"
            optimized = (
                SKILL_DIR
                / "assets"
                / "paper-patterns"
                / "optimized"
                / "vigil"
                / "ablation_curves.png"
            )
            comparison = compare_images(optimized, candidate)
            self.assertTrue(comparison["exact"], comparison)

    def test_immunostruct_uncertainty_rename_is_render_equivalent(self) -> None:
        required = ("matplotlib", "numpy")
        if any(importlib.util.find_spec(module) is None for module in required):
            self.skipTest("matplotlib/numpy are optional runtime dependencies")

        source_dir = SCRIPTS_DIR / "paper_examples" / "immunostruct"
        runner = """
import os
import runpy
import sys
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
script = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(script.parent))
from matplotlib.figure import Figure

original_savefig = Figure.savefig

def compact_savefig(self, *args, **kwargs):
    kwargs["dpi"] = 60
    return original_savefig(self, *args, **kwargs)

Figure.savefig = compact_savefig
runpy.run_path(str(script), run_name="__main__")
"""

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            current_dir = root / "current"
            legacy_dir = root / "legacy"
            current_dir.mkdir()
            legacy_dir.mkdir()
            for directory in (current_dir, legacy_dir):
                shutil.copy2(source_dir / "plot_bars.py", directory / "plot_bars.py")
                shutil.copy2(source_dir / "raw_data.py", directory / "raw_data.py")

            legacy_plot = legacy_dir / "plot_bars.py"
            legacy_data = legacy_dir / "raw_data.py"
            legacy_plot.write_text(
                legacy_plot.read_text(encoding="utf-8").replace("['uncertainty']", "['std']"),
                encoding="utf-8",
            )
            legacy_data.write_text(
                legacy_data.read_text(encoding="utf-8").replace("'uncertainty'", "'std'"),
                encoding="utf-8",
            )

            environment = os.environ.copy()
            environment["MPLBACKEND"] = "Agg"
            for directory in (current_dir, legacy_dir):
                subprocess.run(
                    [sys.executable, "-B", "-c", runner, str(directory / "plot_bars.py")],
                    cwd=directory,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )

            outputs = (
                "bars_comparison_IEDB.png",
                "bars_ablation_IEDB.png",
                "bars_comparison_Cancer.png",
                "bars_ablation_Cancer.png",
            )
            for name in outputs:
                comparison = compare_images(
                    legacy_dir / "figures" / name,
                    current_dir / "figures" / name,
                )
                self.assertTrue(comparison["exact"], {"name": name, **comparison})


if __name__ == "__main__":
    unittest.main()
