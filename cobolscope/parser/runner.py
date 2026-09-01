"""
cobolscope.parser.runner - Java subprocess runner and classpath resolver for ProLeap parser.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

VALID_FORMATS = ("FIXED", "TANDEM", "VARIABLE")
JAVA_MAIN_CLASS = "ProLeapCliRunner"


def find_jar(explicit_jar: Optional[Union[str, Path]] = None) -> Path:
    """Locate the proleap-cobol-parser jar."""
    if explicit_jar:
        jar_path = Path(explicit_jar)
        if not jar_path.exists():
            raise FileNotFoundError(f"Specified jar not found: {jar_path}")
        return jar_path

    env_jar = os.environ.get("PROLEAP_JAR")
    if env_jar and Path(env_jar).exists():
        return Path(env_jar)

    pkg_dir = Path(__file__).resolve().parent.parent
    candidates = [
        pkg_dir / "lib" / "proleap-cobol-parser.jar",
        pkg_dir / "proleap-cobol-parser.jar",
        pkg_dir.parent / "lib" / "proleap-cobol-parser.jar",
        pkg_dir.parent / "lib" / "proleap-fat.jar",
    ]
    for cand in candidates:
        if cand.exists():
            return cand

    raise FileNotFoundError(
        "Could not locate proleap-cobol-parser.jar. "
        "Provide it via --jar, the PROLEAP_JAR environment variable, "
        "or place it in the ./lib or cobolscope/lib directory."
    )


def find_runner_classpath(explicit_cp: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """Locate the directory containing ProLeapCliRunner.class if not bundled in jar."""
    if explicit_cp:
        cp_path = Path(explicit_cp)
        if not cp_path.exists():
            raise FileNotFoundError(f"Specified runner classpath not found: {cp_path}")
        return cp_path

    env_cp = os.environ.get("PROLEAP_RUNNER_CP")
    if env_cp and Path(env_cp).exists():
        return Path(env_cp)

    pkg_dir = Path(__file__).resolve().parent.parent
    candidates = [
        pkg_dir / "lib",
        pkg_dir.parent / "lib",
    ]
    for cand in candidates:
        if cand.exists() and (cand / "ProLeapCliRunner.class").exists():
            return cand

    return None


def check_java_available(java_exe: str = "java") -> None:
    """Verify that a Java runtime is on the PATH."""
    try:
        subprocess.run(
            [java_exe, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise EnvironmentError(
            "Java runtime not found. Please install Java (JRE/JDK 17+) "
            "and ensure 'java' is on your PATH."
        )


def build_classpath(runner_dir: Optional[Path], jar_path: Path) -> str:
    """Construct classpath with runner class directory before or with the jar."""
    if runner_dir and runner_dir.exists():
        sep = ";" if os.name == "nt" else ":"
        return f"{runner_dir}{sep}{jar_path}"
    return str(jar_path)



def parse(
    input_file: Union[str, Path],
    format: str = "FIXED",
    copybook_dirs: Optional[List[Union[str, Path]]] = None,
    copybook_exts: Optional[List[str]] = None,
    ignore_syntax_errors: bool = False,
    jar_path: Optional[Union[str, Path]] = None,
    runner_cp: Optional[Union[str, Path]] = None,
    java_exe: str = "java",
    extra_java_args: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Parse a COBOL source file and return the Canonical IR representation as a Python dict.

    Args:
        input_file: Path to COBOL file.
        format: COBOL source format ("FIXED", "TANDEM", or "VARIABLE").
        copybook_dirs: Optional list of directories containing copybooks.
        copybook_exts: Optional list of file extensions for copybooks.
        ignore_syntax_errors: Whether to ignore minor syntax errors during parsing.
        jar_path: Optional path to proleap jar.
        runner_cp: Optional path to compiled ProLeapCliRunner directory.
        java_exe: Java executable name/path.
        extra_java_args: Optional list of JVM options (e.g. ['-Xmx2g']).

    Returns:
        Dict containing programId, dataDictionary, sections, and paragraphs.
    """
    file_path = Path(input_file).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    fmt = format.upper()
    if fmt not in VALID_FORMATS:
        raise ValueError(f"Invalid format '{format}'. Must be one of {VALID_FORMATS}")

    check_java_available(java_exe)
    resolved_jar = find_jar(jar_path)
    resolved_cp = find_runner_classpath(runner_cp)
    classpath = build_classpath(resolved_cp, resolved_jar)

    # Use a temp file for JSON output to avoid pipe buffer issues with large ASTs
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp_file:
        tmp_output_path = Path(tmp_file.name)

    try:
        cmd = [java_exe]
        if extra_java_args:
            cmd.extend(extra_java_args)
        cmd.extend(["-cp", classpath, JAVA_MAIN_CLASS, str(file_path), fmt, str(tmp_output_path)])

        if copybook_dirs:
            for cp_dir in copybook_dirs:
                cmd.extend(["-I", str(Path(cp_dir).resolve())])
        if copybook_exts:
            cmd.extend(["--copybook-ext", ",".join(copybook_exts)])
        if ignore_syntax_errors:
            cmd.append("--ignore-syntax-errors")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"ProLeap parser failed (exit code {result.returncode}):\n{err_msg}")

        with open(tmp_output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    finally:
        if tmp_output_path.exists():
            try:
                os.remove(tmp_output_path)
            except OSError:
                pass
