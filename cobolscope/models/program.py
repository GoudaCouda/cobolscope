"""
Root ProgramModel for COBOL AST IR.
Provides fast O(1) hash indexing, field lookup, qualification resolution, and serialization.
"""

from __future__ import annotations
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator, AliasChoices
from .data import DataField, DataDictionary
from .statements import AnyStatementNode, EvaluateStatementNode
from .procedure import SectionNode, ParagraphNode, AsgAuditSummary


import re as _re

_PROLEAP_CE_TAG = _re.compile(r"\*>CE\s*", _re.IGNORECASE)


def _sanitize_id_field(value: Optional[str]) -> Optional[str]:
    """
    Strip ProLeap *>CE annotation markers from IDENTIFICATION DIVISION metadata fields.

    ProLeap represents the text of AUTHOR., DATE-WRITTEN., etc. paragraphs verbatim
    including any `*>CE ... *>CE` inline comment delimiters it inserts.  We remove
    those tokens here at the IR boundary so that the clean human-readable value
    propagates everywhere (templates, JSON export, etc.) without ad-hoc filtering.

    Examples:
        "*>CE Jon Collett. *>CE"  ->  "Jon Collett."
        "*>CE 2023-01-01 *>CE"   ->  "2023-01-01"
        "Jon Collett."            ->  "Jon Collett."   (no-op)
    """
    if not value:
        return value
    cleaned = _PROLEAP_CE_TAG.sub("", value).strip().rstrip(".")
    # Collapse any internal runs of whitespace left by stripping
    cleaned = " ".join(cleaned.split())
    return cleaned if cleaned else None


