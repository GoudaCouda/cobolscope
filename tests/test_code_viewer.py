"""
tests/test_code_viewer.py
~~~~~~~~~~~~~~~~~~~~~~~~~

Verification suite for Call Graph split-screen source code viewer,
65/35 graph-to-code default split ratio, and resizable splitters in Call Graph and Portal HTML.
"""

import json
import tempfile
import unittest
from pathlib import Path

from cobolscope.models import ProgramModel, ParagraphNode, SourceLocation, PerformStatementNode
from cobolscope.graph import CallGraphGenerator, generate_call_graph
from cobolscope.portal import generate_portal


SAMPLE_COBOL_SOURCE = """       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO-SPLIT.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-COUNT PIC 9(4) VALUE 0.
       PROCEDURE DIVISION.
       0000-MAIN.
           PERFORM 1000-PROCESS-DATA
           STOP RUN.
       1000-PROCESS-DATA.
           ADD 1 TO WS-COUNT
           PERFORM 2000-PRINT-SUMMARY.
       2000-PRINT-SUMMARY.
           DISPLAY "COUNT=" WS-COUNT.
"""


class TestCodeViewerAndSplitView(unittest.TestCase):

    def test_program_model_source_code_and_fallback(self):
        """Test ProgramModel source_code field and get_source_text() method."""
        model = ProgramModel(
            program_id="HELLO-SPLIT",
            source_code=SAMPLE_COBOL_SOURCE,
        )
        self.assertEqual(model.source_code, SAMPLE_COBOL_SOURCE)
        self.assertEqual(model.get_source_text(), SAMPLE_COBOL_SOURCE)

        with tempfile.TemporaryDirectory() as td:
            cbl_file = Path(td) / "TESTPROG.CBL"
            cbl_file.write_text("       IDENTIFICATION DIVISION.\n       PROGRAM-ID. DISKPROG.\n", encoding="utf-8")
            disk_model = ProgramModel(
                program_id="DISKPROG",
                source_file=str(cbl_file),
            )
            self.assertIsNone(disk_model.source_code)
            self.assertIn("PROGRAM-ID. DISKPROG.", disk_model.get_source_text())

    def test_call_graph_source_code_propagation(self):
        """Verify source_code propagates from model to CallGraph and HTML output."""
        p_main = ParagraphNode(
            name="0000-MAIN",
            location=SourceLocation(start_line=8, end_line=10),
            statements=[
                PerformStatementNode(target="1000-PROCESS-DATA", location=SourceLocation(start_line=9, end_line=9)),
            ]
        )
        p_proc = ParagraphNode(
            name="1000-PROCESS-DATA",
            location=SourceLocation(start_line=11, end_line=13),
            statements=[
                PerformStatementNode(target="2000-PRINT-SUMMARY", location=SourceLocation(start_line=13, end_line=13)),
            ]
        )
        p_sum = ParagraphNode(
            name="2000-PRINT-SUMMARY",
            location=SourceLocation(start_line=14, end_line=15),
            statements=[]
        )

        model = ProgramModel(
            program_id="HELLO-SPLIT",
            paragraphs=[p_main, p_proc, p_sum],
            source_code=SAMPLE_COBOL_SOURCE,
        )

        generator = CallGraphGenerator(model)
        self.assertEqual(generator.graph.source_code, SAMPLE_COBOL_SOURCE)

        html = generator.to_html()

        # Verify split code pane elements exist
        self.assertIn("codeSplitPane", html)
        self.assertIn("splitterCanvasCode", html)
        self.assertIn("splitterInspector", html)
        self.assertIn("btnToggleCodeSplit", html)
        self.assertIn("btnViewRoutineCode", html)

        # Verify 65/35 ratio default in code_viewer script
        self.assertIn("ratio = 65", html)
        self.assertIn("100 - ratio", html)
        self.assertIn("cobolscope_code_split_ratio", html)

        # Verify raw source code is embedded safely in JSON
        self.assertIn("HELLO-SPLIT", html)
        self.assertIn("1000-PROCESS-DATA", html)

    def test_generate_call_graph_with_explicit_source(self):
        """Test convenience functional API generate_call_graph with explicit source_code."""
        p1 = ParagraphNode(
            name="MAIN-PARA",
            location=SourceLocation(start_line=1, end_line=3),
        )
        model = ProgramModel(program_id="EXPLICIT-SRC", paragraphs=[p1])

        custom_source = "       IDENTIFICATION DIVISION.\n       PROGRAM-ID. CUSTOM.\n"
        html = generate_call_graph(model, source_code=custom_source)

        self.assertIn("CUSTOM", html)
        self.assertIn("codeSplitPane", html)
        self.assertIn("splitterCanvasCode", html)

    def test_portal_html_source_tab_and_resizable_splitters(self):
        """Verify Portal HTML contains resizable sidebar splitter, source tab, and dual pane comparison."""
        manifest = {
            "batch_summary": {
                "source_directory": "C:/COBOL/SRC",
                "total_programs_found": 1,
                "succeeded": 1,
                "failed": 0,
            },
            "programs": [
                {
                    "program_id": "TESTPROG",
                    "source_file": "TESTPROG.CBL",
                    "relative_source": "TESTPROG.CBL",
                    "status": "SUCCESS",
                    "total_paragraphs": 3,
                    "total_statements": 5,
                    "max_cyclomatic_complexity": 2,
                    "artifacts": {
                        "call_graph": "TESTPROG.html",
                        "source": "TESTPROG.cbl",
                        "data_dictionary_html": "TESTPROG_dict.html",
                        "ir": "TESTPROG.json",
                    }
                }
            ]
        }

        portal_html = generate_portal(manifest)

        # 1. Resizable sidebar
        self.assertIn('id="sidebar-splitter"', portal_html)
        self.assertIn("setupSidebarSplitter", portal_html)
        self.assertIn("cobolscope_portal_sidebar_width", portal_html)

        # 2. Source Code Tab
        self.assertIn('id="tab-source"', portal_html)
        self.assertIn("Source Code", portal_html)
        self.assertIn('id="source-container"', portal_html)

        # 3. Dual Pane Mode
        self.assertIn('id="btn-dual-pane"', portal_html)
        self.assertIn('id="dual-pane-view"', portal_html)
        self.assertIn('id="dual-pane-splitter"', portal_html)
        self.assertIn('id="drag-shield"', portal_html)
        self.assertIn("togglePortalDualPane", portal_html)
        self.assertIn("setupDualPaneSplitter", portal_html)


if __name__ == "__main__":
    unittest.main()
