"""
tests.test_graph_utils
~~~~~~~~~~~~~~~~~~~~~~

Comprehensive unit tests for zero-dependency static graph algorithms:
1. Tarjan's Strongly Connected Components (SCC) & Condensation DAG Depth
2. Cooper-Harvey-Kennedy (2001) Dominators (idom) & Dead-Code Reachability
3. Immediate Post-Dominator (ipdom) Dual-Graph Analysis
4. Integration with CallGraph and IntraprocedureCfg
"""

import unittest
from cobolscope.graph.utils import (
    tarjan_scc,
    compute_dominators,
    compute_post_dominators,
    SccResult,
    DominatorResult,
    PostDominatorResult,
)
from cobolscope.models import (
    ParagraphNode,
    SourceLocation,
    MoveStatementNode,
    IfStatementNode,
    ComputeStatementNode,
    StopStatementNode,
)
from cobolscope.graph.cfg_builder import build_procedure_cfg
from cobolscope.graph.builder import CallGraphGenerator
from tests.harness.test_cache import get_test_model


class TestTarjanScc(unittest.TestCase):
    """Tests for Tarjan's Strongly Connected Components and cycle detection."""

    def test_dag_no_cycles(self):
        """A directed acyclic graph has zero cycles and valid topological depth."""
        # A -> B -> D
        # A -> C -> D
        nodes = ["A", "B", "C", "D"]
        edges = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

        res = tarjan_scc(nodes, lambda u: edges.get(u, []))
        self.assertFalse(res.has_cycles)
        self.assertEqual(res.cycles, [])
        self.assertEqual(len(res.sccs), 4)
        self.assertEqual(res.max_depth, 3)

    def test_simple_cycle(self):
        """A simple cycle A -> B -> C -> A is detected."""
        nodes = ["A", "B", "C", "D"]
        edges = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}

        res = tarjan_scc(nodes, lambda u: edges.get(u, []))
        self.assertTrue(res.has_cycles)
        self.assertEqual(len(res.cycles), 1)
        self.assertEqual(set(res.cycles[0]), {"A", "B", "C"})

    def test_self_loop(self):
        """A single node with a self-loop is classified as a cycle."""
        nodes = ["A", "B"]
        edges = {"A": ["A", "B"], "B": []}

        res = tarjan_scc(nodes, lambda u: edges.get(u, []))
        self.assertTrue(res.has_cycles)
        self.assertEqual(len(res.cycles), 1)
        self.assertEqual(res.cycles[0], ["A"])

    def test_multiple_disconnected_cycles(self):
        """Multiple independent cycles are correctly segregated."""
        # Cycle 1: 1 <-> 2
        # Cycle 2: 3 <-> 4
        # Linear: 5 -> 6
        nodes = [1, 2, 3, 4, 5, 6]
        edges = {
            1: [2],
            2: [1],
            3: [4],
            4: [3],
            5: [6],
            6: [],
        }
        res = tarjan_scc(nodes, lambda u: edges.get(u, []))
        self.assertTrue(res.has_cycles)
        self.assertEqual(len(res.cycles), 2)
        cycle_sets = [set(c) for c in res.cycles]
        self.assertIn({1, 2}, cycle_sets)
        self.assertIn({3, 4}, cycle_sets)


class TestDominators(unittest.TestCase):
    """Tests for Cooper-Harvey-Kennedy dominator tree calculation."""

    def test_linear_dominance(self):
        """In a linear chain, each node is dominated by its immediate predecessor."""
        nodes = ["A", "B", "C"]
        succs = {"A": ["B"], "B": ["C"], "C": []}
        preds = {"A": [], "B": ["A"], "C": ["B"]}

        res = compute_dominators(nodes, lambda u: succs.get(u, []), lambda u: preds.get(u, []), entry="A")
        self.assertIsNone(res.idom["A"])
        self.assertEqual(res.idom["B"], "A")
        self.assertEqual(res.idom["C"], "B")
        self.assertEqual(res.reachable_nodes, {"A", "B", "C"})
        self.assertEqual(res.unreachable_nodes, set())

    def test_diamond_dominance(self):
        """In a diamond, the convergence node is dominated by the split node."""
        # A -> B -> D
        # A -> C -> D
        nodes = ["A", "B", "C", "D"]
        succs = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        preds = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}

        res = compute_dominators(nodes, lambda u: succs.get(u, []), lambda u: preds.get(u, []), entry="A")
        self.assertEqual(res.idom["B"], "A")
        self.assertEqual(res.idom["C"], "A")
        self.assertEqual(res.idom["D"], "A")

    def test_dead_code_detection(self):
        """Nodes unreachable from entry are captured in unreachable_nodes."""
        nodes = ["A", "B", "DEAD1", "DEAD2"]
        succs = {"A": ["B"], "B": [], "DEAD1": ["DEAD2"], "DEAD2": []}
        preds = {"A": [], "B": ["A"], "DEAD1": [], "DEAD2": ["DEAD1"]}

        res = compute_dominators(nodes, lambda u: succs.get(u, []), lambda u: preds.get(u, []), entry="A")
        self.assertEqual(res.reachable_nodes, {"A", "B"})
        self.assertEqual(res.unreachable_nodes, {"DEAD1", "DEAD2"})
        self.assertNotIn("DEAD1", res.idom)


