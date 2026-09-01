"""
Stress-Test Gauntlet and Automated Mathematical Invariant Verification Suite.
Tests the Data Dictionary and memory layout engine against synthetic edge cases
and verifies compiler ground-truth binary offsets and mathematical invariants.
"""

import sys
from pathlib import Path
from typing import Dict, Tuple

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.data_dictionary import DataDictionaryGenerator
from tests.harness.invariants import DataDictionaryValidator, InvariantViolation


# Exact binary layout ground-truth specification for TEST-DATA-DICT.cbl
EXPECTED_GAUNTLET_OFFSETS: Dict[str, Tuple[int, int]] = {
    # 1. Types Record (Base offset 0, Total 55 bytes)
    "WS-TYPES-RECORD": (0, 55),
    "WS-STR-ALPHANUM": (0, 10),
    "WS-NUM-DISPLAY": (10, 7),
    "WS-COMP-1-FLOAT": (17, 4),
    "WS-COMP-2-FLOAT": (21, 8),
    "WS-COMP-HALFWORD": (29, 2),
    "WS-COMP-FULLWORD": (31, 4),
    "WS-COMP-DOUBLEWORD": (35, 8),
    "WS-COMP3-PACKED-EVEN": (43, 4),  # S9(6) COMP-3: ceil(7/2) = 4 bytes
    "WS-COMP3-PACKED-ODD": (47, 4),   # S9(7) COMP-3: ceil(8/2) = 4 bytes
    "WS-PTR-ADDR": (51, 4),           # POINTER = 4 bytes

    # 2. Overlays & REDEFINES Trees (Base offset 55, Total 12 bytes)
    "WS-BASE-RECORD": (55, 12),
    "WS-RAW-DATE": (55, 8),
    "WS-DATE-PARTS": (55, 8),          # REDEFINES WS-RAW-DATE at offset 55
    "WS-YEAR": (55, 4),                # First child of overlay at offset 55
    "WS-MONTH": (59, 2),               # Second child at offset 59
    "WS-DAY": (61, 2),                 # Third child at offset 61
    "WS-NEXT-FIELD": (63, 4),          # Next sibling resumes at base end (55 + 8 = 63)

    # 3. Multidimensional Arrays (Base offset 67, Total 456 bytes)
    # One month = 3 (name) + 31 (days) + 4 (amt) = 38 bytes. 12 months = 38 * 12 = 456 bytes.
    "WS-MATRIX-RECORD": (67, 456),
    "WS-MONTHS": (67, 456),
    "WS-MONTH-NAME": (67, 3),
    "WS-DAYS": (70, 31),
    "WS-TOTAL-AMT": (101, 4),

    # 4. Level-88 Flags (Base offset 523, Total 1 byte)
    "WS-STATUS-FLAG": (523, 1),
}


from typing import Optional, Dict
from tests.harness.test_cache import get_test_model


def test_gauntlet_program(model: Optional[ProgramModel] = None):
    print(f"\n========================================================")
    print(f"Running Gauntlet Program Invariants (TEST-DATA-DICT.cbl)")
    print(f"========================================================")

    gauntlet_path = "tests/fixtures/TEST-DATA-DICT.cbl"
    if model is None:
        model = get_test_model(gauntlet_path)

    # 1. Run Automated Invariant Checks
    validator = DataDictionaryValidator()
    violations = validator.validate(model)
    error_violations = [v for v in violations if v.severity == "ERROR"]

    if error_violations:
        print(f"FAILED: Found {len(error_violations)} invariant errors:")
        for v in error_violations:
            print(f"   {v}")
        assert False, f"{len(error_violations)} invariant errors in gauntlet program!"
    else:
        print("  [OK] All 4 Mathematical Invariants validated with 0 errors on Gauntlet Program.")

    # 2. Extract Data Dictionary and build offset map
    gen = DataDictionaryGenerator(model, hide_fillers=False)
    actual_offsets: Dict[str, Tuple[int, int]] = {}
    for r in gen.rows:
        actual_offsets[r.name.upper()] = (r.byte_offset, r.byte_length)

    # 3. Assert exact Ground-Truth parity for every single variable
    print("\n  Auditing Exact Binary Offset & Length Ground Truth:")
    for var_name, (exp_offset, exp_len) in EXPECTED_GAUNTLET_OFFSETS.items():
        assert var_name in actual_offsets, f"Missing expected variable in dictionary: {var_name}"
        act_offset, act_len = actual_offsets[var_name]
        assert act_offset == exp_offset, (
            f"Offset mismatch on {var_name}: expected offset {exp_offset}, got {act_offset}"
        )
        assert act_len == exp_len, (
            f"Length mismatch on {var_name}: expected length {exp_len}, got {act_len}"
        )
        print(f"    [OK] {var_name:<24}: Offset={act_offset:<4} Length={act_len:<4}")

    # 4. Check Level-88 Condition Names on WS-STATUS-FLAG
    flag_row = next((r for r in gen.rows if r.name == "WS-STATUS-FLAG"), None)
    assert flag_row is not None, "WS-STATUS-FLAG row missing in dictionary"
    assert len(flag_row.conditions_88) == 3, f"Expected 3 Level-88 rules, got {len(flag_row.conditions_88)}"
    c88_map = {c["name"]: c["values"] for c in flag_row.conditions_88}
    assert "IS-VALID" in c88_map, "IS-VALID rule missing"
    assert "IS-INVALID" in c88_map, "IS-INVALID rule missing"
    assert "IS-UNKNOWN" in c88_map, "IS-UNKNOWN rule missing"
    print("  [OK] Level-88 Condition Rules verified on WS-STATUS-FLAG.")

    print(f"[PASSED] Gauntlet Stress-Test Program Passed 100%!")


def test_production_invariants(models_map: Optional[Dict[str, ProgramModel]] = None):
    print(f"\n========================================================")
    print(f"Running Invariant Suite on Production Codebases")
    print(f"========================================================")

    prod_files = [
        "tests/fixtures/TEST-DATA-DICT.cbl",
        "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
        "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
        "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
        "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
        "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
    ]

    validator = DataDictionaryValidator()
    for pf in prod_files:
        model = models_map.get(pf) if models_map else get_test_model(pf)
        violations = validator.validate(model)
        error_violations = [v for v in violations if v.severity == "ERROR"]
        assert len(error_violations) == 0, f"Found {len(error_violations)} invariant errors in {pf}: {error_violations}"
        print(f"  [OK] {pf:<24}: 0 Invariant Errors (Validated across all sections)")

    print(f"[PASSED] Production Codebase Invariant Checks Passed 100%!")


if __name__ == "__main__":
    test_gauntlet_program()
    test_production_invariants()

    print("\n========================================================")
    print("ALL GAUNTLET & INVARIANT CHECKS PASSED 100%!")
    print("========================================================\n")
