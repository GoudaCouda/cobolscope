"""
Test Suite for Error Trap Decoupling and Default Hiding in Procedure Call Graphs.
Verifies:
1. Normal termination (STOP RUN, GOBACK, wrap-up) is NOT classified as an error trap and NOT rendered with red ERROR_BRANCH edges.
2. Configured abend routines (999-ABEND, CEE3ABD, custom rules) are detected as error traps.
3. Error traps are hidden by default (hide_error_traps=True), removing them and their relationships.
4. Error traps are included when hide_error_traps=False (e.g. via --show-error-traps).
"""

import unittest
from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    PerformStatementNode,
    GoToStatementNode,
    CallStatementNode,
    StopStatementNode,
    GobackStatementNode,
    DisplayStatementNode,
    MoveStatementNode,
    AddStatementNode,
)
from cobolscope.graph import (
    CallGraphGenerator,
    GraphNodeType,
    GraphEdgeType,
)
from cobolscope.rules import GlobalRules, ParagraphNamingRules


class TestErrorTrapDecoupling(unittest.TestCase):

    def setUp(self):
        # Construct synthetic COBOL program with:
        # - 0000-MAIN: Main control driver
        # - 1000-PROCESS-DATA: Reads/processes data, then calls 9000-WRAPUP
        # - 9000-WRAPUP: Normal clean termination routine with GOBACK
        # - 999-ABEND: Abnormal termination / abend routine
        # - 8000-CALC: Normal subroutine
        self.p_main = ParagraphNode(
            name="0000-MAIN",
            statements=[
                PerformStatementNode(target="1000-PROCESS-DATA"),
                PerformStatementNode(target="8000-CALC"),
                PerformStatementNode(target="9000-WRAPUP"),
                StopStatementNode(),
            ],
            successors=["1000-PROCESS-DATA", "8000-CALC", "9000-WRAPUP"],
        )

        self.p_process = ParagraphNode(
            name="1000-PROCESS-DATA",
            statements=[
                DisplayStatementNode(raw_text="DISPLAY 'PROCESSING'"),
                PerformStatementNode(target="999-ABEND"),
                PerformStatementNode(target="9000-WRAPUP"),
            ],
            successors=["999-ABEND", "9000-WRAPUP"],
        )

        self.p_calc = ParagraphNode(
            name="8000-CALC",
            statements=[
                DisplayStatementNode(raw_text="DISPLAY 'CALC'"),
                PerformStatementNode(target="999-ABEND"),
            ],
            successors=["999-ABEND"],
        )

        self.p_wrapup = ParagraphNode(
            name="9000-WRAPUP",
            statements=[
                DisplayStatementNode(raw_text="DISPLAY 'CLEAN SHUTDOWN'"),
                GobackStatementNode(),
            ],
            is_terminal=True,
        )

        self.p_abend = ParagraphNode(
            name="999-ABEND",
            statements=[
                DisplayStatementNode(raw_text="DISPLAY 'FATAL ERROR'"),
                CallStatementNode(program="CEE3ABD"),
                StopStatementNode(),
            ],
            is_terminal=True,
        )

        self.model = ProgramModel(
            program_id="TEST-ABEND-APP",
            paragraphs=[
                self.p_main,
                self.p_process,
                self.p_calc,
                self.p_wrapup,
                self.p_abend,
            ],
        )

    def test_default_hides_error_traps(self):
        """By default, 999-ABEND and its incoming edges must be hidden."""
        gen = CallGraphGenerator(self.model, hide_error_traps=True)
        graph = gen.graph

        # 999-ABEND must NOT be in nodes
        self.assertNotIn("999-ABEND", graph.nodes)
        self.assertIn("999-ABEND", graph.hidden_error_nodes)

        # Normal termination routine 9000-WRAPUP must remain in graph
        self.assertIn("9000-WRAPUP", graph.nodes)
        self.assertIn("1000-PROCESS-DATA", graph.nodes)
        self.assertIn("0000-MAIN", graph.nodes)
        self.assertIn("8000-CALC", graph.nodes)

        # No edges targeting 999-ABEND should exist
        edges_to_abend = [e for e in graph.edges if e.target == "999-ABEND"]
        self.assertEqual(len(edges_to_abend), 0)

        # No ERROR_BRANCH edges should exist
        error_edges = [e for e in graph.edges if e.edge_type == GraphEdgeType.ERROR_BRANCH]
        self.assertEqual(len(error_edges), 0)

        # Call to normal wrapup must be PERFORM (blue), NOT ERROR_BRANCH
        wrapup_edges = [e for e in graph.edges if e.target == "9000-WRAPUP"]
        self.assertGreater(len(wrapup_edges), 0)
        for e in wrapup_edges:
            self.assertEqual(e.edge_type, GraphEdgeType.PERFORM)

        # 999-ABEND must not be in successors of callers
        proc_node = graph.nodes["1000-PROCESS-DATA"]
        self.assertNotIn("999-ABEND", proc_node.successors)
        calc_node = graph.nodes["8000-CALC"]
        self.assertNotIn("999-ABEND", calc_node.successors)

    def test_show_error_traps_when_requested(self):
        """When hide_error_traps=False, 999-ABEND is shown and edges are ERROR_BRANCH."""
        gen = CallGraphGenerator(self.model, hide_error_traps=False)
        graph = gen.graph

        # 999-ABEND must be in nodes
        self.assertIn("999-ABEND", graph.nodes)
        abend_node = graph.nodes["999-ABEND"]
        self.assertEqual(abend_node.node_type, GraphNodeType.ERROR_HANDLING)

        # Edges targeting 999-ABEND must be ERROR_BRANCH
        edges_to_abend = [e for e in graph.edges if e.target == "999-ABEND"]
        self.assertEqual(len(edges_to_abend), 2)
        for e in edges_to_abend:
            self.assertEqual(e.edge_type, GraphEdgeType.ERROR_BRANCH)

        # Edges targeting 9000-WRAPUP must STILL be PERFORM, NOT ERROR_BRANCH
        wrapup_edges = [e for e in graph.edges if e.target == "9000-WRAPUP"]
        for e in wrapup_edges:
            self.assertEqual(e.edge_type, GraphEdgeType.PERFORM)

    def test_normal_termination_not_error_handling(self):
        """Normal termination routine 9000-WRAPUP is TERMINATION, never ERROR_HANDLING."""
        gen = CallGraphGenerator(self.model, hide_error_traps=False)
        graph = gen.graph

        wrapup_node = graph.nodes["9000-WRAPUP"]
        self.assertEqual(wrapup_node.node_type, GraphNodeType.TERMINATION)
        self.assertNotEqual(wrapup_node.node_type, GraphNodeType.ERROR_HANDLING)

    def test_custom_rules_config_detection(self):
        """Custom rules YAML declaring a custom abend module or routine is respected."""
        # Create a routine calling custom abend module MYABEND
        p_custom_abend = ParagraphNode(
            name="CUSTOM-KILL-PROC",
            statements=[
                CallStatementNode(program="MYABEND"),
                StopStatementNode(),
            ],
        )
        custom_model = ProgramModel(
            program_id="CUSTOM-RULES-TEST",
            paragraphs=[
                self.p_main,
                p_custom_abend,
            ],
        )

        custom_rules = GlobalRules(
            runtime_modules=["MYABEND"],
            paragraph_names=ParagraphNamingRules(strict=["CUSTOM-KILL-PROC"]),
        )

        # Hidden by default with custom rules
        gen = CallGraphGenerator(custom_model, rules=custom_rules, hide_error_traps=True)
        self.assertNotIn("CUSTOM-KILL-PROC", gen.graph.nodes)
        self.assertIn("CUSTOM-KILL-PROC", gen.graph.hidden_error_nodes)

        # Shown when requested
        gen_show = CallGraphGenerator(custom_model, rules=custom_rules, hide_error_traps=False)
        self.assertIn("CUSTOM-KILL-PROC", gen_show.graph.nodes)


if __name__ == "__main__":
    unittest.main()
