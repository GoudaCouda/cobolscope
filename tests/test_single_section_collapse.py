"""
tests/test_single_section_collapse.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regression and invariant test suite for single-section programs and section-level
entry procedures. Verifies that programs with a wrapper SECTION (e.g. 0000-MAIN SECTION.)
do NOT collapse all paragraphs into a single node with zero calls.
"""

import sys
import unittest
from pathlib import Path

repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import (
    ProgramModel,
    SectionNode,
    ParagraphNode,
    PerformStatementNode,
    ExitStatementNode,
    SourceLocation,
)
from cobolscope.graph import (
    CallGraphGenerator,
    GraphNodeType,
    GraphEdgeType,
)
from cobolscope.graph.builder import is_section_based_program


class TestSingleSectionCollapse(unittest.TestCase):
    """Validates that single-section programs do not collapse procedure calls."""

    def test_synthetic_single_section_with_paragraphs(self):
        """
        A synthetic program with 1 section ('0000-MAIN') containing direct statements
        that PERFORM two worker paragraphs ('1000-PROCESS' and '2000-OUTPUT').
        Must generate 3 active nodes (0000-MAIN, 1000-PROCESS, 2000-OUTPUT)
        and 2 calls from 0000-MAIN.
        """
        sec = SectionNode(
            name="0000-MAIN",
            statements=[
                PerformStatementNode(target="1000-PROCESS", thru="1000-PROCESS-EXIT"),
                PerformStatementNode(target="2000-OUTPUT", thru="2000-OUTPUT-EXIT"),
            ],
            paragraph_names=[
                "1000-PROCESS", "1000-PROCESS-EXIT",
                "2000-OUTPUT", "2000-OUTPUT-EXIT",
            ],
            location=SourceLocation(start_line=10, end_line=20),
        )
        p_proc = ParagraphNode(
            name="1000-PROCESS",
            statements=[PerformStatementNode(target="2000-OUTPUT")],
            section_parent="0000-MAIN",
            location=SourceLocation(start_line=22, end_line=30),
        )
        p_proc_ex = ParagraphNode(
            name="1000-PROCESS-EXIT",
            statements=[ExitStatementNode()],
            section_parent="0000-MAIN",
            location=SourceLocation(start_line=31, end_line=32),
        )
        p_out = ParagraphNode(
            name="2000-OUTPUT",
            statements=[],
            section_parent="0000-MAIN",
            location=SourceLocation(start_line=34, end_line=40),
        )
        p_out_ex = ParagraphNode(
            name="2000-OUTPUT-EXIT",
            statements=[ExitStatementNode()],
            section_parent="0000-MAIN",
            location=SourceLocation(start_line=41, end_line=42),
        )

        model = ProgramModel(
            program_id="TEST-WRAPPER-SEC",
            sections=[sec],
            paragraphs=[p_proc, p_proc_ex, p_out, p_out_ex],
        )

        # 1. Must NOT be classified as section-based
        self.assertFalse(is_section_based_program(model))

        # 2. Build Call Graph
        gen = CallGraphGenerator(model, collapse_exits=True)
        g = gen.graph

        # 3. Node verification
        self.assertIn("0000-MAIN", g.nodes)
        self.assertIn("1000-PROCESS", g.nodes)
        self.assertIn("2000-OUTPUT", g.nodes)
        self.assertEqual(len(g.nodes), 3)

        # 4. Entry point verification
        self.assertEqual(g.entry_point, "0000-MAIN")
        self.assertTrue(g.nodes["0000-MAIN"].is_entry_point)
        self.assertEqual(g.nodes["0000-MAIN"].node_type, GraphNodeType.MAIN_DRIVER)

        # 5. Calls from 0000-MAIN
        main_successors = g.nodes["0000-MAIN"].successors
        self.assertIn("1000-PROCESS", main_successors)
        self.assertIn("2000-OUTPUT", main_successors)

        # 6. Call from 1000-PROCESS to 2000-OUTPUT
        self.assertIn("2000-OUTPUT", g.nodes["1000-PROCESS"].successors)
        self.assertIn("1000-PROCESS", g.nodes["2000-OUTPUT"].called_by)
        self.assertIn("0000-MAIN", g.nodes["2000-OUTPUT"].called_by)

    def test_multi_section_program_identified_as_section_based(self):
        """
        Programs with multiple sections where calls target section names must be
        identified as section-based.
        """
        sec1 = SectionNode(
            name="MAIN-SEC",
            statements=[PerformStatementNode(target="CALC-SEC")],
            paragraph_names=["M010", "M-EX"],
        )
        sec2 = SectionNode(
            name="CALC-SEC",
            statements=[],
            paragraph_names=["C010", "C-EX"],
        )
        p1 = ParagraphNode(name="M010", statements=[PerformStatementNode(target="CALC-SEC")])
        p2 = ParagraphNode(name="M-EX", statements=[ExitStatementNode()])
        p3 = ParagraphNode(name="C010", statements=[])
        p4 = ParagraphNode(name="C-EX", statements=[ExitStatementNode()])

        model = ProgramModel(
            program_id="TEST-MULTI-SEC",
            sections=[sec1, sec2],
            paragraphs=[p1, p2, p3, p4],
        )

        self.assertTrue(is_section_based_program(model))
        gen = CallGraphGenerator(model)
        self.assertEqual(len(gen.graph.nodes), 2)
        self.assertIn("MAIN-SEC", gen.graph.nodes)
        self.assertIn("CALC-SEC", gen.graph.nodes)

    def test_real_tt35522_program_if_available(self):
        """Validates real fixture TT35522.cbl if present on the local filesystem."""
        fixture_path = Path("C:/Users/austi/cobol-private-tests/fixtures/cobol_lst/mini_test/unit_test/TT35522.cbl")
        if not fixture_path.exists():
            self.skipTest(f"Fixture not found at {fixture_path}")

        raw_dict = parse(fixture_path)
        model = ProgramModel.from_dict(raw_dict)

        self.assertFalse(is_section_based_program(model))
        gen = CallGraphGenerator(model, collapse_exits=True)
        g = gen.graph

        self.assertGreater(len(g.nodes), 1)
        self.assertIn("0000-MAIN", g.nodes)
        self.assertIn("1000-GET-DSN", g.nodes)
        self.assertIn("1000-GET-DSN", g.nodes["0000-MAIN"].successors)
        self.assertIn("0000-MAIN", g.nodes["1000-GET-DSN"].called_by)
        self.assertEqual(len(g.edges), 14)


if __name__ == "__main__":
    unittest.main()
