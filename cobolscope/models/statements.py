"""
Strongly Typed Statement Nodes (Canonical IR).
Supports open polymorphism with dedicated models for rich verbs and GenericStatementNode fallback.
Includes the polymorphic get_child_statements() and walk_tree() traversal protocol.
"""

from __future__ import annotations
import logging
from typing import List, Dict, Optional, Any, Union, Literal, Annotated, Iterator
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from .base import SourceLocation

logger = logging.getLogger(__name__)


class StatementNode(BaseModel):
    """Base IR statement carrying source traceability and operation classification."""
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    type: str = "UNKNOWN"
    location: Optional[SourceLocation] = None
    raw_text: Optional[str] = Field(default=None, validation_alias=AliasChoices("rawText", "raw_text"))
    target_field_ids: List[str] = Field(default_factory=list, validation_alias=AliasChoices("targetFieldIds", "target_field_ids"))
    source_field_ids: List[str] = Field(default_factory=list, validation_alias=AliasChoices("sourceFieldIds", "source_field_ids"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        """
        Polymorphic contract returning all immediate child statements
        across all conditional and exception branches.
        """
        return []

    def walk_tree(self) -> Iterator[AnyStatementNode]:
        """
        Recursively yields self and all descendant statements in preorder traversal.
        """
        yield self
        for child in self.get_child_statements():
            yield from child.walk_tree()


class MoveStatementNode(StatementNode):
    type: Literal["MOVE"] = "MOVE"
    from_expr: str = Field(default="", validation_alias=AliasChoices("fromExpr", "from_expr", "from"))
    to_targets: List[str] = Field(default_factory=list, validation_alias=AliasChoices("toTargets", "to_targets", "to"))
    is_corresponding: bool = Field(default=False, validation_alias=AliasChoices("isCorresponding", "is_corresponding"))
    corresponding_text: Optional[str] = Field(default=None, validation_alias=AliasChoices("correspondingText", "corresponding_text"))


class PerformStatementNode(StatementNode):
    type: Literal["PERFORM"] = "PERFORM"
    target: Optional[str] = None
    thru: Optional[str] = None
    perform_type: Optional[str] = Field(default=None, validation_alias=AliasChoices("performType", "perform_type"))
    times_expr: Optional[str] = Field(default=None, validation_alias=AliasChoices("timesExpr", "times_expr"))
    until_condition: Optional[str] = Field(default=None, validation_alias=AliasChoices("untilCondition", "until_condition"))
    varying_expr: Optional[str] = Field(default=None, validation_alias=AliasChoices("varyingExpr", "varying_expr"))
    is_inline: bool = Field(default=False, validation_alias=AliasChoices("isInline", "is_inline"))
    nested_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("nestedStatements", "nested_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.nested_statements)


class IfStatementNode(StatementNode):
    type: Literal["IF"] = "IF"
    condition: str = ""
    then_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("thenStatements", "then_statements"))
    else_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("elseStatements", "else_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.then_statements) + list(self.else_statements)


class EvaluateWhenBranch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    conditions: List[str] = Field(default_factory=list)
    statements: List[AnyStatementNode] = Field(default_factory=list)


class EvaluateStatementNode(StatementNode):
    type: Literal["EVALUATE"] = "EVALUATE"
    subjects: List[str] = Field(default_factory=list)
    when_branches: List[EvaluateWhenBranch] = Field(default_factory=list, validation_alias=AliasChoices("whenBranches", "when_branches"))
    when_other_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("whenOtherStatements", "when_other_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        res: List[AnyStatementNode] = []
        for b in self.when_branches:
            res.extend(b.statements)
        res.extend(self.when_other_statements)
        return res


class CallStatementNode(StatementNode):
    type: Literal["CALL"] = "CALL"
    program: str = ""
    using_parameters: List[str] = Field(default_factory=list, validation_alias=AliasChoices("usingParameters", "using_parameters", "using"))
    giving: Optional[str] = None
    on_exception_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onExceptionStatements", "on_exception_statements"))
    not_on_exception_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnExceptionStatements", "not_on_exception_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_exception_statements) + list(self.not_on_exception_statements)


class ComputeStatementNode(StatementNode):
    type: Literal["COMPUTE"] = "COMPUTE"
    targets: List[str] = Field(default_factory=list)
    expression: str = ""
    on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onSizeErrorStatements", "on_size_error_statements"))
    not_on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnSizeErrorStatements", "not_on_size_error_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_size_error_statements) + list(self.not_on_size_error_statements)


class AddStatementNode(StatementNode):
    type: Literal["ADD"] = "ADD"
    operation: str = "ADD"
    expression: str = ""
    on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onSizeErrorStatements", "on_size_error_statements"))
    not_on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnSizeErrorStatements", "not_on_size_error_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_size_error_statements) + list(self.not_on_size_error_statements)


class SubtractStatementNode(StatementNode):
    type: Literal["SUBTRACT"] = "SUBTRACT"
    operation: str = "SUBTRACT"
    expression: str = ""
    on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onSizeErrorStatements", "on_size_error_statements"))
    not_on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnSizeErrorStatements", "not_on_size_error_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_size_error_statements) + list(self.not_on_size_error_statements)


