"""
cobolscope.rules_generator
~~~~~~~~~~~~~~~~~~~~~~~~~~

Automated rule generator and codebase scanner. Scans COBOL AST models to extract:
1. External runtime abend modules
2. Paragraph naming patterns and strict names
3. Conditional checks (database connection/query checks, file status errors)
4. Program-specific terminal procedure exceptions
"""

from __future__ import annotations

import logging
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    SectionNode,
    AnyStatementNode,
    CallStatementNode,
    PerformStatementNode,
    IfStatementNode,
    EvaluateStatementNode,
    ExecCicsStatementNode,
    StopStatementNode,
    GobackStatementNode,
    ExitStatementNode,
)
from cobolscope.rules import (
    GlobalRules,
    ParagraphNamingRules,
    ProgramOverrideRules,
    AbendConditionRule,
    save_rules,
    get_default_rules,
)

logger = logging.getLogger(__name__)

_RE_ABEND_MODULE = re.compile(
    r"(?:^|[-_])(?:ABEND|FATAL|KILL|CANCEL|ABORT)(?:[-_]|$)", re.IGNORECASE
)
_RE_ABEND_NAME = re.compile(
    r"(?:^|[-_])(?:ABEND|FATAL|KILL|CANCEL|ABORT)(?:[-_]|$)", re.IGNORECASE
)

_S0C7_CORRUPT_VALUES = {
    "LOW-VALUES",
    "LOW-VALUE",
    "HIGH-VALUES",
    "HIGH-VALUE",
    "SPACES",
    "SPACE",
    "ALL ' '",
    'ALL " "',
}


def _is_s0c7_corrupt_val(val: str) -> bool:
    up = (val or "").strip().upper()
    return up in _S0C7_CORRUPT_VALUES or "LOW-VALUE" in up or "HIGH-VALUE" in up


def _is_s0c7_sequence(s1: AnyStatementNode, s2: AnyStatementNode) -> bool:
    """Fast check for MOVE LOW-VALUES/SPACES immediately followed by arithmetic."""
    s1_type = (getattr(s1, "type", "") or "").upper()
    s1_raw = (getattr(s1, "raw_text", "") or "").strip().upper()
    if s1_type != "MOVE" and not s1_raw.startswith("MOVE"):
        return False

    from_expr = getattr(s1, "from_expr", "") or ""
    if not from_expr and s1_raw:
        m = re.search(r"\bMOVE\s+([A-Za-z0-9_\-\'\"]+)\s+TO\b", s1_raw, re.IGNORECASE)
        if m:
            from_expr = m.group(1)
    if not _is_s0c7_corrupt_val(from_expr):
        return False

    s2_type = (getattr(s2, "type", "") or "").upper()
    s2_raw = (getattr(s2, "raw_text", "") or "").strip().upper()
    return s2_type in ("ADD", "SUBTRACT", "COMPUTE", "MULTIPLY", "DIVIDE") or bool(
        re.match(r"^(?:ADD|SUBTRACT|COMPUTE|MULTIPLY|DIVIDE)\b", s2_raw)
    )


def _has_s0c7_idiom(stmts: List[AnyStatementNode]) -> bool:
    if len(stmts) < 2:
        return False
    for i in range(len(stmts) - 1):
        if _is_s0c7_sequence(stmts[i], stmts[i + 1]):
            return True
        if i + 2 < len(stmts):
            mid_type = (getattr(stmts[i + 1], "type", "") or "").upper()
            if mid_type == "DISPLAY" and _is_s0c7_sequence(stmts[i], stmts[i + 2]):
                return True
    return False


def _is_syntax_terminal(stmt: AnyStatementNode) -> bool:
    if isinstance(stmt, (StopStatementNode, GobackStatementNode)):
        return True
    if isinstance(stmt, ExitStatementNode):
        op = (getattr(stmt, "operation", "") or "").upper()
        raw = (getattr(stmt, "raw_text", "") or "").upper()
        if "PROGRAM" in op or "EXIT PROGRAM" in raw:
            return True
    if isinstance(stmt, ExecCicsStatementNode):
        payload = (getattr(stmt, "raw_payload", "") or "").upper()
        raw = (getattr(stmt, "raw_text", "") or "").upper()
        comb = f"{payload} {raw}"
        if any(h in comb for h in ("HANDLE ABEND", "HANDLE CONDITION", "IGNORE CONDITION")):
            return False
        if "ABEND" in comb or "RETURN" in comb:
            return True
    return False


def _extract_cics_link_target(stmt: AnyStatementNode) -> Optional[str]:
    raw = (getattr(stmt, "raw_text", "") or "").upper()
    payload = (getattr(stmt, "raw_payload", "") or "").upper()
    combined = f"{payload} {raw}"
    m = re.search(r"\bPROGRAM\s*\(\s*['\"]?([A-Za-z0-9_\-]+)['\"]?\s*\)", combined)
    if m:
        return m.group(1).strip()
    return None


def _extract_condition_clauses(cond: str) -> List[str]:
    """Extracts candidate sub-conditions like SQLCODE NOT = 0 or FILE-STATUS NOT = '00'."""
    clean = (cond or "").strip().upper()
    matches = []
    # SQL error checks
    if "SQLCODE" in clean:
        m = re.search(r"SQLCODE\s*(?:NOT\s*=\s*\d+|IS\s+NOT\s+EQUAL\s+TO\s+[A-Z0-9]+|<|\bNOT\s*=\s*ZERO\b)", clean)
        if m:
            matches.append(m.group(0).strip())
        else:
            matches.append("SQLCODE IS NOT EQUAL TO ZERO")

    # File status checks
    if "FILE-STATUS" in clean or "FSCODE" in clean or "STATUS" in clean:
        m = re.search(r"(?:FILE-STATUS|FSCODE|COMM-FSCODE)\s*(?:NOT\s*=\s*['\"][0-9A-Z]+['\"]|<|>|IS\s+NOT\s+EQUAL\s+TO)", clean)
        if m:
            matches.append(m.group(0).strip())

    # Connection failure flags
    if "CONNECT" in clean and ("FAIL" in clean or "ERR" in clean or "NOT OK" in clean):
        matches.append(clean)

    return matches


