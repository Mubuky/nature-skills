# Modified from Yuan1z0825/nature-skills; see repository NOTICE.

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "configure_credentials.py"


class ConfigureCredentialsTest(unittest.TestCase):
    def test_cli_stdin_json_saves_secrets_without_echoing_them(self):
        secret = "publisher-secret-12345678"
        token = "institution-token-abcdef"
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["LIT_DL_CONFIG_DIR"] = tmp
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "set", "elsevier", "--stdin-json"],
                cwd=ROOT,
                env=env,
                input=json.dumps({"api_key": secret, "insttoken": token}) + "\n",
                text=True,
                capture_output=True,
            )
            credentials_path = Path(tmp) / "credentials.json"
            saved = json.loads(credentials_path.read_text(encoding="utf-8"))
            mode = stat.S_IMODE(credentials_path.stat().st_mode)

        self.assertEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout)
        self.assertNotIn(secret, result.stderr)
        self.assertNotIn(token, result.stdout)
        self.assertNotIn(token, result.stderr)
        self.assertEqual(saved["elsevier"]["api_key"], secret)
        self.assertEqual(saved["elsevier"]["insttoken"], token)
        self.assertEqual(mode, 0o600)

    def test_short_secret_is_fully_masked(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["LIT_DL_CONFIG_DIR"] = tmp
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "set", "ieee", "--stdin-json"],
                cwd=ROOT,
                env=env,
                input='{"api_key":"abcd"}\n',
                text=True,
                capture_output=True,
            )
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("abcd", result.stdout)
        self.assertIn('"api_key": "****"', result.stdout)

    def test_parser_rejects_secret_command_line_flags(self):
        for flag in ("--api-key", "--insttoken", "--authtoken", "--fulltext-endpoint"):
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "set",
                    "ieee",
                    flag,
                    "must-not-enter-process-arguments",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0, flag)
            self.assertIn("unrecognized arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
