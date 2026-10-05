"""
cobolscope.graph.renderers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graphviz DOT, SVG, HTML, and JSON visual rendering engines for COBOL Call Graphs.
"""

from __future__ import annotations
import html
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jinja2

from .models import CallGraph, CallGraphNode, GraphNodeType, GraphEdgeType
from .classifier import CLUSTER_THEMES
from cobolscope.assets import AssetMode, resolve_asset_mode, get_bundled_css, get_bundled_js



def format_dot_node(node: CallGraphNode, indent: int = 4, compact: bool = True) -> str:
    """Formats a single node into Graphviz DOT with an HTML-like table label."""
    ind = " " * indent
    theme = CLUSTER_THEMES.get(node.node_type, CLUSTER_THEMES[GraphNodeType.GENERIC])
    border_color = "#0078D4" if node.is_entry_point else theme["color"]
    penwidth = 2.5 if node.is_entry_point else 1.5
    bg_color = "#FFFFFF"

    # Build subtitle badges
    meta_parts = []
    if node.start_line > 0:
        meta_parts.append(f"L{node.start_line}-{node.end_line}")
    meta_parts.append(f"{node.statement_count} stmts")
    meta_parts.append(f"CC:{node.cyclomatic_complexity}")
    meta_str = " | ".join(meta_parts)

    # Build I/O badges
    io_badges = []
    for k, v in node.io_summary.items():
        io_badges.append(f"{k}:{v}")
    if node.is_terminal:
        io_badges.append("TERMINAL")
    if node.collapsed_exit_nodes:
        io_badges.append(f"+{len(node.collapsed_exit_nodes)} exit")

    io_str = " | ".join(io_badges) if io_badges else ""

    # HTML Table Construction with clear visual hierarchy
    rows = []

    # 1. Entry Point Banner
    if node.is_entry_point:
        rows.append('<tr><td align="center" bgcolor="#0078D4" cellpadding="3"><font color="#FFFFFF" point-size="9"><b>[ENTRY] START / ENTRY POINT</b></font></td></tr>')
    elif node.is_clone:
        total_str = f"/{node.clone_total}" if node.clone_total > 1 else ""
        rows.append(f'<tr><td align="center" bgcolor="#F1F5F9" cellpadding="2"><font color="#475569" point-size="8"><b>[CLONE {node.clone_index}{total_str}]</b></font></td></tr>')

    # 2. Section Name & Paragraph Title
    has_distinct_section = bool(node.section and node.section.strip() and node.section.strip().upper() != node.name.strip().upper())
    if has_distinct_section:
        sec_clean = node.section.strip()
        rows.append(f'<tr><td align="center" cellpadding="2"><b><font point-size="11">{html.escape(sec_clean)}</font></b></td></tr>')
        rows.append(f'<tr><td align="center" cellpadding="0"><font color="#475569" point-size="9">&#167; {html.escape(node.name)}</font></td></tr>')
    else:
        rows.append(f'<tr><td align="center" cellpadding="2"><b><font point-size="11">{html.escape(node.name)}</font></b></td></tr>')

    # 3. Unreachable / Dead Code Warning Banner
    if node.is_unreachable:
        rows.append('<tr><td align="center" bgcolor="#FEF2F2" cellpadding="2"><font color="#DC2626" point-size="8"><b>[UNREACHABLE / DEAD CODE]</b></font></td></tr>')

    # 4. Metadata and Complexity
    rows.append(f'<tr><td align="center" cellpadding="1"><font color="#64748B" point-size="8">{html.escape(meta_str)}</font></td></tr>')

    # 5. I/O Badges
    if io_str:
        badge_color = "#475569" if "TERMINAL" in io_str else ("#107C41" if "READ" in io_str or "WRITE" in io_str else "#5C2D91")
        rows.append(f'<tr><td align="center" cellpadding="1"><font color="{badge_color}" point-size="8"><b>[{html.escape(io_str)}]</b></font></td></tr>')

    # 6. Subtle Data Dictionary Field Lineage (rendered on node face when not compact)
    raw_field_ids = node.target_field_ids + [f for f in node.source_field_ids if f not in node.target_field_ids]
    clean_field_names = []
    for fid in raw_field_ids:
        fname = fid.split("_")[-1] if "_" in fid else fid
        if fname and fname not in clean_field_names:
            clean_field_names.append(fname)

    if clean_field_names and not compact:
        limit = 2
        data_preview = ", ".join(clean_field_names[:limit])
        if len(clean_field_names) > limit:
            data_preview += f" (+{len(clean_field_names) - limit})"
        rows.append(f'<tr><td align="center" cellpadding="1"><font color="#64748B" point-size="7.5"><i>data: {html.escape(data_preview)}</i></font></td></tr>')

    table_html = (
        f'<<table border="0" cellborder="0" cellspacing="0" cellpadding="2">'
        f'{"".join(rows)}'
        f'</table>>'
    )

    tooltip_text = f"{node.section} : {node.name}" if has_distinct_section else node.name
    tooltip_text += f" (Lines {node.start_line}-{node.end_line})"
    if clean_field_names:
        tooltip_text += f" | Data: {', '.join(clean_field_names[:4])}"
    if node.is_entry_point:
        tooltip_text = f"[START] {tooltip_text}"
    if node.is_clone:
        tooltip_text = f"[CLONE of {node.original_name}] {tooltip_text}"

    node_style = "dashed,filled" if node.is_clone else "filled,rounded"

    return (
        f'{ind}{node.id} ['
        f'label={table_html}, '
        f'fillcolor="{bg_color}", '
        f'color="{border_color}", '
        f'penwidth={penwidth}, '
        f'style="{node_style}", '
        f'tooltip="{html.escape(tooltip_text)}"'
        f'];'
    )


