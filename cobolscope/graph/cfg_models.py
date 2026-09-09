"""
cobolscope.graph.cfg_models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data models and schemas for Level 3 Intra-Procedural Control Flow Graphs (CFG).
Defines basic blocks, decision points, loop structures, edges, and Cytoscape element mappings.
"""

from __future__ import annotations
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field


class CfgNodeType(str, Enum):
    ENTRY = "ENTRY"               # Routine entry point
    BASIC_BLOCK = "BASIC_BLOCK"   # Linear statement sequence (MOVE, ADD, COMPUTE, etc.)
    DECISION = "DECISION"         # Branching decision (IF condition, EVALUATE subject)
    LOOP_HEADER = "LOOP_HEADER"   # Inline PERFORM loop test (UNTIL, TIMES, VARYING)
    CALL_SITE = "CALL_SITE"       # Subprogram CALL or procedure PERFORM invocation
    JUMP = "JUMP"                 # Unconditional GO TO transfer
    TERMINAL = "TERMINAL"         # GOBACK, STOP RUN, or fatal abend
    EXIT = "EXIT"                 # Normal routine return point / fallthrough
    MERGE = "MERGE"               # Convergence point where branches reunite
    UNREACHABLE = "UNREACHABLE"   # Unreachable / dead code statement sequence


class CfgEdgeType(str, Enum):
    FALLTHROUGH = "FALLTHROUGH"   # Unconditional sequential flow
    TRUE_BRANCH = "TRUE_BRANCH"   # Condition is met (IF-THEN, UNTIL-TRUE)
    FALSE_BRANCH = "FALSE_BRANCH" # Condition is not met (IF-ELSE, UNTIL-FALSE)
    WHEN_BRANCH = "WHEN_BRANCH"   # EVALUATE WHEN match
    WHEN_OTHER = "WHEN_OTHER"     # EVALUATE WHEN OTHER fallback
    LOOP_BODY = "LOOP_BODY"       # Flow entering loop iteration
    LOOP_EXIT = "LOOP_EXIT"       # Flow exiting loop
    EXCEPTION = "EXCEPTION"       # ON SIZE ERROR, INVALID KEY, AT END, ON EXCEPTION
    JUMP = "JUMP"                 # GO TO target
    FALLTHROUGH_DEFAULT = "FALLTHROUGH_DEFAULT"  # Default fallthrough (e.g. GO TO DEPENDING ON out-of-range)
    UNREACHABLE = "UNREACHABLE"   # Unreachable flow transition


class CfgStatementItem(BaseModel):
    """Traceable statement item embedded inside a Basic Block."""
    model_config = ConfigDict(populate_by_name=True)

    type: str                     # MOVE, ADD, COMPUTE, READ, WRITE, etc.
    start_line: int = 0
    end_line: int = 0
    text: str = ""                # Cleaned COBOL text (e.g., "MOVE A TO B")
    target_fields: List[str] = Field(default_factory=list)
    source_fields: List[str] = Field(default_factory=list)