class ProgramModel(BaseModel):
    """The root canonical Intermediate Representation (IR) container."""
    model_config = ConfigDict(populate_by_name=True)

    program_id: str = Field(default="", validation_alias=AliasChoices("programId", "program_id"))
    author: Optional[str] = None
    installation: Optional[str] = None
    date_written: Optional[str] = Field(default=None, validation_alias=AliasChoices("dateWritten", "date_written"))
    date_compiled: Optional[str] = Field(default=None, validation_alias=AliasChoices("dateCompiled", "date_compiled"))
    source_file_path: str = Field(default="", validation_alias=AliasChoices("sourceFile", "source_file_path", "source_file"))
    format: str = "FIXED"
    data_dictionary: DataDictionary = Field(default_factory=DataDictionary, validation_alias=AliasChoices("dataDictionary", "data_dictionary"))
    sections: List[SectionNode] = Field(default_factory=list)
    paragraphs: List[ParagraphNode] = Field(default_factory=list)
    asg_audit_summary: Optional[AsgAuditSummary] = Field(default=None, validation_alias=AliasChoices("asgAuditSummary", "asg_audit_summary"))

    # Precomputed in-memory indices for O(1) lookups
    _field_id_map: Dict[str, DataField] = PrivateAttr(default_factory=dict)
    _field_name_map: Dict[str, List[DataField]] = PrivateAttr(default_factory=dict)
    _field_qualified_map: Dict[str, DataField] = PrivateAttr(default_factory=dict)
    _paragraph_map: Dict[str, ParagraphNode] = PrivateAttr(default_factory=dict)
    _field_usage_index: Dict[str, List[str]] = PrivateAttr(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_paragraphs(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalise paragraphs dict -> list
            paras = data.get("paragraphs")
            if isinstance(paras, dict):
                data["paragraphs"] = list(paras.values())
            # Strip *>CE markers from all IDENTIFICATION DIVISION text fields
            for key in ("author", "installation", "dateWritten", "date_written",
                        "dateCompiled", "date_compiled"):
                if key in data:
                    data[key] = _sanitize_id_field(data[key])
        return data

    def model_post_init(self, __context: Any) -> None:
        self._rebuild_indices()

    def _rebuild_indices(self) -> None:
        """Constructs fast O(1) hash indices for fields, paragraphs, and variable usages."""
        field_id_map: Dict[str, DataField] = {}
        field_name_map: Dict[str, List[DataField]] = {}
        field_qualified_map: Dict[str, DataField] = {}

        def index_field(f: DataField):
            if f.id:
                field_id_map[f.id] = f
            uname = f.name.upper().strip()
            if uname not in field_name_map:
                field_name_map[uname] = []
            field_name_map[uname].append(f)
            if f.qualified_name:
                field_qualified_map[f.qualified_name.upper().strip()] = f
            for child in f.children:
                index_field(child)

        for ws in self.data_dictionary.working_storage_section:
            index_field(ws)
        for lk in self.data_dictionary.linkage_section:
            index_field(lk)
        for ls in self.data_dictionary.local_storage_section:
            index_field(ls)
        for fd in self.data_dictionary.file_section:
            for rec in fd.records:
                index_field(rec)

        self._field_id_map = field_id_map
        self._field_name_map = field_name_map
        self._field_qualified_map = field_qualified_map
        self._paragraph_map = {p.name.upper().strip(): p for p in self.paragraphs}

        # Build comprehensive field usage index covering paragraphs and section statements
        usage: Dict[str, List[str]] = {}

        def scan_stmts(stmts: List[AnyStatementNode], container_name: str):
            for stmt in stmts:
                fids = getattr(stmt, "target_field_ids", None) or []
                srcs = getattr(stmt, "source_field_ids", None) or []
                for fid in fids + srcs:
                    if fid not in usage:
                        usage[fid] = []
                    if container_name not in usage[fid]:
                        usage[fid].append(container_name)
                # Scan nested blocks
                nested = getattr(stmt, "nested_statements", None) or []
                then_s = getattr(stmt, "then_statements", None) or []
                else_s = getattr(stmt, "else_statements", None) or []
                if nested or then_s or else_s:
                    scan_stmts(nested + then_s + else_s, container_name)
                if isinstance(stmt, EvaluateStatementNode):
                    for wb in stmt.when_branches:
                        scan_stmts(wb.statements, container_name)
                    scan_stmts(stmt.when_other_statements, container_name)

        for p in self.paragraphs:
            if p.section_parent and p.section_parent.strip().upper() != p.name.strip().upper():
                ref_label = f"{p.section_parent.strip()} > {p.name.strip()}"
            else:
                ref_label = p.name.strip()
            scan_stmts(p.statements, ref_label)

        for s in self.sections:
            if s.statements:
                scan_stmts(s.statements, s.name.strip())

        self._field_usage_index = usage

    @property
    def paragraphs_map(self) -> Dict[str, ParagraphNode]:
        """Dictionary index for fast paragraph lookup by name."""
        return self._paragraph_map

    def get_paragraph(self, name: str) -> Optional[ParagraphNode]:
        """Retrieve paragraph by name in O(1) time."""
        return self._paragraph_map.get(name.upper().strip())

    def get_next_paragraph(self, current: Union[str, ParagraphNode]) -> Optional[ParagraphNode]:
        """Returns the physically subsequent paragraph in source execution order."""
        curr_name = current.name if isinstance(current, ParagraphNode) else current
        curr_name = curr_name.upper().strip()
        for i, p in enumerate(self.paragraphs):
            if p.name.upper().strip() == curr_name:
                if i + 1 < len(self.paragraphs):
                    return self.paragraphs[i + 1]
                return None
        return None

    def get_field_usage_index(self) -> Dict[str, List[str]]:
        """Returns the precomputed field usage index in O(1) time."""
        return self._field_usage_index

    def get_field_references(self, field_id_or_name: str) -> List[ParagraphNode]:
        """Returns all ParagraphNode instances that reference the specified field in O(1) time."""
        para_names = self._field_usage_index.get(field_id_or_name, [])
        if not para_names:
            f = self.find_field(field_id_or_name)
            if f and f.id:
                para_names = self._field_usage_index.get(f.id, [])
        paras: List[ParagraphNode] = []
        for name in para_names:
            if name.startswith("SECTION:"):
                continue
            p = self.get_paragraph(name)
            if p:
                paras.append(p)
        return paras

    def find_fields(self, name: str) -> List[DataField]:
        """Find all field definitions matching the given simple name in O(1) time."""
        return self._field_name_map.get(name.upper().strip(), [])

    def find_field(self, name_or_path: str) -> Optional[DataField]:
        """
        Find a field using either a simple name or a qualified path.
        Supports:
          - Qualified path: "WS-CUSTOMER-RECORD.WS-CUST-ID"
          - COBOL qualification: "WS-CUST-ID OF WS-CUSTOMER-RECORD"
          - Simple name: "WS-CUST-ID" (returns first match)
        """
        clean_path = name_or_path.strip()

        # Convert "FIELD OF PARENT" into "PARENT.FIELD"
        if " OF " in clean_path.upper() or " IN " in clean_path.upper():
            parts = [p.strip() for p in clean_path.replace(" in ", " OF ").replace(" IN ", " OF ").split(" OF ")]
            clean_path = ".".join(reversed(parts))

        target = clean_path.upper()

        # 1. Exact match on qualified path
        if target in self._field_qualified_map:
            return self._field_qualified_map[target]

        # 2. Match on field ID
        if target in self._field_id_map:
            return self._field_id_map[target]

        # 3. Match on simple name
        simple_matches = self._field_name_map.get(target)
        if simple_matches:
            return simple_matches[0]

        # 4. Suffix match on qualified path (e.g. "RECORD.FIELD")
        target_suffix = "." + target
        for qname, field in self._field_qualified_map.items():
            if qname.endswith(target_suffix):
                return field

        return None

    def to_json(self, indent: int = 2) -> str:
        """Serializes the canonical IR into formatted JSON."""
        return self.model_dump_json(indent=indent, by_alias=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProgramModel:
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str) -> ProgramModel:
        return cls.model_validate_json(json_str)
