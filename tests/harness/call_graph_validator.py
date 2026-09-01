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
        Verifies that every procedure/section/paragraph in the AST is either present as a node
        or properly tracked in a collapsed exit container or procedure container.
        """
        is_section_based = len(self.model.sections) > 0 and any(len(s.paragraph_names) > 0 for s in self.model.sections)

        if is_section_based:
            model_secs = {s.name.upper().strip() for s in self.model.sections}
            graph_nodes = set(self.graph.nodes.keys())
            missing = model_secs - graph_nodes
            assert not missing, f"Missing sections in call graph: {missing}"
        else:
            model_paras = {p.name.upper().strip() for p in self.model.paragraphs}
            graph_nodes = set(self.graph.nodes.keys())
            if self.generator.collapse_exits:
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
        is_section_based = len(self.model.sections) > 0 and any(len(s.paragraph_names) > 0 for s in self.model.sections)
        symbol_to_proc: Dict[str, str] = {}

        if is_section_based:
            for s in self.model.sections:
                s_up = s.name.upper().strip()
                symbol_to_proc[s_up] = s_up
                for p in s.paragraph_names:
                    symbol_to_proc[p.upper().strip()] = s_up
        else:
            for p in self.model.paragraphs:
                p_up = p.name.upper().strip()
                symbol_to_proc[p_up] = p_up

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

        for (caller, target) in ast_calls:
            caller_proc = symbol_to_proc.get(caller, caller)
            target_proc = symbol_to_proc.get(target, target)

            if caller_proc != target_proc and target_proc in self.graph.nodes:
                assert (caller_proc, target_proc) in graph_edges, (
                    f"AST call ({caller} -> {target}, mapped: {caller_proc} -> {target_proc}) missing from graph edges!"
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
        """Verifies that all PERFORM ... THRU statements generate proper procedure calls."""
        is_section_based = len(self.model.sections) > 0 and any(len(s.paragraph_names) > 0 for s in self.model.sections)
        symbol_to_proc: Dict[str, str] = {}

        if is_section_based:
            for s in self.model.sections:
                s_up = s.name.upper().strip()
                symbol_to_proc[s_up] = s_up
                for p in s.paragraph_names:
                    symbol_to_proc[p.upper().strip()] = s_up
        else:
            for p in self.model.paragraphs:
                p_up = p.name.upper().strip()
                symbol_to_proc[p_up] = p_up

        graph_edges = {(e.source.upper().strip(), e.target.upper().strip()) for e in self.graph.edges}

        for p in self.model.paragraphs:
            caller_proc = symbol_to_proc.get(p.name.upper().strip(), p.name.upper().strip())
            for s in p.statements:
                if isinstance(s, PerformStatementNode) and s.target and s.thru:
                    tgt_proc = symbol_to_proc.get(s.target.upper().strip(), s.target.upper().strip())
                    if caller_proc != tgt_proc and tgt_proc in self.graph.nodes:
                        assert (caller_proc, tgt_proc) in graph_edges, (
                            f"Missing procedure edge ({caller_proc} -> {tgt_proc}) for PERFORM {s.target} THRU {s.thru}"
                        )
        return True
