#!/usr/bin/env python3
"""Boundary tests for the local Nature Skills updater."""

from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("update-codex-skills.sh")


class UpdaterBoundaryTests(unittest.TestCase):
    def run_updater(self, destination: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), "--profile", "core", "--dest", str(destination)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_rejects_skill_symlink_before_any_sync(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nature-updater-test.") as tmp:
            root = Path(tmp)
            destination = root / "dest"
            outside = root / "outside"
            destination.mkdir()
            outside.mkdir()
            sentinel = outside / "sentinel"
            sentinel.write_text("do-not-touch\n", encoding="utf-8")
            (destination / "nature-writing").symlink_to(outside, target_is_directory=True)

            result = self.run_updater(destination)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symbolic-link target", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "do-not-touch\n")
            self.assertEqual(
                sorted(path.name for path in destination.iterdir()),
                ["nature-writing"],
            )

    def test_rejects_destination_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nature-updater-test.") as tmp:
            root = Path(tmp)
            real_destination = root / "real-dest"
            real_destination.mkdir()
            destination = root / "dest-link"
            destination.symlink_to(real_destination, target_is_directory=True)

            result = self.run_updater(destination)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("destination must not be a symbolic link", result.stderr)

    def test_rejects_filesystem_root(self) -> None:
        result = self.run_updater(Path("/"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("filesystem root", result.stderr)

    def test_core_profile_installs_only_seven_core_skills(self) -> None:
        expected = [
            "nature-academic-search",
            "nature-citation",
            "nature-data",
            "nature-figure",
            "nature-response",
            "nature-reviewer",
            "nature-writing",
        ]
        with tempfile.TemporaryDirectory(prefix="nature-updater-test.") as tmp:
            destination = Path(tmp) / "dest"

            result = self.run_updater(destination)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                sorted(path.name for path in destination.iterdir()),
                expected,
            )


if __name__ == "__main__":
    unittest.main()
