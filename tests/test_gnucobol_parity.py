"""
GnuCOBOL Compiler Ground-Truth Parity Test Suite.
Validates our Canonical IR Data Dictionary and byte layout calculations against
GnuCOBOL (cobc -std=ibm -Xref) compiler listings for local and CI/CD automated testing.
"""

import json
import sys
from pathlib import Path

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.data_dictionary import DataDictionaryGenerator
from tests.harness.gnucobol_runner import GnuCobolRunner, GnuCobolListing


def test_gnucobol_compiler_parity():
    print(f"\n========================================================")
    print(f"GnuCOBOL (cobc -std=ibm -Xref) Compiler Parity Test")
    print(f"========================================================")

    cobol_file = "tests/fixtures/TEST-DATA-DICT.cbl"
    fixture_listing = Path("tests/fixtures/gnucobol_golden_listings/TEST-DATA-DICT.listing.txt")

    # 1. Parse using our ProLeap Pipeline
    raw_dict = parse(cobol_file, format="FIXED", ignore_syntax_errors=True)
    model = ProgramModel.from_dict(raw_dict)
    gen = DataDictionaryGenerator(model, hide_fillers=False)

    my_offsets = {r.name.upper(): (r.byte_offset, r.byte_length) for r in gen.rows if r.name != "FILLER"}

    # 2. Obtain GnuCOBOL Compiler Listing (Live cobc if available, else Golden Listing)
    runner = GnuCobolRunner()
    if runner.is_available():
        version_str = runner.get_version() or "GnuCOBOL"
        print(f"  [FOUND] Live GnuCOBOL compiler detected: {version_str}")
        print("  Running: cobc -fsyntax-only -std=ibm -ftsymbols -Xref -T ...")
        listing = runner.run_xref(cobol_file, std="ibm")
    else:
        print("  [INFO] Live 'cobc' not found on PATH. Falling back to GnuCOBOL 3.2 Golden Listing Fixture.")
        assert fixture_listing.exists(), f"Golden listing fixture missing: {fixture_listing}"
        raw_text = fixture_listing.read_text(encoding="utf-8")
        listing = GnuCobolRunner.parse_listing_output(raw_text, source_file=cobol_file)

    print(f"  Extracted {len(listing.fields)} symbols from GnuCOBOL compiler listing.\n")

    # 3. Assert 100% Compiler Parity for every symbol
    for sym_name, gnu_field in listing.fields.items():
        assert sym_name in my_offsets, f"Variable '{sym_name}' from GnuCOBOL listing missing in ProLeap Data Dictionary!"
        my_offset, my_len = my_offsets[sym_name]

        assert my_offset == gnu_field.byte_offset, (
            f"Offset mismatch on '{sym_name}': GnuCOBOL={gnu_field.byte_offset}, ProLeap={my_offset}"
        )
        assert my_len == gnu_field.byte_length, (
            f"Length mismatch on '{sym_name}': GnuCOBOL={gnu_field.byte_length}, ProLeap={my_len}"
        )
        print(f"    [MATCH] {sym_name:<24}: GnuCOBOL=({gnu_field.byte_offset:<4}, {gnu_field.byte_length:<4}) == ProLeap=({my_offset:<4}, {my_len:<4})")

    print(f"\n[PASSED] 100% GnuCOBOL Compiler Ground-Truth Parity Verified!")


if __name__ == "__main__":
    test_gnucobol_compiler_parity()

    print("\n========================================================")
    print("ALL GNUCOBOL COMPILER PARITY TESTS PASSED 100%! ")
    print("========================================================\n")
