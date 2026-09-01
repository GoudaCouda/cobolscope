"""Compile the Java bridge and safely update the bundled ProLeap JAR."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JAVA_SOURCES = sorted((ROOT / "java").glob("*.java"))
JAR_PATH = ROOT / "cobolscope" / "lib" / "proleap-cobol-parser.jar"


def require_javac() -> str:
    executable = shutil.which("javac")
    if executable is None:
        raise SystemExit("Required JDK tool 'javac' was not found on PATH.")
    return executable


def update_jar(classes_dir: Path) -> None:
    compiled = {
        path.relative_to(classes_dir).as_posix(): path
        for path in classes_dir.rglob("*.class")
    }
    temp_jar = JAR_PATH.with_suffix(".jar.tmp")
    seen: set[str] = set()
    try:
        with zipfile.ZipFile(JAR_PATH, "r") as source, zipfile.ZipFile(
            temp_jar, "w"
        ) as destination:
            for info in source.infolist():
                if info.filename in compiled or info.filename in seen:
                    continue
                seen.add(info.filename)
                destination.writestr(info, source.read(info.filename))
            for archive_name, class_file in compiled.items():
                destination.write(
                    class_file, archive_name, compress_type=zipfile.ZIP_DEFLATED
                )
        os.replace(temp_jar, JAR_PATH)
    finally:
        temp_jar.unlink(missing_ok=True)


def main() -> int:
    if not JAR_PATH.exists():
        raise SystemExit(f"Bundled ProLeap JAR not found: {JAR_PATH}")
    if not JAVA_SOURCES:
        raise SystemExit(f"No Java sources found under {ROOT / 'java'}")

    javac = require_javac()
    with tempfile.TemporaryDirectory(prefix="cobolscope-java-") as temp_dir:
        classes_dir = Path(temp_dir)
        print(f"Compiling {len(JAVA_SOURCES)} Java source files with Java 17...")
        subprocess.run(
            [
                javac,
                "--release",
                "17",
                "-cp",
                str(JAR_PATH),
                "-d",
                str(classes_dir),
                *(str(source) for source in JAVA_SOURCES),
            ],
            check=True,
        )
        update_jar(classes_dir)

    print(f"Updated Java bridge classes in {JAR_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
