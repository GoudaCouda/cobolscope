"""
tests/test_graph_heuristics.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verification suite for Large Graph Optimization:
- Topological Graph Metrics Computation
- Layout Heuristics Engine (Dynamic ranker, nodesep, ranksep, splines)
- Intelligent Node Cloning for High In-Degree Utilities
- Integration with CallGraphGenerator, DOT, and HTML Viewers
"""

import sys
import unittest
from pathlib import Path

# Ensure repo root is on sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    SectionNode,
    PerformStatementNode,
    ExitStatementNode,
    SourceLocation,
)
from cobolscope.graph.models import (
    CallGraph,
    CallGraphNode,
    CallGraphEdge,
    GraphNodeType,
    GraphEdgeType,
)
from cobolscope.graph.heuristics import (
    compute_graph_metrics,
    calculate_layout_heuristics,
    GraphMetrics,
    LayoutHeuristics,
)
from cobolscope.graph.cloning import (
    identify_clone_candidates,
    apply_node_cloning,
)
from cobolscope.graph.builder import CallGraphGenerator, generate_call_graph


def build_synthetic_graph(num_nodes: int, branching: int = 2) -> CallGraph:
    """Constructs a synthetic DAG with num_nodes and specified branching."""
    nodes = {}
    edges = []
    for i in range(num_nodes):
        name = f"PROC_{i:03d}"
        node_id = f"p_PROC_{i:03d}"
        nodes[name] = CallGraphNode(
            id=node_id,
            name=name,
            node_type=GraphNodeType.BUSINESS_LOGIC if i > 0 else GraphNodeType.MAIN_DRIVER,
            is_entry_point=(i == 0),
            start_line=i * 10 + 1,
            end_line=i * 10 + 8,
        )

    for i in range(num_nodes):
        src_name = f"PROC_{i:03d}"
        for b in range(1, branching + 1):
            tgt_idx = i * branching + b
            if tgt_idx < num_nodes:
                tgt_name = f"PROC_{tgt_idx:03d}"
                edges.append(CallGraphEdge(
                    source=src_name,
                    target=tgt_name,
                    edge_type=GraphEdgeType.PERFORM,
                ))
                nodes[src_name].successors.append(tgt_name)
                nodes[tgt_name].called_by.append(src_name)

    return CallGraph(
        program_id="SYNTH_TEST",
        entry_point="PROC_000",
        nodes=nodes,
        edges=edges,
        total_paragraphs=len(nodes),
        total_calls=len(edges),
    )


class TestGraphMetrics(unittest.TestCase):
    """Validates calculation of topological invariants across graph sizes."""

    def test_empty_and_single_node_metrics(self):
        empty_graph = CallGraph(
            program_id="EMPTY",
            nodes={},
            edges=[],
            total_paragraphs=0,
            total_calls=0,
        )
        m_empty = compute_graph_metrics(empty_graph)
        self.assertEqual(m_empty.total_nodes, 0)
        self.assertEqual(m_empty.density, 0.0)
        self.assertEqual(m_empty.scale_category, "small")

        single_node = CallGraph(
            program_id="SINGLE",
            nodes={"MAIN": CallGraphNode(id="p_MAIN", name="MAIN", is_entry_point=True)},
            edges=[],
            total_paragraphs=1,
            total_calls=0,
        )
        m_single = compute_graph_metrics(single_node)
        self.assertEqual(m_single.total_nodes, 1)
        self.assertEqual(m_single.density, 0.0)
        self.assertEqual(m_single.hierarchy_depth, 1)
        self.assertEqual(m_single.max_rank_width, 1)

    def test_medium_graph_metrics(self):
        graph = build_synthetic_graph(45, branching=2)
        metrics = compute_graph_metrics(graph)

        self.assertEqual(metrics.total_nodes, 45)
        self.assertEqual(metrics.scale_category, "medium")
        self.assertGreater(metrics.hierarchy_depth, 1)
        self.assertGreaterEqual(metrics.max_rank_width, 2)
        self.assertGreater(metrics.density, 0.0)
        self.assertGreater(metrics.avg_degree, 0.0)

        d = metrics.to_dict()
        self.assertEqual(d["total_nodes"], 45)
        self.assertEqual(d["scale_category"], "medium")

    def test_large_graph_metrics(self):
        graph = build_synthetic_graph(110, branching=2)
        metrics = compute_graph_metrics(graph)

        self.assertEqual(metrics.total_nodes, 110)
        self.assertEqual(metrics.scale_category, "large")
        self.assertGreater(metrics.max_rank_width, 10)