class CfgNode(BaseModel):
    """Represents a node in the intra-procedural CFG."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    node_type: CfgNodeType
    label: str
    condition: Optional[str] = None
    statements: List[CfgStatementItem] = Field(default_factory=list)
    start_line: int = 0
    end_line: int = 0
    is_terminal: bool = False


class CfgEdge(BaseModel):
    """Represents a directed control flow edge in the intra-procedural CFG."""
    model_config = ConfigDict(populate_by_name=True)

    source: str
    target: str
    edge_type: CfgEdgeType = CfgEdgeType.FALLTHROUGH
    label: Optional[str] = None
    condition: Optional[str] = None


class IntraprocedureCfg(BaseModel):
    """Complete Level 3 Intra-Procedural Control Flow Graph for a single procedure."""
    model_config = ConfigDict(populate_by_name=True)

    program_id: str
    paragraph_name: str
    section_name: Optional[str] = None
    cyclomatic_complexity: int = 1
    statement_count: int = 0
    is_eligible: bool = True
    eligibility_reason: str = ""
    nodes: Dict[str, CfgNode] = Field(default_factory=dict)
    edges: List[CfgEdge] = Field(default_factory=list)
    entry_node_id: str = "entry"
    exit_node_ids: List[str] = Field(default_factory=list)
    dominators: Dict[str, Optional[str]] = Field(default_factory=dict)
    post_dominators: Dict[str, Optional[str]] = Field(default_factory=dict)
    dead_code_nodes: List[str] = Field(default_factory=list)
    terminal_node_ids: List[str] = Field(default_factory=list)

    def to_cytoscape_elements(self) -> List[Dict[str, Any]]:
        """
        Converts the CFG into Cytoscape.js elements (nodes and edges)
        styled specifically for Level 3 intra-procedural control flow.
        """
        elements: List[Dict[str, Any]] = []

        if not self.is_eligible:
            return elements

        for node_id, node in self.nodes.items():
            classes = ["cfg-node", f"cfg-{node.node_type.value.lower()}"]
            if node.is_terminal:
                classes.append("cfg-terminal")

            # Format multi-line display label
            display_lines: List[str] = []
            short_lines: List[str] = []
            full_lines: List[str] = []
            is_expandable = False

            if node.node_type == CfgNodeType.ENTRY:
                display_lines.append(f"[ENTRY] {self.paragraph_name}")
                if node.start_line > 0:
                    display_lines.append(f"L{node.start_line}")
            elif node.node_type in (CfgNodeType.EXIT, CfgNodeType.TERMINAL):
                display_lines.append(node.label)
                if node.start_line > 0:
                    display_lines.append(f"L{node.start_line}")
            elif node.node_type == CfgNodeType.DECISION:
                cond = (node.condition or "").strip()
                line_str = f"L{node.start_line}" if node.start_line > 0 else ""
                if len(cond) > 38:
                    is_expandable = True
                    classes.append("cfg-expandable")
                    short_lines = [node.label, f"[{cond[:35]}...]"]
                    if line_str:
                        short_lines.append(line_str)
                    short_lines.append("...")

                    full_lines = [node.label, f"[{cond}]"]
                    if line_str:
                        full_lines.append(line_str)
                    display_lines = list(short_lines)
                else:
                    display_lines.append(node.label)
                    if cond:
                        display_lines.append(f"[{cond}]")
                    if line_str:
                        display_lines.append(line_str)
            elif node.node_type == CfgNodeType.LOOP_HEADER:
                cond = (node.condition or "").strip()
                line_str = f"L{node.start_line}" if node.start_line > 0 else ""
                if len(cond) > 38:
                    is_expandable = True
                    classes.append("cfg-expandable")
                    short_lines = [node.label, f"UNTIL: {cond[:35]}..."]
                    if line_str:
                        short_lines.append(line_str)
                    short_lines.append("...")

                    full_lines = [node.label, f"UNTIL: {cond}"]
                    if line_str:
                        full_lines.append(line_str)
                    display_lines = list(short_lines)
                else:
                    display_lines.append(node.label)
                    if cond:
                        display_lines.append(f"UNTIL: {cond}")
                    if line_str:
                        display_lines.append(line_str)
            elif node.node_type == CfgNodeType.BASIC_BLOCK:
                # Present statements cleanly and directly without artificial sequence headers
                for s in node.statements:
                    s_text = (s.text or s.type).strip()
                    full_lines.append(s_text)

                has_many_stmts = len(node.statements) > 4
                any_clipped_lines = any(len((s.text or s.type).strip()) > 38 for s in node.statements)

                if has_many_stmts or any_clipped_lines:
                    is_expandable = True
                    classes.append("cfg-expandable")
                    limit = 4 if has_many_stmts else len(node.statements)
                    for s in node.statements[:limit]:
                        s_text = (s.text or s.type).strip()
                        if len(s_text) > 38:
                            s_text = s_text[:35] + "..."
                        short_lines.append(s_text)

                    if has_many_stmts:
                        remaining = len(node.statements) - 4
                        short_lines.append(f"+{remaining} more...")

                    display_lines = list(short_lines)
                else:
                    short_lines = list(full_lines)
                    display_lines = list(full_lines)
            elif node.node_type == CfgNodeType.UNREACHABLE:
                classes.append("cfg-unreachable")
                display_lines.append(f"[UNREACHABLE] {node.label}")
                for s in node.statements:
                    s_text = (s.text or s.type).strip()
                    full_lines.append(s_text)
                if node.statements:
                    short_lines = [f"[UNREACHABLE] {node.label}"] + [s.text or s.type for s in node.statements[:3]]
                    if len(node.statements) > 3:
                        short_lines.append(f"+{len(node.statements) - 3} more...")
                        is_expandable = True
                        classes.append("cfg-expandable")
                    display_lines = list(short_lines)
            elif node.node_type == CfgNodeType.CALL_SITE:
                display_lines.append(node.label)
                if node.start_line > 0:
                    display_lines.append(f"L{node.start_line}")
            elif node.node_type == CfgNodeType.MERGE:
                display_lines.append("[MERGE]")
            else:
                display_lines.append(node.label)
                if node.start_line > 0:
                    display_lines.append(f"L{node.start_line}")

            elements.append({
                "data": {
                    "id": node.id,
                    "label": "\n".join(display_lines),
                    "short_label": "\n".join(short_lines) if short_lines else "\n".join(display_lines),
                    "full_label": "\n".join(full_lines) if full_lines else "\n".join(display_lines),
                    "node_type": node.node_type.value,
                    "condition": node.condition or "",
                    "start_line": node.start_line,
                    "end_line": node.end_line,
                    "is_terminal": node.is_terminal,
                    "statement_count": len(node.statements),
                    "is_expandable": is_expandable,
                    "is_expanded": False,
                    "statements": [s.model_dump() for s in node.statements],
                },
                "classes": " ".join(classes),
            })

        for edge in self.edges:
            if edge.source not in self.nodes or edge.target not in self.nodes:
                continue

            classes = ["cfg-edge", f"cfg-edge-{edge.edge_type.value.lower().replace('_', '-')}"]
            label_text = edge.label or ""
            if edge.edge_type == CfgEdgeType.TRUE_BRANCH and not label_text:
                label_text = "YES"
            elif edge.edge_type == CfgEdgeType.FALSE_BRANCH and not label_text:
                label_text = "NO"
            elif edge.edge_type == CfgEdgeType.FALLTHROUGH_DEFAULT and not label_text:
                label_text = "DEFAULT"
            elif edge.edge_type == CfgEdgeType.EXCEPTION and not label_text:
                label_text = "EXCEPTION"

            elements.append({
                "data": {
                    "id": f"cfg_e_{edge.source}_{edge.target}_{edge.edge_type.value}",
                    "source": edge.source,
                    "target": edge.target,
                    "edge_type": edge.edge_type.value,
                    "label": label_text,
                },
                "classes": " ".join(classes),
            })

        return elements

    def to_cytoscape_json(self) -> str:
        """Returns JSON string of Cytoscape elements."""
        return json.dumps(self.to_cytoscape_elements(), indent=2)
