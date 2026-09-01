"""
Hardened GnuCOBOL Compiler Ground-Truth Parity Test Suite.
Resolves duplicate field collisions, verifies FILLER allocations,
and scales across multiple golden fixtures.
"""

import sys
from pathlib import Path
from typing import Dict, Tuple

repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.data_dictionary import DataDictionaryGenerator
from tests.harness.gnucobol_runner import GnuCobolRunner, GnuCobolListing


IBM_Z_FIXTURES = (
    "GETCOMPY",
    "GETSCODE",
)

HANDWRITTEN_FIXTURES = ("TEST-COMPLEX-LAYOUT",)


def verify_single_program_parity(
    cobol_path: Path, listing_path: Path, copybook_dir: Path | None = None
):
    print(f"\n--- Auditing: {cobol_path.name} ---")

    # 1. Parse AST
    raw_dict = parse(
        str(cobol_path),
        format="FIXED",
        copybook_dirs=[copybook_dir] if copybook_dir else None,
        ignore_syntax_errors=True,
    )
    model = ProgramModel.from_dict(raw_dict)

    # Keep fillers to detect immediate offset drift
    gen = DataDictionaryGenerator(model, hide_fillers=False)

    # 2. Key our model entries by (line_number, field_name) to avoid collisions
    # Fallback to qualified_name if line number is absent in your AST
    model_field_map: Dict[Tuple[int, str], Tuple[int, int]] = {}
    for r in gen.rows:
        line_no = getattr(r, "line_number", 0)
        clean_name = r.name.upper() if r.name else "FILLER"
        model_field_map[(line_no, clean_name)] = (r.byte_offset, r.byte_length)

    # 3. Retrieve GnuCOBOL Listing
    assert listing_path.exists(), f"Missing golden GnuCOBOL listing: {listing_path}"
    listing = GnuCobolRunner.parse_listing_output(
        listing_path.read_text(encoding="utf-8"), source_file=str(cobol_path)
    )
    assert listing.fields, f"No data fields parsed from golden listing: {listing_path}"

    # 4. Compare using composite identities
    # GnuCOBOL symbol tables provide definition lines for disambiguation
    matched_count = 0
    for sym_name, gnu_field in listing.fields.items():
        sym_name = sym_name.upper()
        sym_line = getattr(gnu_field, "line_number", 0)
        composite_key = (sym_line, sym_name)

        # Disambiguation resolution
        if composite_key in model_field_map:
            my_offset, my_len = model_field_map[composite_key]
        elif sym_name in [k[1] for k in model_field_map]:
            # Fallback to name-only match if line numbers aren't populated by runner
            candidates = [v for k, v in model_field_map.items() if k[1] == sym_name]
            assert len(candidates) == 1, (
                f"Collision: Ambiguous duplicate field '{sym_name}' detected on multiple lines! "
                f"Runner must populate line_number to verify."
            )
            my_offset, my_len = candidates[0]
        else:
            raise AssertionError(f"Symbol '{sym_name}' (line {sym_line}) missing in generated dictionary!")

        # Layout parity assertions
        assert my_offset == gnu_field.byte_offset, (
            f"Offset mismatch on '{sym_name}' (line {sym_line}): "
            f"GnuCOBOL={gnu_field.byte_offset}, Parser={my_offset}"
        )
        assert my_len == gnu_field.byte_length, (
            f"Length mismatch on '{sym_name}' (line {sym_line}): "
            f"GnuCOBOL={gnu_field.byte_length}, Parser={my_len}"
        )
        matched_count += 1

    print(f"  [OK] Verified {matched_count} fields against compiler output without collisions.")


def test_gnucobol_compiler_parity():
    fixture_dir = Path("tests/fixtures")
    golden_dir = fixture_dir / "gnucobol_golden_listings"
    source_dir = fixture_dir / "bank_of_z" / "cobol"
    copybook_dir = fixture_dir / "bank_of_z" / "copy"

    for fixture_name in IBM_Z_FIXTURES:
        verify_single_program_parity(
            source_dir / f"{fixture_name}.cbl",
            golden_dir / f"{fixture_name}.listing.txt",
            copybook_dir,
        )
    for fixture_name in HANDWRITTEN_FIXTURES:
        verify_single_program_parity(
            fixture_dir / f"{fixture_name}.cbl",
            golden_dir / f"{fixture_name}.listing.txt",
        )

    print("\n[PASSED] All compiler ground-truth checks passed.")


def regenerate_golden_listings():
    """Refresh Bank of Z layout goldens with an installed GnuCOBOL compiler."""
    runner = GnuCobolRunner()
    fixture_dir = repo_root / "tests" / "fixtures"
    source_dir = fixture_dir / "bank_of_z" / "cobol"
    copybook_dir = fixture_dir / "bank_of_z" / "copy"
    golden_dir = fixture_dir / "gnucobol_golden_listings"
    for fixture_name in IBM_Z_FIXTURES:
        output = runner.write_xref_listing(
            source_dir / f"{fixture_name}.cbl",
            golden_dir / f"{fixture_name}.listing.txt",
            copybook_dirs=[copybook_dir],
            # These IBM samples contain EXEC CICS statements. GnuCOBOL still
            # emits the data symbol table used by this layout-only oracle.
            allow_syntax_errors=True,
        )
        print(f"[WROTE] {output.relative_to(repo_root)}")
    for fixture_name in HANDWRITTEN_FIXTURES:
        output = runner.write_xref_listing(
            fixture_dir / f"{fixture_name}.cbl",
            golden_dir / f"{fixture_name}.listing.txt",
        )
        print(f"[WROTE] {output.relative_to(repo_root)}")


if __name__ == "__main__":
    if "--regenerate-goldens" in sys.argv:
        regenerate_golden_listings()
    else:
        test_gnucobol_compiler_parity()