class TestLayoutHeuristics(unittest.TestCase):
    """Validates dynamic heuristic derivation based on graph metrics."""

    def test_small_graph_heuristics(self):
        metrics = GraphMetrics(
            total_nodes=20,
            total_edges=25,
            density=0.065,
            avg_degree=1.25,
            max_in_degree=2,
            max_out_degree=2,
            max_rank_width=5,
            hierarchy_depth=6,
            aspect_ratio=0.83,
            scale_category="small",
            high_indegree_nodes=[],
        )
        h = calculate_layout_heuristics(metrics, compact_nodes=True)
        self.assertEqual(h.ranker, "network-simplex")
        self.assertEqual(h.ranksep_in, 0.75)
        self.assertEqual(h.nodesep_in, 0.45)
        self.assertEqual(h.splines, "spline")
        self.assertFalse(h.recommend_elk)

        self.assertFalse(h.recommend_cloning)

        d = h.to_dict()
        self.assertEqual(d["ranker"], "network-simplex")
        self.assertEqual(d["cyto_ranksep"], 60)

    def test_medium_graph_heuristics(self):
        metrics = GraphMetrics(
            total_nodes=60,
            total_edges=80,
            density=0.022,
            avg_degree=1.33,
            max_in_degree=3,
            max_out_degree=3,
            max_rank_width=12,
            hierarchy_depth=10,
            aspect_ratio=1.2,
            scale_category="medium",
            high_indegree_nodes=[],
        )
        h = calculate_layout_heuristics(metrics, compact_nodes=True)
        self.assertEqual(h.ranker, "tight-tree")
        self.assertEqual(h.ranksep_in, 0.60)
        self.assertEqual(h.nodesep_in, 0.55)  # max_rank_width = 12 (8 < W <= 16)
        self.assertEqual(h.splines, "spline")
        self.assertTrue(h.recommend_elk)


    def test_large_and_massive_graph_heuristics(self):
        metrics = GraphMetrics(
            total_nodes=160,
            total_edges=240,
            density=0.009,
            avg_degree=1.5,
            max_in_degree=15,
            max_out_degree=4,
            max_rank_width=25,
            hierarchy_depth=14,
            aspect_ratio=1.78,
            scale_category="massive",
            high_indegree_nodes=["LOG-ERR"],
        )
        h = calculate_layout_heuristics(metrics, compact_nodes=True)
        self.assertEqual(h.ranker, "longest-path")
        self.assertEqual(h.ranksep_in, 0.38)
        self.assertEqual(h.splines, "spline")  # > 75 nodes forces spline
        self.assertTrue(h.recommend_elk)
        self.assertTrue(h.recommend_cloning)

    def test_spaghetti_ladder_aspect_ratio_compression(self):
        metrics = GraphMetrics(
            total_nodes=50,
            total_edges=60,
            density=0.024,
            avg_degree=1.2,
            max_in_degree=2,
            max_out_degree=2,
            max_rank_width=4,
            hierarchy_depth=20,
            aspect_ratio=0.2,  # Tall spaghetti ladder
            scale_category="medium",
            high_indegree_nodes=[],
        )
        h = calculate_layout_heuristics(metrics, compact_nodes=True)
        self.assertAlmostEqual(h.ranksep_in, 0.51, places=2)

    def test_requested_overrides(self):
        metrics = GraphMetrics(
            total_nodes=100,
            total_edges=120,
            density=0.012,
            avg_degree=1.2,
            max_in_degree=2,
            max_out_degree=2,
            max_rank_width=10,
            hierarchy_depth=10,
            aspect_ratio=1.0,
            scale_category="large",
            high_indegree_nodes=[],
        )
        h = calculate_layout_heuristics(
            metrics,
            requested_ranker="network-simplex",
            requested_splines="polyline",
        )
        self.assertEqual(h.ranker, "network-simplex")
        self.assertEqual(h.splines, "polyline")


