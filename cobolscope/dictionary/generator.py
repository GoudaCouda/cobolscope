"""
Data Dictionary Generator for COBOL Programs.
Transforms Canonical IR DataDivision models into rich, business-analyst and
developer-grade data dictionaries across Markdown, HTML, CSV, and JSON formats.
"""

from __future__ import annotations
import csv
import io
import json
from typing import List, Dict, Optional, Any, Set, Tuple, Union
from pathlib import Path

import jinja2

from cobolscope.models import (
    ProgramModel,
    DataDictionary,
    DataField,
    Condition88,
    FileControlEntry,
    FileDescriptionEntry,
)


# ---------------------------------------------------------
# Logical / Business Type Inference
# ---------------------------------------------------------

def infer_logical_type(field: DataField) -> str:
    """
    Translates raw COBOL PIC and USAGE into human-readable logical business types.
    Examples:
      - PIC X(30) DISPLAY -> Alphanumeric(30)
      - PIC S9(7)V99 COMP-3 -> Decimal(9, 2) Packed
      - PIC 9(4) COMP -> SmallInt (16-bit)
      - Group with children -> Group
    """
    if field.children:
        if field.occurs_max and field.occurs_max > 1:
            return f"Group Array [{field.occurs_max}]"
        return "Group"

    pic = (field.pic or "").upper().strip()
    usage = (field.usage or "DISPLAY").upper().replace("-", "_")

    if not pic:
        if usage in ("POINTER", "PROCEDURE_POINTER"):
            return "Memory Pointer (4 bytes)"
        if usage == "INDEX":
            return "Table Index (4 bytes)"
        if usage == "COMP_1":
            return "Float (Single Precision, 4 bytes)"
        if usage == "COMP_2":
            return "Double (Double Precision, 8 bytes)"
        return "Group" if field.children else "Elementary"

    # Analyze PIC string
    is_signed = "S" in pic
    has_decimal = "V" in pic or "." in pic

    # Count integer and decimal digits
    if has_decimal:
        parts = pic.split("V") if "V" in pic else pic.split(".")
        int_part = _expand_pic(parts[0])
        dec_part = _expand_pic(parts[1]) if len(parts) > 1 else ""
        int_digits = _count_digits(int_part)
        dec_digits = _count_digits(dec_part)
        total_digits = int_digits + dec_digits
    else:
        expanded = _expand_pic(pic)
        int_digits = _count_digits(expanded)
        dec_digits = 0
        total_digits = int_digits

    # Check for text/alphanumeric
    if "X" in pic or "A" in pic:
        expanded = _expand_pic(pic)
        length = len(expanded)
        return f"Alphanumeric ({length} chars)"

    # Numeric & Computational types
    if usage in ("COMP_3", "PACKED_DECIMAL"):
        sign_str = "Signed " if is_signed else ""
        if has_decimal:
            return f"{sign_str}Decimal({total_digits}, {dec_digits}) Packed"
        return f"{sign_str}Integer({total_digits}) Packed"

    if usage in ("COMP", "COMP_4", "COMP_5", "BINARY"):
        sign_str = "Signed " if is_signed else "Unsigned "
        if total_digits <= 4:
            return f"{sign_str}SmallInt (16-bit Binary)"
        elif total_digits <= 9:
            return f"{sign_str}Integer (32-bit Binary)"
        else:
            return f"{sign_str}BigInt (64-bit Binary)"

    if usage == "COMP_1":
        return "Float (Single Precision, 4 bytes)"
    if usage == "COMP_2":
        return "Double (Double Precision, 8 bytes)"

    # Display numeric
    sign_str = "Signed " if is_signed else ""
    if has_decimal:
        return f"{sign_str}Decimal Display ({total_digits}, {dec_digits})"
    return f"{sign_str}Numeric Display ({total_digits} digits)"


def _expand_pic(pic: str) -> str:
    res = []
    i = 0
    while i < len(pic):
        c = pic[i]
        if c == '(':
            close = pic.find(')', i)
            if close != -1 and res:
                num_str = pic[i + 1:close].strip()
                prev = res[-1]
                try:
                    count = int(num_str)
                    res.extend([prev] * (count - 1))
                except ValueError:
                    pass
                i = close + 1
                continue
        res.append(c)
        i += 1
    return "".join(res)


def _count_digits(expanded: str) -> int:
    return sum(1 for c in expanded if c in "9Z*+-$")


# ---------------------------------------------------------
# Flattened Row Model for Dictionary Exporters
# ---------------------------------------------------------

