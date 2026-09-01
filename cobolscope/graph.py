"""
Backward-compatibility proxy for cobolscope.graph.
"""

from cobolscope.graph import (
    GraphNodeType,
    GraphEdgeType,
    CallGraphCluster,
    CallGraphNode,
    CallGraphEdge,
    CallGraph,
    CLUSTER_THEMES,
    ParagraphClassifier,
    render_dot,
    render_svg,
    render_html,
    CallGraphGenerator,
    generate_call_graph,
)

__all__ = [
    "GraphNodeType",
    "GraphEdgeType",
    "CallGraphCluster",
    "CallGraphNode",
    "CallGraphEdge",
    "CallGraph",
    "CLUSTER_THEMES",
    "ParagraphClassifier",
    "render_dot",
    "render_svg",
    "render_html",
    "CallGraphGenerator",
    "generate_call_graph",
]