class TestNodeCloning(unittest.TestCase):
    """Validates candidate identification and node cloning transformations."""

    def _build_hub_program_graph(self) -> CallGraph:
        """
        Creates a call graph with 4 callers across 3 sections calling a shared utility leaf 'UTIL-LOG'.
        """
        nodes = {
            "MAIN-LOGIC": CallGraphNode(
                id="p_MAIN_LOGIC", name="MAIN-LOGIC", section="INIT-SEC", is_entry_point=True
            ),
            "PROCESS-A": CallGraphNode(
                id="p_PROCESS_A", name="PROCESS-A", section="PROC-SEC"
            ),
            "PROCESS-B": CallGraphNode(
                id="p_PROCESS_B", name="PROCESS-B", section="PROC-SEC"
            ),
            "AUDIT-REC": CallGraphNode(
                id="p_AUDIT_REC", name="AUDIT-REC", section="AUDIT-SEC"
            ),
            "UTIL-LOG": CallGraphNode(
                id="p_UTIL_LOG", name="UTIL-LOG", section="UTIL-SEC", is_terminal=False
            ),
        }
        edges = [
            CallGraphEdge(source="MAIN-LOGIC", target="PROCESS-A", edge_type=GraphEdgeType.PERFORM),
            CallGraphEdge(source="MAIN-LOGIC", target="PROCESS-B", edge_type=GraphEdgeType.PERFORM),
            CallGraphEdge(source="MAIN-LOGIC", target="UTIL-LOG", edge_type=GraphEdgeType.PERFORM),
            CallGraphEdge(source="PROCESS-A", target="UTIL-LOG", edge_type=GraphEdgeType.PERFORM),
            CallGraphEdge(source="PROCESS-B", target="UTIL-LOG", edge_type=GraphEdgeType.PERFORM),
            CallGraphEdge(source="AUDIT-REC", target="UTIL-LOG", edge_type=GraphEdgeType.PERFORM),
        ]
        nodes["MAIN-LOGIC"].successors = ["PROCESS-A", "PROCESS-B", "UTIL-LOG"]
        nodes["PROCESS-A"].called_by = ["MAIN-LOGIC"]
        nodes["PROCESS-A"].successors = ["UTIL-LOG"]
        nodes["PROCESS-B"].called_by = ["MAIN-LOGIC"]
        nodes["PROCESS-B"].successors = ["UTIL-LOG"]
        nodes["AUDIT-REC"].successors = ["UTIL-LOG"]
        nodes["UTIL-LOG"].called_by = ["MAIN-LOGIC", "PROCESS-A", "PROCESS-B", "AUDIT-REC"]

        return CallGraph(
            program_id="CLONE_HUB_TEST",
            entry_point="MAIN-LOGIC",
            nodes=nodes,
            edges=edges,
            total_paragraphs=len(nodes),
            total_calls=len(edges),
        )

    def test_identify_clone_candidates(self):
        graph = self._build_hub_program_graph()
        candidates = identify_clone_candidates(graph, min_in_degree=3)

        self.assertIn("UTIL-LOG", candidates)
        self.assertNotIn("MAIN-LOGIC", candidates)  # Entry point never cloned
        self.assertNotIn("PROCESS-A", candidates)  # in-degree < 3

    def test_section_mode_cloning(self):
        graph = self._build_hub_program_graph()
        cloned_graph = apply_node_cloning(graph, mode="section", min_in_degree=3)

        # UTIL-LOG called by INIT-SEC (MAIN-LOGIC), PROC-SEC (PROCESS-A, PROCESS-B), AUDIT-SEC (AUDIT-REC) -> 3 distinct sections
        # 1 section stays with primary node, 2 sections get clones -> 2 clone nodes created
        self.assertEqual(cloned_graph.cloned_node_count, 2)
        self.assertIn("UTIL-LOG", cloned_graph.nodes)  # Primary node retained for first section
        self.assertEqual(cloned_graph.nodes["UTIL-LOG"].clone_total, 3)

        # Verify cloned nodes exist
        clone_names = [k for k in cloned_graph.nodes if k.startswith("UTIL-LOG [")]
        self.assertEqual(len(clone_names), 2)

        for c_name in clone_names:
            c_node = cloned_graph.nodes[c_name]
            self.assertTrue(c_node.is_clone)
            self.assertEqual(c_node.original_name, "UTIL-LOG")
            self.assertEqual(c_node.clone_total, 3)
            self.assertIn(c_node.clone_index, (2, 3))

        # Incoming edges to UTIL-LOG must be retargeted to the appropriate section clone
        for edge in cloned_graph.edges:
            if edge.source in ("PROCESS-A", "PROCESS-B"):
                self.assertTrue(edge.target.startswith("UTIL-LOG ["))
                target_node = cloned_graph.nodes[edge.target]
                self.assertEqual(target_node.section, "PROC-SEC")

    def test_caller_mode_cloning(self):
        graph = self._build_hub_program_graph()
        cloned_graph = apply_node_cloning(graph, mode="caller", min_in_degree=3)

        # 4 distinct callers -> 1 primary node + 3 clones = 3 clone nodes created
        self.assertEqual(cloned_graph.cloned_node_count, 3)
        self.assertIn("UTIL-LOG", cloned_graph.nodes)
        self.assertEqual(cloned_graph.nodes["UTIL-LOG"].clone_total, 4)

        clone_names = [k for k in cloned_graph.nodes if k.startswith("UTIL-LOG#")]
        self.assertEqual(len(clone_names), 3)

        for c_name in clone_names:
            c_node = cloned_graph.nodes[c_name]
            self.assertTrue(c_node.is_clone)
            self.assertEqual(c_node.original_name, "UTIL-LOG")
            self.assertEqual(c_node.clone_total, 4)
            self.assertEqual(len(c_node.called_by), 1)

    def test_non_leaf_nodes_disqualified_from_cloning(self):
        graph = self._build_hub_program_graph()
        # Give UTIL-LOG two outgoing edges to sub-routines
        graph.nodes["UTIL-LOG"].successors = ["SUB-1", "SUB-2"]
        graph.nodes["SUB-1"] = CallGraphNode(id="p_SUB1", name="SUB-1")
        graph.nodes["SUB-2"] = CallGraphNode(id="p_SUB2", name="SUB-2")
        graph.edges.append(CallGraphEdge(source="UTIL-LOG", target="SUB-1", edge_type=GraphEdgeType.PERFORM))
        graph.edges.append(CallGraphEdge(source="UTIL-LOG", target="SUB-2", edge_type=GraphEdgeType.PERFORM))

        candidates = identify_clone_candidates(graph, min_in_degree=3, max_out_degree=1)
        self.assertNotIn("UTIL-LOG", candidates)  # Disqualified because out-degree is 2