class MultiplyStatementNode(StatementNode):
    type: Literal["MULTIPLY"] = "MULTIPLY"
    operation: str = "MULTIPLY"
    expression: str = ""
    on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onSizeErrorStatements", "on_size_error_statements"))
    not_on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnSizeErrorStatements", "not_on_size_error_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_size_error_statements) + list(self.not_on_size_error_statements)


class DivideStatementNode(StatementNode):
    type: Literal["DIVIDE"] = "DIVIDE"
    operation: str = "DIVIDE"
    expression: str = ""
    remainder: Optional[str] = None
    on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onSizeErrorStatements", "on_size_error_statements"))
    not_on_size_error_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnSizeErrorStatements", "not_on_size_error_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_size_error_statements) + list(self.not_on_size_error_statements)


class ReadStatementNode(StatementNode):
    type: Literal["READ"] = "READ"
    operation: str = "READ"
    file: Optional[str] = None
    record: Optional[str] = None
    into: Optional[str] = None
    key: Optional[str] = None
    at_end_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("atEndStatements", "at_end_statements"))
    not_at_end_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notAtEndStatements", "not_at_end_statements"))
    invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("invalidKeyStatements", "invalid_key_statements"))
    not_invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notInvalidKeyStatements", "not_invalid_key_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return (
            list(self.at_end_statements)
            + list(self.not_at_end_statements)
            + list(self.invalid_key_statements)
            + list(self.not_invalid_key_statements)
        )


class WriteStatementNode(StatementNode):
    type: Literal["WRITE"] = "WRITE"
    operation: str = "WRITE"
    record: Optional[str] = None
    from_expr: Optional[str] = Field(default=None, validation_alias=AliasChoices("fromExpr", "from_expr", "from"))
    invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("invalidKeyStatements", "invalid_key_statements"))
    not_invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notInvalidKeyStatements", "not_invalid_key_statements"))
    end_of_page_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("endOfPageStatements", "end_of_page_statements"))
    not_end_of_page_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notEndOfPageStatements", "not_end_of_page_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return (
            list(self.invalid_key_statements)
            + list(self.not_invalid_key_statements)
            + list(self.end_of_page_statements)
            + list(self.not_end_of_page_statements)
        )


class RewriteStatementNode(StatementNode):
    type: Literal["REWRITE"] = "REWRITE"
    operation: str = "REWRITE"
    expression: str = ""
    invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("invalidKeyStatements", "invalid_key_statements"))
    not_invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notInvalidKeyStatements", "not_invalid_key_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.invalid_key_statements) + list(self.not_invalid_key_statements)


class DeleteStatementNode(StatementNode):
    type: Literal["DELETE"] = "DELETE"
    operation: str = "DELETE"
    expression: str = ""
    invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("invalidKeyStatements", "invalid_key_statements"))
    not_invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notInvalidKeyStatements", "not_invalid_key_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.invalid_key_statements) + list(self.not_invalid_key_statements)


class OpenStatementNode(StatementNode):
    type: Literal["OPEN"] = "OPEN"
    operation: str = "OPEN"
    expression: str = ""


class CloseStatementNode(StatementNode):
    type: Literal["CLOSE"] = "CLOSE"
    operation: str = "CLOSE"
    expression: str = ""


