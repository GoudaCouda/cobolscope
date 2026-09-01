"""
cobolscope.reachability.analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interprocedural Pushdown Reachability Analysis Engine executing a LIFO worklist algorithm.
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Set, Tuple

from cobolscope.models import (
    AnyStatementNode,
    EvaluateStatementNode,
    ExitStatementNode,
    GoToStatementNode,
    GobackStatementNode,
    IfStatementNode,
    ParagraphNode,
    PerformStatementNode,
    ProgramModel,
    StopStatementNode,
)
from .models import (
    PerformFrame,
    ReachabilityModel,
    StateTransition,
    TransitionKind,
)


class PushdownReachabilityAnalyzer:
    """
    Interprocedural Pushdown System executing a LIFO worklist algorithm to evaluate
    reachable control states in COBOL Procedure Divisions.
    """

    def __init__(self, model: ProgramModel, max_stack_depth: int = 32, max_steps: int = 50000):
        self.model = model
        self.max_stack_depth = max_stack_depth
        self.max_steps = max_steps

        # Index paragraphs in physical lexical order
        self.paragraphs = model.paragraphs
        self.para_names = [p.name.upper().strip() for p in self.paragraphs]
        self.para_map: Dict[str, ParagraphNode] = {
            p.name.upper().strip(): p for p in self.paragraphs
        }
        self.para_indices: Dict[str, int] = {
            name: i for i, name in enumerate(self.para_names)
        }

        # Index sections and map section names to (first_para, last_para)
        self.section_map: Dict[str, Tuple[str, str]] = {}
        for sec in model.sections:
            if sec.paragraph_names:
                first_p = sec.paragraph_names[0].upper().strip()
                last_p = sec.paragraph_names[-1].upper().strip()
                self.section_map[sec.name.upper().strip()] = (first_p, last_p)

        # Build sequential statement representations
        self.para_stmts: Dict[str, List[AnyStatementNode]] = {
            p.name.upper().strip(): self._collect_statements(p.statements)
            for p in self.paragraphs
        }

    @staticmethod
    def _collect_statements(stmts: List[AnyStatementNode]) -> List[AnyStatementNode]:
        """Flattens top-level and branch statements for indexed execution steps."""
        result: List[AnyStatementNode] = []
        for s in stmts:
            result.append(s)
        return result

    def _discover_entrypoints(self) -> List[str]:
        """Identifies primary and secondary Procedure Division entrypoints."""
        if not self.para_names:
            return []

        primary = ""
        # 1. Prefer uncalled MAIN / MAINLINE / START paragraph if present
        for name in self.para_names:
            if any(k in name for k in ("MAINLINE", "MAIN-LINE", "MAIN-PROGRAM", "MAIN-DRIVER", "START")):
                primary = name
                break
        if not primary:
            for name in self.para_names:
                if name.startswith("000") or name.startswith("010") or name.startswith("100-"):
                    primary = name
                    break
        if not primary:
            primary = self.para_names[0]

        entrypoints = [primary]

        # 2. Secondary Entry Points: Check sections and paragraphs for ENTRY statements
        for sec in self.model.sections:
            has_entry_stmt = any(
                "ENTRY " in (getattr(s, "raw_text", "") or "").upper() or getattr(s, "type", "") == "ENTRY"
                for s in sec.statements
            )
            if has_entry_stmt and sec.paragraph_names:
                sec_ep = sec.paragraph_names[0].upper().strip()
                if sec_ep not in entrypoints and sec_ep in self.para_map:
                    entrypoints.append(sec_ep)

        for p in self.paragraphs:
            name_up = p.name.upper().strip()
            if "ALT-ENTRY" in name_up or name_up.startswith("ENTRY-"):
                if name_up not in entrypoints and name_up in self.para_map:
                    entrypoints.append(name_up)

        return entrypoints

    def _extract_goto_targets(self, stmt: GoToStatementNode) -> List[str]:
        """Extracts all target paragraphs from simple and GO TO DEPENDING ON statements."""
        targets: List[str] = []
        if stmt.target:
            tgt = stmt.target.upper().strip()
            if tgt in self.para_map:
                targets.append(tgt)
            elif tgt in self.section_map:
                targets.append(self.section_map[tgt][0])
        if stmt.depending_on:
            before_dep = stmt.depending_on.upper().split("DEPENDING")[0]
            tokens = re.findall(r"[A-Za-z0-9_\-]+", before_dep)
            for token in tokens:
                token_up = token.strip().upper()
                if token_up in self.para_map and token_up not in targets:
                    targets.append(token_up)
                elif token_up in self.section_map and self.section_map[token_up][0] not in targets:
                    targets.append(self.section_map[token_up][0])
        return targets

    def analyze(self) -> ReachabilityModel:
        """
        Executes the LIFO worklist pushdown reachability algorithm.
        Returns the proven ReachabilityModel.
        """
        entrypoints = self._discover_entrypoints()
        if not entrypoints:
            return ReachabilityModel(entrypoint="")

        primary_entry = entrypoints[0]

        # LIFO Worklist of Configurations: (para_name, stmt_idx, call_stack)
        worklist: List[Tuple[str, int, Tuple[PerformFrame, ...]]] = [
            (ep, 0, ()) for ep in entrypoints
        ]

        visited_configs: Set[Tuple[str, int, Tuple[str, ...]]] = set()

        reachable_paras: Set[str] = set(entrypoints)
        state_transitions: List[StateTransition] = []
        seen_transitions: Set[Tuple[str, int, TransitionKind, Optional[str], int, int]] = set()

        perform_edges: Set[Tuple[str, str]] = set()
        goto_edges: Set[Tuple[str, str]] = set()
        fallthrough_edges: Set[Tuple[str, str]] = set()
        return_points: Dict[str, Set[str]] = {}

        steps = 0

        while worklist and steps < self.max_steps:
            steps += 1
            curr_para, curr_stmt_idx, call_stack = worklist.pop()

            curr_para = curr_para.upper().strip()
            if curr_para not in self.para_map:
                continue

            reachable_paras.add(curr_para)
            stack_key = tuple(f.return_boundary for f in call_stack)
            config_key = (curr_para, curr_stmt_idx, stack_key)

            if config_key in visited_configs:
                continue
            visited_configs.add(config_key)

            stmts = self.para_stmts.get(curr_para, [])
            stack_summary = [f.summary() for f in call_stack]

            # Case 1: Reached End of Paragraph (Past last statement)
            if curr_stmt_idx >= len(stmts):
                if call_stack:
                    top_frame = call_stack[-1]
                    if top_frame.return_boundary == curr_para:
                        new_stack = call_stack[:-1]
                        ret_caller = top_frame.caller
                        ret_idx = top_frame.return_stmt_idx

                        trans = StateTransition(
                            source_paragraph=curr_para,
                            source_stmt_idx=curr_stmt_idx,
                            kind=TransitionKind.RETURN_PERFORM,
                            target_paragraph=ret_caller,
                            target_stmt_idx=ret_idx,
                            stack_depth=len(new_stack),
                            stack_summary=[f.summary() for f in new_stack],
                        )
                        trans_key = (curr_para, curr_stmt_idx, TransitionKind.RETURN_PERFORM, ret_caller, ret_idx, len(new_stack))
                        if trans_key not in seen_transitions:
                            seen_transitions.add(trans_key)
                            state_transitions.append(trans)

                        return_points.setdefault(curr_para, set()).add(ret_caller)
                        worklist.append((ret_caller, ret_idx, new_stack))
                        continue

                    else:
                        # Intra-PERFORM Range Fallthrough
                        curr_idx = self.para_indices.get(curr_para, -1)
                        if curr_idx != -1 and curr_idx + 1 < len(self.para_names):
                            next_para = self.para_names[curr_idx + 1]
                            trans = StateTransition(
                                source_paragraph=curr_para,
                                source_stmt_idx=curr_stmt_idx,
                                kind=TransitionKind.INTRA_FALLTHROUGH,
                                target_paragraph=next_para,
                                target_stmt_idx=0,
                                stack_depth=len(call_stack),
                                stack_summary=stack_summary,
                            )
                            trans_key = (curr_para, curr_stmt_idx, TransitionKind.INTRA_FALLTHROUGH, next_para, 0, len(call_stack))
                            if trans_key not in seen_transitions:
                                seen_transitions.add(trans_key)
                                state_transitions.append(trans)

                            fallthrough_edges.add((curr_para, next_para))
                            worklist.append((next_para, 0, call_stack))
                            continue

                else:
                    # Top-Level Sequential Fallthrough (Stack is Empty)
                    curr_para_node = self.para_map[curr_para]
                    if not curr_para_node.is_terminal:
                        curr_idx = self.para_indices.get(curr_para, -1)
                        if curr_idx != -1 and curr_idx + 1 < len(self.para_names):
                            next_para = self.para_names[curr_idx + 1]
                            trans = StateTransition(
                                source_paragraph=curr_para,
                                source_stmt_idx=curr_stmt_idx,
                                kind=TransitionKind.TOP_LEVEL_FALLTHROUGH,
                                target_paragraph=next_para,
                                target_stmt_idx=0,
                                stack_depth=0,
                                stack_summary=[],
                            )
                            trans_key = (curr_para, curr_stmt_idx, TransitionKind.TOP_LEVEL_FALLTHROUGH, next_para, 0, 0)
                            if trans_key not in seen_transitions:
                                seen_transitions.add(trans_key)
                                state_transitions.append(trans)

                            fallthrough_edges.add((curr_para, next_para))
                            worklist.append((next_para, 0, ()))
                            continue

                continue

            # Case 2: Statement Execution within Paragraph
            stmt = stmts[curr_stmt_idx]

            # 2A. Terminal Statements (STOP RUN / GOBACK)
            if isinstance(stmt, (StopStatementNode, GobackStatementNode)):
                trans = StateTransition(
                    source_paragraph=curr_para,
                    source_stmt_idx=curr_stmt_idx,
                    kind=TransitionKind.TERMINATE,
                    target_paragraph=None,
                    target_stmt_idx=0,
                    stack_depth=len(call_stack),
                    stack_summary=stack_summary,
                )
                trans_key = (curr_para, curr_stmt_idx, TransitionKind.TERMINATE, None, 0, len(call_stack))
                if trans_key not in seen_transitions:
                    seen_transitions.add(trans_key)
                    state_transitions.append(trans)
                continue

            # 2B. PERFORM Statements
            elif isinstance(stmt, PerformStatementNode) and stmt.target:
                tgt = stmt.target.upper().strip()
                thru = stmt.thru.upper().strip() if stmt.thru else None

                if tgt in self.section_map:
                    first_p, last_p = self.section_map[tgt]
                    tgt = first_p
                    thru = thru if thru else last_p

                return_boundary = thru if thru else tgt

                if tgt in self.para_map and len(call_stack) < self.max_stack_depth:
                    new_frame = PerformFrame(
                        caller=curr_para,
                        target=tgt,
                        thru=thru,
                        return_boundary=return_boundary,
                        return_stmt_idx=curr_stmt_idx + 1,
                    )
                    new_stack = call_stack + (new_frame,)
                    perform_edges.add((curr_para, tgt))
                    if thru and thru != tgt:
                        perform_edges.add((curr_para, thru))

                    trans = StateTransition(
                        source_paragraph=curr_para,
                        source_stmt_idx=curr_stmt_idx,
                        kind=TransitionKind.CALL_PERFORM,
                        target_paragraph=tgt,
                        target_stmt_idx=0,
                        stack_depth=len(new_stack),
                        stack_summary=[f.summary() for f in new_stack],
                    )
                    trans_key = (curr_para, curr_stmt_idx, TransitionKind.CALL_PERFORM, tgt, 0, len(new_stack))
                    if trans_key not in seen_transitions:
                        seen_transitions.add(trans_key)
                        state_transitions.append(trans)

                    worklist.append((tgt, 0, new_stack))

                    if stmt.until_condition or stmt.varying_expr:
                        worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                    continue

                else:
                    worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                    continue

            # 2C. GO TO Statements
            elif isinstance(stmt, GoToStatementNode):
                goto_targets = self._extract_goto_targets(stmt)
                if goto_targets:
                    for tgt in goto_targets:
                        goto_edges.add((curr_para, tgt))
                        trans = StateTransition(
                            source_paragraph=curr_para,
                            source_stmt_idx=curr_stmt_idx,
                            kind=TransitionKind.JUMP_GOTO,
                            target_paragraph=tgt,
                            target_stmt_idx=0,
                            stack_depth=len(call_stack),
                            stack_summary=stack_summary,
                        )
                        trans_key = (curr_para, curr_stmt_idx, TransitionKind.JUMP_GOTO, tgt, 0, len(call_stack))
                        if trans_key not in seen_transitions:
                            seen_transitions.add(trans_key)
                            state_transitions.append(trans)

                        worklist.append((tgt, 0, call_stack))

                    if stmt.depending_on:
                        worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                    continue

                else:
                    worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                    continue

            # 2D. Statements with Nested Branches / Clauses (IF, EVALUATE, READ, WRITE, SEARCH, etc.)
            nested = self._extract_nested_branches(stmt)
            if nested:
                for n_stmt in nested:
                    if isinstance(n_stmt, PerformStatementNode) and n_stmt.target:
                        n_tgt = n_stmt.target.upper().strip()
                        n_thru = n_stmt.thru.upper().strip() if n_stmt.thru else None
                        if n_tgt in self.section_map:
                            first_p, last_p = self.section_map[n_tgt]
                            n_tgt = first_p
                            n_thru = n_thru if n_thru else last_p
                        n_boundary = n_thru if n_thru else n_tgt
                        if n_tgt in self.para_map and len(call_stack) < self.max_stack_depth:
                            n_frame = PerformFrame(
                                caller=curr_para,
                                target=n_tgt,
                                thru=n_thru,
                                return_boundary=n_boundary,
                                return_stmt_idx=curr_stmt_idx + 1,
                            )
                            perform_edges.add((curr_para, n_tgt))
                            if n_thru and n_thru != n_tgt:
                                perform_edges.add((curr_para, n_thru))
                            trans = StateTransition(
                                source_paragraph=curr_para,
                                source_stmt_idx=curr_stmt_idx,
                                kind=TransitionKind.CALL_PERFORM,
                                target_paragraph=n_tgt,
                                target_stmt_idx=0,
                                stack_depth=len(call_stack) + 1,
                                stack_summary=[f.summary() for f in call_stack] + [n_frame.summary()],
                            )
                            trans_key = (curr_para, curr_stmt_idx, TransitionKind.CALL_PERFORM, n_tgt, 0, len(call_stack) + 1)
                            if trans_key not in seen_transitions:
                                seen_transitions.add(trans_key)
                                state_transitions.append(trans)
                            worklist.append((n_tgt, 0, call_stack + (n_frame,)))
                    elif isinstance(n_stmt, GoToStatementNode):
                        goto_targets = self._extract_goto_targets(n_stmt)
                        for n_tgt in goto_targets:
                            goto_edges.add((curr_para, n_tgt))
                            trans = StateTransition(
                                source_paragraph=curr_para,
                                source_stmt_idx=curr_stmt_idx,
                                kind=TransitionKind.JUMP_GOTO,
                                target_paragraph=n_tgt,
                                target_stmt_idx=0,
                                stack_depth=len(call_stack),
                                stack_summary=stack_summary,
                            )
                            trans_key = (curr_para, curr_stmt_idx, TransitionKind.JUMP_GOTO, n_tgt, 0, len(call_stack))
                            if trans_key not in seen_transitions:
                                seen_transitions.add(trans_key)
                                state_transitions.append(trans)
                            worklist.append((n_tgt, 0, call_stack))

                # Continue through the normal continuation path after the conditional
                worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                continue

            # 2E. Exit Statement
            elif isinstance(stmt, ExitStatementNode):
                worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                continue

            # 2F. Standard Sequential Statement
            else:
                worklist.append((curr_para, curr_stmt_idx + 1, call_stack))
                continue

        unreachable = [p for p in self.para_names if p not in reachable_paras]
        ret_map = {k: sorted(list(v)) for k, v in return_points.items()}

        return ReachabilityModel(
            entrypoint=primary_entry,
            reachable_paragraphs=sorted(list(reachable_paras)),
            unreachable_paragraphs=unreachable,
            state_transitions=state_transitions,
            validated_perform_edges=sorted([[src, tgt] for src, tgt in perform_edges]),
            validated_goto_edges=sorted([[src, tgt] for src, tgt in goto_edges]),
            validated_fallthrough_edges=sorted([[src, tgt] for src, tgt in fallthrough_edges]),
            perform_return_points=ret_map,
        )

    def _extract_nested_branches(self, stmt: AnyStatementNode) -> List[AnyStatementNode]:
        """Extracts nested PERFORM and GO TO statements inside any parent statement."""
        branches: List[AnyStatementNode] = []
        for child in stmt.walk_tree():
            if child is stmt:
                continue
            if isinstance(child, (PerformStatementNode, GoToStatementNode)):
                branches.append(child)
        return branches
