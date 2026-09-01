"""
Call Graph Mathematical & Structural Invariant Validator.
Oracle engine for verifying that generated Level-2 procedure call graphs
strictly adhere to AST call-site completeness, cluster partitioning,
and Graphviz DOT compilation validity.
"""

from __future__ import annotations

import re
import subprocess
from typing import Dict, List, Set, Tuple

from cobolscope.models import (
    AnyStatementNode,
    EvaluateStatementNode,
    GoToStatementNode,
    IfStatementNode,
    ParagraphNode,
    PerformStatementNode,
    ProgramModel,
)
from cobolscope.graph import (
    CallGraph,
    CallGraphGenerator,
    GraphEdgeType,
)


class CallGraphValidator:
    """Mathematical and structural validator for CallGraph instances."""

    def __init__(self, model: ProgramModel, generator: CallGraphGenerator):
        self.model = model
        self.generator = generator
        self.graph: CallGraph = generator.graph

    def validate_all(self) -> Dict[str, bool]:
        """Runs the complete suite of graph mathematical invariant checks."""
        return {
            "node_coverage": self.verify_node_coverage(),
            "ast_call_parity": self.verify_ast_call_parity(),
            "cluster_partition": self.verify_cluster_partition(),
            "graphviz_compilation": self.verify_graphviz_compilation(),
            "thru_expansion": self.verify_thru_expansion(),
        }

    def verify_node_coverage(self) -> bool:
        """
        Verifies that every paragraph in the AST is either present as a node
        or properly tracked in a collapsed exit container.
        """
        model_paras = {p.name.upper().strip() for p in self.model.paragraphs}
        graph_nodes = set(self.graph.nodes.keys())

        if self.generator.collapse_exits:
            # Add all collapsed exits
            for node in self.graph.nodes.values():
                for exit_name in node.collapsed_exit_nodes:
                    graph_nodes.add(exit_name.upper().strip())

        missing = model_paras - graph_nodes
        assert not missing, f"Missing paragraphs in call graph: {missing}"
        return True

    def verify_ast_call_parity(self) -> bool:
        """
        Verifies that every PERFORM and GO TO call-site in the AST
        is accounted for in the graph edges.
        """
        ast_calls: Set[Tuple[str, str]] = set()

        def scan_stmts(stmts: List[AnyStatementNode], caller: str):
            for s in stmts:
                if isinstance(s, PerformStatementNode) and s.target:
                    ast_calls.add((caller.upper().strip(), s.target.upper().strip()))
                elif isinstance(s, GoToStatementNode) and s.target:
                    ast_calls.add((caller.upper().strip(), s.target.upper().strip()))
                elif isinstance(s, IfStatementNode):
                    scan_stmts(s.then_statements + s.else_statements, caller)
                elif isinstance(s, EvaluateStatementNode):
                    for wb in s.when_branches:
                        scan_stmts(wb.statements, caller)
                    scan_stmts(s.when_other_statements, caller)
                elif isinstance(s, PerformStatementNode) and s.nested_statements:
                    scan_stmts(s.nested_statements, caller)

        for p in self.model.paragraphs:
            scan_stmts(p.statements, p.name)

        # Build graph edge set
        graph_edges: Set[Tuple[str, str]] = set()
        for e in self.graph.edges:
            if e.edge_type in (GraphEdgeType.PERFORM, GraphEdgeType.GO_TO, GraphEdgeType.ERROR_BRANCH):
                graph_edges.add((e.source.upper().strip(), e.target.upper().strip()))

        # For collapsed exits, map target names
        if self.generator.collapse_exits:
            for (caller, target) in ast_calls:
                target_mapped = target
                if target.endswith("-EXIT"):
                    parent_candidate = target[:-5]
                    if parent_candidate in self.graph.nodes:
                        target_mapped = parent_candidate
                caller_mapped = caller
                if caller.endswith("-EXIT"):
                    parent_candidate = caller[:-5]
                    if parent_candidate in self.graph.nodes:
                        caller_mapped = parent_candidate

                if caller_mapped != target_mapped and target_mapped in self.graph.nodes:
                    assert (caller_mapped, target_mapped) in graph_edges, (
                        f"AST call ({caller} -> {target}) missing from graph edges!"
                    )
        else:
            for (caller, target) in ast_calls:
                if caller != target and target in self.graph.nodes:
                    assert (caller, target) in graph_edges, (
                        f"AST call ({caller} -> {target}) missing from graph edges!"
                    )

        return True

    def verify_cluster_partition(self) -> bool:
        """
        Verifies that every active node belongs to exactly one cluster,
        forming a mathematical partition of the graph's vertex set.
        """
        if not self.generator.enable_clustering:
            return True

        node_ids_in_graph = {n.id for n in self.graph.nodes.values()}
        node_ids_in_clusters: Set[str] = set()

        for c in self.graph.clusters:
            for nid in c.node_ids:
                assert nid not in node_ids_in_clusters, f"Node {nid} assigned to multiple clusters!"
                node_ids_in_clusters.add(nid)

        assert node_ids_in_clusters == node_ids_in_graph, (
            f"Cluster partition mismatch! In graph: {len(node_ids_in_graph)}, in clusters: {len(node_ids_in_clusters)}"
        )
        return True

    def verify_graphviz_compilation(self) -> bool:
        """
        Compiles the emitted .dot string through Graphviz dot binary
        to prove zero syntax errors, valid escaping, and well-formed SVG emission.
        """
        dot_str = self.generator.to_dot()
        assert dot_str.startswith("digraph "), "Emitted DOT does not begin with 'digraph'"
        assert dot_str.rstrip().endswith("}"), "Emitted DOT does not terminate with '}'"

        svg_out = self.generator.to_svg()
        assert "<svg" in svg_out, "Generated output does not contain '<svg'"
        assert "</svg>" in svg_out, "Generated output does not contain '</svg>'"
        return True

    def verify_thru_expansion(self) -> bool:
        """Verifies that all PERFORM ... THRU statements generate proper THRU edges."""
        thru_stmts = []
        for p in self.model.paragraphs:
            for s in p.statements:
                if isinstance(s, PerformStatementNode) and s.target and s.thru:
                    thru_stmts.append((p.name.upper().strip(), s.target.upper().strip(), s.thru.upper().strip()))

        for caller, target, thru in thru_stmts:
            if not self.generator.collapse_exits:
                thru_edges = [
                    e for e in self.graph.edges
                    if e.source.upper().strip() == caller and e.edge_type == GraphEdgeType.PERFORM_THRU
                ]
                if thru in self.graph.nodes and caller != thru:
                    assert any(e.target.upper().strip() == thru for e in thru_edges), (
                        f"Missing THRU edge from {caller} to {thru}"
                    )
        return True