def render_dot(
    graph: CallGraph,
    enable_clustering: bool = True,
    compact_nodes: bool = True,
    concentrate: bool = True,
    splines: str = "spline",
    ranker: Optional[str] = None,
    nodesep: Optional[float] = None,
    ranksep: Optional[float] = None,
    dynamic_heuristics: bool = True,
) -> str:
    """Emits standards-compliant Graphviz .dot syntax with clean vertical hierarchy and dynamic heuristics."""
    from .heuristics import compute_graph_metrics, calculate_layout_heuristics

    if dynamic_heuristics:
        metrics = compute_graph_metrics(graph)
        heuristics = calculate_layout_heuristics(
            metrics,
            compact_nodes=compact_nodes,
            requested_splines=splines if splines != "spline" else None,
            requested_ranker=ranker,
        )
        active_ranker = ranker or heuristics.ranker
        active_splines = splines if splines else heuristics.splines

        active_nodesep = nodesep if nodesep is not None else heuristics.nodesep_in
        active_ranksep = ranksep if ranksep is not None else heuristics.ranksep_in
    else:
        active_ranker = ranker or "network-simplex"
        active_splines = splines
        active_nodesep = nodesep if nodesep is not None else 0.45
        active_ranksep = ranksep if ranksep is not None else 0.75

    lines = []
    lines.append(f'digraph "{graph.program_id}_CallGraph" {{')
    lines.append('    // Global Graph Attributes')
    lines.append('    rankdir=TB;')
    lines.append('    compound=true;')
    lines.append('    newrank=true;')
    if concentrate:
        lines.append('    concentrate=true;')
    lines.append(f'    ranker="{active_ranker}";')
    lines.append(f'    splines="{active_splines}";')

    lines.append(f'    nodesep={active_nodesep};')
    lines.append(f'    ranksep={active_ranksep};')
    lines.append('    ratio=auto;')
    lines.append('    bgcolor="#FFFFFF";')
    lines.append('    fontname="Segoe UI, -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif";')
    lines.append('    fontsize=12;')
    lines.append('')
    lines.append('    // Top-Level Program Header Title')
    lines.append('    labelloc="t";')
    lines.append('    labeljust="c";')
    cloned_note = f" | {graph.cloned_node_count} Cloned Utilities" if getattr(graph, "cloned_node_count", 0) > 0 else ""
    lines.append(f'    label=<<table border="0" cellborder="0" cellspacing="0" cellpadding="3">'
                 f'<tr><td><font point-size="15" color="#0F172A"><b>Procedure Call Graph: {html.escape(graph.program_id)}</b></font></td></tr>'
                 f'<tr><td><font point-size="9" color="#64748B">{len(graph.nodes)} Procedures | {len(graph.edges)} Calls &amp; Transfers{cloned_note} | Max Depth: {graph.max_depth}</font></td></tr>'
                 f'</table>>;')
    lines.append('')
    lines.append('    node [fontname="Segoe UI, Helvetica, Arial, sans-serif", fontsize=10, shape=box, style="filled,rounded", penwidth=1.5, margin="0.15,0.08"];')
    lines.append('    edge [fontname="Segoe UI, Helvetica, Arial, sans-serif", fontsize=8, arrowsize=0.75];')
    lines.append('')

    # Emit Clusters & Nodes
    if enable_clustering and graph.clusters:
        for c_idx, cluster in enumerate(graph.clusters):
            lines.append(f'    subgraph "cluster_{c_idx}_{cluster.id}" {{')
            lines.append(f'        label="{html.escape(cluster.name)}";')
            lines.append(f'        style="filled,rounded";')
            lines.append(f'        color="{cluster.color}";')
            lines.append(f'        fillcolor="{cluster.fill_color}";')
            lines.append(f'        fontcolor="{cluster.text_color}";')
            lines.append('        fontsize=11;')
            lines.append('        penwidth=1.5;')
            lines.append('')

            for node_name in graph.nodes:
                node = graph.nodes[node_name]
                if node.id in cluster.node_ids:
                    lines.append(format_dot_node(node, indent=8, compact=compact_nodes))
            lines.append('    }')
            lines.append('')
    else:
        for node_name in graph.nodes:
            node = graph.nodes[node_name]
            lines.append(format_dot_node(node, indent=4, compact=compact_nodes))
        lines.append('')

    # Emit Edges
    lines.append('    // Procedure Control Flow Edges')
    for edge in graph.edges:
        src_node = graph.nodes.get(edge.source)
        tgt_node = graph.nodes.get(edge.target)
        if not src_node or not tgt_node:
            continue

        src_id = src_node.id
        tgt_id = tgt_node.id

        attr_list = []
        if edge.edge_type == GraphEdgeType.PERFORM:
            attr_list.append('color="#0078D4"')
            attr_list.append('penwidth=1.5')
            attr_list.append('tooltip="PERFORM"')
        elif edge.edge_type == GraphEdgeType.PERFORM_THRU:
            attr_list.append('style="dashed"')
            attr_list.append('color="#0078D4"')
            attr_list.append('penwidth=1.2')
            attr_list.append('label="THRU"')
            attr_list.append('fontcolor="#0078D4"')
        elif edge.edge_type == GraphEdgeType.CALL:
            attr_list.append('style="bold"')
            attr_list.append('color="#107C41"')
            attr_list.append('penwidth=2.0')
            attr_list.append('tooltip="CALL"')
        elif edge.edge_type == GraphEdgeType.GO_TO:
            attr_list.append('style="dashed"')
            attr_list.append('color="#5C2D91"')
            attr_list.append('penwidth=1.2')
            attr_list.append('label="GO TO"')
            attr_list.append('fontcolor="#5C2D91"')
        elif edge.edge_type == GraphEdgeType.FALLTHROUGH:
            attr_list.append('style="dotted"')
            attr_list.append('color="#94A3B8"')
            attr_list.append('fontcolor="#94A3B8"')
            attr_list.append('penwidth=1.0')
            attr_list.append('constraint=false')
            attr_list.append('tooltip="Fall-through flow"')
        elif edge.edge_type == GraphEdgeType.ERROR_BRANCH:
            attr_list.append('style="dashed"')
            attr_list.append('color="#DC2626"')
            attr_list.append('fontcolor="#DC2626"')
            attr_list.append('penwidth=1.5')
            attr_list.append('constraint=false')
            attr_list.append('tooltip="Error trap / abend"')

        attrs = f" [{', '.join(attr_list)}]" if attr_list else ""
        lines.append(f'    {src_id} -> {tgt_id}{attrs};')

    lines.append('}')
    return '\n'.join(lines)


