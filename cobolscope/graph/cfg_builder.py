"""
cobolscope.graph.cfg_builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compiler-grade Intra-Procedural Control Flow Graph (CFG) builder.
Constructs basic blocks, decision points, loop structures, and terminal flows.
Applies the noise-reduction readability heuristic to omit trivial linear routines.
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Any, Tuple, Set, Union

from cobolscope.models import (
    ParagraphNode,
    SectionNode,
    IfStatementNode,
    EvaluateStatementNode,
    SearchStatementNode,
    PerformStatementNode,
    GoToStatementNode,
    ExitStatementNode,
    ExecCicsStatementNode,
    StopStatementNode,
    GobackStatementNode,
    ReadStatementNode,
    WriteStatementNode,
    RewriteStatementNode,
    DeleteStatementNode,
    ComputeStatementNode,
    AddStatementNode,
    SubtractStatementNode,
    MultiplyStatementNode,
    DivideStatementNode,
    CallStatementNode,
    StringStatementNode,
    UnstringStatementNode,
    AnyStatementNode,
)
from .cfg_models import (
    IntraprocedureCfg,
    CfgNode,
    CfgEdge,
    CfgNodeType,
    CfgEdgeType,
    CfgStatementItem,
)
from .termination import TerminationClassifier
from cobolscope.rules import GlobalRules, EffectiveProgramRules


def format_statement_text(stmt: AnyStatementNode) -> str:
    """Extracts or reconstructs clean, readable text for a statement."""
    if stmt.raw_text and stmt.raw_text.strip():
        return stmt.raw_text.strip()
    verb = (stmt.type or "UNKNOWN").upper()
    target = getattr(stmt, "target", None) or getattr(stmt, "program", None) or ""
    if hasattr(stmt, "from_expr") and hasattr(stmt, "to_targets"):
        targets = ", ".join(stmt.to_targets) if stmt.to_targets else ""
        return f"MOVE {stmt.from_expr} TO {targets}".strip()
    elif hasattr(stmt, "expression") and getattr(stmt, "expression", None):
        targets = ", ".join(getattr(stmt, "targets", [])) if getattr(stmt, "targets", None) else ""
        if targets:
            return f"{verb} {getattr(stmt, 'expression', '')} GIVING {targets}".strip()
        return f"{verb} {getattr(stmt, 'expression', '')}".strip()
    elif target:
        return f"{verb} {target}".strip()
    return verb


def has_conditional_clauses(stmt: AnyStatementNode) -> bool:
    """Returns True if the statement carries nested conditional or exception clauses."""
    clause_attrs = (
        "at_end_statements",
        "not_at_end_statements",
        "invalid_key_statements",
        "not_invalid_key_statements",
        "on_size_error_statements",
        "not_on_size_error_statements",
        "end_of_page_statements",
        "not_end_of_page_statements",
        "on_exception_statements",
        "not_on_exception_statements",
        "on_overflow_statements",
        "not_on_overflow_statements",
    )
    for attr in clause_attrs:
        val = getattr(stmt, attr, None)
        if val and len(val) > 0:
            return True
    return False


def compute_cyclomatic_complexity(statements: List[AnyStatementNode]) -> int:
    """
    Computes McCabe Cyclomatic Complexity across all statements and nested clauses.
    CC = 1 + Decision Points
    """
    cc = 1
    all_stmts: List[AnyStatementNode] = []
    for s in statements:
        for sub in s.walk_tree():
            all_stmts.append(sub)

    for s in all_stmts:
        if isinstance(s, IfStatementNode):
            cc += 1
        elif isinstance(s, EvaluateStatementNode):
            cc += max(1, len(s.when_branches))
        elif isinstance(s, SearchStatementNode):
            cc += max(1, len(s.when_branches))
            if s.at_end_statements:
                cc += 1
        elif isinstance(s, PerformStatementNode) and (s.until_condition or s.times_expr or s.varying_expr):
            cc += 1
        elif isinstance(s, GoToStatementNode) and s.depending_on:
            before_dep = s.depending_on.upper().split("DEPENDING")[0]
            targets = re.findall(r"[A-Za-z0-9_\-]+", before_dep)
            cc += max(1, len(targets))
        else:
            if getattr(s, "on_size_error_statements", None):
                cc += 1
            if getattr(s, "invalid_key_statements", None):
                cc += 1
            if getattr(s, "at_end_statements", None) and not isinstance(s, SearchStatementNode):
                cc += 1
            if getattr(s, "end_of_page_statements", None):
                cc += 1
            if getattr(s, "on_exception_statements", None):
                cc += 1
            if getattr(s, "on_overflow_statements", None):
                cc += 1

    return cc


class IntraprocedureCfgBuilder:
    """
    Constructs a Level 3 Control Flow Graph (CFG) for an individual procedure routine or section.
    Groups consecutive linear statements into Basic Blocks and creates decision / merge
    structures for conditionals. Filters out trivial procedures to maximize readability.
    """

    def __init__(
        self,
        program_id: str,
        paragraph: Union[ParagraphNode, SectionNode],
        paragraphs_in_section: Optional[List[ParagraphNode]] = None,
        linear_statement_threshold: int = 2,
        classifier: Optional[TerminationClassifier] = None,
        terminal_procedure_names: Optional[Set[str]] = None,
        rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
    ):
        self.program_id = program_id
        self.paragraph = paragraph
        self.paragraphs_in_section = paragraphs_in_section
        self.linear_statement_threshold = linear_statement_threshold
        if classifier is not None:
            self.classifier = classifier
        else:
            self.classifier = TerminationClassifier(
                rules=rules,
                program_id=program_id,
                config_terminal_paras=terminal_procedure_names,
            )
        self._counter = 0
        self.nodes: Dict[str, CfgNode] = {}
        self.edges: List[CfgEdge] = []
        self._label_entry_map: Dict[str, str] = {}

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"{prefix}_{self._counter}"

    def build(self) -> IntraprocedureCfg:
        p = self.paragraph
        statements = p.statements

        # 1. Compute Cyclomatic Complexity & Structural Features
        cc = compute_cyclomatic_complexity(statements)
        stmt_count = len(statements)

        # 2. Noise-Reduction / Readability Eligibility Filter
        is_eligible = True
        eligibility_reason = ""

        if stmt_count == 0:
            is_eligible = False
            eligibility_reason = "Empty procedure (0 statements)."
        elif cc == 1:
            is_eligible = False
            eligibility_reason = (
                f"Linear routine with no conditional branches (CC: 1, {stmt_count} statements) - flowchart omitted."
            )

        start_line = p.location.start_line if p.location else 0
        end_line = p.location.end_line if p.location else 0

        sec_parent = getattr(p, "section_parent", None) or (p.name if isinstance(p, SectionNode) else None)
        cfg = IntraprocedureCfg(
            program_id=self.program_id,
            paragraph_name=p.name,
            section_name=sec_parent,
            cyclomatic_complexity=cc,
            statement_count=stmt_count,
            is_eligible=is_eligible,
            eligibility_reason=eligibility_reason,
        )

        if not is_eligible:
            return cfg

        # 3. Construct Complete CFG with Basic Blocks and Decision Nodes
        entry_node = CfgNode(
            id="entry",
            node_type=CfgNodeType.ENTRY,
            label=f"START: {p.name}",
            start_line=start_line,
            end_line=start_line,
        )
        self.nodes["entry"] = entry_node
        cfg.entry_node_id = "entry"

        # Active sources flowing into the next sequential statement:
        active_sources: List[Tuple[str, CfgEdgeType, Optional[str]]] = [
            ("entry", CfgEdgeType.FALLTHROUGH, None)
        ]

        if self.paragraphs_in_section:
            active_sources = self._build_section_paragraphs(self.paragraphs_in_section, active_sources)
        else:
            active_sources = self._build_statement_sequence(statements, active_sources)

        # Connect remaining active sources to EXIT node
        terminal_nodes: List[str] = [n.id for n in self.nodes.values() if n.is_terminal]
        if active_sources:
            exit_node = CfgNode(
                id="exit",
                node_type=CfgNodeType.EXIT,
                label=f"RETURN: {p.name}",
                start_line=end_line,
                end_line=end_line,
            )
            self.nodes["exit"] = exit_node
            for src_id, etype, elabel in active_sources:
                self.edges.append(CfgEdge(source=src_id, target="exit", edge_type=etype, label=elabel))
            cfg.exit_node_ids = ["exit"]
        else:
            cfg.exit_node_ids = terminal_nodes

        # Prune redundant 1:1 intermediate MERGE nodes
        self._prune_redundant_merges()

        cfg.nodes = self.nodes
        cfg.edges = self.edges
        return cfg

    def _build_section_paragraphs(
        self,
        paragraphs: List[ParagraphNode],
        initial_sources: List[Tuple[str, CfgEdgeType, Optional[str]]],
    ) -> List[Tuple[str, CfgEdgeType, Optional[str]]]:
        """
        Builds CFG across multiple paragraphs in a section, establishing paragraph
        entry points and allowing intra-section GO TO targets to resolve correctly.
        """
        current_sources = list(initial_sources)

        for i, para in enumerate(paragraphs):
            p_clean = para.name.upper().strip()
            p_start = para.location.start_line if para.location else 0
            p_end = para.location.end_line if para.location else 0

            para_entry_id = self._next_id("p_entry")
            para_entry_node = CfgNode(
                id=para_entry_id,
                node_type=CfgNodeType.BASIC_BLOCK,
                label=f"[{para.name}]",
                start_line=p_start,
                end_line=p_start,
            )
            self.nodes[para_entry_id] = para_entry_node
            self._label_entry_map[p_clean] = para_entry_id

            if current_sources:
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=para_entry_id, edge_type=etype, label=elabel))

            p_sources = [(para_entry_id, CfgEdgeType.FALLTHROUGH, None)]
            current_sources = self._build_statement_sequence(para.statements, p_sources)

        for nid, node in list(self.nodes.items()):
            if node.node_type == CfgNodeType.JUMP:
                lbl = node.label.replace("GO TO ", "").strip().upper()
                if lbl in self._label_entry_map:
                    dest_entry = self._label_entry_map[lbl]
                    self.edges.append(CfgEdge(
                        source=node.id,
                        target=dest_entry,
                        edge_type=CfgEdgeType.JUMP,
                        label=f"JUMP {lbl}",
                    ))

        return current_sources

    def _build_statement_sequence(
        self,
        stmts: List[AnyStatementNode],
        sources: List[Tuple[str, CfgEdgeType, Optional[str]]],
    ) -> List[Tuple[str, CfgEdgeType, Optional[str]]]:
        current_sources = list(sources)
        current_block: List[CfgStatementItem] = []

        def flush_block() -> None:
            nonlocal current_sources, current_block
            if not current_block:
                return
            b_start = current_block[0].start_line
            b_end = current_block[-1].end_line
            b_id = self._next_id("bb")
            node = CfgNode(
                id=b_id,
                node_type=CfgNodeType.BASIC_BLOCK,
                label=f"BLOCK ({len(current_block)} stmts)",
                statements=list(current_block),
                start_line=b_start,
                end_line=b_end,
            )
            self.nodes[b_id] = node
            if current_sources:
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=b_id, edge_type=etype, label=elabel))
                current_sources = [(b_id, CfgEdgeType.FALLTHROUGH, None)]
            current_block = []

        i = 0
        while i < len(stmts):
            stmt = stmts[i]

            # Dead code / unreachable check
            if not current_sources and not current_block:
                unreach_items: List[CfgStatementItem] = []
                while i < len(stmts):
                    u_s = stmts[i]
                    for sub in u_s.walk_tree():
                        u_start = sub.location.start_line if sub.location else 0
                        u_end = sub.location.end_line if sub.location else 0
                        unreach_items.append(CfgStatementItem(
                            type=sub.type,
                            start_line=u_start,
                            end_line=u_end,
                            text=format_statement_text(sub),
                            target_fields=getattr(sub, "target_field_ids", []) or [],
                            source_fields=getattr(sub, "source_field_ids", []) or [],
                        ))
                    i += 1

                if unreach_items:
                    u_id = self._next_id("unreach")
                    u_node = CfgNode(
                        id=u_id,
                        node_type=CfgNodeType.UNREACHABLE,
                        label=f"UNREACHABLE ({len(unreach_items)} stmts)",
                        statements=unreach_items,
                        start_line=unreach_items[0].start_line,
                        end_line=unreach_items[-1].end_line,
                    )
                    self.nodes[u_id] = u_node
                break

            s_start = stmt.location.start_line if stmt.location else 0
            s_end = stmt.location.end_line if stmt.location else 0
            raw_txt = format_statement_text(stmt)

            # --- 0. Deliberate S0C7 Hardware Crash Idiom (MOVE LOW-VALUES/SPACES + Arithmetic S0C7) ---
            if i + 1 < len(stmts) and self.classifier.is_s0c7_crash_sequence(stmts[i], stmts[i + 1]):
                flush_block()
                if not current_sources:
                    i += 2
                    continue
                s1 = stmts[i]
                s2 = stmts[i + 1]
                t_start = s1.location.start_line if s1.location else (s2.location.start_line if s2.location else 0)
                t_end = s2.location.end_line if s2.location else (s1.location.end_line if s1.location else 0)
                term_id = self._next_id("term")
                term_node = CfgNode(
                    id=term_id,
                    node_type=CfgNodeType.TERMINAL,
                    label="ABEND (S0C7 DATA-EXCEPTION)",
                    start_line=t_start,
                    end_line=t_end,
                    is_terminal=True,
                )
                self.nodes[term_id] = term_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=term_id, edge_type=etype, label=elabel))
                current_sources = []
                i += 2
                continue

            # --- 1. IF Statement ---
            if isinstance(stmt, IfStatementNode):
                flush_block()
                if not current_sources:
                    i += 1
                    continue
                dec_id = self._next_id("if")
                dec_node = CfgNode(
                    id=dec_id,
                    node_type=CfgNodeType.DECISION,
                    label="IF",
                    condition=stmt.condition or "condition",
                    start_line=s_start,
                    end_line=s_end,
                )
                self.nodes[dec_id] = dec_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=dec_id, edge_type=etype, label=elabel))

                # Then Branch
                then_sources = [(dec_id, CfgEdgeType.TRUE_BRANCH, "YES")]
                then_exits = self._build_statement_sequence(stmt.then_statements, then_sources)

                # Else Branch
                if stmt.else_statements:
                    else_sources = [(dec_id, CfgEdgeType.FALSE_BRANCH, "NO")]
                    else_exits = self._build_statement_sequence(stmt.else_statements, else_sources)
                else:
                    else_exits = [(dec_id, CfgEdgeType.FALSE_BRANCH, "NO")]

                converged_exits = then_exits + else_exits
                if len(converged_exits) > 1:
                    merge_id = self._next_id("merge")
                    merge_node = CfgNode(
                        id=merge_id,
                        node_type=CfgNodeType.MERGE,
                        label="MERGE",
                        start_line=s_end,
                        end_line=s_end,
                    )
                    self.nodes[merge_id] = merge_node
                    for src_id, etype, elabel in converged_exits:
                        self.edges.append(CfgEdge(source=src_id, target=merge_id, edge_type=etype, label=elabel))
                    current_sources = [(merge_id, CfgEdgeType.FALLTHROUGH, None)]
                elif len(converged_exits) == 1:
                    current_sources = list(converged_exits)
                else:
                    current_sources = []

            # --- 2. EVALUATE Statement ---
            elif isinstance(stmt, EvaluateStatementNode):
                flush_block()
                if not current_sources:
                    i += 1
                    continue
                dec_id = self._next_id("eval")
                subj_text = ", ".join(stmt.subjects) if stmt.subjects else "EVALUATE"
                dec_node = CfgNode(
                    id=dec_id,
                    node_type=CfgNodeType.DECISION,
                    label="EVALUATE",
                    condition=subj_text,
                    start_line=s_start,
                    end_line=s_end,
                )
                self.nodes[dec_id] = dec_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=dec_id, edge_type=etype, label=elabel))

                branch_exits: List[Tuple[str, CfgEdgeType, Optional[str]]] = []
                for b in stmt.when_branches:
                    cond_str = ", ".join(b.conditions) if b.conditions else "WHEN"
                    w_sources = [(dec_id, CfgEdgeType.WHEN_BRANCH, f"WHEN {cond_str}")]
                    w_exits = self._build_statement_sequence(b.statements, w_sources)
                    branch_exits.extend(w_exits)

                if stmt.when_other_statements:
                    o_sources = [(dec_id, CfgEdgeType.WHEN_OTHER, "OTHER")]
                    o_exits = self._build_statement_sequence(stmt.when_other_statements, o_sources)
                    branch_exits.extend(o_exits)
                else:
                    branch_exits.append((dec_id, CfgEdgeType.WHEN_OTHER, "OTHER"))

                if len(branch_exits) > 1:
                    merge_id = self._next_id("merge")
                    merge_node = CfgNode(
                        id=merge_id,
                        node_type=CfgNodeType.MERGE,
                        label="MERGE",
                        start_line=s_end,
                        end_line=s_end,
                    )
                    self.nodes[merge_id] = merge_node
                    for src_id, etype, elabel in branch_exits:
                        self.edges.append(CfgEdge(source=src_id, target=merge_id, edge_type=etype, label=elabel))
                    current_sources = [(merge_id, CfgEdgeType.FALLTHROUGH, None)]
                elif len(branch_exits) == 1:
                    current_sources = list(branch_exits)
                else:
                    current_sources = []

            # --- 3. SEARCH Statement ---
            elif isinstance(stmt, SearchStatementNode):
                flush_block()
                if not current_sources:
                    i += 1
                    continue
                dec_id = self._next_id("search")
                cond = stmt.expression or "SEARCH"
                dec_node = CfgNode(
                    id=dec_id,
                    node_type=CfgNodeType.DECISION,
                    label="SEARCH",
                    condition=cond,
                    start_line=s_start,
                    end_line=s_end,
                )
                self.nodes[dec_id] = dec_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=dec_id, edge_type=etype, label=elabel))

                search_exits: List[Tuple[str, CfgEdgeType, Optional[str]]] = []
                for b in stmt.when_branches:
                    w_cond = b.condition or "WHEN"
                    w_sources = [(dec_id, CfgEdgeType.WHEN_BRANCH, f"WHEN {w_cond}")]
                    w_exits = self._build_statement_sequence(b.statements, w_sources)
                    search_exits.extend(w_exits)

                if stmt.at_end_statements:
                    end_sources = [(dec_id, CfgEdgeType.EXCEPTION, "AT END")]
                    end_exits = self._build_statement_sequence(stmt.at_end_statements, end_sources)
                    search_exits.extend(end_exits)
                else:
                    search_exits.append((dec_id, CfgEdgeType.FALLTHROUGH, "NOT FOUND"))

                if len(search_exits) > 1:
                    merge_id = self._next_id("merge")
                    merge_node = CfgNode(
                        id=merge_id,
                        node_type=CfgNodeType.MERGE,
                        label="MERGE",
                        start_line=s_end,
                        end_line=s_end,
                    )
                    self.nodes[merge_id] = merge_node
                    for src_id, etype, elabel in search_exits:
                        self.edges.append(CfgEdge(source=src_id, target=merge_id, edge_type=etype, label=elabel))
                    current_sources = [(merge_id, CfgEdgeType.FALLTHROUGH, None)]
                elif len(search_exits) == 1:
                    current_sources = list(search_exits)
                else:
                    current_sources = []

            # --- 4. Statements with Conditional Exception / Status Clauses ---
            elif has_conditional_clauses(stmt):
                flush_block()
                if not current_sources:
                    i += 1
                    continue
                dec_id = self._next_id("clause")
                verb_label = (stmt.type or "OP").upper()
                cond_label = raw_txt[:35] + "..." if len(raw_txt) > 38 else raw_txt
                dec_node = CfgNode(
                    id=dec_id,
                    node_type=CfgNodeType.DECISION,
                    label=verb_label,
                    condition=cond_label,
                    start_line=s_start,
                    end_line=s_end,
                )
                self.nodes[dec_id] = dec_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=dec_id, edge_type=etype, label=elabel))

                clause_exits: List[Tuple[str, CfgEdgeType, Optional[str]]] = []

                # Normal continuation
                norm_stmts = (
                    getattr(stmt, "not_at_end_statements", [])
                    or getattr(stmt, "not_invalid_key_statements", [])
                    or getattr(stmt, "not_on_size_error_statements", [])
                    or getattr(stmt, "not_on_exception_statements", [])
                    or getattr(stmt, "not_on_overflow_statements", [])
                    or getattr(stmt, "not_end_of_page_statements", [])
                )
                if norm_stmts:
                    n_sources = [(dec_id, CfgEdgeType.FALLTHROUGH, "NORMAL")]
                    n_exits = self._build_statement_sequence(norm_stmts, n_sources)
                    clause_exits.extend(n_exits)
                else:
                    clause_exits.append((dec_id, CfgEdgeType.FALLTHROUGH, "NORMAL"))

                # Exception clauses
                clause_mappings = [
                    ("at_end_statements", "AT END"),
                    ("invalid_key_statements", "INVALID KEY"),
                    ("on_size_error_statements", "SIZE ERROR"),
                    ("on_exception_statements", "EXCEPTION"),
                    ("on_overflow_statements", "OVERFLOW"),
                    ("end_of_page_statements", "END-OF-PAGE"),
                ]
                for attr_name, branch_lbl in clause_mappings:
                    c_stmts = getattr(stmt, attr_name, [])
                    if c_stmts:
                        ex_sources = [(dec_id, CfgEdgeType.EXCEPTION, branch_lbl)]
                        ex_exits = self._build_statement_sequence(c_stmts, ex_sources)
                        clause_exits.extend(ex_exits)

                if len(clause_exits) > 1:
                    merge_id = self._next_id("merge")
                    merge_node = CfgNode(
                        id=merge_id,
                        node_type=CfgNodeType.MERGE,
                        label="MERGE",
                        start_line=s_end,
                        end_line=s_end,
                    )
                    self.nodes[merge_id] = merge_node
                    for src_id, etype, elabel in clause_exits:
                        self.edges.append(CfgEdge(source=src_id, target=merge_id, edge_type=etype, label=elabel))
                    current_sources = [(merge_id, CfgEdgeType.FALLTHROUGH, None)]
                elif len(clause_exits) == 1:
                    current_sources = list(clause_exits)
                else:
                    current_sources = []

            # --- 5. Terminal Statements (STOP RUN, GOBACK, EXIT PROGRAM, EXEC CICS ABEND, CALL ABEND, PERFORM ABEND) ---
            elif self.classifier.is_statement_terminal(stmt, raw_txt):
                flush_block()
                if not current_sources:
                    i += 1
                    continue
                term_id = self._next_id("term")
                term_lbl = self.classifier.get_terminal_label(stmt, raw_txt)
                term_node = CfgNode(
                    id=term_id,
                    node_type=CfgNodeType.TERMINAL,
                    label=term_lbl,
                    start_line=s_start,
                    end_line=s_end,
                    is_terminal=True,
                )
                self.nodes[term_id] = term_node
                for src_id, etype, elabel in current_sources:
                    self.edges.append(CfgEdge(source=src_id, target=term_id, edge_type=etype, label=elabel))
                current_sources = []

            # --- 6. PERFORM Statement ---
            elif isinstance(stmt, PerformStatementNode):
                has_loop = bool(stmt.until_condition or stmt.times_expr or stmt.varying_expr)
                if stmt.is_inline and has_loop:
                    flush_block()
                    if not current_sources:
                        i += 1
                        continue
                    loop_id = self._next_id("loop")
                    cond = stmt.until_condition or stmt.varying_expr or f"{stmt.times_expr} TIMES"
                    loop_node = CfgNode(
                        id=loop_id,
                        node_type=CfgNodeType.LOOP_HEADER,
                        label="PERFORM LOOP",
                        condition=cond,
                        start_line=s_start,
                        end_line=s_end,
                    )
                    self.nodes[loop_id] = loop_node
                    for src_id, etype, elabel in current_sources:
                        self.edges.append(CfgEdge(source=src_id, target=loop_id, edge_type=etype, label=elabel))

                    body_sources = [(loop_id, CfgEdgeType.LOOP_BODY, "ITERATE")]
                    body_exits = self._build_statement_sequence(stmt.nested_statements, body_sources)
                    for b_src, b_type, b_lbl in body_exits:
                        self.edges.append(CfgEdge(source=b_src, target=loop_id, edge_type=CfgEdgeType.FALLTHROUGH, label="LOOP BACK"))

                    current_sources = [(loop_id, CfgEdgeType.LOOP_EXIT, "EXIT LOOP")]

                elif stmt.is_inline and not has_loop:
                    current_sources = self._build_statement_sequence(stmt.nested_statements, current_sources)

                elif not stmt.is_inline and has_loop:
                    flush_block()
                    if not current_sources:
                        i += 1
                        continue
                    loop_id = self._next_id("loop")
                    cond = stmt.until_condition or stmt.varying_expr or f"{stmt.times_expr} TIMES"
                    loop_node = CfgNode(
                        id=loop_id,
                        node_type=CfgNodeType.LOOP_HEADER,
                        label=f"PERFORM {stmt.target or 'ROUTINE'}",
                        condition=cond,
                        start_line=s_start,
                        end_line=s_end,
                    )
                    self.nodes[loop_id] = loop_node
                    for src_id, etype, elabel in current_sources:
                        self.edges.append(CfgEdge(source=src_id, target=loop_id, edge_type=etype, label=elabel))

                    call_id = self._next_id("call")
                    call_node = CfgNode(
                        id=call_id,
                        node_type=CfgNodeType.CALL_SITE,
                        label=f"CALL {stmt.target or 'ROUTINE'}",
                        start_line=s_start,
                        end_line=s_end,
                    )
                    self.nodes[call_id] = call_node
                    self.edges.append(CfgEdge(source=loop_id, target=call_id, edge_type=CfgEdgeType.LOOP_BODY, label="ITERATE"))
                    self.edges.append(CfgEdge(source=call_id, target=loop_id, edge_type=CfgEdgeType.FALLTHROUGH, label="LOOP BACK"))

                    current_sources = [(loop_id, CfgEdgeType.LOOP_EXIT, "EXIT LOOP")]

                else:
                    item = CfgStatementItem(
                        type=stmt.type,
                        start_line=s_start,
                        end_line=s_end,
                        text=raw_txt,
                        target_fields=getattr(stmt, "target_field_ids", []) or [],
                        source_fields=getattr(stmt, "source_field_ids", []) or [],
                    )
                    current_block.append(item)

            # --- 6. GO TO Statement ---
            elif isinstance(stmt, GoToStatementNode):
                flush_block()
                if not current_sources:
                    i += 1
                    continue

                if stmt.depending_on:
                    before_dep = stmt.depending_on.upper().split("DEPENDING")[0]
                    targets = re.findall(r"[A-Za-z0-9_\-]+", before_dep)
                    dec_id = self._next_id("goto_dep")
                    dec_node = CfgNode(
                        id=dec_id,
                        node_type=CfgNodeType.DECISION,
                        label="GO TO DEPENDING",
                        condition=stmt.depending_on,
                        start_line=s_start,
                        end_line=s_end,
                    )
                    self.nodes[dec_id] = dec_node
                    for src_id, etype, elabel in current_sources:
                        self.edges.append(CfgEdge(source=src_id, target=dec_id, edge_type=etype, label=elabel))

                    for tgt in targets:
                        j_id = self._next_id("goto")
                        j_node = CfgNode(
                            id=j_id,
                            node_type=CfgNodeType.JUMP,
                            label=f"GO TO {tgt}",
                            start_line=s_start,
                            end_line=s_end,
                        )
                        self.nodes[j_id] = j_node
                        self.edges.append(CfgEdge(source=dec_id, target=j_id, edge_type=CfgEdgeType.JUMP, label=f"TO {tgt}"))

                    current_sources = [(dec_id, CfgEdgeType.FALLTHROUGH_DEFAULT, "FALLTHROUGH")]

                else:
                    jump_id = self._next_id("goto")
                    jump_node = CfgNode(
                        id=jump_id,
                        node_type=CfgNodeType.JUMP,
                        label=f"GO TO {stmt.target or 'UNKNOWN'}",
                        start_line=s_start,
                        end_line=s_end,
                    )
                    self.nodes[jump_id] = jump_node
                    for src_id, etype, elabel in current_sources:
                        self.edges.append(CfgEdge(source=src_id, target=jump_id, edge_type=etype, label=elabel))
                    current_sources = []

            # --- 8. Linear Statements (MOVE, ADD, COMPUTE, DISPLAY, CALL, etc.) ---
            else:
                item = CfgStatementItem(
                    type=stmt.type,
                    start_line=s_start,
                    end_line=s_end,
                    text=raw_txt,
                    target_fields=getattr(stmt, "target_field_ids", []) or [],
                    source_fields=getattr(stmt, "source_field_ids", []) or [],
                )
                current_block.append(item)

            i += 1

        flush_block()
        return current_sources

    def _prune_redundant_merges(self) -> None:
        """
        Prunes 1:1 pass-through MERGE nodes.
        If a MERGE node has exactly 1 incoming edge and 1 outgoing edge,
        bypasses it to declutter the graph. Iteratively resolves cascades
        and validates that all edge endpoints reference existing nodes.
        """
        while True:
            in_edges: Dict[str, List[CfgEdge]] = {nid: [] for nid in self.nodes}
            out_edges: Dict[str, List[CfgEdge]] = {nid: [] for nid in self.nodes}

            for e in self.edges:
                if e.target in in_edges:
                    in_edges[e.target].append(e)
                if e.source in out_edges:
                    out_edges[e.source].append(e)

            pruned_any = False
            for nid, node in list(self.nodes.items()):
                if node.node_type == CfgNodeType.MERGE:
                    in_e = in_edges.get(nid, [])
                    out_e = out_edges.get(nid, [])
                    if len(in_e) == 1 and len(out_e) == 1:
                        src_edge = in_e[0]
                        tgt_edge = out_e[0]
                        src_edge.target = tgt_edge.target
                        if not src_edge.label and tgt_edge.label:
                            src_edge.label = tgt_edge.label
                        if tgt_edge in self.edges:
                            self.edges.remove(tgt_edge)
                        del self.nodes[nid]
                        pruned_any = True
                        break

            if not pruned_any:
                break

        # Safety filter: ensure no edges point to or originate from pruned or non-existent nodes
        valid_node_ids = set(self.nodes.keys())
        self.edges = [
            e for e in self.edges
            if e.source in valid_node_ids and e.target in valid_node_ids
        ]


def build_procedure_cfg(
    program_id: str,
    paragraph: Union[ParagraphNode, SectionNode],
    paragraphs_in_section: Optional[List[ParagraphNode]] = None,
    linear_statement_threshold: int = 2,
    classifier: Optional[TerminationClassifier] = None,
    terminal_procedure_names: Optional[Set[str]] = None,
    rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
) -> IntraprocedureCfg:
    """Convenience helper to generate an IntraprocedureCfg for a paragraph or section."""
    builder = IntraprocedureCfgBuilder(
        program_id=program_id,
        paragraph=paragraph,
        paragraphs_in_section=paragraphs_in_section,
        linear_statement_threshold=linear_statement_threshold,
        classifier=classifier,
        terminal_procedure_names=terminal_procedure_names,
        rules=rules,
    )
    return builder.build()
