"""
Unit and integration tests for CobolScope documentation portal generator.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from cobolscope.portal import generate_portal
from cobolscope.cli import main as cli_main


class TestDocumentationPortal(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="cobolscope_portal_test_"))
        self.sample_manifest = {
            "batch_summary": {
                "source_directory": "tests/fixtures/bank_of_z/cobol",
                "total_programs_found": 3,
                "succeeded": 2,
                "failed": 1,
                "format": "FIXED",
                "duration_ms": 1250.0,
            },
            "programs": [
                {
                    "program_id": "INQCUST",
                    "source_file": "INQCUST.cbl",
                    "relative_source": "INQCUST.cbl",
                    "total_paragraphs": 20,
                    "total_statements": 101,
                    "max_cyclomatic_complexity": 3,
                    "entry_point": "0000-MAIN",
                    "status": "SUCCESS",
                    "artifacts": {
                        "call_graph": "INQCUST.html",
                        "data_dictionary": "INQCUST_dict.md",
                        "data_dictionary_html": "INQCUST_dict.html",
                        "ir": "ir/INQCUST.json",
                    },
                },
                {
                    "program_id": "UPDACC",
                    "source_file": "UPDACC.cbl",
                    "relative_source": "UPDACC.cbl",
                    "total_paragraphs": 8,
                    "total_statements": 47,
                    "max_cyclomatic_complexity": 2,
                    "entry_point": "0000-PROCESS",
                    "status": "SUCCESS",
                    "artifacts": {
                        "call_graph": "UPDACC.html",
                        "data_dictionary": "UPDACC_dict.md",
                        "data_dictionary_html": "UPDACC_dict.html",
                        "ir": "ir/UPDACC.json",
                    },
                },
                {
                    "program_id": "BNKMENU",
                    "source_file": "BNKMENU.cbl",
                    "relative_source": "BNKMENU.cbl",
                    "status": "FAILED",
                    "error": "Could not find copybook BNK1MAI",
                    "artifacts": {},
                },
            ],
        }

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_portal_from_dict(self):
        """Verify generating portal HTML from in-memory manifest dictionary."""
        out_html = self.temp_dir / "index.html"
        html = generate_portal(self.sample_manifest, output_path=out_html)

        self.assertTrue(out_html.exists())
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("CobolScope Documentation Portal", html)
        self.assertIn("INQCUST", html)
        self.assertIn("UPDACC", html)
        self.assertIn("BNKMENU", html)
        self.assertIn("cobolscope-manifest", html)

    def test_generate_portal_from_directory(self):
        """Verify generating portal from a folder containing manifest.json."""
        manifest_file = self.temp_dir / "manifest.json"
        manifest_file.write_text(json.dumps(self.sample_manifest, indent=2), encoding="utf-8")

        html = generate_portal(self.temp_dir)
        portal_file = self.temp_dir / "index.html"
        self.assertTrue(portal_file.exists())
        self.assertIn("INQCUST", portal_file.read_text(encoding="utf-8"))

    def test_cli_portal_command(self):
        """Verify cobolscope --portal <directory> regenerates index.html cleanly."""
        manifest_file = self.temp_dir / "manifest.json"
        manifest_file.write_text(json.dumps(self.sample_manifest, indent=2), encoding="utf-8")

        ret = cli_main([
            "--portal", str(self.temp_dir),
        ])

        self.assertEqual(ret, 0)
        portal_file = self.temp_dir / "index.html"
        self.assertTrue(portal_file.exists())
        content = portal_file.read_text(encoding="utf-8")
        self.assertIn("CobolScope", content)
        self.assertIn("INQCUST", content)

    def test_portal_missing_manifest_raises(self):
        """Verify error raised when directory lacks manifest.json."""
        empty_dir = self.temp_dir / "empty"
        empty_dir.mkdir()
        with self.assertRaises(FileNotFoundError):
            generate_portal(empty_dir)


if __name__ == "__main__":
    unittest.main()
