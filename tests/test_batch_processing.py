"""
Unit and integration tests for CobolScope batch folder processing and single-JVM execution.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from cobolscope.parser import parse_batch
from cobolscope.models import ProgramModel
from cobolscope.cli import main as cli_main

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"
BANK_COBOL = FIXTURES_DIR / "bank_of_z" / "cobol"
BANK_COPY = FIXTURES_DIR / "bank_of_z" / "copy"


class TestBatchProcessing(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="cobolscope_batch_test_"))

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_batch_single_jvm(self):
        """Verify parse_batch parses multiple files in a single JVM run."""
        test_files = [
            BANK_COBOL / "INQCUST.cbl",
            BANK_COBOL / "UPDACC.cbl",
            BANK_COBOL / "GETCOMPY.cbl",
        ]
        out_ir = self.temp_dir / "ir"

        results = parse_batch(
            input_files=test_files,
            output_dir=out_ir,
            format="FIXED",
            copybook_dirs=[BANK_COPY],
            ignore_syntax_errors=True,
        )

        self.assertEqual(len(results), len(test_files))
        for tf in test_files:
            self.assertIn(str(tf.resolve()), results)
            json_file = results[str(tf.resolve())]
            self.assertTrue(json_file.exists())

            # Verify valid Canonical IR
            raw = json.loads(json_file.read_text(encoding="utf-8"))
            model = ProgramModel.from_dict(raw)
            self.assertTrue(len(model.paragraphs) > 0)
            self.assertTrue(model.program_id)

    def test_cli_folder_execution_graph_and_dict(self):
        """Verify running CLI on a folder generates call graphs, data dictionaries, and manifest.json."""
        # Create a small folder fixture with 2 programs
        fixture_folder = self.temp_dir / "programs"
        fixture_folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BANK_COBOL / "INQCUST.cbl", fixture_folder / "INQCUST.cbl")
        shutil.copy2(BANK_COBOL / "UPDACC.cbl", fixture_folder / "UPDACC.cbl")

        out_dir = self.temp_dir / "output"

        # Execute CLI on folder with both --graph and --dict
        ret = cli_main([
            str(fixture_folder),
            "-o", str(out_dir),
            "--graph",
            "--dict",
            "-I", str(BANK_COPY),
            "--ignore-syntax-errors",
        ])

        self.assertEqual(ret, 0)
        self.assertTrue(out_dir.exists())

        # Verify manifest.json
        manifest_file = out_dir / "manifest.json"
        self.assertTrue(manifest_file.exists())
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))

        self.assertEqual(manifest["batch_summary"]["total_programs_found"], 2)
        self.assertEqual(manifest["batch_summary"]["succeeded"], 2)
        self.assertEqual(manifest["batch_summary"]["portal"], "index.html")
        self.assertTrue((out_dir / "index.html").exists())

        # Verify artifacts for both programs
        for prog in manifest["programs"]:
            self.assertEqual(prog["status"], "SUCCESS")
            artifacts = prog["artifacts"]
            self.assertIn("call_graph", artifacts)
            self.assertIn("data_dictionary", artifacts)
            self.assertIn("data_dictionary_html", artifacts)
            self.assertIn("ir", artifacts)

            self.assertTrue((out_dir / artifacts["call_graph"]).exists())
            self.assertTrue((out_dir / artifacts["data_dictionary"]).exists())
            self.assertTrue((out_dir / artifacts["data_dictionary_html"]).exists())
            self.assertTrue((out_dir / artifacts["ir"]).exists())

            # Verify call graph links to relative external assets
            cg_html = (out_dir / artifacts["call_graph"]).read_text(encoding="utf-8")
            self.assertIn('src="assets/cobolscope-viewer.bundle.js"', cg_html)
            self.assertIn('href="assets/cobolscope-viewer.css"', cg_html)

        # Verify static assets were automatically copied to output directory
        self.assertTrue((out_dir / "assets" / "cobolscope-viewer.bundle.js").exists())
        self.assertTrue((out_dir / "assets" / "cobolscope-viewer.css").exists())



if __name__ == "__main__":
    unittest.main()
