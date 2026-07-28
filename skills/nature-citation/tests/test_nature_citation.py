# Context-engineered edition regression tests; see repository NOTICE.
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "nature_citation", ROOT / "scripts" / "nature_citation.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def candidate():
    return MODULE.Candidate(
        title="A verified candidate",
        journal="Nature Machine Intelligence",
        family="Nature Portfolio",
        year="2026",
        y1="2026/01/01",
        doi="10.0000/example",
        url="https://doi.org/10.0000/example",
        volume="1",
        issue="1",
        start_page="1",
        end_page="2",
        issn="0000-0000",
        authors=["Example, A."],
        abstract="",
        type="journal-article",
        score=10.0,
        source_query="test",
    )


class CitationSafetyTests(unittest.TestCase):
    def test_strict_nature_scope_fails_closed(self):
        self.assertIsNone(MODULE.journal_family("Nature and Culture"))
        self.assertIsNone(MODULE.journal_family("Nature Reviews Imaginary Systems"))
        self.assertEqual(
            "Nature Portfolio", MODULE.journal_family("npj Artificial Intelligence")
        )

    def test_metadata_candidate_has_no_insertion_or_export_record(self):
        record = candidate().as_dict()
        for forbidden in (
            "citation_marker",
            "enw_record",
            "ris_record",
            "zotero_rdf_article",
        ):
            self.assertNotIn(forbidden, record)
        self.assertEqual("metadata-only candidate", record["support_grade"])

    def test_screened_selection_is_required_and_validated(self):
        segment = MODULE.Segment("S001", "Claim text.", "claim text", 1)
        valid = {
            "selections": [
                {
                    "segment_id": "S001",
                    "doi": "10.0000/example",
                    "support_grade": "strong",
                    "evidence_basis": "full_text",
                    "evidence_locator": "Results, paragraph 3",
                    "evidence_paraphrase": "The experiment directly tests the claim.",
                    "checked_url": "https://doi.org/10.0000/example",
                    "checked_at": "2026-07-28T12:00:00+08:00",
                    "contradiction_status": "none_found",
                    "retraction_status": "none_found",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selection.json"
            path.write_text(json.dumps(valid), encoding="utf-8")
            selected, audit = MODULE.load_screened_selection(
                path, [candidate()], [segment]
            )
            self.assertEqual(["10.0000/example"], [item.doi for item in selected])
            self.assertEqual("S001", audit[0]["segment_id"])

            valid["selections"][0]["support_grade"] = "metadata-only"
            path.write_text(json.dumps(valid), encoding="utf-8")
            with self.assertRaises(ValueError):
                MODULE.load_screened_selection(path, [candidate()], [segment])

    def test_legacy_candidate_browser_export_is_disabled(self):
        with self.assertRaises(RuntimeError):
            MODULE.write_html([], [], Path("."), Path("x.html"), Path("x.enw"), "enw")


if __name__ == "__main__":
    unittest.main()
