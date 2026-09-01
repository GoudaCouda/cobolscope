"""
Unified Test Runner for ProLeap CLI Verification Suite.
Orchestrates all 6 verification tiers, sharing pre-parsed in-memory models across all test suites
for lightning-fast regression testing (~10-15s total suite execution).
"""

import sys
import time
from pathlib import Path
from typing import Dict

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.models import ProgramModel
from tests.harness.test_cache import get_test_model
from tests.test_pipeline import test_program
from tests.test_data_dictionary import verify_program_dictionary
from tests.test_invariants import test_gauntlet_program, test_production_invariants
from tests.test_asg_parity import audit_program
from tests.test_call_graph import verify_program_call_graph
from tests.test_gnucobol_parity import test_gnucobol_compiler_parity

TEST_FILES = [
    "tests/fixtures/TEST-DATA-DICT.cbl",
    "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
    "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
    "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
    "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
    "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
]

PROD_FILES = [
    "tests/fixtures/TEST-DATA-DICT.cbl",
    "tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl",
    "tests/fixtures/bank_of_z/cobol/INQCUST.cbl",
    "tests/fixtures/bank_of_z/cobol/INQACC.cbl",
    "tests/fixtures/bank_of_z/cobol/UPDACC.cbl",
    "tests/fixtures/bank_of_z/cobol/XFRFUN.cbl",
]


def run_all_tiers():
    total_start = time.time()
    tier_timings = {}

    print("================================================================================")
    print("                COBOLSCOPE - UNIFIED VERIFICATION SUITE                         ")
    print("================================================================================")

    # 0. Session Model Warming (Loads from tests/.cache or parses once)
    print("\n>>> Warming In-Memory Program Models...")
    warm_start = time.time()
    models: Dict[str, ProgramModel] = {}
    for tf in TEST_FILES:
        models[tf] = get_test_model(tf)
    warm_dur = time.time() - warm_start
    print(f"    [LOADED] {len(models)} Program Models cached in {warm_dur:.2f}s.\n")

    # Tier 1: Canonical AST Pipeline Tests
    t0 = time.time()
    print(">>> Running Tier 1: Canonical AST IR & DFG Pipeline Tests...")
    for pf in PROD_FILES:
        test_program(pf, model=models[pf])
    tier_timings["Tier 1: AST IR Pipeline"] = time.time() - t0

    # Tier 2: Data Dictionary & Memory Layout Reconcilers
    t0 = time.time()
    print("\n>>> Running Tier 2: Data Dictionary & Memory Layout Reconciliation...")
    for pf in PROD_FILES:
        verify_program_dictionary(pf, model=models[pf])
    tier_timings["Tier 2: Data Dictionary"] = time.time() - t0

    # Tier 3: Mathematical Invariant Audits
    t0 = time.time()
    print("\n>>> Running Tier 3: Mathematical Invariant Audits...")
    test_gauntlet_program(model=models["tests/fixtures/TEST-DATA-DICT.cbl"])
    test_production_invariants(models_map=models)
    tier_timings["Tier 3: Mathematical Invariants"] = time.time() - t0

    # Tier 4: Native ProLeap ASG Parity Audits
    t0 = time.time()
    print("\n>>> Running Tier 4: Native ProLeap ASG Semantic Parity...")
    for tf in TEST_FILES:
        audit_program(tf, model=models[tf])
    tier_timings["Tier 4: ASG Semantic Parity"] = time.time() - t0

    # Tier 5: Level-2 Procedure Call Graph & Visual Pipeline
    t0 = time.time()
    print("\n>>> Running Tier 5: Level-2 Call Graph & Visual Exporters...")
    for pf in PROD_FILES:
        verify_program_call_graph(pf, model=models[pf])
    tier_timings["Tier 5: Call Graph & Visuals"] = time.time() - t0

    # Tier 6: GnuCOBOL Compiler Parity
    t0 = time.time()
    print("\n>>> Running Tier 6: GnuCOBOL Compiler Parity...")
    test_gnucobol_compiler_parity()
    tier_timings["Tier 6: GnuCOBOL Parity"] = time.time() - t0

    total_dur = time.time() - total_start

    # Final Summary Table
    print("\n" + "=" * 80)
    print("                       VERIFICATION SUITE SUMMARY                               ")
    print("=" * 80)
    for name, dur in tier_timings.items():
        print(f"  [PASSED]  {name:<45} : {dur:6.2f}s")
    print("-" * 80)
    print(f"  TOTAL DURATION                                        : {total_dur:6.2f}s")
    print("=" * 80)
    print("  STATUS: 100% OF ALL TIERS AND INVARIANTS PASSED SUCCESSFULLY!\n")


if __name__ == "__main__":
    run_all_tiers()