class StartStatementNode(StatementNode):
    type: Literal["START"] = "START"
    operation: str = "START"
    expression: str = ""
    invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("invalidKeyStatements", "invalid_key_statements"))
    not_invalid_key_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notInvalidKeyStatements", "not_invalid_key_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.invalid_key_statements) + list(self.not_invalid_key_statements)


class GoToStatementNode(StatementNode):
    type: Literal["GO_TO"] = "GO_TO"
    operation: str = "GO_TO"
    target: Optional[str] = None
    depending_on: Optional[str] = Field(default=None, validation_alias=AliasChoices("dependingOn", "depending_on"))


class StopStatementNode(StatementNode):
    type: Literal["STOP"] = "STOP"
    operation: str = "STOP"
    expression: str = ""


class GobackStatementNode(StatementNode):
    type: Literal["GOBACK"] = "GOBACK"
    operation: str = "GOBACK"


class ExitStatementNode(StatementNode):
    type: Literal["EXIT"] = "EXIT"
    operation: str = "EXIT"


class ContinueStatementNode(StatementNode):
    type: Literal["CONTINUE"] = "CONTINUE"
    operation: str = "CONTINUE"


class DisplayStatementNode(StatementNode):
    type: Literal["DISPLAY"] = "DISPLAY"
    operands: List[str] = Field(default_factory=list)


class AcceptStatementNode(StatementNode):
    type: Literal["ACCEPT"] = "ACCEPT"
    operation: str = "ACCEPT"
    expression: str = ""


class InitializeStatementNode(StatementNode):
    type: Literal["INITIALIZE"] = "INITIALIZE"
    targets: List[str] = Field(default_factory=list)


class SetStatementNode(StatementNode):
    type: Literal["SET"] = "SET"
    operation: str = "SET"
    expression: str = ""


class StringStatementNode(StatementNode):
    type: Literal["STRING"] = "STRING"
    operation: str = "STRING"
    expression: str = ""
    on_overflow_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onOverflowStatements", "on_overflow_statements"))
    not_on_overflow_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnOverflowStatements", "not_on_overflow_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_overflow_statements) + list(self.not_on_overflow_statements)


