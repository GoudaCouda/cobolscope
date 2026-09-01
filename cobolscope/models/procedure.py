"""
Procedure Division Models: SectionNode, ParagraphNode, AsgAuditSummary.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, AliasChoices
from .base import SourceLocation
from .statements import AnyStatementNode, _normalize_statement_dict


class SectionNode(BaseModel):
    """Represents a PROCEDURE DIVISION SECTION."""
    model_config = ConfigDict(populate_by_name=True)

    name: str = ""
    location: Optional[SourceLocation] = None
    statements: List[AnyStatementNode] = Field(default_factory=list)
    paragraph_names: List[str] = Field(default_factory=list, validation_alias=AliasChoices("paragraphNames", "paragraph_names"))

    @field_validator("statements", mode="before")
    @classmethod
    def normalize_statements(cls, v: Any) -> Any:
        if isinstance(v, list):
            return [_normalize_statement_dict(s) for s in v]
        return v


class ParagraphNode(BaseModel):
    """Represents a callable paragraph routine in physical sequence."""
    model_config = ConfigDict(populate_by_name=True)

    name: str = ""
    section_parent: Optional[str] = Field(default=None, validation_alias=AliasChoices("sectionParent", "section_parent"))
    location: Optional[SourceLocation] = None
    called_by: List[str] = Field(default_factory=list, validation_alias=AliasChoices("calledBy", "called_by"))
    successors: List[str] = Field(default_factory=list)
    is_terminal: bool = Field(default=False, validation_alias=AliasChoices("isTerminal", "is_terminal"))
    fallthrough_successor: Optional[str] = Field(default=None, validation_alias=AliasChoices("fallthroughSuccessor", "fallthrough_successor"))
    statements: List[AnyStatementNode] = Field(default_factory=list)

    @field_validator("statements", mode="before")
    @classmethod
    def normalize_statements(cls, v: Any) -> Any:
        if isinstance(v, list):
            return [_normalize_statement_dict(s) for s in v]
        return v


class AsgAuditSummary(BaseModel):
    """Objective ground-truth metrics and symbol sets collected directly from ProLeap's native ASG."""
    model_config = ConfigDict(populate_by_name=True)

    total_asg_data_entries: int = Field(default=0, validation_alias=AliasChoices("totalAsgDataEntries", "total_asg_data_entries"))
    total_asg_level88_entries: int = Field(default=0, validation_alias=AliasChoices("totalAsgLevel88Entries", "total_asg_level88_entries"))
    total_asg_paragraphs: int = Field(default=0, validation_alias=AliasChoices("totalAsgParagraphs", "total_asg_paragraphs"))
    total_asg_statements: int = Field(default=0, validation_alias=AliasChoices("totalAsgStatements", "total_asg_statements"))
    total_asg_calls: int = Field(default=0, validation_alias=AliasChoices("totalAsgCalls", "total_asg_calls"))
    asg_variable_names: List[str] = Field(default_factory=list, validation_alias=AliasChoices("asgVariableNames", "asg_variable_names"))
    asg_level88_names: List[str] = Field(default_factory=list, validation_alias=AliasChoices("asgLevel88Names", "asg_level88_names"))
    asg_paragraph_calls: Dict[str, List[str]] = Field(default_factory=dict, validation_alias=AliasChoices("asgParagraphCalls", "asg_paragraph_calls"))
