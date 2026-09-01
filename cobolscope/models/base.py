"""
Base coordinate, enum, and primitive types for COBOL AST IR.
"""

from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class SourceLocation(BaseModel):
    """Tracks the exact line/token coordinate span in the raw source."""
    model_config = ConfigDict(populate_by_name=True)

    start_line: int = Field(default=0, validation_alias=AliasChoices("startLine", "start_line"))
    end_line: int = Field(default=0, validation_alias=AliasChoices("endLine", "end_line"))
    start_column: int = Field(default=0, validation_alias=AliasChoices("startColumn", "start_column"))
    end_column: int = Field(default=0, validation_alias=AliasChoices("endColumn", "end_column"))
    source_file: str = Field(default="", validation_alias=AliasChoices("sourceFile", "source_file"))


class FieldUsage(str, Enum):
    DISPLAY = "DISPLAY"
    COMP = "COMP"
    COMP_1 = "COMP_1"
    COMP_2 = "COMP_2"
    COMP_3 = "COMP_3"
    COMP_4 = "COMP_4"
    COMP_5 = "COMP_5"
    BINARY = "BINARY"
    PACKED_DECIMAL = "PACKED_DECIMAL"
    POINTER = "POINTER"
    INDEX = "INDEX"
    PROCEDURE_POINTER = "PROCEDURE_POINTER"
    UNKNOWN = "UNKNOWN"