class DictionaryRow:
    def __init__(
        self,
        section: str,
        level: int,
        name: str,
        id: str,
        qualified_name: str,
        logical_type: str,
        pic: str,
        usage: str,
        byte_offset: int,
        relative_offset: int,
        byte_length: int,
        occurs_str: str,
        redefines: str,
        value: str,
        conditions_88: List[Dict[str, Any]],
        references: List[str],
        is_filler: bool,
        depth: int,
    ):
        self.section = section
        self.level = level
        self.name = name
        self.id = id
        self.qualified_name = qualified_name
        self.logical_type = logical_type
        self.pic = pic
        self.usage = usage
        self.byte_offset = byte_offset
        self.relative_offset = relative_offset
        self.byte_length = byte_length
        self.occurs_str = occurs_str
        self.redefines = redefines
        self.value = value
        self.conditions_88 = conditions_88
        self.references = references
        self.is_filler = is_filler
        self.depth = depth

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section": self.section,
            "level": self.level,
            "name": self.name,
            "id": self.id,
            "qualified_name": self.qualified_name,
            "logical_type": self.logical_type,
            "pic": self.pic,
            "usage": self.usage,
            "byte_offset": self.byte_offset,
            "relative_offset": self.relative_offset,
            "byte_length": self.byte_length,
            "occurs": self.occurs_str,
            "redefines": self.redefines,
            "initial_value": self.value,
            "conditions_88": self.conditions_88,
            "references": self.references,
            "is_filler": self.is_filler,
        }


# ---------------------------------------------------------
# Jinja2 Template Environment & Helpers
# ---------------------------------------------------------

