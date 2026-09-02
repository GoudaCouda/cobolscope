"""
Comprehensive Verification Test Suite for the Data Dictionary Generator.
Ensures 100% data integrity, memory layout reconciliation, Level-88 rule preservation,
and procedure cross-reference parity between scanned AST models and generated dictionaries.
"""

import csv
import io
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

from cobolscope.parser import parse
from cobolscope.models import ProgramModel, DataField
from cobolscope.data_dictionary import (
    DataDictionaryGenerator,
    generate_data_dictionary,
    infer_logical_type,
)


def collect_all_fields_from_model(model: ProgramModel) -> List[tuple[str, DataField, int]]:
    """Walks the entire ProgramModel DataDictionary and collects every DataField with section and depth."""
    results: List[tuple[str, DataField, int]] = []

    def walk(fields: List[DataField], section_name: str, depth: int):
        for f in fields:
            results.append((section_name, f, depth))
            walk(f.children, section_name, depth + 1)

    dd = model.data_dictionary
    for fd in dd.file_section:
        walk(fd.records, f"FILE: {fd.name}", 0)
    walk(dd.working_storage_section, "WORKING-STORAGE", 0)
    walk(dd.linkage_section, "LINKAGE", 0)
    walk(dd.local_storage_section, "LOCAL-STORAGE", 0)

    return results


from typing import List, Dict, Any, Set, Optional
from tests.harness.test_cache import get_test_model


