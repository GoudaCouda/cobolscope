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

from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    SourceLocation,
    PerformStatementNode,
    GoToStatementNode,
    ExitStatementNode,
)
from cobolscope.graph import CallGraphGenerator, generate_call_graph
from cobolscope.portal import generate_portal
from cobolscope.dictionary.generator import generate_data_dictionary


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
        self.assertIn("btnToggleInspector", html)
        self.assertIn("btnCloseInspector", html)
        self.assertIn("btnViewRoutineCode", html)
        self.assertIn("btn-view-routine-code", html)

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
        """Verify Portal HTML contains resizable sidebar splitter and source tab."""
        manifest = {
            "batch_summary": {
                "total_programs_found": 1,
                "succeeded": 1,
                "failed": 0,
            },
            "programs": [
                {
                    "program_id": "TESTPROG",
                    "status": "SUCCESS",
                    "total_paragraphs": 3,
                    "total_statements": 5,
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

        # 1. Resizable & Collapsible sidebar
        self.assertIn('id="sidebar-splitter"', portal_html)
        self.assertIn("setupSidebarSplitter", portal_html)
        self.assertIn("cobolscope_portal_sidebar_width", portal_html)
        self.assertIn('id="sidebar-rail-indicator"', portal_html)
        self.assertIn('id="btn-toggle-sidebar"', portal_html)
        self.assertIn("collapseSidebar", portal_html)

        # 2. Source Code Tab
        self.assertIn('id="tab-source"', portal_html)
        self.assertIn("Source Code", portal_html)
        self.assertIn('id="source-container"', portal_html)

    def test_source_map_exact_line_resolution(self):
        """Verify that ProLeap compiler source mapping resolves exact physical lines across copybooks."""
        cbl_path = Path("tests/fixtures/bank_of_z/cobol/ABNDPROC.cbl")
        copy_dir = Path("tests/fixtures/bank_of_z/copy")
        if not cbl_path.exists() or not copy_dir.exists():
            self.skipTest("ABNDPROC.cbl fixture or copybook dir not found")

        from cobolscope.parser import parse
        from cobolscope.graph import CallGraphGenerator
        from cobolscope.graph.renderers import render_cytoscape_elements

        raw_ir = parse(cbl_path, copybook_dirs=[copy_dir])
        self.assertIsInstance(raw_ir, dict)

        para_map = {p["name"]: p for p in raw_ir.get("paragraphs", [])}
        self.assertIn("A010", para_map)
        self.assertIn("A999", para_map)
        self.assertIn("GMOOH010", para_map)
        self.assertIn("GMOOH999", para_map)

        # Exact physical line assertions in ABNDPROC.cbl
        self.assertEqual(para_map["A010"]["location"]["startLine"], 132)
        self.assertEqual(para_map["A999"]["location"]["startLine"], 165)
        self.assertEqual(para_map["GMOOH010"]["location"]["startLine"], 170)
        self.assertEqual(para_map["GMOOH999"]["location"]["startLine"], 175)
        self.assertEqual(para_map["A010"]["location"]["sourceFile"], "ABNDPROC.cbl")

        # Verify copybook field location resolution
        dd = raw_ir.get("dataDictionary", {})
        ws_fields = dd.get("workingStorageSection", [])
        abnd_area = next((f for f in ws_fields if f.get("name") == "WS-ABND-AREA"), None)
        self.assertIsNotNone(abnd_area)
        self.assertEqual(abnd_area["location"]["startLine"], 37)
        self.assertEqual(abnd_area["location"]["sourceFile"], "ABNDPROC.cbl")

        vsam_key = next((c for c in abnd_area.get("children", []) if c.get("name") == "ABND-VSAM-KEY"), None)
        self.assertIsNotNone(vsam_key)
        self.assertEqual(vsam_key["location"]["startLine"], 7)
        self.assertEqual(vsam_key["location"]["sourceFile"], "ABNDINFO.cpy")

        # Verify CallGraphNode and Cytoscape elements carry source_file
        model = ProgramModel.model_validate(raw_ir)
        gen = CallGraphGenerator(model)
        self.assertIn("PREMIERE", gen.graph.nodes)
        self.assertEqual(gen.graph.nodes["PREMIERE"].source_file, "ABNDPROC.cbl")
        self.assertEqual(gen.graph.nodes["PREMIERE"].start_line, 131)

        cyto_elements = render_cytoscape_elements(gen.graph)
        node_elem = next((e for e in cyto_elements if e["data"].get("name") == "PREMIERE"), None)
        self.assertIsNotNone(node_elem)
        self.assertEqual(node_elem["data"].get("source_file"), "ABNDPROC.cbl")
        self.assertEqual(node_elem["data"].get("start_line"), 131)

    def test_continuation_lines_source_mapping(self):
        """Verify that continuation lines in WORKING-STORAGE do not shift Procedure Division line mappings."""
        cobol_source = (
            "000001 IDENTIFICATION DIVISION.                                             ORIG\n"
            "000002 PROGRAM-ID. TESTCONT.                                                ORIG\n"
            "000003 DATA DIVISION.                                                       ORIG\n"
            "000004 WORKING-STORAGE SECTION.                                             ORIG\n"
            "000005 01 WS-LONG-TEXT PIC X(40) VALUE 'HELLO WORLD                         ORIG\n"
            "000006-                                ' CONTINUED'.                        ORIG\n"
            "000007 01 WS-OTHER PIC X(40) VALUE 'SECOND LINE                             ORIG\n"
            "000008-                                ' AGAIN CONTINUED'.                  ORIG\n"
            "000009 PROCEDURE DIVISION.                                                  ORIG\n"
            "000010 1000-PROCESS.                                                        ORIG\n"
            "000011     DISPLAY WS-LONG-TEXT.                                            ORIG\n"
            "000012 1000-PROCESS-EXIT.                                                   ORIG\n"
            "000013     EXIT.                                                            ORIG\n"
        )
        with tempfile.TemporaryDirectory() as td:
            cbl_file = Path(td) / "TESTCONT.CBL"
            cbl_file.write_text(cobol_source, encoding="utf-8")

            from cobolscope.parser import parse
            raw_ir = parse(cbl_file)
            para_map = {p["name"]: p for p in raw_ir.get("paragraphs", [])}

            self.assertIn("1000-PROCESS", para_map)
            self.assertIn("1000-PROCESS-EXIT", para_map)

            # In the file, 1000-PROCESS is exactly on line 10, and 1000-PROCESS-EXIT is on line 12
            self.assertEqual(para_map["1000-PROCESS"]["location"]["startLine"], 10)
            self.assertEqual(para_map["1000-PROCESS-EXIT"]["location"]["startLine"], 12)

    def test_child_goto_parent_exit_no_cycle(self):
        """Verify that GO TO <parent>-EXIT from an invoked child routine does not create false recursion cycles."""
        main_p = ParagraphNode(
            name="999-DRIVER",
            location=SourceLocation(start_line=1, end_line=5),
            statements=[
                PerformStatementNode(target="999-CHILD-READ"),
            ],
        )
        main_exit = ParagraphNode(
            name="999-DRIVER-EXIT",
            location=SourceLocation(start_line=6, end_line=8),
            statements=[
                ExitStatementNode(),
            ],
        )
        child_p = ParagraphNode(
            name="999-CHILD-READ",
            location=SourceLocation(start_line=9, end_line=15),
            statements=[
                GoToStatementNode(target="999-DRIVER-EXIT"),
            ],
        )
        model = ProgramModel(
            program_id="TESTCYCLE",
            paragraphs=[main_p, main_exit, child_p],
        )

        gen_collapsed = CallGraphGenerator(model, collapse_exits=True)
        cg_collapsed = gen_collapsed.graph

        self.assertIn("999-DRIVER", cg_collapsed.nodes)
        self.assertNotIn("999-DRIVER-EXIT", cg_collapsed.nodes)
        self.assertIn("999-CHILD-READ", cg_collapsed.nodes)
        self.assertIn("999-DRIVER-EXIT", cg_collapsed.nodes["999-DRIVER"].collapsed_exit_nodes)

        # Ensure no edge 999-CHILD-READ -> 999-DRIVER exists
        child_to_driver = [
            e for e in cg_collapsed.edges
            if e.source == "999-CHILD-READ" and e.target == "999-DRIVER"
        ]
        self.assertEqual(len(child_to_driver), 0)
        self.assertFalse(cg_collapsed.has_cycles)
        self.assertEqual(cg_collapsed.cycles, [])

        # Also verify with TT05943N fixture if present
        tt_path = Path("mini_test/TT05943N.cbl")
        if tt_path.exists():
            from tests.harness.test_cache import get_test_model
            tt_model = get_test_model(str(tt_path))
            tt_cg = CallGraphGenerator(tt_model, collapse_exits=True).graph
            self.assertFalse(tt_cg.has_cycles)
            self.assertEqual(tt_cg.cycles, [])

    def test_procedure_details_popover_and_no_l3_cc(self):
        """Verify that routine details are in a popover, meta-grid is removed from body, and L3 card has no CC counter."""
        model = ProgramModel(
            program_id="POPOVERTEST",
            paragraphs=[
                ParagraphNode(
                    name="1000-PROCESS",
                    section_parent="MAIN-SECTION",
                    location=SourceLocation(start_line=10, end_line=20),
                    statements=[
                        PerformStatementNode(target="2000-CALC"),
                    ],
                ),
                ParagraphNode(
                    name="2000-CALC",
                    section_parent="CALC-SECTION",
                    location=SourceLocation(start_line=21, end_line=30),
                ),
            ],
        )
        html = generate_call_graph(model, format="html")

        # 1. Popover elements exist in header
        self.assertIn('id="btnRoutineInfo"', html)
        self.assertIn('id="routineInfoPopover"', html)
        self.assertIn('id="inspPara"', html)
        self.assertIn('id="inspSection"', html)
        self.assertIn('id="inspLines"', html)
        self.assertIn('id="inspCC"', html)
        self.assertIn('id="inspStmts"', html)
        self.assertIn('id="inspCluster"', html)

        # 2. meta-grid removed from inspector body
        self.assertNotIn('class="meta-grid"', html)

        # 3. L3 card has no CC counter badges
        self.assertNotIn("CC: 1 (No Branches)", html)
        self.assertNotIn("ccBadge", html)

    def test_data_dictionary_where_used_jump(self):
        """Verify that Data Dictionary Where-Used breadcrumbs have jumpToRoutine and portal message handler."""
        from cobolscope.models import DataDictionary, DataField
        dd = DataDictionary(
            working_storage_section=[
                DataField(
                    id="WS_COUNT",
                    name="WS-COUNT",
                    pic="9(4)",
                    byte_length=4,
                    byte_offset=0,
                )
            ]
        )
        model = ProgramModel(
            program_id="DICTJUMP",
            data_dictionary=dd,
            paragraphs=[
                ParagraphNode(
                    name="1000-PROCESS",
                    statements=[
                        PerformStatementNode(target="2000-CALC", source_field_ids=["WS_COUNT"]),
                    ],
                )
            ],
        )

        dd_html = generate_data_dictionary(model, format="html")
        self.assertIn("jumpToRoutine", dd_html)
        self.assertIn("COBOLSCOPE_JUMP_TO_ROUTINE", dd_html)
        self.assertIn("ref-breadcrumb", dd_html)

        portal_html = generate_portal({
            "programs": [
                {
                    "program_id": "DICTJUMP",
                    "status": "SUCCESS",
                    "artifacts": {
                        "call_graph": "DICTJUMP.html",
                        "data_dictionary_html": "DICTJUMP_dict.html",
                    },
                }
            ]
        })
        self.assertIn("handleJumpToRoutine", portal_html)
        self.assertIn("COBOLSCOPE_SELECT_ROUTINE", portal_html)


if __name__ == "__main__":
    unittest.main()