def _create_jinja_env() -> jinja2.Environment:
    """Initializes a Jinja2 template environment with loaders and custom filters."""
    try:
        loader = jinja2.PackageLoader("cobolscope", "templates")
    except Exception:
        loader = jinja2.FileSystemLoader(str(Path(__file__).resolve().parent.parent / "templates"))

    env = jinja2.Environment(
        loader=loader,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def format_bytes(val: Any) -> str:
        try:
            return f"{int(val):,} bytes"
        except (ValueError, TypeError):
            return f"{val} bytes"

    def format_md_pic_usage(r: DictionaryRow) -> str:
        pic_usage = f"`{r.pic}`" if r.pic else f"*{r.usage}*"
        if r.pic and r.usage != "DISPLAY":
            pic_usage += f"<br/>*{r.usage}*"
        return pic_usage

    def format_md_attributes(r: DictionaryRow) -> str:
        attrs = []
        if r.redefines:
            attrs.append(f"<mark>REDEFINES {r.redefines}</mark>")
        if r.occurs_str:
            attrs.append(f"**OCCURS:** {r.occurs_str}")
        if r.value:
            attrs.append(f"**Default:** `{r.value}`")
        for c in r.conditions_88:
            vals_str = ", ".join(f"'{v}'" if not v.startswith("'") else v for v in c["values"])
            attrs.append(f"• `88 {c['name']}`: {vals_str}")
        return "<br/>".join(attrs) if attrs else "—"

    def format_md_references(r: DictionaryRow) -> str:
        if not r.references:
            return "—"
        if len(r.references) <= 3:
            return ", ".join(f"`{ref}`" for ref in r.references)
        return f"{', '.join(f'`{ref}`' for ref in r.references[:2])} *(+{len(r.references)-2} more)*"

    env.filters["format_bytes"] = format_bytes
    env.filters["format_md_pic_usage"] = format_md_pic_usage
    env.filters["format_md_attributes"] = format_md_attributes
    env.filters["format_md_references"] = format_md_references

    return env


_jinja_env: Optional[jinja2.Environment] = None


def get_jinja_env() -> jinja2.Environment:
    """Returns the cached Jinja2 environment singleton."""
    global _jinja_env
    if _jinja_env is None:
        _jinja_env = _create_jinja_env()
    return _jinja_env


# ---------------------------------------------------------
# Data Dictionary Collector & Exporter
# ---------------------------------------------------------

class DataDictionaryGenerator:
    """Generates comprehensive multi-format data dictionaries from a ProgramModel."""

    def __init__(self, program: ProgramModel, hide_fillers: bool = False):
        self.program = program
        self.hide_fillers = hide_fillers
        self.usage_index = program.get_field_usage_index()
        self.rows: List[DictionaryRow] = []
        self._collect_rows()

    def _collect_rows(self) -> None:
        dd = self.program.data_dictionary

        # 1. FILE SECTION
        for fd in dd.file_section:
            sec_name = f"FILE: {fd.name}"
            for rec in fd.records:
                self._traverse_field(rec, sec_name, depth=0)

        # 2. WORKING-STORAGE SECTION
        for field in dd.working_storage_section:
            self._traverse_field(field, "WORKING-STORAGE", depth=0)

        # 3. LINKAGE SECTION
        for field in dd.linkage_section:
            self._traverse_field(field, "LINKAGE", depth=0)

        # 4. LOCAL-STORAGE SECTION
        for field in dd.local_storage_section:
            self._traverse_field(field, "LOCAL-STORAGE", depth=0)

    def _traverse_field(self, field: DataField, section: str, depth: int) -> None:
        if self.hide_fillers and field.is_filler:
            return

        occurs_str = ""
        if field.occurs_max:
            if field.occurs_min and field.occurs_min != field.occurs_max:
                occurs_str = f"{field.occurs_min} TO {field.occurs_max}"
            else:
                occurs_str = str(field.occurs_max)
            if field.depending_on:
                occurs_str += f" (DEPENDING ON {field.depending_on})"
            if field.indexed_by:
                occurs_str += f" [INDEXED BY {', '.join(field.indexed_by)}]"

        c88_list = [{"name": c.name, "values": c.values} for c in field.conditions_88]

        # References
        refs = self.usage_index.get(field.id or "", [])
        clean_refs = [r for r in refs if not r.startswith("SECTION:")]

        row = DictionaryRow(
            section=section,
            level=field.level,
            name=field.name,
            id=field.id or "",
            qualified_name=field.qualified_name or field.name,
            logical_type=infer_logical_type(field),
            pic=field.pic or "",
            usage=field.usage or "DISPLAY",
            byte_offset=field.byte_offset,
            relative_offset=field.relative_offset,
            byte_length=field.byte_length,
            occurs_str=occurs_str,
            redefines=field.redefines or "",
            value=field.value or "",
            conditions_88=c88_list,
            references=clean_refs,
            is_filler=field.is_filler,
            depth=depth,
        )
        self.rows.append(row)

        for child in field.children:
            self._traverse_field(child, section, depth + 1)

    def _build_context(self) -> Dict[str, Any]:
        """Assembles data context for Jinja2 template rendering."""
        total_fields = len(self.rows)
        total_88s = sum(len(r.conditions_88) for r in self.rows)
        total_redefines = sum(1 for r in self.rows if r.redefines)
        ws_bytes = sum(
            r.byte_length
            for r in self.rows
            if r.section == "WORKING-STORAGE" and r.level == 1 and not r.redefines
        )

        sections: Dict[str, List[DictionaryRow]] = {}
        for r in self.rows:
            sections.setdefault(r.section, []).append(r)

        available_sections = list(sections.keys())
        available_types = sorted({r.logical_type for r in self.rows if r.logical_type})

        return {
            "program": self.program,
            "summary": {
                "total_fields": total_fields,
                "total_88s": total_88s,
                "total_redefines": total_redefines,
                "ws_bytes": ws_bytes,
            },
            "file_controls": self.program.data_dictionary.file_controls if hasattr(self.program.data_dictionary, 'file_controls') else [],
            "sections": sections,
            "rows": self.rows,
            "available_sections": available_sections,
            "available_types": available_types,
        }

    def to_markdown(self) -> str:
        """Renders GitHub Flavored Markdown documentation via Jinja2."""
        env = get_jinja_env()
        template = env.get_template("data_dictionary.md.j2")
        return template.render(self._build_context())

    def to_html(self) -> str:
        """Renders an interactive, searchable standalone HTML data dictionary via Jinja2."""
        env = get_jinja_env()
        template = env.get_template("data_dictionary.html.j2")
        return template.render(self._build_context())

    def to_csv(self) -> str:
        """Renders flat CSV table suitable for spreadsheet import."""
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow([
            "Section",
            "Level",
            "Field Name",
            "Field ID",
            "Qualified Path",
            "Logical Type",
            "PIC",
            "USAGE",
            "Byte Offset",
            "Relative Offset",
            "Byte Length",
            "Occurs",
            "Redefines",
            "Initial Value",
            "Level 88 Conditions",
            "Referencing Paragraphs",
            "Is Filler",
        ])

        for r in self.rows:
            conds_str = "; ".join(f"{c['name']} = {','.join(c['values'])}" for c in r.conditions_88)
            refs_str = "; ".join(r.references)
            writer.writerow([
                r.section,
                r.level,
                r.name,
                r.id,
                r.qualified_name,
                r.logical_type,
                r.pic,
                r.usage,
                r.byte_offset,
                r.relative_offset,
                r.byte_length,
                r.occurs_str,
                r.redefines,
                r.value,
                conds_str,
                refs_str,
                r.is_filler,
            ])
        return output.getvalue()

    def to_json(self, indent: int = 2) -> str:
        """Renders structured JSON representation."""
        data = {
            "program_id": self.program.program_id,
            "source_file": self.program.source_file_path,
            "fields": [r.to_dict() for r in self.rows],
        }
        return json.dumps(data, indent=indent)


# ---------------------------------------------------------
# Convenience Pipeline Functions
# ---------------------------------------------------------

def generate_data_dictionary(
    source_or_model: ProgramModel | str | Path,
    format: str = "markdown",
    hide_fillers: bool = False,
    output_path: Optional[str | Path] = None,
) -> str:
    """
    High-level entry point to generate a data dictionary in any format.
    Accepts a ProgramModel, COBOL source file path, or JSON file path.
    """
    if isinstance(source_or_model, ProgramModel):
        model = source_or_model
    else:
        path = Path(source_or_model)
        if path.suffix.lower() == ".json":
            model = ProgramModel.from_json(path.read_text(encoding="utf-8"))
        else:
            from cobolscope.parser import parse
            data = parse(str(path))
            model = ProgramModel.from_dict(data)

    gen = DataDictionaryGenerator(model, hide_fillers=hide_fillers)
    fmt = format.lower().strip()

    if fmt in ("md", "markdown"):
        content = gen.to_markdown()
    elif fmt == "html":
        content = gen.to_html()
    elif fmt == "csv":
        content = gen.to_csv()
    elif fmt == "json":
        content = gen.to_json()
    else:
        raise ValueError(f"Unknown format '{format}'. Supported: markdown, html, csv, json")

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")

    return content
