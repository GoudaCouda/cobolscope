"""
NIST COBOL-85 Standard Conformance Verification Test Suite.
Executes the ProLeap IR pipeline, Data Dictionary engine, Mathematical Invariant suite,
and Native ASG auditor against official NIST COBOL-85 standard test programs (tests/nistcobol85/src).
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import List

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.data_dictionary import DataDictionaryGenerator
from tests.harness.invariants import DataDictionaryValidator
from tests.harness.asg_auditor import AsgSemanticAuditor


def sanitize_nist_lines(lines: List[str]) -> List[str]:
    """
    NIST CCVS85 test programs and copybooks use conditional compilation flags in column 7
    (e.g., 'S', 'Y', 'N', 'A', 'B', 'C', 'G') that are not standard COBOL indicators.
    Normalizes non-standard column 7 characters to spaces for standard COBOL-85 lexing.
    """
    clean = []
    for line in lines:
        if len(line) > 6:
            indicator = line[6]
            if indicator not in (" ", "-", "*", "/", "D", "d"):
                clean.append(line[:6] + " " + line[7:])
            else:
                clean.append(line)
        else:
            clean.append(line)
    return clean


def sanitize_nist_indicators(source_path: Path) -> Path:
    """Preprocesses a single NIST COBOL source file into a temporary clean file."""
    lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
    clean_lines = sanitize_nist_lines(lines)

    tf = tempfile.NamedTemporaryFile(suffix=".CBL", delete=False, mode="w", encoding="utf-8")
    tf.write("\n".join(clean_lines))
    tf.close()
    return Path(tf.name)


def prepare_clean_copybook_dir(src_dir: Path, out_dir: Path) -> None:
    """Creates normalized copies of all .CPY copybooks in a clean temporary directory."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for cpy_file in src_dir.glob("*.CPY"):
        lines = cpy_file.read_text(encoding="utf-8", errors="replace").splitlines()
        clean = sanitize_nist_lines(lines)
        (out_dir / cpy_file.name).write_text("\n".join(clean), encoding="utf-8")
    for cpy_file in src_dir.glob("*.cpy"):
        lines = cpy_file.read_text(encoding="utf-8", errors="replace").splitlines()
        clean = sanitize_nist_lines(lines)
        (out_dir / cpy_file.name).write_text("\n".join(clean), encoding="utf-8")


def run_nist_program_test(nist_filename: str, clean_copybook_dir: Path):
    print(f"\n========================================================")
    print(f"NIST COBOL-85 Conformance Test: {nist_filename}")
    print(f"========================================================")

    nist_src_dir = Path("tests/nistcobol85/src")
    source_file = nist_src_dir / nist_filename

    assert source_file.exists(), f"NIST test file not found: {source_file}"

    # 1. Preprocess NIST indicators if needed
    clean_file = sanitize_nist_indicators(source_file)

    try:
        # 2. Parse using ProLeap with copybook resolution
        raw_dict = parse(
            str(clean_file),
            format="FIXED",
            copybook_dirs=[str(clean_copybook_dir)],
            copybook_exts=["CPY", "cpy", "CBL", "cbl"],
            ignore_syntax_errors=True,
        )
        assert isinstance(raw_dict, dict), "Parser returned invalid response"

        # 3. Build Canonical IR ProgramModel
        model = ProgramModel.from_dict(raw_dict)
        print(f"  Program ID:         {model.program_id}")
        print(f"  Working Storage:    {len(model.data_dictionary.working_storage_section)} root records")
        print(f"  Paragraphs:         {len(model.paragraphs)}")
        print(f"  Sections:           {len(model.sections)}")
        stmt_count = sum(len(p.statements) for p in model.paragraphs)
        print(f"  Total Statements:   {stmt_count}")

        # 4. Run Mathematical Invariants
        validator = DataDictionaryValidator()
        violations = validator.validate(model)
        error_violations = [v for v in violations if v.severity == "ERROR"]
        assert len(error_violations) == 0, f"Found {len(error_violations)} invariant errors: {error_violations}"
        print(f"  [OK] Mathematical Invariants Verified (0 errors).")

        # 5. Run Native ASG Semantic Audit
        auditor = AsgSemanticAuditor(model, clean_file)
        asg_violations = auditor.audit_all()
        assert len(asg_violations) == 0, f"Found {len(asg_violations)} ASG semantic violations: {asg_violations}"
        print(f"  [OK] Native ASG Completeness & CFG Integrity Verified.")

        # 6. Generate Data Dictionary
        gen = DataDictionaryGenerator(model, hide_fillers=False)
        print(f"  [OK] Data Dictionary Generated ({len(gen.rows)} variables mapped).")

        print(f"[PASSED] NIST Conformance Test Passed for {nist_filename}")

    finally:
        if clean_file.exists():
            clean_file.unlink()


def test_nist_suite():
    # Curated representative selection across key NIST COBOL-85 modules:
    # NC: Nucleus
    # SQ: Sequential I/O
    # IX: Indexed I/O
    # RL: Relative I/O
    # ST: Sort / Merge
    # SM: Source Text Manipulation
    # IC: Inter-Program Communication
    # DB: Debug Module
    # IF: Intrinsic Functions
    test_programs = [
        "NC101A.CBL",  # Nucleus Level 1 Core
        "NC102A.CBL",  # Nucleus Level 1 Arithmetic & Control
        "NC103A.CBL",  # Nucleus Level 1 Conditions & Perform
        "SQ102A.CBL",  # Sequential I/O Level 1
        "IX101A.CBL",  # Indexed I/O Level 1 Key Processing
        "RL101A.CBL",  # Relative I/O Level 1
        "ST101A.CBL",  # Sort / Merge Level 1
        "SM101A.CBL",  # Source Text Manipulation & Copy
        "IC101A.CBL",  # Inter-Program Calls & Linkage
        "DB101A.CBL",  # Debug Module
        "IF101A.CBL",  # Intrinsic Functions
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        clean_cpy_dir = Path(tmpdir) / "copybooks"
        prepare_clean_copybook_dir(Path("tests/nistcobol85/src"), clean_cpy_dir)

        passed_count = 0
        for prog in test_programs:
            try:
                run_nist_program_test(prog, clean_cpy_dir)
                passed_count += 1
            except Exception as e:
                print(f"FAILED on NIST test {prog}: {e}")
                raise

    print(f"\n========================================================")
    print(f"ALL {passed_count}/{len(test_programs)} NIST COBOL-85 CONFORMANCE TESTS PASSED 100%!")
    print(f"========================================================\n")


if __name__ == "__main__":
    test_nist_suite()
