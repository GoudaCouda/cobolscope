"""
Data Division Domain Models: DataField, Condition88, FileControlEntry, FileDescriptionEntry, DataDictionary.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from .base import SourceLocation


class Condition88(BaseModel):
    """Represents Level-88 condition names and valid value intervals."""
    model_config = ConfigDict(populate_by_name=True)

    name: str = ""
    values: List[str] = Field(default_factory=list)
    location: Optional[SourceLocation] = None


class DataField(BaseModel):
    """
    Hierarchical representation of a variable or record structure.
    Carries memory layout (absolute and relative byte offsets),
    deterministic IDs, qualified naming paths, and structural overlays.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = None
    qualified_name: Optional[str] = Field(default=None, validation_alias=AliasChoices("qualifiedName", "qualified_name"))
    level: int = 1
    name: str = "FILLER"
    pic: Optional[str] = None
    usage: str = "DISPLAY"
    value: Optional[str] = None

    # Memory Layout Specs (Precomputed upstream during ingestion)
    byte_offset: int = Field(default=0, validation_alias=AliasChoices("byteOffset", "byte_offset"))
    relative_offset: int = Field(default=0, validation_alias=AliasChoices("relativeOffset", "relative_offset"))
    byte_length: int = Field(default=0, validation_alias=AliasChoices("byteLength", "byte_length"))
    element_byte_length: int = Field(default=0, validation_alias=AliasChoices("elementByteLength", "element_byte_length"))
    logical_type: Optional[str] = Field(default=None, validation_alias=AliasChoices("logicalType", "logical_type"))

    # Structural Bindings
    redefines: Optional[str] = None
    occurs_min: Optional[int] = Field(default=None, validation_alias=AliasChoices("occursMin", "occurs_min"))
    occurs_max: Optional[int] = Field(default=None, validation_alias=AliasChoices("occursMax", "occurs_max"))
    depending_on: Optional[str] = Field(default=None, validation_alias=AliasChoices("dependingOn", "depending_on"))
    indexed_by: List[str] = Field(default_factory=list, validation_alias=AliasChoices("indexedBy", "indexed_by"))

    # Flags
    is_filler: bool = Field(default=False, validation_alias=AliasChoices("isFiller", "is_filler"))
    is_justified: bool = Field(default=False, validation_alias=AliasChoices("isJustified", "is_justified"))
    is_blank_when_zero: bool = Field(default=False, validation_alias=AliasChoices("isBlankWhenZero", "is_blank_when_zero"))
    is_synchronized: bool = Field(default=False, validation_alias=AliasChoices("isSynchronized", "is_synchronized"))
    is_sign_separate: bool = Field(default=False, validation_alias=AliasChoices("isSignSeparate", "is_sign_separate"))

    location: Optional[SourceLocation] = None
    conditions: List[Condition88] = Field(default_factory=list, validation_alias=AliasChoices("conditions", "conditions88", "conditions_88"))
    children: List[DataField] = Field(default_factory=list)

    @property
    def conditions_88(self) -> List[Condition88]:
        return self.conditions


class FileControlEntry(BaseModel):
    """SELECT ... ASSIGN file mapping entry in ENVIRONMENT DIVISION."""
    model_config = ConfigDict(populate_by_name=True)

    select_name: str = Field(default="", validation_alias=AliasChoices("selectName", "select_name"))
    assign_to: Optional[str] = Field(default=None, validation_alias=AliasChoices("assignTo", "assign_to"))
    file_status: Optional[str] = Field(default=None, validation_alias=AliasChoices("fileStatus", "file_status"))
    organization: Optional[str] = None
    access_mode: Optional[str] = Field(default=None, validation_alias=AliasChoices("accessMode", "access_mode"))


class FileDescriptionEntry(BaseModel):
    """FD / SD entry in DATA DIVISION with record layout children."""
    model_config = ConfigDict(populate_by_name=True)

    name: str = ""
    is_external: bool = Field(default=False, validation_alias=AliasChoices("isExternal", "is_external"))
    is_global: bool = Field(default=False, validation_alias=AliasChoices("isGlobal", "is_global"))
    block_contains: Optional[str] = Field(default=None, validation_alias=AliasChoices("blockContains", "block_contains"))
    record_contains: Optional[str] = Field(default=None, validation_alias=AliasChoices("recordContains", "record_contains"))
    records: List[DataField] = Field(default_factory=list)


class DataDictionary(BaseModel):
    """Complete logical index of all data items declared across memory sections."""
    model_config = ConfigDict(populate_by_name=True)

    file_controls: List[FileControlEntry] = Field(default_factory=list, validation_alias=AliasChoices("fileControls", "file_controls"))
    working_storage_section: List[DataField] = Field(default_factory=list, validation_alias=AliasChoices("workingStorageSection", "working_storage_section"))
    linkage_section: List[DataField] = Field(default_factory=list, validation_alias=AliasChoices("linkageSection", "linkage_section"))
    local_storage_section: List[DataField] = Field(default_factory=list, validation_alias=AliasChoices("localStorageSection", "local_storage_section"))
    file_section: List[FileDescriptionEntry] = Field(default_factory=list, validation_alias=AliasChoices("fileSection", "file_section"))
    working_storage_bytes: int = Field(default=0, validation_alias=AliasChoices("workingStorageBytes", "working_storage_bytes"))
