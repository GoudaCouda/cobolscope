"""
cobolscope.graph.builder
~~~~~~~~~~~~~~~~~~~~~~~~~

Core CallGraphGenerator constructing structured Level-2 Call Graphs from ProgramModels.
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

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
from .cfg_builder import build_procedure_cfg, IntraprocedureCfg
from .termination import TerminationClassifier
from cobolscope.rules import GlobalRules, EffectiveProgramRules
from .utils import tarjan_scc


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
        cluster_mode: str = "auto",
        compact_nodes: bool = True,
        concentrate: bool = True,
        splines: str = "spline",
        rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
    ):
        self.model = model
        self.rules = rules
        self.hide_fallthrough = hide_fallthrough
        self.collapse_exits = collapse_exits
        self.compact_nodes = compact_nodes
        self.concentrate = concentrate
        self.splines = splines
        self.cluster_mode = (cluster_mode or "auto").lower().strip()

        is_section_based = len(self.model.sections) > 0 and any(len(s.paragraph_names) > 0 for s in self.model.sections)
        if not enable_clustering or self.cluster_mode == "none":
            self.enable_clustering = False
        elif self.cluster_mode == "sections":
            self.enable_clustering = is_section_based
        elif self.cluster_mode == "semantic":
            self.enable_clustering = True
        else:  # "auto"
            self.enable_clustering = is_section_based

        self._dot_cache: Optional[str] = None
        self._svg_cache: Optional[str] = None
        self._cfg_cache: Dict[str, IntraprocedureCfg] = {}
        self.graph: CallGraph = self._build_graph()

    def _extract_linear_statement_item(self, stmt: AnyStatementNode) -> Dict[str, Any]:
        verb = (stmt.type or "STATEMENT").upper()
        raw = (stmt.raw_text or "").strip()
        target = getattr(stmt, "target", "") or ""
        line = stmt.location.start_line if stmt.location else 0
        if not raw:
            raw = f"{verb} {target}".strip()

        category = "other"
        classifier = getattr(self, "termination_classifier", None)
        if classifier and classifier.is_statement_terminal(stmt, raw):
            category = "terminal"
        elif verb in ("MOVE", "INITIALIZE", "SET", "INSPECT"):
            category = "data"
        elif verb in ("PERFORM", "CALL", "INVOKE", "GO TO", "GOTO"):
            if target and classifier and (
                target.upper().strip() in classifier.terminal_paragraphs
                or classifier.effective_rules.is_terminal_name(target)
            ):
                category = "terminal"
            else:
                category = "call"
        elif verb in ("READ", "WRITE", "REWRITE", "DELETE", "START", "OPEN", "CLOSE") or "SQL" in verb or "CICS" in verb:
            category = "io"
        elif verb in ("ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "COMPUTE"):
            category = "math"
        elif verb in ("GOBACK", "STOP", "EXIT"):
            category = "terminal"
        elif target and classifier and (
            target.upper().strip() in classifier.terminal_paragraphs
            or classifier.effective_rules.is_terminal_name(target)
        ):
            category = "terminal"

        return {
            "line": line,
            "verb": verb,
            "category": category,
            "text": raw,
            "target": target,
        }

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

        # 0. Initialize Multi-Layer Termination Classifier & Reachability
        self.termination_classifier = TerminationClassifier.for_program(self.model, rules=self.rules)
        reachability_engine = PushdownReachabilityAnalyzer(self.model, rules=self.rules)
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

                    if self.termination_classifier.is_statement_terminal(stmt):
                        has_terminal = True

                    for fid in getattr(stmt, "source_field_ids", None) or []:
                        src_fields.add(fid)
                    for fid in getattr(stmt, "target_field_ids", None) or []:
                        tgt_fields.add(fid)

                if self.termination_classifier.is_paragraph_terminal(s):
                    has_terminal = True

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

                # Compute Level 3 Intra-Procedural CFG metadata for Section
                pseudo_p = ParagraphNode(name=s.name, location=s.location, statements=all_stmts)
                paras_in_sec = [p_obj for pn in s.paragraph_names if (p_obj := self.model.get_paragraph(pn))]
                s_cfg = build_procedure_cfg(
                    self.model.program_id,
                    pseudo_p,
                    paragraphs_in_section=paras_in_sec if paras_in_sec else None,
                    classifier=self.termination_classifier,
                )
                self._cfg_cache[proc_key] = s_cfg
                s_cfg_elements = s_cfg.to_cytoscape_elements() if s_cfg.is_eligible else []
                s_linear_stmts = [self._extract_linear_statement_item(stm) for stm in all_stmts]

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
                    is_cfg_eligible=s_cfg.is_eligible,
                    cfg_eligibility_reason=s_cfg.eligibility_reason,
                    cfg_elements=s_cfg_elements,
                    cfg_linear_statements=s_linear_stmts,
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

                    if self.termination_classifier.is_statement_terminal(stmt):
                        has_terminal = True

                    for fid in getattr(stmt, "source_field_ids", None) or []:
                        src_fields.add(fid)
                    for fid in getattr(stmt, "target_field_ids", None) or []:
                        tgt_fields.add(fid)

                if self.termination_classifier.is_paragraph_terminal(p):
                    has_terminal = True

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

                # Compute Level 3 Intra-Procedural CFG metadata
                p_cfg = build_procedure_cfg(
                    self.model.program_id,
                    p,
                    classifier=self.termination_classifier,
                )
                self._cfg_cache[p_name_up] = p_cfg
                is_cfg_eligible = p_cfg.is_eligible
                cfg_eligibility_reason = p_cfg.eligibility_reason
                cfg_elements = p_cfg.to_cytoscape_elements() if p_cfg.is_eligible else []
                cfg_linear_stmts = [self._extract_linear_statement_item(s) for s in p.statements]

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
                    is_cfg_eligible=is_cfg_eligible,
                    cfg_eligibility_reason=cfg_eligibility_reason,
                    cfg_elements=cfg_elements,
                    cfg_linear_statements=cfg_linear_stmts,
                )
                nodes[p_name_up] = node
                if cluster_id in cluster_map:
                    cluster_map[cluster_id].node_ids.append(node.id)

        # 2. Second Pass: Extract Clean Invocation Edges (Single Edge per Call)
        seen_edges: Set[Tuple[str, str, GraphEdgeType]] = set()

        def is_error_trap(node_obj: CallGraphNode) -> bool:
            if node_obj.node_type == GraphNodeType.ERROR_HANDLING:
                return True
            n_clean = node_obj.name.upper().strip()
            if getattr(self, "termination_classifier", None):
                if (
                    node_obj.is_terminal
                    or n_clean in self.termination_classifier.terminal_paragraphs
                    or self.termination_classifier.effective_rules.is_terminal_name(n_clean)
                ):
                    return True
            return any(k in n_clean for k in ("ABEND", "ERROR", "SYS-ERR", "FATAL", "TRAP", "EXCEPTION"))

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
            ep_node = nodes[entry_point_name]
            ep_node.is_entry_point = True
            old_cluster_id = ep_node.cluster_id
            ep_node.node_type = GraphNodeType.MAIN_DRIVER
            if self.enable_clustering:
                new_cluster_id = CLUSTER_THEMES[GraphNodeType.MAIN_DRIVER]["id"]
                ep_node.cluster_id = new_cluster_id
                if old_cluster_id in cluster_map and ep_node.id in cluster_map[old_cluster_id].node_ids:
                    cluster_map[old_cluster_id].node_ids.remove(ep_node.id)
                if new_cluster_id in cluster_map and ep_node.id not in cluster_map[new_cluster_id].node_ids:
                    cluster_map[new_cluster_id].node_ids.append(ep_node.id)

        # Filter out empty clusters
        active_clusters = [c for c in cluster_map.values() if c.node_ids]

        # Calculate max depth, cycles, and SCCs via Tarjan's algorithm
        max_depth, has_cycles, cycles, sccs = self._analyze_graph_topology(nodes, edges)

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
            cycles=cycles,
            sccs=sccs,
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

    def _analyze_graph_topology(
        self, nodes: Dict[str, CallGraphNode], edges: List[CallGraphEdge]
    ) -> Tuple[int, bool, List[List[str]], List[List[str]]]:
        """Calculates longest path depth, cycles, and SCCs using Tarjan's algorithm."""
        adj: Dict[str, List[str]] = {k: [] for k in nodes}

        for e in edges:
            if e.edge_type in (GraphEdgeType.PERFORM, GraphEdgeType.CALL, GraphEdgeType.GO_TO):
                if e.source in adj and e.target in adj:
                    adj[e.source].append(e.target)

        scc_res = tarjan_scc(nodes.keys(), lambda u: adj.get(u, []))
        return scc_res.max_depth, scc_res.has_cycles, scc_res.cycles, scc_res.sccs

    def to_dot(
        self,
        compact_nodes: Optional[bool] = None,
        concentrate: Optional[bool] = None,
        splines: Optional[str] = None,
    ) -> str:
        if self._dot_cache is None:
            c_nodes = self.compact_nodes if compact_nodes is None else compact_nodes
            conc = self.concentrate if concentrate is None else concentrate
            spl = self.splines if splines is None else splines
            self._dot_cache = render_dot(
                self.graph,
                enable_clustering=self.enable_clustering,
                compact_nodes=c_nodes,
                concentrate=conc,
                splines=spl,
            )
        return self._dot_cache

    def to_svg(
        self,
        compact_nodes: Optional[bool] = None,
        concentrate: Optional[bool] = None,
        splines: Optional[str] = None,
    ) -> str:
        if self._svg_cache is None:
            self._svg_cache = render_svg(self.to_dot(compact_nodes=compact_nodes, concentrate=concentrate, splines=splines))
        return self._svg_cache

    def get_procedure_cfg(self, proc_name: str) -> Optional[IntraprocedureCfg]:
        """
        Builds and returns the Level 3 Intra-Procedural CFG for the specified procedure.
        Uses cached CFGs computed during graph build whenever available.
        """
        name_up = proc_name.upper().strip()
        if name_up in self._cfg_cache:
            return self._cfg_cache[name_up]

        term_clf = getattr(self, "termination_classifier", None)
        para = self.model.get_paragraph(proc_name)
        if para:
            cfg = build_procedure_cfg(self.graph.program_id, para, classifier=term_clf)
            self._cfg_cache[name_up] = cfg
            return cfg

        for s in self.model.sections:
            if s.name.upper().strip() == name_up:
                pseudo_p = ParagraphNode(
                    name=s.name,
                    location=s.location,
                    statements=s.statements,
                )
                paras_in_sec = [p_obj for pn in s.paragraph_names if (p_obj := self.model.get_paragraph(pn))]
                cfg = build_procedure_cfg(
                    self.graph.program_id,
                    pseudo_p,
                    paragraphs_in_section=paras_in_sec if paras_in_sec else None,
                    classifier=term_clf,
                )
                self._cfg_cache[name_up] = cfg
                return cfg
        return None

    def to_cytoscape_elements(self) -> List[Dict[str, Any]]:
        """
        Converts the CallGraph into a list of Cytoscape.js elements (compound parent
        clusters, routine nodes, and directed control transfer edges).
        """
        elements: List[Dict[str, Any]] = []

        # 1. Emit Parent Compound Cluster Nodes
        if self.enable_clustering:
            for cluster in self.graph.clusters:
                if not cluster.node_ids:
                    continue
                elements.append({
                    "data": {
                        "id": cluster.id,
                        "label": cluster.name,
                        "name": cluster.name,
                        "color": cluster.color,
                        "fill_color": cluster.fill_color,
                        "text_color": cluster.text_color,
                        "is_cluster": True,
                    },
                    "classes": "cluster-node",
                })

        # 2. Emit Child Routine Nodes
        for node_name, node in self.graph.nodes.items():
            theme = CLUSTER_THEMES.get(node.node_type, CLUSTER_THEMES[GraphNodeType.GENERIC])
            
            # Format I/O badge summary
            io_parts = []
            if node.statement_count > 0:
                for k in ("READ", "WRITE", "REWRITE", "DELETE", "SQL", "CICS", "CALL"):
                    c = node.io_summary.get(k, 0)
                    if c > 0:
                        io_parts.append(f"{k}:{c}")
            if node.is_terminal:
                io_parts.append("TERMINAL")
            io_str = " | ".join(io_parts)

            parent_id = node.cluster_id if (self.enable_clustering and node.cluster_id) else None
            # Validate parent actually exists in active clusters
            if parent_id and not any(c.id == parent_id for c in self.graph.clusters):
                parent_id = None

            node_data = {
                "id": node.id,
                "label": node.name,
                "name": node.name,
                "section": node.section or "",
                "node_type": node.node_type.value,
                "type_label": theme["name"].split(" ")[0].upper() if theme and "name" in theme else node.node_type.value,
                "cluster_name": theme["name"] if theme and "name" in theme else "",
                "cluster_id": node.cluster_id,
                "start_line": node.start_line,
                "end_line": node.end_line,
                "lines": f"L{node.start_line}-{node.end_line}",
                "statement_count": node.statement_count,
                "cyclomatic_complexity": node.cyclomatic_complexity,
                "is_entry_point": node.is_entry_point,
                "is_terminal": node.is_terminal,
                "color": theme["color"],
                "fill_color": theme["fill_color"],
                "text_color": theme["text_color"],
                "io_badge": io_str,
                "source_field_ids": node.source_field_ids,
                "target_field_ids": node.target_field_ids,
                "called_by": node.called_by,
                "successors": node.successors,
            }

            # Attach Level 3 Intra-Procedural CFG and Readability Heuristic Metadata
            node_data["is_cfg_eligible"] = node.is_cfg_eligible
            node_data["cfg_eligibility_reason"] = node.cfg_eligibility_reason
            node_data["cfg_elements"] = node.cfg_elements
            node_data["cfg_linear_statements"] = node.cfg_linear_statements

            if parent_id:
                node_data["parent"] = parent_id

            node_classes = ["routine-node", f"type-{node.node_type.value.lower()}"]
            if node.is_entry_point:
                node_classes.append("entry-point")
            if node.is_terminal:
                node_classes.append("terminal-node")

            elements.append({
                "data": node_data,
                "classes": " ".join(node_classes),
            })

        # 3. Emit Directed Control Edges
        for edge in self.graph.edges:
            src_node = self.graph.nodes.get(edge.source)
            tgt_node = self.graph.nodes.get(edge.target)
            if not src_node or not tgt_node:
                continue

            edge_data = {
                "id": f"{src_node.id}->{tgt_node.id}::{edge.edge_type.value}",
                "source": src_node.id,
                "target": tgt_node.id,
                "edge_type": edge.edge_type.value,
                "label": edge.label or "",
                "line_number": edge.line_number,
                "is_error": edge.edge_type == GraphEdgeType.ERROR_BRANCH,
            }

            edge_classes = ["call-edge", f"edge-{edge.edge_type.value.lower()}"]
            if edge.edge_type == GraphEdgeType.ERROR_BRANCH:
                edge_classes.append("error-branch")

            elements.append({
                "data": edge_data,
                "classes": " ".join(edge_classes),
            })

        return elements

    def to_cytoscape_json(self, indent: int = 2) -> str:
        """Returns the Cytoscape.js elements serialized as a JSON string."""
        import json
        return json.dumps(self.to_cytoscape_elements(), indent=indent)

    def to_html(
        self,
        svg_content: Optional[str] = None,
        initial_engine: str = "cytoscape",
    ) -> str:
        cyto_elements = self.to_cytoscape_elements()
        return render_html(
            self.graph,
            dot_code=self._dot_cache if self._dot_cache is not None else "",
            svg_content=svg_content or self._svg_cache or "",
            cyto_elements=cyto_elements,
            initial_engine=initial_engine,
        )

    def to_json(self, indent: int = 2) -> str:
        return self.graph.model_dump_json(indent=indent)