def render_svg(dot_code: str) -> str:
    """Compiles DOT to SVG using local Graphviz dot binary with execution timeout guard."""
    try:
        res = subprocess.run(
            ["dot", "-Tsvg"],
            input=dot_code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=10,
            check=True,
        )
        return res.stdout
    except subprocess.TimeoutExpired as te:
        raise RuntimeError("Graphviz 'dot' execution timed out after 10 seconds.") from te
    except subprocess.CalledProcessError as cpe:
        raise RuntimeError(
            f"Graphviz 'dot' execution failed (exit code {cpe.returncode}). Stderr:\n{cpe.stderr}"
        ) from cpe
    except Exception as e2:
        raise RuntimeError(
            f"Graphviz 'dot' execution failed. Ensure Graphviz is installed and on PATH: {e2}"
        ) from e2



def render_cytoscape_elements(
    graph: CallGraph,
    enable_clustering: bool = True,
) -> List[Dict[str, Any]]:
    """
    Converts a CallGraph into a list of Cytoscape.js elements (compound parent
    clusters, routine nodes, and directed control transfer edges).
    """
    elements: List[Dict[str, Any]] = []

    # 1. Emit Parent Compound Cluster Nodes
    if enable_clustering:
        for cluster in graph.clusters:
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
    for node_name, node in graph.nodes.items():
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

        parent_id = node.cluster_id if (enable_clustering and node.cluster_id) else None
        # Validate parent actually exists in active clusters
        if parent_id and not any(c.id == parent_id for c in graph.clusters):
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
            "source_file": node.source_file or "",
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

        # Clone Metadata
        node_data["is_clone"] = node.is_clone
        node_data["original_name"] = node.original_name or node.name
        node_data["clone_index"] = node.clone_index
        node_data["clone_total"] = node.clone_total
        node_data["clone_caller"] = node.clone_caller or ""

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
        if node.is_clone:
            node_classes.append("clone-node")

        elements.append({
            "data": node_data,
            "classes": " ".join(node_classes),
        })

    # 3. Emit Directed Control Edges
    for edge in graph.edges:
        src_node = graph.nodes.get(edge.source)
        tgt_node = graph.nodes.get(edge.target)
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


