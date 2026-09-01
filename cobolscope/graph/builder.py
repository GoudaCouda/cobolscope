"""
cobolscope.graph.builder
~~~~~~~~~~~~~~~~~~~~~~~~~

Core CallGraphGenerator constructing structured Level-2 Call Graphs from ProgramModels.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from cobolscope.models import (
    AnyStatementNode,
    CallStatementNode,
    EvaluateStatementNode,
    GoToStatementNode,
    IfStatementNode,
    ParagraphNode,
    PerformStatementNode,
    ProgramModel,
    ReadStatementNode,
    WriteStatementNode,
    RewriteStatementNode,
    DeleteStatementNode,
    OpenStatementNode,
    CloseStatementNode,
    ExecSqlStatementNode,
    ExecCicsStatementNode,
    ExecSqlImsStatementNode,
)
from cobolscope.reachability import PushdownReachabilityAnalyzer
from .models import (
    CallGraph,
    CallGraphCluster,
    CallGraphEdge,
    CallGraphNode,
    GraphEdgeType,
    GraphNodeType,
)
from .classifier import CLUSTER_THEMES, ParagraphClassifier
from .renderers import render_dot, render_svg, render_html


class CallGraphGenerator:
    """
    Transforms canonical ProgramModel into a structured Level-2 CallGraph,
    evaluating inter-routine calls, PERFORM THRU sequences, and functional clusters.
    """

    def __init__(
        self,
        model: ProgramModel,
        hide_fallthrough: bool = True,
        collapse_exits: bool = True,
        enable_clustering: bool = True,
    ):
        self.model = model
        self.hide_fallthrough = hide_fallthrough
        self.collapse_exits = collapse_exits
        self.enable_clustering = enable_clustering
        self._dot_cache: Optional[str] = None
        self._svg_cache: Optional[str] = None
        self.graph: CallGraph = self._build_graph()

    def _build_graph(self) -> CallGraph:
        program_id = self.model.program_id or "COBOL_PROGRAM"
        nodes: Dict[str, CallGraphNode] = {}
        edges: List[CallGraphEdge] = []
        cluster_map: Dict[str, CallGraphCluster] = {}

        # Initialize cluster containers
        for ntype, theme in CLUSTER_THEMES.items():
            cluster_map[theme["id"]] = CallGraphCluster(
                id=theme["id"],
                name=theme["name"],
                color=theme["color"],
                fill_color=theme["fill_color"],
                text_color=theme["text_color"],
                node_ids=[],
            )

        # 0. Execute Pushdown Reachability Analysis to validate control flow, LIFO return points, and dead code
        reachability_engine = PushdownReachabilityAnalyzer(self.model)
        reachability_model = reachability_engine.analyze()

        # 1. First Pass: Create all nodes
        para_list = self.model.paragraphs
        exit_to_parent_map: Dict[str, str] = {}

        # Detect exit pairs if collapsing is enabled
        for i, p in enumerate(para_list):
            p_name_up = p.name.upper().strip()
            if p_name_up.endswith("-EXIT") and i > 0:
                parent_candidate = para_list[i - 1].name.upper().strip()
                if p_name_up == f"{parent_candidate}-EXIT":
                    exit_to_parent_map[p_name_up] = parent_candidate

        for i, p in enumerate(para_list):
            p_name_up = p.name.upper().strip()
            if self.collapse_exits and p_name_up in exit_to_parent_map:
                # Merge into parent node
                parent_name = exit_to_parent_map[p_name_up]
                if parent_name in nodes:
                    nodes[parent_name].collapsed_exit_nodes.append(p.name)
                continue

            node_type = ParagraphClassifier.classify(p)
            cluster_theme = CLUSTER_THEMES[node_type]
            if not self.enable_clustering:
                cluster_id = "cluster_generic"
            elif node_type == GraphNodeType.ROUTINE_EXIT and not self.collapse_exits:
                parent_name = exit_to_parent_map.get(p_name_up)
                if parent_name and parent_name in nodes:
                    cluster_id = nodes[parent_name].cluster_id
                else:
                    cluster_id = cluster_theme["id"]
            else:
                cluster_id = cluster_theme["id"]

            # Compute Statement Metrics & Complexity
            all_stmts = self._collect_all_statements(p.statements)
            stmt_count = len(all_stmts)
            cc = 1  # Base cyclomatic complexity

            io_summary: Dict[str, int] = {"READ": 0, "WRITE": 0, "SQL": 0, "CALL": 0}
            src_fields: Set[str] = set()
            tgt_fields: Set[str] = set()

            for s in all_stmts:
                # Branch complexity
                if isinstance(s, IfStatementNode):
                    cc += 1
                elif isinstance(s, EvaluateStatementNode):
                    cc += len(s.when_branches)
                elif isinstance(s, PerformStatementNode) and (s.until_condition or s.times_expr):
                    cc += 1

                # I/O counters
                if isinstance(s, ReadStatementNode):
                    io_summary["READ"] += 1
                elif isinstance(s, (WriteStatementNode, RewriteStatementNode)):
                    io_summary["WRITE"] += 1
                elif isinstance(s, (ExecSqlStatementNode, ExecCicsStatementNode, ExecSqlImsStatementNode)):
                    io_summary["SQL"] += 1
                elif isinstance(s, CallStatementNode):
                    io_summary["CALL"] += 1

                # Data lineages
                for fid in getattr(s, "source_field_ids", None) or []:
                    src_fields.add(fid)
                for fid in getattr(s, "target_field_ids", None) or []:
                    tgt_fields.add(fid)

            # Prune 0-value I/O counters
            io_summary = {k: v for k, v in io_summary.items() if v > 0}

            start_line = p.location.start_line if p.location else 0
            end_line = p.location.end_line if p.location else 0
            is_unreachable = p_name_up in reachability_model.unreachable_paragraphs

            node = CallGraphNode(
                id=self._sanitize_id(p.name),
                name=p.name,
                section=p.section_parent,
                node_type=node_type,
                cluster_id=cluster_id,
                start_line=start_line,
                end_line=end_line,
                statement_count=stmt_count,
                cyclomatic_complexity=cc,
                is_terminal=p.is_terminal,
                is_exit_paragraph=(node_type == GraphNodeType.ROUTINE_EXIT),
                is_unreachable=is_unreachable,
                io_summary=io_summary,
                source_field_ids=sorted(list(src_fields)),
                target_field_ids=sorted(list(tgt_fields)),
                called_by=list(p.called_by),
                successors=list(p.successors),
                fallthrough_successor=p.fallthrough_successor,
            )

            nodes[p_name_up] = node
            if cluster_id in cluster_map:
                cluster_map[cluster_id].node_ids.append(node.id)

        # 2. Second Pass: Extract Edges (Calls, Jumps, Thru, Fallthrough)
        seen_edges: Set[Tuple[str, str, GraphEdgeType]] = set()

        section_map: Dict[str, Tuple[str, str]] = {}
        for sec in self.model.sections:
            if sec.paragraph_names:
                first_p = sec.paragraph_names[0].upper().strip()
                last_p = sec.paragraph_names[-1].upper().strip()
                section_map[sec.name.upper().strip()] = (first_p, last_p)

        def is_error_trap(node_obj: CallGraphNode) -> bool:
            if node_obj.node_type == GraphNodeType.ERROR_HANDLING:
                return True
            n_up = node_obj.name.upper()
            return any(k in n_up for k in ("ABEND", "ERROR", "SYS-ERR", "FATAL", "TRAP", "EXCEPTION"))

        for p in para_list:
            caller_name_up = p.name.upper().strip()
            if self.collapse_exits and caller_name_up in exit_to_parent_map:
                continue

            all_stmts = self._collect_all_statements(p.statements)
            for stmt in all_stmts:
                # 2A. PERFORM Statements
                if isinstance(stmt, PerformStatementNode) and stmt.target:
                    target_raw = stmt.target.upper().strip()
                    thru_raw = stmt.thru.upper().strip() if stmt.thru else None

                    # Expand Section target if applicable
                    if target_raw in section_map:
                        first_p, last_p = section_map[target_raw]
                        target_raw = first_p
                        thru_raw = thru_raw if thru_raw else last_p

                    target_name = exit_to_parent_map.get(target_raw, target_raw) if self.collapse_exits else target_raw

                    # Check if target exists in nodes
                    if target_name in nodes:
                        target_node = nodes[target_name]
                        edge_type = GraphEdgeType.ERROR_BRANCH if is_error_trap(target_node) else GraphEdgeType.PERFORM
                        edge_key = (caller_name_up, target_name, edge_type)

                        if edge_key not in seen_edges and caller_name_up != target_name:
                            seen_edges.add(edge_key)
                            line_no = stmt.location.start_line if stmt.location else None
                            edges.append(CallGraphEdge(
                                source=caller_name_up,
                                target=target_name,
                                edge_type=edge_type,
                                line_number=line_no,
                            ))

                    # Expand PERFORM ... THRU sequence if present
                    if thru_raw:
                        thru_name = exit_to_parent_map.get(thru_raw, thru_raw) if self.collapse_exits else thru_raw
                        if thru_name != target_name and thru_name in nodes:
                            thru_edge_key = (caller_name_up, thru_name, GraphEdgeType.PERFORM_THRU)
                            if thru_edge_key not in seen_edges and caller_name_up != thru_name:
                                seen_edges.add(thru_edge_key)
                                edges.append(CallGraphEdge(
                                    source=caller_name_up,
                                    target=thru_name,
                                    edge_type=GraphEdgeType.PERFORM_THRU,
                                    label="THRU",
                                    line_number=stmt.location.start_line if stmt.location else None,
                                ))

                # 2B. GO TO Statements (Simple and GO TO DEPENDING ON)
                elif isinstance(stmt, GoToStatementNode):
                    goto_targets: List[str] = []
                    if stmt.target:
                        tgt = stmt.target.upper().strip()
                        if tgt in section_map:
                            goto_targets.append(section_map[tgt][0])
                        else:
                            goto_targets.append(tgt)
                    if stmt.depending_on:
                        before_dep = stmt.depending_on.upper().split("DEPENDING")[0]
                        for token in re.findall(r"[A-Za-z0-9_\-]+", before_dep):
                            token_up = token.strip().upper()
                            if token_up in section_map:
                                sec_tgt = section_map[token_up][0]
                                if sec_tgt not in goto_targets:
                                    goto_targets.append(sec_tgt)
                            elif token_up not in goto_targets:
                                goto_targets.append(token_up)

                    for target_raw in goto_targets:
                        target_name = exit_to_parent_map.get(target_raw, target_raw) if self.collapse_exits else target_raw
                        if target_name in nodes and caller_name_up != target_name:
                            target_node = nodes[target_name]
                            edge_type = GraphEdgeType.ERROR_BRANCH if is_error_trap(target_node) else GraphEdgeType.GO_TO
                            edge_key = (caller_name_up, target_name, edge_type)
                            if edge_key not in seen_edges:
                                seen_edges.add(edge_key)
                                edges.append(CallGraphEdge(
                                    source=caller_name_up,
                                    target=target_name,
                                    edge_type=edge_type,
                                    line_number=stmt.location.start_line if stmt.location else None,
                                ))

        # 2C. Validated Fallthrough Edges (Computed directly from Pushdown Reachability Fixed-Point)
        if not self.hide_fallthrough:
            for ft_pair in reachability_model.validated_fallthrough_edges:
                src_raw, tgt_raw = ft_pair[0], ft_pair[1]
                src = exit_to_parent_map.get(src_raw, src_raw) if self.collapse_exits else src_raw
                tgt = exit_to_parent_map.get(tgt_raw, tgt_raw) if self.collapse_exits else tgt_raw
                if src in nodes and tgt in nodes and src != tgt:
                    edge_key = (src, tgt, GraphEdgeType.FALLTHROUGH)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append(CallGraphEdge(
                            source=src,
                            target=tgt,
                            edge_type=GraphEdgeType.FALLTHROUGH,
                        ))

        # Determine Entry Point
        entry_point_name: Optional[str] = None
        reach_ep = getattr(reachability_model, "entrypoint", None) or getattr(reachability_model, "entry_point", None)
        if reach_ep and reach_ep.upper().strip() in nodes:
            entry_point_name = reach_ep.upper().strip()
        else:
            # First non-exit paragraph in execution sequence
            for p in para_list:
                p_up = p.name.upper().strip()
                if p_up in nodes and not nodes[p_up].is_exit_paragraph:
                    entry_point_name = p_up
                    break
            if not entry_point_name and nodes:
                entry_point_name = next(iter(nodes.keys()))

        if entry_point_name and entry_point_name in nodes:
            nodes[entry_point_name].is_entry_point = True
            if nodes[entry_point_name].node_type == GraphNodeType.GENERIC:
                nodes[entry_point_name].node_type = GraphNodeType.MAIN_DRIVER

        # Filter out empty clusters
        active_clusters = [c for c in cluster_map.values() if c.node_ids]

        # Calculate max depth and cycle detection
        max_depth, has_cycles = self._analyze_graph_topology(nodes, edges)

        return CallGraph(
            program_id=program_id,
            entry_point=entry_point_name,
            nodes=nodes,
            edges=edges,
            clusters=active_clusters,
            total_paragraphs=len(nodes),
            total_calls=len([e for e in edges if e.edge_type in (GraphEdgeType.PERFORM, GraphEdgeType.CALL, GraphEdgeType.GO_TO)]),
            max_depth=max_depth,
            has_cycles=has_cycles,
            reachability_transitions_count=len(reachability_model.state_transitions),
        )

    def _collect_all_statements(self, stmts: List[AnyStatementNode]) -> List[AnyStatementNode]:
        """Recursively collects all nested statements using the polymorphic walk_tree protocol."""
        collected: List[AnyStatementNode] = []
        for s in stmts:
            collected.extend(list(s.walk_tree()))
        return collected

    def _sanitize_id(self, name: str) -> str:
        """Sanitizes COBOL paragraph name into a valid Graphviz node ID."""
        clean = re.sub(r"[^A-Za-z0-9_]", "_", name.strip())
        return f"p_{clean}"

    def _analyze_graph_topology(self, nodes: Dict[str, CallGraphNode], edges: List[CallGraphEdge]) -> Tuple[int, bool]:
        """Calculates longest path depth and checks for cycles via DFS."""
        adj: Dict[str, List[str]] = {k: [] for k in nodes}
        in_degree: Dict[str, int] = {k: 0 for k in nodes}

        for e in edges:
            if e.edge_type in (GraphEdgeType.PERFORM, GraphEdgeType.CALL, GraphEdgeType.GO_TO):
                if e.source in adj and e.target in adj:
                    adj[e.source].append(e.target)
                    in_degree[e.target] += 1

        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        has_cycles = False

        def dfs_cycle(u: str) -> bool:
            visited.add(u)
            rec_stack.add(u)
            for v in adj.get(u, []):
                if v not in visited:
                    if dfs_cycle(v):
                        return True
                elif v in rec_stack:
                    return True
            rec_stack.remove(u)
            return False

        for n in nodes:
            if n not in visited:
                if dfs_cycle(n):
                    has_cycles = True
                    break

        memo: Dict[str, int] = {}

        def get_depth(u: str, path: Set[str]) -> int:
            if u in path:
                return 0
            if u in memo:
                return memo[u]
            d = 1
            path.add(u)
            for v in adj.get(u, []):
                d = max(d, 1 + get_depth(v, path))
            path.remove(u)
            memo[u] = d
            return d

        roots = [n for n, deg in in_degree.items() if deg == 0]
        if not roots:
            roots = list(nodes.keys())

        max_depth = max((get_depth(r, set()) for r in roots), default=0)
        return max_depth, has_cycles

    def to_dot(self) -> str:
        if self._dot_cache is None:
            self._dot_cache = render_dot(self.graph, enable_clustering=self.enable_clustering)
        return self._dot_cache

    def to_svg(self) -> str:
        if self._svg_cache is None:
            self._svg_cache = render_svg(self.to_dot())
        return self._svg_cache

    def to_html(self, svg_content: Optional[str] = None) -> str:
        if svg_content is None:
            svg_content = self.to_svg()
        return render_html(self.graph, self.to_dot(), svg_content)

    def to_json(self, indent: int = 2) -> str:
        return self.graph.model_dump_json(indent=indent)


def generate_call_graph(
    model: ProgramModel,
    format: str = "svg",
    hide_fallthrough: bool = True,
    collapse_exits: bool = True,
    enable_clustering: bool = True,
    output_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Convenience functional API to generate Level-2 Procedure Call Graphs
    in SVG, DOT, HTML, or JSON formats.
    """
    generator = CallGraphGenerator(
        model=model,
        hide_fallthrough=hide_fallthrough,
        collapse_exits=collapse_exits,
        enable_clustering=enable_clustering,
    )

    fmt = format.lower().strip()
    if fmt in ("svg", "image"):
        content = generator.to_svg()
    elif fmt in ("dot", "gv", "graphviz"):
        content = generator.to_dot()
    elif fmt in ("html", "htm"):
        content = generator.to_html()
    elif fmt in ("json", "ir"):
        content = generator.to_json()
    else:
        content = generator.to_svg()

    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")

    return content