def generate_call_graph(
    model: ProgramModel,
    format: str = "html",
    hide_fallthrough: bool = True,
    collapse_exits: bool = True,
    enable_clustering: bool = True,
    cluster_mode: str = "auto",
    compact_nodes: bool = True,
    concentrate: bool = True,
    splines: str = "spline",
    initial_engine: str = "cytoscape",
    rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Convenience functional API to generate Level-2 Procedure Call Graphs
    in HTML (default Cytoscape), SVG, DOT, Cytoscape JSON, or JSON formats.
    """
    generator = CallGraphGenerator(
        model=model,
        hide_fallthrough=hide_fallthrough,
        collapse_exits=collapse_exits,
        enable_clustering=enable_clustering,
        cluster_mode=cluster_mode,
        compact_nodes=compact_nodes,
        concentrate=concentrate,
        splines=splines,
        rules=rules,
    )

    fmt = format.lower().strip()
    if fmt in ("html", "htm"):
        content = generator.to_html(initial_engine=initial_engine)
    elif fmt in ("cytoscape", "cyto"):
        content = generator.to_cytoscape_json()
    elif fmt in ("svg", "image"):
        content = generator.to_svg()
    elif fmt in ("dot", "gv", "graphviz"):
        content = generator.to_dot()
    elif fmt in ("json", "ir"):
        content = generator.to_json()
    else:
        content = generator.to_html(initial_engine=initial_engine)

    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")

    return content