class TestCallGraphGeneratorIntegration(unittest.TestCase):
    """Validates full pipeline generation with dynamic heuristics and cloning."""

    def _create_mock_program_model(self) -> ProgramModel:
        """Builds a realistic ProgramModel with multiple sections and utility routines."""
        sec_init = SectionNode(name="INIT-SECTION", paragraph_names=["0000-INIT"])
        sec_calc = SectionNode(name="CALC-SECTION", paragraph_names=["1000-CALC"])
        sec_io = SectionNode(name="IO-SECTION", paragraph_names=["2000-IO"])
        sec_util = SectionNode(name="UTIL-SECTION", paragraph_names=["9999-LOG"])

        p_init = ParagraphNode(
            name="0000-INIT",
            section_parent="INIT-SECTION",
            location=SourceLocation(start_line=10, end_line=15),
            statements=[
                PerformStatementNode(target="1000-CALC"),
                PerformStatementNode(target="2000-IO"),
                PerformStatementNode(target="9999-LOG"),
            ]
        )
        p_calc = ParagraphNode(
            name="1000-CALC",
            section_parent="CALC-SECTION",
            location=SourceLocation(start_line=20, end_line=28),
            statements=[
                PerformStatementNode(target="9999-LOG"),
            ]
        )
        p_io = ParagraphNode(
            name="2000-IO",
            section_parent="IO-SECTION",
            location=SourceLocation(start_line=30, end_line=38),
            statements=[
                PerformStatementNode(target="9999-LOG"),
            ]
        )
        p_log = ParagraphNode(
            name="9999-LOG",
            section_parent="UTIL-SECTION",
            location=SourceLocation(start_line=50, end_line=55),
            statements=[
                ExitStatementNode(),
            ]
        )

        return ProgramModel(
            program_id="MOCK_CLONE_PGM",
            sections=[sec_init, sec_calc, sec_io, sec_util],
            paragraphs=[p_init, p_calc, p_io, p_log],
            source_code="0000-INIT.\n    PERFORM 1000-CALC.\n    PERFORM 2000-IO.\n    PERFORM 9999-LOG.\n",
        )

    def test_generator_cloning_enabled(self):
        model = self._create_mock_program_model()
        generator = CallGraphGenerator(
            model=model,
            enable_cloning=True,
            clone_threshold=3,
            clone_mode="section",
        )

        # In section mode, UTIL-SECTION has 3 callers (INIT-SECTION, CALC-SECTION, IO-SECTION).
        # 1 section stays with primary, 2 sections get clones -> 2 clones created
        self.assertEqual(generator.graph.cloned_node_count, 2)
        self.assertTrue(hasattr(generator, "heuristics"))
        self.assertTrue(hasattr(generator, "metrics"))

        # Check DOT rendering includes clone badge and dynamic layout
        dot = generator.to_dot()
        self.assertIn("[CLONE", dot)
        self.assertIn("ranker=", dot)
        self.assertIn("nodesep=", dot)
        self.assertIn("ranksep=", dot)

        # Check HTML rendering includes layoutHeuristics and toggle
        html = generator.to_html()
        self.assertIn("layoutHeuristics", html)
        self.assertIn("toggleCloneUtilities", html)
        self.assertIn("ELK (Layered)", html)

    def test_generator_cloning_disabled_by_default(self):
        model = self._create_mock_program_model()
        generator = CallGraphGenerator(
            model=model,
            enable_cloning=False,
            clone_threshold=3,
        )

        # Canonical graph is active by default
        self.assertEqual(generator.graph.cloned_node_count, 0)
        self.assertIn("UTIL-SECTION", generator.graph.nodes)

        # But cloned elements are pre-computed for the UI checkbox!
        self.assertGreater(len(generator.cloned_cyto_elements), 0)
        html = generator.to_html()
        self.assertIn("Disentangle (", html)


    def test_generate_call_graph_functional_api(self):
        model = self._create_mock_program_model()
        html = generate_call_graph(
            model,
            format="html",
            enable_cloning=True,
            ranker="longest-path",
            nodesep=0.8,
            ranksep=0.5,
        )
        self.assertIn("Procedure Call Graph - MOCK_CLONE_PGM", html)
        self.assertIn("longest-path", html)



if __name__ == "__main__":
    unittest.main()
