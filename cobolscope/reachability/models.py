"""
cobolscope.reachability.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydantic models for Reachability Analysis, State Transitions, and Perform Frames.
"""

from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TransitionKind(str, Enum):
    """Classification of control flow state transitions."""
    CALL_PERFORM = "CALL_PERFORM"
    RETURN_PERFORM = "RETURN_PERFORM"
    JUMP_GOTO = "JUMP_GOTO"
    INTRA_FALLTHROUGH = "INTRA_FALLTHROUGH"
    TOP_LEVEL_FALLTHROUGH = "TOP_LEVEL_FALLTHROUGH"
    TERMINATE = "TERMINATE"


class PerformFrame(BaseModel):
    """Represents an active PERFORM subroutine frame on the LIFO call stack."""
    model_config = ConfigDict(populate_by_name=True, frozen=True)

    caller: str
    target: str
    thru: Optional[str] = None
    return_boundary: str
    return_stmt_idx: int

    def summary(self) -> str:
        if self.thru and self.thru != self.target:
            return f"{self.caller}->[{self.target}..{self.thru}]"
        return f"{self.caller}->{self.target}"


class StateTransition(BaseModel):
    """Recorded runtime state transition between abstract execution configurations."""
    model_config = ConfigDict(populate_by_name=True)

    source_paragraph: str
    source_stmt_idx: int
    kind: TransitionKind
    target_paragraph: Optional[str] = None
    target_stmt_idx: int = 0
    stack_depth: int = 0
    stack_summary: List[str] = Field(default_factory=list)


class ReachabilityModel(BaseModel):
    """
    Serializable container for verified reachability results, state transitions,
    and proven control flow edge sets.
    """
    model_config = ConfigDict(populate_by_name=True)

    entrypoint: str
    reachable_paragraphs: List[str] = Field(default_factory=list)
    unreachable_paragraphs: List[str] = Field(default_factory=list)
    state_transitions: List[StateTransition] = Field(default_factory=list)
    validated_perform_edges: List[List[str]] = Field(default_factory=list)
    validated_goto_edges: List[List[str]] = Field(default_factory=list)
    validated_fallthrough_edges: List[List[str]] = Field(default_factory=list)
    perform_return_points: Dict[str, List[str]] = Field(default_factory=dict)

    def to_json_file(self, path: Path | str) -> None:
        """Exports the reachability model and state transitions to a JSON file."""
        target_path = Path(path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))
