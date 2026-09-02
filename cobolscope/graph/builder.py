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
    ExitStatementNode,
    GobackStatementNode,
    StopStatementNode,
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
        proc_statements: Dict[str, List[AnyStatementNode]] = {}

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

        # 0. Execute Pushdown Reachability Analysis
        reachability_engine = PushdownReachabilityAnalyzer(self.model)
        reachability_model = reachability_engine.analyze()

        # 1. Determine whether program is Section-Structured or Paragraph-Structured
        is_section_based = len(self.model.sections) > 0 and any(len(s.paragraph_names) > 0 for s in self.model.sections)
        symbol_to_proc: Dict[str, str] = {}

        def is_exit_name(pname: str) -> bool:
            up = pname.upper().strip()
            return (
                up.endswith("-EXIT")
                or up.endswith("_EXIT")
                or up.endswith("-EX")
                or up.endswith("_EX")
                or up.endswith("999")
                or up.endswith("99")
                or up.endswith("9999")
            )

        if is_section_based:
            # === Section-Driven Procedures ===
            for s in self.model.sections:
                proc_key = s.name.upper().strip()
                all_stmts: List[AnyStatementNode] = []
                exit_paras: List[str] = []

                if s.statements:
                    all_stmts.extend(self._collect_all_statements(s.statements))

                for p_name in s.paragraph_names:
                    p_obj = self.model.get_paragraph(p_name)
                    if p_obj:
                        p_stmts = self._collect_all_statements(p_obj.statements)
                        all_stmts.extend(p_stmts)
                        if is_exit_name(p_name) or (len(p_stmts) == 1 and isinstance(p_stmts[0], (ExitStatementNode, GobackStatementNode))):
                            exit_paras.append(p_name)
                    elif is_exit_name(p_name):
                        exit_paras.append(p_name)

                proc_statements[proc_key] = all_stmts
                symbol_to_proc[proc_key] = proc_key
                for p_name in s.paragraph_names:
                    symbol_to_proc[p_name.upper().strip()] = proc_key

                # Statement metrics & Complexity
                stmt_count = len(all_stmts)
                cc = 1
                io_summary: Dict[str, int] = {"READ": 0, "WRITE": 0, "SQL": 0, "CALL": 0}
                src_fields: Set[str] = set()
                tgt_fields: Set[str] = set()
                has_terminal = False

                for stmt in all_stmts:
                    if isinstance(stmt, IfStatementNode):
                        cc += 1
                    elif isinstance(stmt, EvaluateStatementNode):
                        cc += len(stmt.when_branches)
                    elif isinstance(stmt, PerformStatementNode) and (stmt.until_condition or stmt.times_expr):
                        cc += 1

                    if isinstance(stmt, ReadStatementNode):
                        io_summary["READ"] += 1
                    elif isinstance(stmt, (WriteStatementNode, RewriteStatementNode)):
                        io_summary["WRITE"] += 1
                    elif isinstance(stmt, (ExecSqlStatementNode, ExecCicsStatementNode, ExecSqlImsStatementNode)):
                        io_summary["SQL"] += 1
                    elif isinstance(stmt, CallStatementNode):
                        io_summary["CALL"] += 1

                    if isinstance(stmt, (StopStatementNode, GobackStatementNode)):
                        has_terminal = True
                    elif isinstance(stmt, ExecCicsStatementNode) and "RETURN" in (stmt.raw_payload or "").upper():
                        has_terminal = True

                    for fid in getattr(stmt, "source_field_ids", None) or []:
                        src_fields.add(fid)
                    for fid in getattr(stmt, "target_field_ids", None) or []:
                        tgt_fields.add(fid)

                io_summary = {k: v for k, v in io_summary.items() if v > 0}

                # Classification
                node_type = ParagraphClassifier.classify_procedure(
                    name=s.name,
                    section=s.name,
                    statements=all_stmts,
                    is_terminal=has_terminal,
                )
                cluster_theme = CLUSTER_THEMES[node_type]
                cluster_id = cluster_theme["id"] if self.enable_clustering else "cluster_generic"

                start_line = s.location.start_line if s.location else 0
                end_line = s.location.end_line if s.location else 0

                node = CallGraphNode(
                    id=self._sanitize_id(s.name),
                    name=s.name,
                    section=s.name,
                    node_type=node_type,
                    cluster_id=cluster_id,
                    start_line=start_line,
                    end_line=end_line,
                    statement_count=stmt_count,
                    cyclomatic_complexity=cc,
                    is_terminal=has_terminal,
                    is_exit_paragraph=False,
                    is_unreachable=False,
                    io_summary=io_summary,
                    source_field_ids=sorted(list(src_fields)),
                    target_field_ids=sorted(list(tgt_fields)),
                    collapsed_exit_nodes=exit_paras,
                )
                nodes[proc_key] = node
                if cluster_id in cluster_map:
                    cluster_map[cluster_id].node_ids.append(node.id)

        else:
            # === Paragraph-Driven Procedures ===
            para_list = self.model.paragraphs
            exit_to_parent_map: Dict[str, str] = {}

            for i, p in enumerate(para_list):
                p_name_up = p.name.upper().strip()
                if (is_exit_name(p_name_up) or (len(p.statements) == 1 and isinstance(p.statements[0], ExitStatementNode))) and i > 0:
                    parent_candidate = para_list[i - 1].name.upper().strip()
                    exit_to_parent_map[p_name_up] = parent_candidate

            for i, p in enumerate(para_list):
                p_name_up = p.name.upper().strip()
                if self.collapse_exits and p_name_up in exit_to_parent_map:
                    parent_name = exit_to_parent_map[p_name_up]
                    if parent_name in nodes:
                        nodes[parent_name].collapsed_exit_nodes.append(p.name)
                    symbol_to_proc[p_name_up] = parent_name
                    continue

                all_stmts = self._collect_all_statements(p.statements)
                proc_statements[p_name_up] = all_stmts
                symbol_to_proc[p_name_up] = p_name_up

                stmt_count = len(all_stmts)
                cc = 1
                io_summary = {"READ": 0, "WRITE": 0, "SQL": 0, "CALL": 0}
                src_fields = set()
                tgt_fields = set()
                has_terminal = p.is_terminal

                for stmt in all_stmts:
                    if isinstance(stmt, IfStatementNode):
                        cc += 1
                    elif isinstance(stmt, EvaluateStatementNode):
                        cc += len(stmt.when_branches)
                    elif isinstance(stmt, PerformStatementNode) and (stmt.until_condition or stmt.times_expr):
                        cc += 1

                    if isinstance(stmt, ReadStatementNode):
                        io_summary["READ"] += 1
                    elif isinstance(stmt, (WriteStatementNode, RewriteStatementNode)):
                        io_summary["WRITE"] += 1
                    elif isinstance(stmt, (ExecSqlStatementNode, ExecCicsStatementNode, ExecSqlImsStatementNode)):
                        io_summary["SQL"] += 1
                    elif isinstance(stmt, CallStatementNode):
                        io_summary["CALL"] += 1

                    if isinstance(stmt, (StopStatementNode, GobackStatementNode)):
                        has_terminal = True
                    elif isinstance(stmt, ExecCicsStatementNode) and "RETURN" in (stmt.raw_payload or "").upper():
                        has_terminal = True

                    for fid in getattr(stmt, "source_field_ids", None) or []:
                        src_fields.add(fid)
                    for fid in getattr(stmt, "target_field_ids", None) or []:
                        tgt_fields.add(fid)

                io_summary = {k: v for k, v in io_summary.items() if v > 0}

                node_type = ParagraphClassifier.classify_procedure(
                    name=p.name,
                    section=p.section_parent,
                    statements=all_stmts,
                    is_terminal=has_terminal,
                )
                cluster_theme = CLUSTER_THEMES[node_type]
                cluster_id = cluster_theme["id"] if self.enable_clustering else "cluster_generic"

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
                    is_terminal=has_terminal,
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

        # 2. Second Pass: Extract Clean Invocation Edges (Single Edge per Call)
        seen_edges: Set[Tuple[str, str, GraphEdgeType]] = set()

        def is_error_trap(node_obj: CallGraphNode) -> bool:
            if node_obj.node_type == GraphNodeType.ERROR_HANDLING:
                return True
            n_up = node_obj.name.upper()
            return any(k in n_up for k in ("ABEND", "ERROR", "SYS-ERR", "FATAL", "TRAP", "EXCEPTION"))

        for src_proc_key, src_node in nodes.items():
            stmts = proc_statements.get(src_proc_key, [])
            for stmt in stmts:
                # 2A. PERFORM Statements
                if isinstance(stmt, PerformStatementNode) and stmt.target:
                    tgt_sym = stmt.target.upper().strip()
                    tgt_proc = symbol_to_proc.get(tgt_sym)

                    if tgt_proc and tgt_proc in nodes and tgt_proc != src_proc_key:
                        target_node = nodes[tgt_proc]
                        edge_type = GraphEdgeType.ERROR_BRANCH if is_error_trap(target_node) else GraphEdgeType.PERFORM
                        edge_key = (src_proc_key, tgt_proc, edge_type)

                        if edge_key not in seen_edges:
                            seen_edges.add(edge_key)
                            line_no = stmt.location.start_line if stmt.location else None
                            edges.append(CallGraphEdge(
                                source=src_proc_key,
                                target=tgt_proc,
                                edge_type=edge_type,
                                line_number=line_no,
                            ))
                            if tgt_proc not in src_node.successors:
                                src_node.successors.append(tgt_proc)
                            if src_proc_key not in target_node.called_by:
                                target_node.called_by.append(src_proc_key)

                # 2B. GO TO Statements (Inter-Procedure Only)
                elif isinstance(stmt, GoToStatementNode):
                    goto_targets: List[str] = []
                    if stmt.target:
                        goto_targets.append(stmt.target.upper().strip())
                    if stmt.depending_on:
                        before_dep = stmt.depending_on.upper().split("DEPENDING")[0]
                        for token in re.findall(r"[A-Za-z0-9_\-]+", before_dep):
                            goto_targets.append(token.strip().upper())

                    for raw_tgt in goto_targets:
                        tgt_proc = symbol_to_proc.get(raw_tgt)
                        if tgt_proc and tgt_proc in nodes and tgt_proc != src_proc_key:
                            target_node = nodes[tgt_proc]
                            edge_type = GraphEdgeType.ERROR_BRANCH if is_error_trap(target_node) else GraphEdgeType.GO_TO
                            edge_key = (src_proc_key, tgt_proc, edge_type)

                            if edge_key not in seen_edges:
                                seen_edges.add(edge_key)
                                line_no = stmt.location.start_line if stmt.location else None
                                edges.append(CallGraphEdge(
                                    source=src_proc_key,
                                    target=tgt_proc,
                                    edge_type=edge_type,
                                    line_number=line_no,
                                ))
                                if tgt_proc not in src_node.successors:
                                    src_node.successors.append(tgt_proc)
                                if src_proc_key not in target_node.called_by:
                                    target_node.called_by.append(src_proc_key)

                # 2C. CALL Statements (Dynamic/External Subprograms)
                elif isinstance(stmt, CallStatementNode):
                    call_tgt = getattr(stmt, "program", None) or getattr(stmt, "target", None)
                    if call_tgt:
                        tgt_raw = call_tgt.replace("'", "").replace('"', '').strip()
                        tgt_proc = symbol_to_proc.get(tgt_raw.upper())
                        if tgt_proc and tgt_proc in nodes and tgt_proc != src_proc_key:
                            edge_key = (src_proc_key, tgt_proc, GraphEdgeType.CALL)
                            if edge_key not in seen_edges:
                                seen_edges.add(edge_key)
                                edges.append(CallGraphEdge(
                                    source=src_proc_key,
                                    target=tgt_proc,
                                    edge_type=GraphEdgeType.CALL,
                                    line_number=stmt.location.start_line if stmt.location else None,
                                ))
                                target_node = nodes[tgt_proc]
                                if tgt_proc not in src_node.successors:
                                    src_node.successors.append(tgt_proc)
                                if src_proc_key not in target_node.called_by:
                                    target_node.called_by.append(src_proc_key)

        # 2D. Validated Fallthrough Edges
        if not self.hide_fallthrough:
            for ft_pair in reachability_model.validated_fallthrough_edges:
                src_raw, tgt_raw = ft_pair[0].upper().strip(), ft_pair[1].upper().strip()
                src_proc = symbol_to_proc.get(src_raw)
                tgt_proc = symbol_to_proc.get(tgt_raw)
                if src_proc and tgt_proc and src_proc in nodes and tgt_proc in nodes and src_proc != tgt_proc:
                    edge_key = (src_proc, tgt_proc, GraphEdgeType.FALLTHROUGH)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append(CallGraphEdge(
                            source=src_proc,
                            target=tgt_proc,
                            edge_type=GraphEdgeType.FALLTHROUGH,
                        ))

        # Determine Entry Point
        entry_point_name: Optional[str] = None
        reach_ep = getattr(reachability_model, "entrypoint", None) or getattr(reachability_model, "entry_point", None)
        if reach_ep:
            ep_proc = symbol_to_proc.get(reach_ep.upper().strip())
            if ep_proc and ep_proc in nodes:
                entry_point_name = ep_proc

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
