"""
GnuCOBOL (cobc) Compiler Bridge and Listing Parser Test Harness.
Enables fast, local, and CI/CD automated ground-truth compiler testing
without requiring mainframe credentials.
"""

from __future__ import annotations
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class GnuCobolField:
    name: str
    level: int
    pic: str = ""
    usage: str = "DISPLAY"
    byte_offset: int = 0
    byte_length: int = 0
    line_num: int = 0
    section: str = ""
    redefines: str = ""
    occurs: Optional[int] = None


@dataclass
class GnuCobolListing:
    program_id: str
    source_file: str
    fields: Dict[str, GnuCobolField] = field(default_factory=dict)
    symbols: List[str] = field(default_factory=list)
    raw_output: str = ""

    def get_field(self, name: str) -> Optional[GnuCobolField]:
        return self.fields.get(name.upper().strip())


class GnuCobolRunner:
    """
    Invokes GnuCOBOL (cobc) with standard IBM compatibility flags (-std=ibm -ftsymbols -Xref)
    and parses the compiler symbol table to extract ground-truth memory offsets and lengths.
    """

    KNOWN_COBC_PATHS = [
        r"C:\GnuCOBOL\bin\cobc.exe",
        r"C:\GnuCOBOL\bin\cobc",
        r"C:\Program Files\GnuCOBOL\bin\cobc.exe",
        r"C:\Program Files (x86)\GnuCOBOL\bin\cobc.exe",
        "/usr/bin/cobc",
        "/usr/local/bin/cobc",
        "/opt/homebrew/bin/cobc",
    ]

    def __init__(self, cobc_path: Optional[str] = None):
        self.cobc_path = self._find_cobc(cobc_path)
        self.env = self._build_env()

    def _find_cobc(self, explicit: Optional[str] = None) -> Optional[str]:
        if explicit and Path(explicit).exists():
            return str(Path(explicit).resolve())

        from_env = os.environ.get("COBC_PATH") or os.environ.get("GNUCOBOL_BIN")
        if from_env and Path(from_env).exists():
            return str(Path(from_env).resolve())

        which_path = shutil.which("cobc")
        if which_path:
            return which_path

        for candidate in self.KNOWN_COBC_PATHS:
            if Path(candidate).exists():
                return str(Path(candidate).resolve())

        return None

    def _build_env(self) -> Dict[str, str]:
        env = dict(os.environ)
        if self.cobc_path:
            cobc_p = Path(self.cobc_path)
            parent_dir = cobc_p.parent.parent
            config_dir = parent_dir / "config"
            copy_dir = parent_dir / "copy"

            if config_dir.exists() and "COB_CONFIG_DIR" not in env:
                env["COB_CONFIG_DIR"] = str(config_dir)
            if copy_dir.exists() and "COB_COPY_DIR" not in env:
                env["COB_COPY_DIR"] = str(copy_dir)

            bin_dir = str(cobc_p.parent)
            current_path = env.get("PATH", "")
            if bin_dir.lower() not in current_path.lower():
                env["PATH"] = f"{bin_dir};{current_path}" if os.name == "nt" else f"{bin_dir}:{current_path}"

        return env

    def is_available(self) -> bool:
        """Returns True if the GnuCOBOL compiler (cobc) is executable."""
        if not self.cobc_path:
            return False
        try:
            res = subprocess.run(
                [self.cobc_path, "--version"],
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            return res.returncode == 0
        except (FileNotFoundError, PermissionError, OSError):
            return False

    def get_version(self) -> Optional[str]:
        """Returns the GnuCOBOL version string."""
        if not self.is_available():
            return None
        try:
            res = subprocess.run(
                [self.cobc_path, "--version"],
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            first_line = res.stdout.splitlines()[0] if res.stdout else ""
            return first_line.strip()
        except Exception:
            return None

    def run_xref(
        self,
        cobol_file: str | Path,
        std: str = "ibm",
        copybook_dirs: Optional[List[str | Path]] = None,
        extra_args: Optional[List[str]] = None,
    ) -> GnuCobolListing:
        """
        Runs `cobc -fsyntax-only -std={std} -ftsymbols -Xref -T {listing_file} {cobol_file}`
        to extract the official compiler symbol table and binary layout.
        """
        if not self.is_available():
            raise EnvironmentError(
                "GnuCOBOL compiler (cobc) not found on PATH or known directories."
            )

        path = Path(cobol_file).resolve()
        if not path.exists():
            raise FileNotFoundError(f"COBOL source file not found: {path}")

        with tempfile.TemporaryDirectory() as tmpdir:
            listing_file = Path(tmpdir) / "cobc_listing.txt"

            cmd = [
                self.cobc_path,
                "-fsyntax-only",
                f"-std={std}",
                "-ftsymbols",
                "-Xref",
                "-T",
                str(listing_file),
            ]

            if copybook_dirs:
                for cp in copybook_dirs:
                    cmd.extend(["-I", str(Path(cp).resolve())])

            if extra_args:
                cmd.extend(extra_args)

            cmd.append(str(path))

            result = subprocess.run(
                cmd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

            output_parts = [result.stdout, result.stderr]
            if listing_file.exists():
                output_parts.append(listing_file.read_text(encoding="utf-8", errors="replace"))

            full_output = "\n".join(output_parts)
            return self.parse_listing_output(full_output, str(path))

    def write_xref_listing(
        self,
        cobol_file: str | Path,
        output_file: str | Path,
        std: str = "ibm",
        copybook_dirs: Optional[List[str | Path]] = None,
        allow_syntax_errors: bool = False,
    ) -> Path:
        """Run GnuCOBOL and persist its unmodified ``-T`` listing output."""
        if not self.is_available():
            raise EnvironmentError(
                "GnuCOBOL compiler (cobc) not found on PATH or known directories."
            )

        source = Path(cobol_file).resolve()
        destination = Path(output_file).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            self.cobc_path,
            "-fsyntax-only",
            f"-std={std}",
            "-ftsymbols",
            "-Xref",
        ]
        for copybook_dir in copybook_dirs or []:
            cmd.extend(["-I", str(Path(copybook_dir).resolve())])
        source_arg = os.path.relpath(source, Path.cwd())
        cmd.extend(["-T", str(destination), source_arg])

        result = subprocess.run(
            cmd,
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if not destination.exists():
            diagnostics = "\n".join((result.stdout, result.stderr)).strip()
            raise RuntimeError(f"GnuCOBOL did not emit {destination}:\n{diagnostics}")
        if result.returncode != 0 and not allow_syntax_errors:
            destination.unlink(missing_ok=True)
            diagnostics = "\n".join((result.stdout, result.stderr)).strip()
            raise RuntimeError(f"GnuCOBOL failed to compile {source}:\n{diagnostics}")
        return destination

    @staticmethod
    def parse_listing_output(raw_text: str, source_file: str = "") -> GnuCobolListing:
        """
        Parses GnuCOBOL -Xref and -T listing output to extract field names,
        levels, byte offsets, lengths, and PIC clauses.
        """
        fields: Dict[str, GnuCobolField] = {}
        symbols: List[str] = []
        program_id = ""

        prog_match = re.search(r"PROGRAM-ID\.\s+([A-Za-z0-9_-]+)", raw_text, re.IGNORECASE)
        if prog_match:
            program_id = prog_match.group(1).upper()

        lines = raw_text.splitlines()

        # Layout A: Standard Listing with explicit Offset column
        pattern_a = re.compile(
            r"^\s*(\d+)\s+(\d{1,2})\s+([A-Za-z0-9_-]+)\s+([A-Za-z0-9\(\)\$\+\-\*\,\.\/\s_]+?)\s+(\d+)\s+(\d+)",
            re.IGNORECASE,
        )

        # Layout B (GnuCOBOL 3.2 Symbols table):
        pattern_symbols = re.compile(
            r"^\s*(\d{5})\s+([A-Za-z0-9_-]+)\s+(\d{1,2})\s+([A-Za-z0-9_-]+)(?:,\s*REDEFINES\s+([A-Za-z0-9_-]+))?(?:\s+(.*))?$",
            re.IGNORECASE,
        )

        # Layout C (GnuCOBOL 3.2 Xref NAME section):
        pattern_xref_name = re.compile(r"^([A-Za-z0-9_-]+)\s+(\d+)\s+(.*)$")

        in_symbols_table = False
        in_xref_names = False

        symbol_entries: List[Tuple[int, int, str, str, str, str, str]] = []
        current_section = ""

        for line in lines:
            if "SIZE" in line and "TYPE" in line and "LVL" in line and "NAME" in line:
                in_symbols_table = True
                continue

            if in_symbols_table:
                section_match = re.match(r"^\s*(.+? SECTION)\s*$", line)
                if section_match:
                    current_section = section_match.group(1).upper()
                    continue
                if "NAME" in line and "DEFINED" in line and "REFERENCES" in line:
                    in_symbols_table = False
                    in_xref_names = True
                    continue
                if line.strip().startswith("GnuCOBOL") or "\x0c" in line:
                    continue

                m_sym = pattern_symbols.match(line)
                if m_sym:
                    size_str, type_str, lvl_str, name_str, redef_str, pic_str = m_sym.groups()
                    clean_name = name_str.upper().strip()
                    redef_target = (redef_str or "").upper().strip()
                    symbol_entries.append((
                        int(size_str),
                        int(lvl_str),
                        clean_name,
                        type_str.upper().strip(),
                        redef_target,
                        (pic_str or "").strip(),
                        current_section,
                    ))
                    continue

            if in_xref_names:
                if "LABEL" in line or "warnings in compilation" in line:
                    in_xref_names = False
                else:
                    m_x = pattern_xref_name.match(line.strip())
                    if m_x:
                        name, line_num, refs = m_x.groups()
                        uname = name.upper().strip()
                        if uname not in symbols:
                            symbols.append(uname)

            m_a = pattern_a.match(line)
            if m_a:
                line_no, lvl, name, pic_use, offset, length = m_a.groups()
                uname = name.upper().strip()
                if uname != "FILLER" and uname not in fields:
                    fields[uname] = GnuCobolField(
                        name=uname,
                        level=int(lvl),
                        pic=pic_use.strip(),
                        byte_offset=int(offset),
                        byte_length=int(length),
                        line_num=int(line_no),
                    )

        if symbol_entries and not fields:
            running_offset = 0
            field_offsets: Dict[str, int] = {}
            level_stack: List[Tuple[int, int]] = []
            active_section = ""

            for size, lvl, name, ftype, redefines, pic, section in symbol_entries:
                if section != active_section:
                    active_section = section
                    running_offset = 0
                    field_offsets = {}
                    level_stack = []
                if lvl == 88:
                    continue

                occurs_mult = 1
                occ_match = re.search(r"\bOCCURS\s+(\d+)\b", pic, re.IGNORECASE)
                if occ_match:
                    occurs_mult = int(occ_match.group(1))

                total_allocated_size = size if ftype == "GROUP" else (size * occurs_mult)

                if lvl in (1, 77):
                    current_offset = (
                        field_offsets[redefines]
                        if redefines and redefines in field_offsets
                        else running_offset
                    )
                    level_stack = [(lvl, current_offset)]
                    field_offsets[name] = current_offset
                    fields[name] = GnuCobolField(
                        name=name,
                        level=lvl,
                        pic=pic,
                        usage=ftype,
                        byte_offset=current_offset,
                        byte_length=total_allocated_size,
                        redefines=redefines,
                        section=section,
                    )
                    if not redefines:
                        running_offset += total_allocated_size
                else:
                    while level_stack and level_stack[-1][0] >= lvl:
                        level_stack.pop()

                    parent_offset = level_stack[-1][1] if level_stack else 0

                    if redefines and redefines in field_offsets:
                        current_offset = field_offsets[redefines]
                    else:
                        current_offset = parent_offset

                    field_offsets[name] = current_offset
                    fields[name] = GnuCobolField(
                        name=name,
                        level=lvl,
                        pic=pic,
                        usage=ftype,
                        byte_offset=current_offset,
                        byte_length=total_allocated_size,
                        redefines=redefines,
                        section=section,
                    )

                    if not redefines and level_stack:
                        top_lvl, top_off = level_stack.pop()
                        level_stack.append((top_lvl, top_off + total_allocated_size))

                    if ftype == "GROUP":
                        level_stack.append((lvl, current_offset))

        return GnuCobolListing(
            program_id=program_id,
            source_file=source_file,
            fields=fields,
            symbols=symbols,
            raw_output=raw_text,
        )