class TestPostDominators(unittest.TestCase):
    """Tests for Immediate Post-Dominance (ipdom) analysis."""

    def test_diamond_convergence_post_dominance(self):
        """In a diamond, D post-dominates A, B, and C."""
        nodes = ["A", "B", "C", "D", "exit"]
        succs = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["exit"], "exit": []}
        preds = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"], "exit": ["D"]}

        res = compute_post_dominators(
            nodes,
            lambda u: succs.get(u, []),
            lambda u: preds.get(u, []),
            exits=["exit"],
        )
        self.assertEqual(res.ipdom["A"], "D")
        self.assertEqual(res.ipdom["B"], "D")
        self.assertEqual(res.ipdom["C"], "D")
        self.assertEqual(res.ipdom["D"], "exit")
        self.assertIsNone(res.ipdom["exit"])

    def test_abend_branch_post_dominance(self):
        """
        When branch B abends and branch C continues to D -> exit,
        D is the post-dominator for A because path B never reaches exit.
        """
        nodes = ["A", "B_ABEND", "C", "D", "exit"]
        succs = {
            "A": ["B_ABEND", "C"],
            "B_ABEND": [],      # terminal sink
            "C": ["D"],
            "D": ["exit"],
            "exit": [],
        }
        preds = {
            "A": [],
            "B_ABEND": ["A"],
            "C": ["A"],
            "D": ["C"],
            "exit": ["D"],
        }

        res = compute_post_dominators(
            nodes,
            lambda u: succs.get(u, []),
            lambda u: preds.get(u, []),
            exits=["exit"],
        )
        self.assertIn("B_ABEND", res.dead_ends)
        self.assertNotIn("B_ABEND", res.reaches_exit)
        # All paths reaching exit from A must pass through C and D
        self.assertEqual(res.ipdom["A"], "C")
        self.assertEqual(res.ipdom["C"], "D")
        self.assertEqual(res.ipdom["D"], "exit")


class TestGraphUtilsIntegration(unittest.TestCase):
    """Integration test verifying CallGraph and IntraprocedureCfg integration."""

    def test_call_graph_cycles_and_sccs_populated(self):
        """CallGraph model stores exact cycles and sccs from Tarjan algorithm."""
        model = get_test_model("tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl")
        gen = CallGraphGenerator(model)
        cg = gen.graph

        self.assertIsInstance(cg.cycles, list)
        self.assertIsInstance(cg.sccs, list)
        self.assertEqual(cg.has_cycles, len(cg.cycles) > 0)
        self.assertGreater(cg.max_depth, 0)

    def test_cfg_dominators_and_post_dominators_populated(self):
        """IntraprocedureCfg accurately stores dominator and post-dominator maps."""
        p = ParagraphNode(
            name="TEST-BRANCH",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                MoveStatementNode(raw_text="MOVE 1 TO X", location=SourceLocation(start_line=2, end_line=2)),
                IfStatementNode(
                    condition="X > 0",
                    location=SourceLocation(start_line=3, end_line=7),
                    then_statements=[
                        ComputeStatementNode(raw_text="COMPUTE Y = X + 1", location=SourceLocation(start_line=4, end_line=4)),
                    ],
                    else_statements=[
                        MoveStatementNode(raw_text="MOVE 0 TO Y", location=SourceLocation(start_line=6, end_line=6)),
                    ],
                ),
                MoveStatementNode(raw_text="MOVE Y TO Z", location=SourceLocation(start_line=8, end_line=8)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertIn("entry", cfg.dominators)
        self.assertIn("exit", cfg.post_dominators)
        self.assertEqual(len(cfg.dead_code_nodes), 0)
        # Verify no nonexistent edge targets exist
        node_ids = set(cfg.nodes.keys())
        for e in cfg.edges:
            self.assertIn(e.source, node_ids)
            self.assertIn(e.target, node_ids)


if __name__ == "__main__":
    unittest.main()