def scan_program_for_rules(model: ProgramModel) -> Dict[str, Any]:
    """
    Scans a ProgramModel and returns discovered terminal elements:
      - runtime_modules: Set[str]
      - global_strict_paragraphs: Set[str]
      - program_terminal_paragraphs: Set[str]
      - abend_conditions: List[AbendConditionRule]
    """
    program_id = (model.program_id or "UNKNOWN").upper().strip()
    runtime_modules: Set[str] = set()
    global_strict_paragraphs: Set[str] = set()
    program_terminal_paragraphs: Set[str] = set()
    detected_conditions: Set[str] = set()

    all_routines: List[Union[ParagraphNode, SectionNode]] = list(model.paragraphs) + list(model.sections)

    for routine in all_routines:
        r_name = routine.name.upper().strip()
        stmts = getattr(routine, "statements", []) or []

        is_term = False

        # 1. Deliberate S0C7
        if _has_s0c7_idiom(stmts):
            is_term = True

        # 2. Syntax terminal or calls
        for stmt in stmts:
            if _is_syntax_terminal(stmt):
                is_term = True

            # Check CALL statements
            if isinstance(stmt, CallStatementNode):
                prog = (
                    getattr(stmt, "program", "") or getattr(stmt, "target", "") or ""
                ).strip().strip("'\"").upper()
                if prog and (_RE_ABEND_MODULE.search(prog) or prog in ("CEE3ABD", "ILBOABN0", "ABNDPROC", "ABORT", "CANCL")):
                    runtime_modules.add(prog)
                    is_term = True

            # Check EXEC CICS LINK statements
            if isinstance(stmt, ExecCicsStatementNode):
                tgt = _extract_cics_link_target(stmt)
                if tgt and (_RE_ABEND_MODULE.search(tgt) or tgt in ("CEE3ABD", "ILBOABN0", "ABNDPROC")):
                    runtime_modules.add(tgt)
                    is_term = True

            # Check conditional branches that abend
            if isinstance(stmt, IfStatementNode):
                then_stmts = getattr(stmt, "then_statements", []) or []
                else_stmts = getattr(stmt, "else_statements", []) or []
                cond_text = getattr(stmt, "condition", "") or ""

                branch_abends = any(
                    _is_syntax_terminal(s)
                    or (isinstance(s, CallStatementNode) and _RE_ABEND_MODULE.search(getattr(s, "program", "") or ""))
                    for s in then_stmts
                )
                if branch_abends:
                    clauses = _extract_condition_clauses(cond_text)
                    for c in clauses:
                        detected_conditions.add(c)

        # Categorize terminal routine
        if is_term or _RE_ABEND_NAME.search(r_name):
            if _RE_ABEND_NAME.search(r_name) or r_name.startswith("999") or r_name.startswith("9999"):
                global_strict_paragraphs.add(r_name)
            else:
                # Custom program-specific paragraph
                program_terminal_paragraphs.add(r_name)

    # Build condition rules
    condition_rules = [
        AbendConditionRule(condition_pattern=re.escape(c), description=f"Auto-detected in {program_id}")
        for c in sorted(detected_conditions)
    ]

    return {
        "program_id": program_id,
        "runtime_modules": runtime_modules,
        "global_strict_paragraphs": global_strict_paragraphs,
        "program_terminal_paragraphs": program_terminal_paragraphs,
        "abend_conditions": condition_rules,
    }


def generate_rules_from_models(models: List[ProgramModel]) -> GlobalRules:
    """
    Synthesizes a unified GlobalRules configuration by scanning a collection of ProgramModels.
    Preserves default standard rules and merges discovered runtime modules, paragraphs, and overrides.
    """
    rules = get_default_rules()

    all_discovered_modules: Set[str] = set()
    all_global_strict: Set[str] = set()

    for m in models:
        scan_result = scan_program_for_rules(m)
        prog_id = scan_result["program_id"]

        all_discovered_modules.update(scan_result["runtime_modules"])
        all_global_strict.update(scan_result["global_strict_paragraphs"])

        prog_terminal = sorted(scan_result["program_terminal_paragraphs"])
        prog_conditions = scan_result["abend_conditions"]

        if prog_terminal or prog_conditions:
            rules.programs[prog_id] = ProgramOverrideRules(
                terminal_paragraphs=prog_terminal,
                non_terminal_paragraphs=[],
                runtime_modules=[],
                abend_conditions=prog_conditions,
            )

    # Merge into global rules
    existing_modules = set(rules.runtime_modules)
    for mod in sorted(all_discovered_modules):
        if mod not in existing_modules:
            rules.runtime_modules.append(mod)

    existing_strict = set(rules.paragraph_names.strict)
    for para in sorted(all_global_strict):
        if para not in existing_strict:
            rules.paragraph_names.strict.append(para)

    return rules


def generate_rules_file(
    output_path: Union[str, Path], models: Optional[List[ProgramModel]] = None
) -> Path:
    """
    Generates and writes a clean cobolscope-rules.yaml file to output_path.
    If models are provided, rules are auto-populated from scanning; otherwise default rules template is used.
    """
    out = Path(output_path).resolve()
    if models:
        rules = generate_rules_from_models(models)
    else:
        rules = get_default_rules()

    save_rules(rules, out)
    return out
