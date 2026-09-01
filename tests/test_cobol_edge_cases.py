"""
Comprehensive Test Runner for Legacy COBOL Control-Flow and Structural Edge Cases.
Evaluates the current parsing and graph logic against:
1. Section Header Shadow Fall-Throughs
2. Post-Terminal Linear Shadow Blocks
3. Infinite Jump Traps & Forward Bypasses
4. Dynamic Jump Tables (GO TO DEPENDING ON)
5. USE Declaratives & Error Handlers
6. Secondary Entry Points (ENTRY statements)
"""

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel, GoToStatementNode, PerformStatementNode
from cobolscope.graph import CallGraphGenerator, GraphEdgeType, GraphNodeType

def run_edge_case_tests():
    cobol_path = repo_root / "tests" / "fixtures" / "TEST-GRAPH-EDGE-CASES.cbl"
    raw_ir = parse(str(cobol_path), format="FIXED", ignore_syntax_errors=True)
    model = ProgramModel.from_dict(raw_ir)
    gen = CallGraphGenerator(model=model, hide_fallthrough=False, collapse_exits=False, enable_clustering=True)
    graph = gen.graph

    results = {}

    # 1. Section Header Shadow Fall-Throughs
    # Expectation: PERFORM 2000-CALC-SECTION transfers reachability/edge to 2000-FIRST-PARA
    p_main = next((p for p in model.paragraphs if p.name == "0000-START"), None)
    p_first = next((p for p in model.paragraphs if p.name == "2000-FIRST-PARA"), None)
    edges_to_first = [e for e in graph.edges if e.target == "2000-FIRST-PARA" and e.source == "0000-START"]
    has_section_edge = len(edges_to_first) > 0 or ("0000-START" in (p_first.called_by if p_first else []))
    results["1_section_shadow_propagation"] = {
        "passed": has_section_edge,
        "details": f"0000-START -> 2000-FIRST-PARA edge exists: {len(edges_to_first) > 0}, called_by: {p_first.called_by if p_first else []}"
    }

    # 2. Post-Terminal Linear Shadow Blocks
    # Expectation: 1000-TERMINATE suppresses fallthrough, 1100-OBSOLETE-CLEANUP has no incoming edges
    p_term = next((p for p in model.paragraphs if p.name == "1000-TERMINATE"), None)
    p_obs = next((p for p in model.paragraphs if p.name == "1100-OBSOLETE-CLEANUP"), None)
    ft_suppressed = (p_term.fallthrough_successor is None) if p_term else False
    edges_to_obs = [e for e in graph.edges if e.target == "1100-OBSOLETE-CLEANUP"]
    results["2_post_terminal_suppression"] = {
        "passed": ft_suppressed and len(edges_to_obs) == 0,
        "details": f"1000-TERMINATE fallthrough: {p_term.fallthrough_successor if p_term else None}, Incoming edges to 1100: {len(edges_to_obs)}"
    }

    # 3. Infinite Jump Traps & Forward Bypasses
    # Expectation: 3000-ROUTINE unconditionally branches to 3000-EXIT; fallthrough to 3100-SKIPPED-LOGIC is suppressed
    p_rtn = next((p for p in model.paragraphs if p.name == "3000-ROUTINE"), None)
    p_skip = next((p for p in model.paragraphs if p.name == "3100-SKIPPED-LOGIC"), None)
    goto_edges = [e for e in graph.edges if e.source == "3000-ROUTINE" and e.target == "3000-EXIT" and e.edge_type == GraphEdgeType.GO_TO]
    edges_to_skip = [e for e in graph.edges if e.target == "3100-SKIPPED-LOGIC"]
    results["3_forward_bypass_suppression"] = {
        "passed": (p_rtn.fallthrough_successor is None if p_rtn else False) and len(goto_edges) == 1 and len(edges_to_skip) == 0,
        "details": f"3000-ROUTINE fallthrough: {p_rtn.fallthrough_successor if p_rtn else None}, GO_TO edges: {len(goto_edges)}, Incoming to skipped: {len(edges_to_skip)}"
    }

    # 4. Dynamic Jump Tables (GO TO DEPENDING ON)
    # Expectation: GO TO targets (4100, 4200, 4300) are extracted as GO_TO edges and in called_by
    p_disp = next((p for p in model.paragraphs if p.name == "4000-DISPATCH"), None)
    goto_depending_edges = [
        e for e in graph.edges
        if e.source == "4000-DISPATCH" and e.target in ("4100-NEW-ACCT", "4200-UPDATE-ACCT", "4300-CLOSE-ACCT") and e.edge_type == GraphEdgeType.GO_TO
    ]
    p_4100 = next((p for p in model.paragraphs if p.name == "4100-NEW-ACCT"), None)
    p_4200 = next((p for p in model.paragraphs if p.name == "4200-UPDATE-ACCT"), None)
    p_4300 = next((p for p in model.paragraphs if p.name == "4300-CLOSE-ACCT"), None)
    all_called = all("4000-DISPATCH" in (p.called_by if p else []) for p in (p_4100, p_4200, p_4300))
    results["4_goto_depending_on_targets"] = {
        "passed": len(goto_depending_edges) == 3 and all_called,
        "details": f"Extracted GO_TO edges from DISPATCH: {len(goto_depending_edges)} (targets: {[e.target for e in goto_depending_edges]}), called_by linked: {all_called}"
    }

    # 5. USE Declaratives & Error Handlers
    # Expectation: Declaratives section preserved, ERROR-LOG-PARA marked as event-driven root / exception handler
    decl_sections = [s for s in model.sections if "DECLARATIVE" in s.name.upper() or "ERROR" in s.name.upper()]
    p_err = next((p for p in model.paragraphs if p.name == "ERROR-LOG-PARA"), None)
    node_err = graph.nodes.get("ERROR-LOG-PARA")
    results["5_declaratives_protection"] = {
        "passed": len(decl_sections) > 0 and (node_err.node_type == GraphNodeType.ERROR_HANDLING if node_err else False) and (p_err.section_parent is not None if p_err else False),
        "details": f"Declaratives section captured in sections list: {len(decl_sections) > 0}, ERROR-LOG-PARA section_parent: {p_err.section_parent if p_err else None}, Node type: {node_err.node_type if node_err else None}"
    }

    # 6. Secondary Entry Points (ENTRY statement)
    # Expectation: ENTRY statement target 5000-ALT-ENTRY-PARA recognized as entry point / root
    node_alt = graph.nodes.get("5000-ALT-ENTRY-PARA")
    is_alt_entry_root = node_alt and node_alt.node_type == GraphNodeType.MAIN_DRIVER
    results["6_secondary_entry_points"] = {
        "passed": is_alt_entry_root,
        "details": f"5000-ALT-ENTRY-PARA node type: {node_alt.node_type if node_alt else None}, In-degree: {len([e for e in graph.edges if e.target == '5000-ALT-ENTRY-PARA'])}"
    }

    # 7. Nested Clause Traversal (READ ... AT END ... PERFORM ... THRU)
    from tests.harness.test_cache import resolve_cobol_path
    tt_path = resolve_cobol_path("TT35794")
    if tt_path:
        raw_tt = parse(str(tt_path), format="FIXED", ignore_syntax_errors=True)
        model_tt = ProgramModel.from_dict(raw_tt)
        p_read = next((p for p in model_tt.paragraphs if p.name == "3000-READ-INPUT"), None)
        read_stmt = p_read.statements[1] if (p_read and len(p_read.statements) > 1) else None
        has_at_end_perform = False
        if read_stmt and hasattr(read_stmt, "at_end_statements"):
            has_at_end_perform = any(
                isinstance(s, PerformStatementNode) and s.target == "9000-END-FILE-PROCESSING"
                for s in read_stmt.walk_tree()
            )
        gen_tt = CallGraphGenerator(model=model_tt)
        has_perform_edge = any(
            e.source == "3000-READ-INPUT" and e.target == "9000-END-FILE-PROCESSING" and e.edge_type == GraphEdgeType.PERFORM
            for e in gen_tt.graph.edges
        )
        results["7_nested_statement_phrase_traversal"] = {
            "passed": has_at_end_perform and has_perform_edge,
            "details": f"at_end_statements has PERFORM 9000: {has_at_end_perform}, Call graph has 3000 -> 9000 edge: {has_perform_edge}"
        }

    print("\n========================================================")
    print("COBOL GRAPH PARSER EDGE-CASE AUDIT RESULTS")
    print("========================================================")
    for test_key, res in results.items():
        status = "[PASSED]" if res["passed"] else "[FAILED]"
        print(f"{status} {test_key}")
        print(f"         Details: {res['details']}")

    return results

if __name__ == "__main__":
    run_edge_case_tests()
