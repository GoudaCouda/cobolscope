"""
Simple test model loader and cache.
Loads pre-parsed JSON IR from tests/.cache/ if available; otherwise parses once and saves it.
"""

import json
from pathlib import Path
from typing import Dict, Optional
from cobolscope.models import ProgramModel
from cobolscope.parser import parse

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
_MEMORY_STORE: Dict[str, ProgramModel] = {}


def resolve_cobol_path(cobol_path: str) -> Path:
    """Resolves a COBOL path to an actual file on disk."""
    p = Path(cobol_path)
    if p.is_file():
        return p

    candidates = [
        REPO_ROOT / p,
        FIXTURES_DIR / p.name,
        FIXTURES_DIR / "bank_of_z" / "cobol" / p.name,
        REPO_ROOT / "tests" / "fixtures" / p.name,
        REPO_ROOT / "tests" / "fixtures" / "bank_of_z" / "cobol" / p.name,
    ]
    for c in candidates:
        if c.is_file():
            return c
    return p


def get_test_model(cobol_path: str, force_parse: bool = False) -> ProgramModel:
    """Returns a parsed ProgramModel, loading from disk cache or memory store when available."""
    p = resolve_cobol_path(cobol_path)
    stem = p.stem

    if not force_parse and stem in _MEMORY_STORE:
        return _MEMORY_STORE[stem]

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{stem}.json"

    if not force_parse and cache_file.exists():
        try:
            raw = json.loads(cache_file.read_text(encoding="utf-8"))
            model = ProgramModel.from_dict(raw)
            _MEMORY_STORE[stem] = model
            return model
        except Exception:
            pass

    copybook_dirs = [
        str(FIXTURES_DIR / "bank_of_z" / "copy"),
        str(p.parent),
    ]
    raw = parse(str(p), copybook_dirs=copybook_dirs, format="FIXED", ignore_syntax_errors=True)
    try:
        cache_file.write_text(json.dumps(raw), encoding="utf-8")
    except Exception:
        pass

    model = ProgramModel.from_dict(raw)
    _MEMORY_STORE[stem] = model
    return model
