"""
tests.test_cfg
~~~~~~~~~~~~~~

Unit and integration tests for Level 3 Intra-Procedural Control Flow Graph (CFG) generation.
Verifies compiler basic blocks, decision points, loop headers, terminal nodes,
noise-reduction eligibility heuristics, and Cytoscape export.
"""

import json
import unittest
from cobolscope.models import (
    ParagraphNode,
    SectionNode,
    SourceLocation,
    MoveStatementNode,
    IfStatementNode,
    EvaluateStatementNode,
    EvaluateWhenBranch,
    SearchStatementNode,
    SearchWhenBranch,
    PerformStatementNode,
    GoToStatementNode,
    StopStatementNode,
    GobackStatementNode,
    ComputeStatementNode,
    ReadStatementNode,
    CallStatementNode,
    AddStatementNode,
    ProgramModel,
)
from cobolscope.graph.cfg_models import (
    IntraprocedureCfg,
    CfgNodeType,
    CfgEdgeType,
)
from cobolscope.graph.cfg_builder import (
    IntraprocedureCfgBuilder,
    build_procedure_cfg,
)
from tests.harness.test_cache import get_test_model


class TestIntraprocedureCfg(unittest.TestCase):
    """Verifies Level 3 CFG construction and eligibility rules."""

    def test_trivial_linear_paragraph_omitted(self):
        """
        Rule: If a paragraph has only <= 2 linear statements and zero branches (CC=1),
        do not generate a Level 3 diagram.
        """
        p = ParagraphNode(
            name="INIT-VARS",
            location=SourceLocation(start_line=10, end_line=12),
            statements=[
                MoveStatementNode(raw_text="MOVE ZERO TO WS-CTR", location=SourceLocation(start_line=11, end_line=11)),
                MoveStatementNode(raw_text="MOVE SPACES TO WS-BUF", location=SourceLocation(start_line=12, end_line=12)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p, linear_statement_threshold=2)

        self.assertEqual(cfg.cyclomatic_complexity, 1)
        self.assertEqual(cfg.statement_count, 2)
        self.assertFalse(cfg.is_eligible)
        self.assertIn("Linear routine with no conditional branches", cfg.eligibility_reason)
        self.assertEqual(len(cfg.nodes), 0)
        self.assertEqual(len(cfg.edges), 0)
        # Cytoscape elements should be empty when ineligible
        self.assertEqual(cfg.to_cytoscape_elements(), [])

    def test_single_statement_paragraph_omitted(self):
        """Return / exit paragraph with 1 linear statement is omitted."""
        p = ParagraphNode(
            name="A999-EXIT",
            location=SourceLocation(start_line=50, end_line=50),
            statements=[
                MoveStatementNode(raw_text="MOVE 'DONE' TO WS-STATUS", location=SourceLocation(start_line=50, end_line=50)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertFalse(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 1)

    def test_empty_paragraph_omitted(self):
        """Empty paragraph with 0 statements is omitted."""
        p = ParagraphNode(name="EMPTY-PARA", location=SourceLocation(start_line=1, end_line=1), statements=[])
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertFalse(cfg.is_eligible)
        self.assertIn("Empty procedure", cfg.eligibility_reason)

    def test_if_then_else_branching(self):
        """Paragraph with IF-THEN-ELSE generates decision node and true/false branches."""
        p = ParagraphNode(
            name="PROCESS-RECORD",
            location=SourceLocation(start_line=100, end_line=115),
            statements=[
                MoveStatementNode(raw_text="MOVE REC-IN TO REC-WORK", location=SourceLocation(start_line=101, end_line=101)),
                IfStatementNode(
                    condition="BALANCE > 0",
                    location=SourceLocation(start_line=102, end_line=108),
                    then_statements=[
                        ComputeStatementNode(raw_text="COMPUTE INTEREST = BALANCE * 0.05", location=SourceLocation(start_line=103, end_line=103)),
                    ],
                    else_statements=[
                        MoveStatementNode(raw_text="MOVE ZERO TO INTEREST", location=SourceLocation(start_line=105, end_line=105)),
                    ],
                ),
                MoveStatementNode(raw_text="MOVE INTEREST TO OUT-FIELD", location=SourceLocation(start_line=110, end_line=110)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)

        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)
        self.assertEqual(cfg.statement_count, 3)

        node_types = [n.node_type for n in cfg.nodes.values()]
        self.assertIn(CfgNodeType.ENTRY, node_types)
        self.assertIn(CfgNodeType.BASIC_BLOCK, node_types)
        self.assertIn(CfgNodeType.DECISION, node_types)
        self.assertIn(CfgNodeType.MERGE, node_types)
        self.assertIn(CfgNodeType.EXIT, node_types)

        # Check edge types
        edge_types = [e.edge_type for e in cfg.edges]
        self.assertIn(CfgEdgeType.TRUE_BRANCH, edge_types)
        self.assertIn(CfgEdgeType.FALSE_BRANCH, edge_types)
        self.assertIn(CfgEdgeType.FALLTHROUGH, edge_types)

        # Verify Cytoscape serialization
        cyto_elements = cfg.to_cytoscape_elements()
        self.assertEqual(len(cyto_elements), len(cfg.nodes) + len(cfg.edges))

        # Verify JSON model dump
        raw_json = cfg.model_dump_json()
        data = json.loads(raw_json)
        self.assertEqual(data["paragraph_name"], "PROCESS-RECORD")
        self.assertTrue(data["is_eligible"])

    def test_evaluate_when_branches(self):
        """Paragraph with EVALUATE generates multi-branch decision nodes."""
        p = ParagraphNode(
            name="EVAL-ROUTINE",
            location=SourceLocation(start_line=200, end_line=220),
            statements=[
                EvaluateStatementNode(
                    subjects=["TX-TYPE"],
                    location=SourceLocation(start_line=201, end_line=215),
                    when_branches=[
                        EvaluateWhenBranch(
                            conditions=["'D'"],
                            statements=[MoveStatementNode(raw_text="MOVE 1 TO D-FLAG", location=SourceLocation(start_line=203, end_line=203))],
                        ),
                        EvaluateWhenBranch(
                            conditions=["'W'"],
                            statements=[MoveStatementNode(raw_text="MOVE 1 TO W-FLAG", location=SourceLocation(start_line=205, end_line=205))],
                        ),
                    ],
                    when_other_statements=[
                        MoveStatementNode(raw_text="MOVE 1 TO ERR-FLAG", location=SourceLocation(start_line=208, end_line=208)),
                    ],
                ),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 3)

        edge_types = [e.edge_type for e in cfg.edges]
        self.assertIn(CfgEdgeType.WHEN_BRANCH, edge_types)
        self.assertIn(CfgEdgeType.WHEN_OTHER, edge_types)

    def test_inline_perform_until_loop(self):
        """Inline PERFORM with UNTIL condition generates LOOP_HEADER and back-edges."""
        p = ParagraphNode(
            name="LOOP-ROUTINE",
            location=SourceLocation(start_line=300, end_line=310),
            statements=[
                PerformStatementNode(
                    is_inline=True,
                    until_condition="IDX > 10",
                    location=SourceLocation(start_line=301, end_line=305),
                    nested_statements=[
                        ComputeStatementNode(raw_text="COMPUTE TOTAL = TOTAL + TABLE-VAL(IDX)", location=SourceLocation(start_line=302, end_line=302)),
                        ComputeStatementNode(raw_text="COMPUTE IDX = IDX + 1", location=SourceLocation(start_line=303, end_line=303)),
                    ],
                ),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)

        node_types = [n.node_type for n in cfg.nodes.values()]
        self.assertIn(CfgNodeType.LOOP_HEADER, node_types)

        edge_types = [e.edge_type for e in cfg.edges]
        self.assertIn(CfgEdgeType.LOOP_BODY, edge_types)
        self.assertIn(CfgEdgeType.LOOP_EXIT, edge_types)

    def test_terminal_verbs_suppress_fallthrough(self):
        """Conditional paragraph with GOBACK marks terminal without fallthrough to exit."""
        p = ParagraphNode(
            name="FATAL-EXIT",
            location=SourceLocation(start_line=400, end_line=405),
            statements=[
                IfStatementNode(
                    condition="ERR-FLAG = 'Y'",
                    then_statements=[
                        MoveStatementNode(raw_text="MOVE 'ERR' TO WS-MSG", location=SourceLocation(start_line=402, end_line=402))
                    ],
                    location=SourceLocation(start_line=401, end_line=403),
                ),
                GobackStatementNode(raw_text="GOBACK", location=SourceLocation(start_line=404, end_line=404)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)

        node_types = [n.node_type for n in cfg.nodes.values()]
        self.assertIn(CfgNodeType.TERMINAL, node_types)
        # Verify terminal node is in exit_node_ids
        term_nodes = [nid for nid, n in cfg.nodes.items() if n.is_terminal]
        self.assertEqual(cfg.exit_node_ids, term_nodes)

    def test_fixture_xfrfun_paragraphs(self):
        """Integration test on real fixture XFRFUN.cbl."""
        model = get_test_model("tests/fixtures/bank_of_z/cobol/XFRFUN.cbl")

        # PTD010 is 2 statements, linear CC=1 -> must be omitted
        ptd = model.get_paragraph("PTD010")
        self.assertIsNotNone(ptd)
        cfg_ptd = build_procedure_cfg(model.program_id, ptd)
        self.assertFalse(cfg_ptd.is_eligible)
        self.assertIn("Linear routine with no conditional branches", cfg_ptd.eligibility_reason)

        # UAD010 is complex branching -> must be eligible
        uad = model.get_paragraph("UAD010")
        self.assertIsNotNone(uad)
        cfg_uad = build_procedure_cfg(model.program_id, uad)
        self.assertTrue(cfg_uad.is_eligible)
        self.assertGreater(cfg_uad.cyclomatic_complexity, 5)
        self.assertGreater(len(cfg_uad.nodes), 20)
        self.assertGreater(len(cfg_uad.edges), 20)

    def test_search_statement_cfg(self):
        """SEARCH statement with WHEN branches and AT END generates decision branches and merge."""
        p = ParagraphNode(
            name="SEARCH-TABLE",
            location=SourceLocation(start_line=500, end_line=515),
            statements=[
                SearchStatementNode(
                    expression="WS-TABLE-ENTRY VARYING WS-IDX",
                    when_branches=[
                        SearchWhenBranch(
                            condition="TBL-KEY(WS-IDX) = WS-TARGET",
                            statements=[
                                MoveStatementNode(raw_text="MOVE TBL-VAL(WS-IDX) TO WS-FOUND-VAL", location=SourceLocation(start_line=503, end_line=503))
                            ],
                        ),
                        SearchWhenBranch(
                            condition="TBL-KEY(WS-IDX) > WS-TARGET",
                            statements=[
                                MoveStatementNode(raw_text="MOVE 'HIGH' TO WS-STATUS", location=SourceLocation(start_line=506, end_line=506))
                            ],
                        ),
                    ],
                    at_end_statements=[
                        MoveStatementNode(raw_text="MOVE 'NOT FOUND' TO WS-STATUS", location=SourceLocation(start_line=509, end_line=509))
                    ],
                    location=SourceLocation(start_line=501, end_line=510),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertGreaterEqual(cfg.cyclomatic_complexity, 3)

        dec_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.DECISION and n.label == "SEARCH"]
        self.assertEqual(len(dec_nodes), 1)

        when_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.WHEN_BRANCH]
        self.assertEqual(len(when_edges), 2)

        exception_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.EXCEPTION and e.label == "AT END"]
        self.assertEqual(len(exception_edges), 1)

        merge_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.MERGE]
        self.assertGreaterEqual(len(merge_nodes), 1)

    def test_read_at_end_branching(self):
        """READ statement with AT END and NOT AT END elevates to decision branching."""
        p = ParagraphNode(
            name="READ-FILE-RECORD",
            location=SourceLocation(start_line=600, end_line=615),
            statements=[
                ReadStatementNode(
                    target="INPUT-FILE",
                    at_end_statements=[
                        MoveStatementNode(raw_text="MOVE 'Y' TO WS-EOF", location=SourceLocation(start_line=603, end_line=603))
                    ],
                    not_at_end_statements=[
                        ComputeStatementNode(raw_text="COMPUTE WS-RECS = WS-RECS + 1", location=SourceLocation(start_line=606, end_line=606))
                    ],
                    location=SourceLocation(start_line=601, end_line=607),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)

        dec_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.DECISION]
        self.assertEqual(len(dec_nodes), 1)

        ex_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.EXCEPTION and e.label == "AT END"]
        self.assertEqual(len(ex_edges), 1)

        norm_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.FALLTHROUGH and e.label == "NORMAL"]
        self.assertEqual(len(norm_edges), 1)

    def test_compute_size_error_branching(self):
        """COMPUTE with ON SIZE ERROR elevates to decision branching."""
        p = ParagraphNode(
            name="CALC-TOTAL",
            location=SourceLocation(start_line=700, end_line=710),
            statements=[
                ComputeStatementNode(
                    raw_text="COMPUTE WS-TOTAL = WS-TOTAL * WS-FACTOR",
                    on_size_error_statements=[
                        MoveStatementNode(raw_text="MOVE 99999 TO WS-TOTAL", location=SourceLocation(start_line=703, end_line=703))
                    ],
                    location=SourceLocation(start_line=701, end_line=704),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)

        ex_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.EXCEPTION and e.label == "SIZE ERROR"]
        self.assertEqual(len(ex_edges), 1)

    def test_goto_depending_on_fallthrough(self):
        """GO TO ... DEPENDING ON preserves targets and fallthrough path."""
        p = ParagraphNode(
            name="DISPATCH-ACTION",
            location=SourceLocation(start_line=800, end_line=815),
            statements=[
                GoToStatementNode(
                    raw_text="GO TO PROC-ADD PROC-UPDATE PROC-DEL DEPENDING ON WS-ACTION",
                    depending_on="PROC-ADD PROC-UPDATE PROC-DEL DEPENDING ON WS-ACTION",
                    location=SourceLocation(start_line=801, end_line=802),
                ),
                MoveStatementNode(raw_text="MOVE 'INVALID' TO WS-STATUS", location=SourceLocation(start_line=804, end_line=804)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertGreaterEqual(cfg.cyclomatic_complexity, 4)

        jump_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.JUMP]
        self.assertEqual(len(jump_nodes), 3)

        default_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.FALLTHROUGH_DEFAULT]
        self.assertEqual(len(default_edges), 1)

    def test_out_of_line_perform_loop(self):
        """Out-of-line conditional PERFORM generates LOOP_HEADER and CALL_SITE."""
        p = ParagraphNode(
            name="CALL-LOOP",
            location=SourceLocation(start_line=900, end_line=910),
            statements=[
                PerformStatementNode(
                    target="PROCESS-LINE",
                    until_condition="WS-IDX > 100",
                    is_inline=False,
                    location=SourceLocation(start_line=901, end_line=902),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)

        loop_headers = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.LOOP_HEADER]
        self.assertEqual(len(loop_headers), 1)

        call_sites = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.CALL_SITE]
        self.assertEqual(len(call_sites), 1)

        body_edges = [e for e in cfg.edges if e.edge_type == CfgEdgeType.LOOP_BODY]
        self.assertEqual(len(body_edges), 1)

    def test_dead_code_unreachable_node(self):
        """Statements following GOBACK/STOP RUN are preserved in an UNREACHABLE node."""
        p = ParagraphNode(
            name="TERMINATE-EARLY",
            location=SourceLocation(start_line=1000, end_line=1015),
            statements=[
                IfStatementNode(
                    condition="ERR-CODE > 0",
                    then_statements=[
                        MoveStatementNode(raw_text="MOVE 'FATAL' TO WS-MSG", location=SourceLocation(start_line=1002, end_line=1002))
                    ],
                    location=SourceLocation(start_line=1001, end_line=1003),
                ),
                GobackStatementNode(raw_text="GOBACK", location=SourceLocation(start_line=1004, end_line=1004)),
                MoveStatementNode(raw_text="MOVE 'SHOULD-NOT-RUN' TO WS-DEAD", location=SourceLocation(start_line=1006, end_line=1006)),
                ComputeStatementNode(raw_text="COMPUTE WS-DEAD = 0", location=SourceLocation(start_line=1007, end_line=1007)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)

        unreach_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.UNREACHABLE]
        self.assertEqual(len(unreach_nodes), 1)
        self.assertEqual(len(unreach_nodes[0].statements), 2)
        self.assertEqual(unreach_nodes[0].statements[0].text, "MOVE 'SHOULD-NOT-RUN' TO WS-DEAD")

    def test_section_cfg_with_multiple_paragraphs(self):
        """Section CFG builds across multiple paragraphs, resolving intra-section jumps."""
        para1 = ParagraphNode(
            name="SEC-P1",
            section_parent="MAIN-SECTION",
            location=SourceLocation(start_line=1100, end_line=1108),
            statements=[
                IfStatementNode(
                    condition="WS-FLAG = 'Y'",
                    then_statements=[
                        GoToStatementNode(raw_text="GO TO SEC-P2", target="SEC-P2", location=SourceLocation(start_line=1102, end_line=1102))
                    ],
                    location=SourceLocation(start_line=1101, end_line=1103),
                ),
                MoveStatementNode(raw_text="MOVE 1 TO WS-VAL", location=SourceLocation(start_line=1105, end_line=1105)),
            ],
        )
        para2 = ParagraphNode(
            name="SEC-P2",
            section_parent="MAIN-SECTION",
            location=SourceLocation(start_line=1110, end_line=1115),
            statements=[
                MoveStatementNode(raw_text="MOVE 2 TO WS-VAL", location=SourceLocation(start_line=1111, end_line=1111)),
                GobackStatementNode(raw_text="GOBACK", location=SourceLocation(start_line=1112, end_line=1112)),
            ],
        )
        sec = SectionNode(
            name="MAIN-SECTION",
            paragraph_names=["SEC-P1", "SEC-P2"],
            statements=para1.statements + para2.statements,
            location=SourceLocation(start_line=1100, end_line=1115),
        )

        cfg = build_procedure_cfg(
            program_id="TESTPROG",
            paragraph=sec,
            paragraphs_in_section=[para1, para2],
        )
        self.assertTrue(cfg.is_eligible)

        # Paragraph boundary markers should exist
        para_labels = [n.label for n in cfg.nodes.values() if n.label in ("[SEC-P1]", "[SEC-P2]")]
        self.assertIn("[SEC-P1]", para_labels)
        self.assertIn("[SEC-P2]", para_labels)

        # Intra-section jump should link to SEC-P2
        jump_to_p2 = [e for e in cfg.edges if e.edge_type == CfgEdgeType.JUMP and "SEC-P2" in (e.label or "")]
        self.assertGreaterEqual(len(jump_to_p2), 1)


class TestCfgMathematicalInvariants(unittest.TestCase):
    """
    Automated verification of formal graph-theoretic invariants for Level 3 CFGs:
    1. Cyclomatic Complexity Conservation (McCabe's Invariant: M = E - N + 2P)
    2. Conservation of Flow (Zero Dangling Branch / Join Leakage)
    """

    def _assert_conservation_of_flow(self, cfg: IntraprocedureCfg, routine_name: str = ""):
        """
        Verifies Principle 2: Conservation of Flow:
        - Every split must either rejoin or explicitly terminate.
        - Decision Nodes (IF, EVALUATE, SEARCH, clauses): out_degree >= 2.
        - Join Nodes (MERGE): in_degree >= 2.
        - Terminal / Exit Nodes: in_degree >= 1, out_degree == 0 (for standard terminals).
        - Internal Nodes (BASIC_BLOCK, DECISION, LOOP_HEADER, CALL_SITE, MERGE):
            in_degree(v) >= 1 and out_degree(v) >= 1.
        """
        for nid, node in cfg.nodes.items():
            in_deg = sum(1 for e in cfg.edges if e.target == nid)
            out_deg = sum(1 for e in cfg.edges if e.source == nid)

            if node.node_type == CfgNodeType.ENTRY:
                self.assertEqual(in_deg, 0, f"[{routine_name}] ENTRY node '{nid}' must have in_degree == 0")
                self.assertGreaterEqual(out_deg, 1, f"[{routine_name}] ENTRY node '{nid}' must have out_degree >= 1")
            elif node.node_type == CfgNodeType.EXIT:
                self.assertGreaterEqual(in_deg, 1, f"[{routine_name}] EXIT node '{nid}' must have in_degree >= 1")
                self.assertEqual(out_deg, 0, f"[{routine_name}] EXIT node '{nid}' must have out_degree == 0")
            elif node.node_type == CfgNodeType.TERMINAL:
                self.assertGreaterEqual(in_deg, 1, f"[{routine_name}] TERMINAL node '{nid}' must have in_degree >= 1")
                self.assertEqual(out_deg, 0, f"[{routine_name}] TERMINAL node '{nid}' must have out_degree == 0")
            elif node.node_type == CfgNodeType.JUMP:
                # Unconditional JUMP transfers flow out (either to resolved intra-section entry or terminates procedure)
                self.assertGreaterEqual(in_deg, 1, f"[{routine_name}] JUMP node '{nid}' must have in_degree >= 1")
            elif node.node_type == CfgNodeType.UNREACHABLE:
                # Dead code sequence
                self.assertGreaterEqual(len(node.statements), 1, f"[{routine_name}] UNREACHABLE block '{nid}' must contain statements")
            else:
                # Internal nodes must satisfy: in_degree(v) >= 1 and out_degree(v) >= 1
                self.assertGreaterEqual(
                    in_deg, 1,
                    f"[{routine_name}] Internal node '{nid}' ({node.node_type}) violates in_degree >= 1 (got {in_deg})"
                )
                self.assertGreaterEqual(
                    out_deg, 1,
                    f"[{routine_name}] Internal node '{nid}' ({node.node_type}) violates out_degree >= 1 (got {out_deg})"
                )

                # Decision nodes must split flow: out_degree >= 2
                if node.node_type == CfgNodeType.DECISION:
                    self.assertGreaterEqual(
                        out_deg, 2,
                        f"[{routine_name}] Decision node '{nid}' violates out_degree >= 2 (got {out_deg})"
                    )

                # Join nodes must merge flow: in_degree >= 2
                if node.node_type == CfgNodeType.MERGE:
                    self.assertGreaterEqual(
                        in_deg, 2,
                        f"[{routine_name}] Join node '{nid}' violates in_degree >= 2 (got {in_deg})"
                    )

    def _assert_mccabe_invariant(self, cfg: IntraprocedureCfg, routine_name: str = ""):
        """
        Verifies Principle 1: McCabe's Invariant (M = E - N + 2P):
        For any structured, single-entry/single-exit graph without arbitrary jumps,
        the graph's Cyclomatic Complexity M = E - N + 2 must mathematically match cfg.cyclomatic_complexity.
        """
        E = len(cfg.edges)
        N = len(cfg.nodes)
        P = 1  # Single routine connected component
        M = E - N + 2 * P

        self.assertEqual(
            M, cfg.cyclomatic_complexity,
            f"[{routine_name}] McCabe's Invariant violated: E - N + 2P = {E} - {N} + {2*P} = {M} "
            f"!= AST Cyclomatic Complexity {cfg.cyclomatic_complexity}"
        )

    def test_structured_if_then_else_invariants(self):
        """Tests McCabe invariant and conservation of flow on structured IF-THEN-ELSE."""
        p = ParagraphNode(
            name="IF-THEN-ELSE-INVARIANT",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                MoveStatementNode(raw_text="MOVE 1 TO A", location=SourceLocation(start_line=2, end_line=2)),
                IfStatementNode(
                    condition="A > 0",
                    then_statements=[MoveStatementNode(raw_text="MOVE 2 TO B", location=SourceLocation(start_line=4, end_line=4))],
                    else_statements=[MoveStatementNode(raw_text="MOVE 3 TO B", location=SourceLocation(start_line=6, end_line=6))],
                    location=SourceLocation(start_line=3, end_line=7),
                ),
                MoveStatementNode(raw_text="MOVE B TO C", location=SourceLocation(start_line=8, end_line=8)),
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_structured_if_no_else_invariants(self):
        """Tests McCabe invariant and conservation of flow on IF without ELSE."""
        p = ParagraphNode(
            name="IF-NO-ELSE-INVARIANT",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                IfStatementNode(
                    condition="FLAG = 'Y'",
                    then_statements=[MoveStatementNode(raw_text="MOVE 1 TO VAL", location=SourceLocation(start_line=3, end_line=3))],
                    location=SourceLocation(start_line=2, end_line=4),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_nested_structured_conditionals_invariants(self):
        """Tests McCabe invariant and conservation of flow on nested IF structures."""
        p = ParagraphNode(
            name="NESTED-COND-INVARIANT",
            location=SourceLocation(start_line=1, end_line=20),
            statements=[
                IfStatementNode(
                    condition="LEVEL = 1",
                    then_statements=[
                        IfStatementNode(
                            condition="SUB-LEVEL = 'A'",
                            then_statements=[MoveStatementNode(raw_text="MOVE 10 TO BONUS", location=SourceLocation(start_line=4, end_line=4))],
                            else_statements=[MoveStatementNode(raw_text="MOVE 5 TO BONUS", location=SourceLocation(start_line=6, end_line=6))],
                            location=SourceLocation(start_line=3, end_line=7),
                        )
                    ],
                    else_statements=[MoveStatementNode(raw_text="MOVE 0 TO BONUS", location=SourceLocation(start_line=9, end_line=9))],
                    location=SourceLocation(start_line=2, end_line=10),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 3)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_multiway_evaluate_invariants(self):
        """Tests McCabe invariant and conservation of flow on multi-way EVALUATE."""
        p = ParagraphNode(
            name="EVALUATE-INVARIANT",
            location=SourceLocation(start_line=1, end_line=20),
            statements=[
                EvaluateStatementNode(
                    subjects=["TRAN-TYPE"],
                    when_branches=[
                        EvaluateWhenBranch(conditions=["'D'"], statements=[MoveStatementNode(raw_text="PERFORM DEPOSIT", location=SourceLocation(start_line=3, end_line=3))]),
                        EvaluateWhenBranch(conditions=["'W'"], statements=[MoveStatementNode(raw_text="PERFORM WITHDRAW", location=SourceLocation(start_line=5, end_line=5))]),
                        EvaluateWhenBranch(conditions=["'T'"], statements=[MoveStatementNode(raw_text="PERFORM TRANSFER", location=SourceLocation(start_line=7, end_line=7))]),
                    ],
                    when_other_statements=[MoveStatementNode(raw_text="PERFORM ERROR-LOG", location=SourceLocation(start_line=9, end_line=9))],
                    location=SourceLocation(start_line=2, end_line=10),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 4)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_inline_perform_loop_invariants(self):
        """Tests McCabe invariant and conservation of flow on inline PERFORM loop."""
        p = ParagraphNode(
            name="LOOP-INVARIANT",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                PerformStatementNode(
                    is_inline=True,
                    until_condition="WS-IDX > 100",
                    nested_statements=[
                        ComputeStatementNode(raw_text="COMPUTE WS-TOTAL = WS-TOTAL + WS-IDX", location=SourceLocation(start_line=3, end_line=3)),
                        ComputeStatementNode(raw_text="COMPUTE WS-IDX = WS-IDX + 1", location=SourceLocation(start_line=4, end_line=4)),
                    ],
                    location=SourceLocation(start_line=2, end_line=5),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_conditional_clause_read_invariants(self):
        """Tests McCabe invariant and conservation of flow on READ with AT END / NOT AT END."""
        p = ParagraphNode(
            name="READ-CLAUSE-INVARIANT",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                ReadStatementNode(
                    target="ACCT-FILE",
                    at_end_statements=[MoveStatementNode(raw_text="MOVE 'Y' TO WS-EOF", location=SourceLocation(start_line=3, end_line=3))],
                    not_at_end_statements=[MoveStatementNode(raw_text="ADD 1 TO WS-COUNT", location=SourceLocation(start_line=5, end_line=5))],
                    location=SourceLocation(start_line=2, end_line=6),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self.assertEqual(cfg.cyclomatic_complexity, 2)
        self._assert_mccabe_invariant(cfg, p.name)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_conservation_of_flow_with_terminal_branch(self):
        """Tests conservation of flow where one branch terminates explicitly (GOBACK)."""
        p = ParagraphNode(
            name="TERMINAL-BRANCH-INVARIANT",
            location=SourceLocation(start_line=1, end_line=10),
            statements=[
                IfStatementNode(
                    condition="FATAL-ERR = 'Y'",
                    then_statements=[GobackStatementNode(raw_text="GOBACK", location=SourceLocation(start_line=3, end_line=3))],
                    else_statements=[MoveStatementNode(raw_text="MOVE 'OK' TO WS-STATUS", location=SourceLocation(start_line=5, end_line=5))],
                    location=SourceLocation(start_line=2, end_line=6),
                )
            ],
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)
        self._assert_conservation_of_flow(cfg, p.name)

    def test_production_fixtures_conservation_of_flow(self):
        """
        Audits all eligible procedures across production fixtures (e.g. XFRFUN.cbl)
        for Conservation of Flow compliance.
        """
        model = get_test_model("tests/fixtures/bank_of_z/cobol/XFRFUN.cbl")
        eligible_count = 0

        for p in model.paragraphs:
            cfg = build_procedure_cfg(model.program_id, p)
            if not cfg.is_eligible:
                continue
            eligible_count += 1
            self._assert_conservation_of_flow(cfg, p.name)

        self.assertGreater(eligible_count, 0, "Must audit at least one eligible fixture paragraph")

    def test_cfg_with_s0c7_crash_sequence(self):
        """Validates that a deliberate S0C7 crash sequence inside a branch becomes an isolated TERMINAL node."""
        s1 = MoveStatementNode(
            type="MOVE", location=SourceLocation(start_line=3, end_line=3),
            raw_text="MOVE LOW-VALUES TO DATA-EXCEPTION",
            target_field_ids=["DATA-EXCEPTION"], source_field_ids=[],
            from_expr="LOW-VALUES", to_targets=["DATA-EXCEPTION"]
        )
        s2 = AddStatementNode(
            type="ADD", location=SourceLocation(start_line=4, end_line=4),
            raw_text="ADD 1 TO DATA-EXCEPTION-TRIGGER",
            target_field_ids=["DATA-EXCEPTION-TRIGGER"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO DATA-EXCEPTION-TRIGGER"
        )
        p = ParagraphNode(
            name="CHECK-AND-CRASH",
            location=SourceLocation(start_line=1, end_line=8),
            statements=[
                IfStatementNode(
                    condition="FATAL-ERROR = 'Y'",
                    then_statements=[s1, s2],
                    else_statements=[
                        MoveStatementNode(
                            type="MOVE", location=SourceLocation(start_line=6, end_line=6),
                            raw_text="MOVE 'OK' TO WS-STATUS",
                            from_expr="'OK'", to_targets=["WS-STATUS"]
                        )
                    ],
                    location=SourceLocation(start_line=2, end_line=7),
                )
            ]
        )
        cfg = build_procedure_cfg("TESTPROG", p)
        self.assertTrue(cfg.is_eligible)

        term_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.TERMINAL]
        self.assertEqual(len(term_nodes), 1)
        self.assertIn("S0C7", term_nodes[0].label)
        out_deg = sum(1 for e in cfg.edges if e.source == term_nodes[0].id)
        self.assertEqual(out_deg, 0)

        # Merge node is bypassed because only 1 branch survives
        merge_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.MERGE]
        self.assertEqual(len(merge_nodes), 0)

        self._assert_conservation_of_flow(cfg, p.name)

    def test_cfg_terminal_procedure_call_pruning(self):
        """
        Validates that PERFORM 999-ABEND is recognized as terminal when classifier is provided,
        and its branch does not falsely merge back into surviving code.
        """
        from cobolscope.graph.termination import TerminationClassifier

        s1_move = MoveStatementNode(
            type="MOVE", location=SourceLocation(start_line=20, end_line=20),
            raw_text="MOVE LOW-VALUES TO DATA-EXCEPTION",
            from_expr="LOW-VALUES", to_targets=["DATA-EXCEPTION"]
        )
        s2_add = AddStatementNode(
            type="ADD", location=SourceLocation(start_line=21, end_line=21),
            raw_text="ADD 1 TO DATA-EXCEPTION-TRIGGER",
            operation="ADD", expression="ADD 1 TO DATA-EXCEPTION-TRIGGER"
        )
        p_abend = ParagraphNode(
            name="999-ABEND", location=SourceLocation(start_line=19, end_line=22),
            statements=[s1_move, s2_add]
        )

        p_worker = ParagraphNode(
            name="CHECK-RECORD",
            location=SourceLocation(start_line=1, end_line=15),
            statements=[
                IfStatementNode(
                    condition="REC-NOT-FOUND = 'Y'",
                    then_statements=[
                        PerformStatementNode(
                            type="PERFORM", location=SourceLocation(start_line=3, end_line=3),
                            raw_text="PERFORM 999-ABEND", target="999-ABEND", is_inline=False
                        )
                    ],
                    else_statements=[
                        MoveStatementNode(
                            type="MOVE", location=SourceLocation(start_line=5, end_line=5),
                            raw_text="MOVE 'PROCESSED' TO WS-STATUS",
                            from_expr="'PROCESSED'", to_targets=["WS-STATUS"]
                        )
                    ],
                    location=SourceLocation(start_line=2, end_line=6),
                ),
                MoveStatementNode(
                    type="MOVE", location=SourceLocation(start_line=7, end_line=7),
                    raw_text="MOVE 'DONE' TO WS-RESULT",
                    from_expr="'DONE'", to_targets=["WS-RESULT"]
                )
            ]
        )

        dummy_prog = ProgramModel(
            program_id="TESTPROG",
            paragraphs=[p_abend, p_worker],
            sections=[],
            data_division_summary=None,
            source_file="TESTPROG.cbl"
        )
        classifier = TerminationClassifier.for_program(dummy_prog)
        self.assertIn("999-ABEND", classifier.terminal_paragraphs)

        cfg = build_procedure_cfg("TESTPROG", p_worker, classifier=classifier)
        self.assertTrue(cfg.is_eligible)

        # Confirm the PERFORM 999-ABEND node is TERMINAL with out_degree == 0
        term_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.TERMINAL]
        self.assertEqual(len(term_nodes), 1)
        self.assertIn("999-ABEND", term_nodes[0].label)
        out_deg = sum(1 for e in cfg.edges if e.source == term_nodes[0].id)
        self.assertEqual(out_deg, 0)

        # Confirm no redundant 1:1 merge node was created for the IF
        merge_nodes = [n for n in cfg.nodes.values() if n.node_type == CfgNodeType.MERGE]
        self.assertEqual(len(merge_nodes), 0, "Single surviving branch must bypass 1:1 merge node")

        self._assert_conservation_of_flow(cfg, p_worker.name)


if __name__ == "__main__":
    unittest.main()
