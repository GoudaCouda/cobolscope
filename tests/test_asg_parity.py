"""
Objective ProLeap ASG Semantic Parity & Graph Cross-Validation Test Suite.
Validates that our emitted Canonical IR, Data Dictionary, and Graph structures
faithfully preserve 100% of ProLeap's native ASG metamodel and token coordinates.
"""

import sys
from pathlib import Path

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from typing import Optional
from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from tests.harness.asg_auditor import AsgSemanticAuditor
from tests.harness.test_cache import get_test_model


def audit_program(cobol_file: str, model: Optional[ProgramModel] = None):
    print(f"\n========================================================")
    print(f"Auditing Native ASG Semantic Parity for: {cobol_file}")
    print(f"========================================================")

    # 1. Obtain model from cache or parse
    if model is None:
        model = get_test_model(cobol_file)

    audit_summary = model.asg_audit_summary
    assert audit_summary is not None, "ASG Audit Summary missing in ProgramModel!"

    print(f"  Native ASG Ground-Truth:")
    print(f"    - Total Data Entries:      {audit_summary.total_asg_data_entries}")
    print(f"    - Total Level-88 Entries:  {audit_summary.total_asg_level88_entries}")
    print(f"    - Total Paragraphs:        {audit_summary.total_asg_paragraphs}")
    print(f"    - Total Statements:        {audit_summary.total_asg_statements}")
    print(f"    - Total ASG Calls:         {audit_summary.total_asg_calls}")

    # 2. Run Comprehensive ASG Semantic Audits
    auditor = AsgSemanticAuditor(model, cobol_file)
    violations = auditor.audit_all()

    if violations:
        print(f"FAILED: Found {len(violations)} ASG semantic violations:")
        for v in violations:
            print(f"   [VIOLATION] {v}")
        assert False, f"{len(violations)} ASG semantic violations found in {cobol_file}!"

    print(f"  [OK] 100% ASG Metamodel Completeness Verified (Zero Dropped Nodes).")
    print(f"  [OK] 100% CFG Successor & Fallthrough Integrity Verified.")
    print(f"[PASSED] ASG Semantic Parity Verified for {cobol_file}")


test_program_asg_semantic_parity = audit_program


def test_all_programs():
    test_files = [
        "tests/fixtures/TEST-DATA-DICT.cbl",
        "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
        "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
        "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
        "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
        "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
    ]

    for tf in test_files:
        test_program_asg_semantic_parity(tf)

    print("\n========================================================")
    print("ALL NATIVE PROLEAP ASG SEMANTIC AUDITS PASSED 100%!")
    print("========================================================\n")


if __name__ == "__main__":
    test_all_programs()