def render_cytoscape_json(
    graph: CallGraph,
    enable_clustering: bool = True,
    indent: int = 2,
) -> str:
    """Returns Cytoscape.js elements serialized as a JSON string."""
    import json
    return json.dumps(render_cytoscape_elements(graph, enable_clustering=enable_clustering), indent=indent)


def render_html(
    graph: CallGraph,
    dot_code: Optional[str] = None,
    svg_content: Optional[str] = None,
    cyto_elements: Optional[List[Dict[str, Any]]] = None,
    initial_engine: str = "cytoscape",
    heuristics: Optional[Any] = None,
    metrics: Optional[Any] = None,
    cloned_elements: Optional[List[Dict[str, Any]]] = None,
    canonical_elements: Optional[List[Dict[str, Any]]] = None,
    enable_cloning: bool = False,
    asset_mode: Union[str, AssetMode] = "inline",
    assets_rel_path: str = "assets",
) -> str:
    """Renders standalone interactive HTML visualization powered by Cytoscape.js with dynamic heuristics and dual-mode bundling."""
    from .heuristics import compute_graph_metrics, calculate_layout_heuristics
    if metrics is None:
        metrics = compute_graph_metrics(graph)
    if heuristics is None:
        heuristics = calculate_layout_heuristics(metrics, compact_nodes=True)

    template_dir = Path(__file__).resolve().parent.parent / "templates"
    try:
        loader = jinja2.PackageLoader("cobolscope", "templates")
    except Exception:
        loader = jinja2.FileSystemLoader(str(template_dir))

    env = jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    try:
        template = env.get_template("call_graph.html.j2")
    except Exception:
        template = env.from_string(_DEFAULT_CALL_GRAPH_HTML_TEMPLATE)

    import json
    cyto_json = json.dumps(cyto_elements or [])
    cloned_json = json.dumps(cloned_elements or [])
    canonical_json = json.dumps(canonical_elements or (cyto_elements if not enable_cloning else []))
    clone_count = len([e for e in (cloned_elements or []) if e.get("data", {}).get("is_clone")])

    resolved_mode = resolve_asset_mode(asset_mode)
    if resolved_mode == AssetMode.INLINE:
        bundled_css = get_bundled_css()
        bundled_js = get_bundled_js(monolithic=True)
    else:
        bundled_css = ""
        bundled_js = ""

    payload = {
        "graph": graph.model_dump(),
        "cytoElements": cyto_elements or [],
        "canonicalElements": canonical_elements or (cyto_elements if not enable_cloning else []),
        "clonedElements": cloned_elements or [],
        "initialEnableCloning": enable_cloning,
        "layoutHeuristics": heuristics.to_dict() if heuristics else {},
        "initialEnginePreference": initial_engine,
        "sourceCodeRaw": graph.source_code or "",
    }
    graph_payload_json = json.dumps(payload)

    return template.render(
        program_id=graph.program_id,
        graph=graph,
        svg_content=svg_content or "",
        dot_content=dot_code or "",
        cyto_elements=cyto_elements or [],
        cyto_json=cyto_json,
        cloned_elements=cloned_elements or [],
        cloned_json=cloned_json,
        canonical_elements=canonical_elements or [],
        canonical_json=canonical_json,
        clone_count=clone_count,
        enable_cloning=enable_cloning,
        initial_engine=initial_engine,
        source_code=graph.source_code or "",
        heuristics=heuristics,
        metrics=metrics,
        graph_payload_json=graph_payload_json,
        asset_mode=resolved_mode.value,
        assets_rel_path=assets_rel_path,
        bundled_css=bundled_css,
        bundled_js=bundled_js,
    )





_DEFAULT_CALL_GRAPH_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Procedure Call Graph - {{ program_id }}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; background: #F8FAFC; color: #1E293B; }
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 16px; }
  .header h1 { margin: 0; font-size: 22px; color: #0F172A; }
  .svg-container { background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; overflow: auto; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  svg { max-width: 100%; height: auto; }
</style>
</head>
<body>
<div class="header">
  <h1>Procedure Call Graph: <code>{{ program_id }}</code></h1>
  <div>Paragraphs: <b>{{ graph.total_paragraphs }}</b> | Calls: <b>{{ graph.total_calls }}</b></div>
</div>
<div class="svg-container">
  {{ svg_content | safe }}
</div>
</body>
</html>
"""