def verify_program_dictionary(cobol_file: str, model: Optional[ProgramModel] = None):
    print(f"\n========================================================")
    print(f"Auditing Data Dictionary Integrity for: {cobol_file}")
    print(f"========================================================")

    # 1. Get canonical IR model
    if model is None:
        model = get_test_model(cobol_file)
    scanned_fields = collect_all_fields_from_model(model)
    print(f"Scanned total DataFields in Model: {len(scanned_fields)}")

    # 2. Instantiate generator
    gen_all = DataDictionaryGenerator(model, hide_fillers=False)
    print(f"Extracted rows in Data Dictionary: {len(gen_all.rows)}")

    # --- Test 1: Total Count Parity ---
    assert len(gen_all.rows) == len(scanned_fields), (
        f"Row count mismatch! Expected {len(scanned_fields)}, got {len(gen_all.rows)}"
    )

    # --- Test 2: 1:1 Attribute Reconciliation ---
    usage_index = model.get_field_usage_index()
    for idx, (expected_sec, expected_field, expected_depth) in enumerate(scanned_fields):
        row = gen_all.rows[idx]

        # Check section & hierarchy
        assert row.section == expected_sec, f"Section mismatch at index {idx}: {row.section} != {expected_sec}"
        assert row.level == expected_field.level, f"Level mismatch at index {idx}: {row.level} != {expected_field.level}"
        assert row.name == expected_field.name, f"Name mismatch at index {idx}: {row.name} != {expected_field.name}"
        assert row.id == (expected_field.id or ""), f"ID mismatch at index {idx}: {row.id} != {expected_field.id}"
        assert row.qualified_name == (expected_field.qualified_name or expected_field.name), (
            f"Qualified name mismatch at index {idx}: {row.qualified_name} != {expected_field.qualified_name}"
        )
        assert row.depth == expected_depth, f"Depth mismatch at index {idx}: {row.depth} != {expected_depth}"
        assert row.is_filler == expected_field.is_filler, f"is_filler mismatch at index {idx}"

        # Check memory layout alignment
        assert row.byte_offset == expected_field.byte_offset, (
            f"Byte offset mismatch for '{row.name}' ({row.id}): dict={row.byte_offset}, model={expected_field.byte_offset}"
        )
        assert row.relative_offset == expected_field.relative_offset, (
            f"Relative offset mismatch for '{row.name}': dict={row.relative_offset}, model={expected_field.relative_offset}"
        )
        assert row.byte_length == expected_field.byte_length, (
            f"Byte length mismatch for '{row.name}': dict={row.byte_length}, model={expected_field.byte_length}"
        )

        # Check COBOL attributes
        assert row.pic == (expected_field.pic or ""), f"PIC mismatch for '{row.name}'"
        assert row.usage == (expected_field.usage or "DISPLAY"), f"Usage mismatch for '{row.name}'"
        assert row.redefines == (expected_field.redefines or ""), f"Redefines mismatch for '{row.name}'"
        assert row.value == (expected_field.value or ""), f"Value mismatch for '{row.name}'"
        assert row.logical_type == expected_field.logical_type, f"Logical type mismatch for '{row.name}': {row.logical_type} != {expected_field.logical_type}"
        assert row.element_byte_length == (expected_field.element_byte_length or expected_field.byte_length), f"Element byte length mismatch for '{row.name}'"

        # Check Level-88 preservation
        assert len(row.conditions_88) == len(expected_field.conditions_88), (
            f"Level-88 count mismatch for '{row.name}': dict={len(row.conditions_88)}, model={len(expected_field.conditions_88)}"
        )
        for c_idx, c88 in enumerate(expected_field.conditions_88):
            row_c88 = row.conditions_88[c_idx]
            assert row_c88["name"] == c88.name, f"Condition88 name mismatch: {row_c88['name']} != {c88.name}"
            assert row_c88["values"] == c88.values, f"Condition88 values mismatch: {row_c88['values']} != {c88.values}"

        # Check procedure references cross-reference parity
        expected_refs = usage_index.get(expected_field.id or "", [])
        assert row.references == expected_refs, (
            f"References mismatch for '{row.name}': dict={row.references}, model={expected_refs}"
        )

    # Validate authoritative working_storage_bytes if working storage exists
    if model.data_dictionary.working_storage_section:
        assert model.data_dictionary.working_storage_bytes > 0, "working_storage_bytes should be > 0"

    print("  [OK] 1:1 Attribute and memory layout reconciliation verified.")

    # --- Test 3: REDEFINES Overlay Integrity ---
    redefines_count = 0
    for row in gen_all.rows:
        if row.redefines:
            redefines_count += 1
            # Find redefined target field in the same section/record
            target_field = None
            for s_name, f, depth in scanned_fields:
                if s_name == row.section and f.name == row.redefines:
                    if f.byte_offset == row.byte_offset:
                        target_field = f
                        break
            if target_field is None:
                target_field = model.find_field(row.redefines)

            assert target_field is not None, f"Target of REDEFINES '{row.redefines}' not found in model!"
            assert row.byte_offset == target_field.byte_offset, (
                f"Overlay offset error for '{row.name}' REDEFINES '{row.redefines}': "
                f"redefining offset ({row.byte_offset}) != target offset ({target_field.byte_offset})"
            )
    print(f"  [OK] {redefines_count} REDEFINES memory overlays validated with exact base offset alignment.")

    # --- Test 4: Exporter Format Parity ---
    # JSON export validation
    json_str = gen_all.to_json()
    json_data = json.loads(json_str)
    assert json_data["program_id"] == model.program_id
    assert len(json_data["fields"]) == len(gen_all.rows)
    for idx, f_dict in enumerate(json_data["fields"]):
        assert f_dict["id"] == gen_all.rows[idx].id
        assert f_dict["byte_offset"] == gen_all.rows[idx].byte_offset
        assert f_dict["byte_length"] == gen_all.rows[idx].byte_length
    print("  [OK] JSON export reconciled with 100% parity.")

    # CSV export validation
    csv_str = gen_all.to_csv()
    reader = csv.DictReader(io.StringIO(csv_str))
    csv_rows = list(reader)
    assert len(csv_rows) == len(gen_all.rows)
    for idx, c_row in enumerate(csv_rows):
        assert c_row["Field ID"] == gen_all.rows[idx].id
        assert int(c_row["Byte Offset"]) == gen_all.rows[idx].byte_offset
        assert int(c_row["Byte Length"]) == gen_all.rows[idx].byte_length
        assert c_row["Logical Type"] == gen_all.rows[idx].logical_type
    print("  [OK] CSV export parsed and reconciled with 100% parity.")

    # Markdown export validation
    md_str = gen_all.to_markdown()
    assert f"# Data Dictionary: `{model.program_id}`" in md_str
    assert "## Executive Summary" in md_str
    # Verify every non-empty field name is present in Markdown
    for row in gen_all.rows:
        if row.name and row.name != "FILLER":
            assert f"`{row.name}`" in md_str, f"Field `{row.name}` missing in Markdown output!"
    print("  [OK] Markdown documentation table structure verified.")

    # HTML export validation
    html_str = gen_all.to_html()
    assert f"<title>Data Dictionary - {model.program_id}</title>" in html_str
    assert "id=\"dictTableBody\"" in html_str
    print("  [OK] HTML interactive report verified.")

    # --- Test 5: "Hide Fillers" Filtering Accuracy ---
    total_fillers = sum(1 for _, f, _ in scanned_fields if f.is_filler)
    gen_no_fillers = DataDictionaryGenerator(model, hide_fillers=True)
    expected_no_fillers = len(scanned_fields) - total_fillers
    assert len(gen_no_fillers.rows) == expected_no_fillers, (
        f"Hide fillers count error: expected {expected_no_fillers}, got {len(gen_no_fillers.rows)}"
    )
    for row in gen_no_fillers.rows:
        assert not row.is_filler, f"Found unexpected filler row in hide_fillers=True: {row.name} ({row.id})"
    print(f"  [OK] 'Hide Fillers' filter verified ({total_fillers} filler fields cleanly excluded).")

    print(f"[PASSED] Data Dictionary Integrity Test for {cobol_file}")


if __name__ == "__main__":
    test_programs = [
        "tests/fixtures/TEST-DATA-DICT.cbl",
        "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
        "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
        "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
        "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
        "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
    ]
    for prog in test_programs:
        verify_program_dictionary(prog)

    print("\n========================================================")
    print("ALL DATA DICTIONARY RECONCILIATION TESTS PASSED 100%!")
    print("========================================================\n")
