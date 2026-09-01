import json
import sys
from pathlib import Path
from cobolscope.parser import parse
from cobolscope.models import (
    ProgramModel,
    MoveStatementNode,
    PerformStatementNode,
    IfStatementNode,
    CallStatementNode,
    IoStatementNode,
    BranchStatementNode,
    DataField,
)

from typing import Optional
from tests.harness.test_cache import get_test_model

def test_program(file_path_str: str, model: Optional[ProgramModel] = None):
    print(f"\n==========================================")
    print(f"Testing: {file_path_str}")
    print(f"==========================================")

    if model is None:
        model = get_test_model(file_path_str)
    print(f"Program ID: {model.program_id}")
    print(f"Working Storage Fields: {len(model.data_dictionary.working_storage_section)}")
    print(f"Paragraphs: {len(model.paragraphs)}")
    print(f"Sections: {len(model.sections)}")

    # Check fallthroughs and terminal status
    for p in model.paragraphs:
        print(f"  Paragraph '{p.name}': called_by={p.called_by}, successors={p.successors}, terminal={p.is_terminal}, fallthrough={p.fallthrough_successor}")

    # Check fast symbol indexing
    if model.data_dictionary.working_storage_section:
        first_ws = model.data_dictionary.working_storage_section[0]
        found = model.find_field(first_ws.name)
        assert found is not None, f"Could not find field {first_ws.name}"
        assert found.name == first_ws.name

    # Check field usage index
    usage_index = model.get_field_usage_index()
    print(f"Indexed variable references: {len(usage_index)} fields referenced across code")
    for fid, callers in list(usage_index.items())[:5]:
        print(f"    {fid} -> {callers}")

    # Verify statement typing
    stmt_count = 0
    dfg_sources = 0
    dfg_targets = 0
    for p in model.paragraphs:
        for stmt in p.statements:
            stmt_count += 1
            if stmt.source_field_ids:
                dfg_sources += len(stmt.source_field_ids)
            if stmt.target_field_ids:
                dfg_targets += len(stmt.target_field_ids)

    print(f"Total Statements: {stmt_count}, Total DFG Source Refs: {dfg_sources}, Total DFG Target Refs: {dfg_targets}")
    print(f"[PASSED] {file_path_str}")

if __name__ == "__main__":
    test_files = [
        "tests/fixtures/TEST-DATA-DICT.cbl",
        "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
        "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
        "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
        "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
        "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
    ]
    for tf in test_files:
        test_program(tf)
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