class UnstringStatementNode(StatementNode):
    type: Literal["UNSTRING"] = "UNSTRING"
    operation: str = "UNSTRING"
    expression: str = ""
    on_overflow_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("onOverflowStatements", "on_overflow_statements"))
    not_on_overflow_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("notOnOverflowStatements", "not_on_overflow_statements"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        return list(self.on_overflow_statements) + list(self.not_on_overflow_statements)


class InspectStatementNode(StatementNode):
    type: Literal["INSPECT"] = "INSPECT"
    operation: str = "INSPECT"
    expression: str = ""


class SearchWhenBranch(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    condition: str = ""
    statements: List[AnyStatementNode] = Field(default_factory=list)


class SearchStatementNode(StatementNode):
    type: Literal["SEARCH"] = "SEARCH"
    operation: str = "SEARCH"
    expression: str = ""
    at_end_statements: List[AnyStatementNode] = Field(default_factory=list, validation_alias=AliasChoices("atEndStatements", "at_end_statements"))
    when_branches: List[SearchWhenBranch] = Field(default_factory=list, validation_alias=AliasChoices("searchWhenBranches", "whenBranches", "when_branches"))

    def get_child_statements(self) -> List[AnyStatementNode]:
        res = list(self.at_end_statements)
        for b in self.when_branches:
            res.extend(b.statements)
        return res


class ExecSqlStatementNode(StatementNode):
    type: Literal["EXEC_SQL"] = "EXEC_SQL"
    subsystem: str = "SQL"
    raw_payload: str = Field(default="", validation_alias=AliasChoices("rawPayload", "raw_payload", "rawSql"))


class ExecCicsStatementNode(StatementNode):
    type: Literal["EXEC_CICS"] = "EXEC_CICS"
    subsystem: str = "CICS"
    raw_payload: str = Field(default="", validation_alias=AliasChoices("rawPayload", "raw_payload", "rawCics"))


class ExecSqlImsStatementNode(StatementNode):
    type: Literal["EXEC_SQLIMS"] = "EXEC_SQLIMS"
    subsystem: str = "SQLIMS"
    raw_payload: str = Field(default="", validation_alias=AliasChoices("rawPayload", "raw_payload", "rawSqlIms"))


class GenericStatementNode(StatementNode):
    """
    Open-ended container for standard COBOL statements (e.g., SORT, RELEASE,
    RETURN, ALTER, USE) and dialect extensions that do not require dedicated
    sub-AST branching models.
    """
    type: Literal["UNKNOWN"] = "UNKNOWN"
    details: Dict[str, Any] = Field(default_factory=dict)

    @property
    def verb(self) -> str:
        """Returns the original COBOL verb (e.g. 'SORT', 'RELEASE', 'ALTER')."""
        return str(self.details.get("original_type") or self.type)


# Set of statement types with dedicated Pydantic subclass models
_SPECIALIZED_STATEMENT_TYPES = {
    "MOVE", "PERFORM", "IF", "EVALUATE", "CALL", "COMPUTE",
    "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "READ", "WRITE",
    "REWRITE", "DELETE", "OPEN", "CLOSE", "START", "GO_TO",
    "STOP", "GOBACK", "EXIT", "CONTINUE", "DISPLAY", "ACCEPT",
    "INITIALIZE", "SET", "STRING", "UNSTRING", "INSPECT", "SEARCH",
    "EXEC_SQL", "EXEC_CICS", "EXEC_SQLIMS", "UNKNOWN",
}


def _normalize_statement_dict(stmt: Any) -> Any:
    """
    Normalizes statement dictionaries before Pydantic validation.
    Maps unspecialized verbs to GenericStatementNode while logging the fallback.
    """
    if isinstance(stmt, dict):
        raw_type = stmt.get("type", "UNKNOWN")
        if raw_type not in _SPECIALIZED_STATEMENT_TYPES:
            loc = stmt.get("location")
            loc_str = f"lines {loc.get('startLine')}-{loc.get('endLine')}" if isinstance(loc, dict) else "unknown location"
            logger.info(
                "Statement verb '%s' at %s mapped to open GenericStatementNode fallback.",
                raw_type,
                loc_str,
            )
            details = stmt.setdefault("details", {})
            if isinstance(details, dict):
                details.setdefault("original_type", raw_type)
            stmt["type"] = "UNKNOWN"
    return stmt


# Type Alias for Polymorphic Statements using Pydantic v2 Discriminated Union
AnyStatementNode = Annotated[
    Union[
        MoveStatementNode,
        PerformStatementNode,
        IfStatementNode,
        EvaluateStatementNode,
        CallStatementNode,
        ComputeStatementNode,
        AddStatementNode,
        SubtractStatementNode,
        MultiplyStatementNode,
        DivideStatementNode,
        ReadStatementNode,
        WriteStatementNode,
        RewriteStatementNode,
        DeleteStatementNode,
        OpenStatementNode,
        CloseStatementNode,
        StartStatementNode,
        GoToStatementNode,
        StopStatementNode,
        GobackStatementNode,
        ExitStatementNode,
        ContinueStatementNode,
        DisplayStatementNode,
        AcceptStatementNode,
        InitializeStatementNode,
        SetStatementNode,
        StringStatementNode,
        UnstringStatementNode,
        InspectStatementNode,
        SearchStatementNode,
        ExecSqlStatementNode,
        ExecCicsStatementNode,
        ExecSqlImsStatementNode,
        GenericStatementNode,
    ],
    Field(discriminator="type"),
]

# Category aliases
ArithmeticStatementNode = Union[AddStatementNode, SubtractStatementNode, MultiplyStatementNode, DivideStatementNode, ComputeStatementNode]
IoStatementNode = Union[ReadStatementNode, WriteStatementNode, RewriteStatementNode, DeleteStatementNode, OpenStatementNode, CloseStatementNode, StartStatementNode]
BranchStatementNode = Union[GoToStatementNode, StopStatementNode, GobackStatementNode, ExitStatementNode, ContinueStatementNode]
EmbeddedSubsystemNode = Union[ExecSqlStatementNode, ExecCicsStatementNode, ExecSqlImsStatementNode]

_statement_adapter = None


def parse_statement(data: Dict[str, Any]) -> AnyStatementNode:
    """Helper to deserialize any statement dictionary into its concrete Pydantic model."""
    global _statement_adapter
    if _statement_adapter is None:
        from pydantic import TypeAdapter
        _statement_adapter = TypeAdapter(AnyStatementNode)
    norm_data = _normalize_statement_dict(data)
    return _statement_adapter.validate_python(norm_data)
