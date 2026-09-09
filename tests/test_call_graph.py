"""
Comprehensive Test Suite for Level-2 Procedure Call Graph & Visual Pipeline.
Verifies Graphviz DOT emission, SVG compilation, HTML interactivity,
exit-node collapsing, and mathematical invariant satisfaction across COBOL benchmarks.
"""

import json
import sys
from pathlib import Path

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.graph import (
    CallGraphGenerator,
    generate_call_graph,
    GraphNodeType,
    GraphEdgeType,
)
from tests.harness.call_graph_validator import CallGraphValidator


from typing import Optional
from tests.harness.test_cache import get_test_model


def verify_program_call_graph(cobol_file: str, model: Optional[ProgramModel] = None):
    print(f"\n========================================================")
    print(f"Auditing Call Graph Generation for: {cobol_file}")
    print(f"========================================================")

    # 1. Obtain canonical IR
    if model is None:
        model = get_test_model(cobol_file)
    print(f"Program ID: {model.program_id} | Total Paragraphs: {len(model.paragraphs)}")

    # 2. Test Default Graph Generation (With Clustering & Fallthrough)
    gen_default = CallGraphGenerator(
        model=model,
        hide_fallthrough=False,
        collapse_exits=False,
        enable_clustering=True,
    )
    graph_default = gen_default.graph
    print(f"Default Graph: {len(graph_default.nodes)} nodes, {len(graph_default.edges)} edges, {len(graph_default.clusters)} clusters")
    print(f"Max Depth: {graph_default.max_depth} | Has Cycles: {graph_default.has_cycles}")

    # Validate mathematical invariants
    validator_default = CallGraphValidator(model, gen_default)
    results_default = validator_default.validate_all()
    for check_name, passed in results_default.items():
        assert passed, f"Invariant check '{check_name}' failed for default graph of {cobol_file}"
    print("  [OK] Default graph invariants (coverage, call parity, partition, SVG compilation) validated.")

    # 3. Test DOT & SVG Exporters
    dot_str = gen_default.to_dot()
    assert dot_str.startswith("digraph "), "DOT output invalid"
    svg_str = gen_default.to_svg()
    assert "<svg" in svg_str and "</svg>" in svg_str, "SVG output invalid"
    print(f"  [OK] DOT ({len(dot_str)} bytes) and SVG ({len(svg_str)} bytes) generated cleanly.")

    # 4. Test Interactive HTML Exporter
    html_str = gen_default.to_html()
    assert f"<title>Procedure Call Graph - {model.program_id}</title>" in html_str
    assert "id=\"canvas\"" in html_str
    assert "id=\"nodeSearch\"" in html_str
    assert "id=\"inspector\"" in html_str
    assert "id=\"cy-container\"" in html_str
    assert "cytoElements" in html_str
    print("  [OK] Interactive HTML viewer structure verified.")

    # 5. Test JSON Export
    json_str = gen_default.to_json()
    json_obj = json.loads(json_str)
    assert json_obj["program_id"] == model.program_id
    assert len(json_obj["nodes"]) == len(graph_default.nodes)
    print("  [OK] JSON graph schema export verified.")

    # 6. Test Exit Collapsing Mode (--collapse-exits)
    gen_collapsed = CallGraphGenerator(
        model=model,
        hide_fallthrough=False,
        collapse_exits=True,
        enable_clustering=True,
    )
    validator_collapsed = CallGraphValidator(model, gen_collapsed)
    results_collapsed = validator_collapsed.validate_all()
    for check_name, passed in results_collapsed.items():
        assert passed, f"Invariant check '{check_name}' failed for collapsed graph of {cobol_file}"

    total_collapsed_exits = sum(len(n.collapsed_exit_nodes) for n in gen_collapsed.graph.nodes.values())
    print(f"  [OK] Exit Collapsing verified ({total_collapsed_exits} -EXIT nodes merged into parent routines).")

    # 7. Test Hide Fallthrough Mode (--hide-fallthrough)
    gen_no_ft = CallGraphGenerator(
        model=model,
        hide_fallthrough=True,
        collapse_exits=False,
        enable_clustering=True,
    )
    ft_edges = [e for e in gen_no_ft.graph.edges if e.edge_type == GraphEdgeType.FALLTHROUGH]
    assert len(ft_edges) == 0, f"Expected 0 fallthrough edges in --hide-fallthrough, found {len(ft_edges)}"
    print("  [OK] Hide Fallthrough mode verified (all physical fallthrough connectors cleanly excluded).")

    # 8. Test Functional API & Output File Writing
    temp_dir = Path("output/call_graphs")
    temp_dir.mkdir(parents=True, exist_ok=True)

    svg_file = temp_dir / f"{model.program_id}.svg"
    html_file = temp_dir / f"{model.program_id}.html"
    dot_file = temp_dir / f"{model.program_id}.dot"

    generate_call_graph(model, format="svg", output_path=svg_file)
    generate_call_graph(model, format="html", output_path=html_file)
    generate_call_graph(model, format="dot", output_path=dot_file)

    assert svg_file.exists() and svg_file.stat().st_size > 0
    assert html_file.exists() and html_file.stat().st_size > 0
    assert dot_file.exists() and dot_file.stat().st_size > 0
    print(f"  [OK] Functional file outputs created in {temp_dir}")

    print(f"[PASSED] Call Graph Verification for {cobol_file}")


if __name__ == "__main__":
    test_programs = [
        "tests/fixtures/TEST-DATA-DICT.cbl",
        "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
        "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
        "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
        "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
        "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
    ]

    for p in test_programs:
        verify_program_call_graph(p)

    print("\n========================================================")
    print("ALL PROCEDURE CALL GRAPH TESTS PASSED 100%!")
    print("========================================================\n")
