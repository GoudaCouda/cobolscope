"""
cobolscope.graph - Procedure Call Graph generation, clustering, and visual renderers.
"""

from .models import (
    GraphNodeType,
    GraphEdgeType,
    CallGraphCluster,
    CallGraphNode,
    CallGraphEdge,
    CallGraph,
)
from .classifier import CLUSTER_THEMES, ParagraphClassifier
from .renderers import render_dot, render_svg, render_html
from .builder import CallGraphGenerator, generate_call_graph
from .cfg_models import (
    CfgNodeType,
    CfgEdgeType,
    CfgStatementItem,
    CfgNode,
    CfgEdge,
    IntraprocedureCfg,
)
from .cfg_builder import IntraprocedureCfgBuilder, build_procedure_cfg
from .termination import TerminationClassifier

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
    "CfgNodeType",
    "CfgEdgeType",
    "CfgStatementItem",
    "CfgNode",
    "CfgEdge",
    "IntraprocedureCfg",
    "IntraprocedureCfgBuilder",
    "build_procedure_cfg",
    "TerminationClassifier",
]
