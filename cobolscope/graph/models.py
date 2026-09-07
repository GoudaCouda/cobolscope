"""
cobolscope.graph.models
~~~~~~~~~~~~~~~~~~~~~~~~

Data models and enums for Procedure Call Graphs, nodes, edges, and clusters.
"""

from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field


class GraphNodeType(str, Enum):
    MAIN_DRIVER = "MAIN_DRIVER"
    INITIALIZATION = "INITIALIZATION"
    FILE_IO = "FILE_IO"
    DATABASE_IO = "DATABASE_IO"
    BUSINESS_LOGIC = "BUSINESS_LOGIC"
    TABLE_LOOKUP = "TABLE_LOOKUP"
    ERROR_HANDLING = "ERROR_HANDLING"
    TERMINATION = "TERMINATION"
    ROUTINE_EXIT = "ROUTINE_EXIT"
    GENERIC = "GENERIC"


class GraphEdgeType(str, Enum):
    PERFORM = "PERFORM"
    PERFORM_THRU = "PERFORM_THRU"
    CALL = "CALL"
    GO_TO = "GO_TO"
    FALLTHROUGH = "FALLTHROUGH"
    ERROR_BRANCH = "ERROR_BRANCH"


class CallGraphCluster(BaseModel):
    """Represents a functional subgraph grouping related routines."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    color: str = "#2B6CB0"
    fill_color: str = "#F0F9FF"
    text_color: str = "#1A365D"
    node_ids: List[str] = Field(default_factory=list)


class CallGraphNode(BaseModel):
    """Represents a paragraph routine as a node in the call graph."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    section: Optional[str] = None
    node_type: GraphNodeType = GraphNodeType.GENERIC
    cluster_id: str = "cluster_generic"
    start_line: int = 0
    end_line: int = 0
    statement_count: int = 0
    cyclomatic_complexity: int = 1
    is_entry_point: bool = False
    is_terminal: bool = False
    is_exit_paragraph: bool = False
    is_unreachable: bool = False
    io_summary: Dict[str, int] = Field(default_factory=dict)
    source_field_ids: List[str] = Field(default_factory=list)
    target_field_ids: List[str] = Field(default_factory=list)
    called_by: List[str] = Field(default_factory=list)
    successors: List[str] = Field(default_factory=list)
    fallthrough_successor: Optional[str] = None
    collapsed_exit_nodes: List[str] = Field(default_factory=list)
    is_cfg_eligible: bool = True
    cfg_eligibility_reason: str = ""
    cfg_elements: List[Dict[str, Any]] = Field(default_factory=list)
    cfg_linear_statements: List[Dict[str, Any]] = Field(default_factory=list)


class CallGraphEdge(BaseModel):
    """Represents a control transfer or procedure invocation edge."""
    model_config = ConfigDict(populate_by_name=True)

    source: str
    target: str
    edge_type: GraphEdgeType = GraphEdgeType.PERFORM
    label: Optional[str] = None
    line_number: Optional[int] = None


class CallGraph(BaseModel):
    """The complete in-memory Level-2 Procedure Call Graph."""
    model_config = ConfigDict(populate_by_name=True)

    program_id: str
    entry_point: Optional[str] = None
    nodes: Dict[str, CallGraphNode] = Field(default_factory=dict)
    edges: List[CallGraphEdge] = Field(default_factory=list)
    clusters: List[CallGraphCluster] = Field(default_factory=list)
    total_paragraphs: int = 0
    total_calls: int = 0
    max_depth: int = 0
    has_cycles: bool = False
    reachability_transitions_count: int = 0
