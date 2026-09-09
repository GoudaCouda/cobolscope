"""
cobolscope.graph.termination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multi-layer compiler-grade abnormal termination (ABEND) and exit point classifier.
Accurately identifies:
  Layer 1: Language syntax primitives (STOP RUN, GOBACK, EXIT PROGRAM, EXEC CICS ABEND/RETURN)
  Layer 2: Well-known runtime abend modules (CEE3ABD, ILBOABN0, ABORT, CBLTDLI ROLL)
  Layer 3: Deliberate S0C7 hardware crash sequences (MOVE LOW-VALUES/SPACES + arithmetic S0C7)
  Layer 4: Transitive fixed-point propagation across procedures and sections
"""

from __future__ import annotations
import logging
import re
from typing import Dict, List, Optional, Set, Tuple, Union, Any

from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    SectionNode,
    AnyStatementNode,
    StatementNode,
    MoveStatementNode,
    PerformStatementNode,
    GoToStatementNode,
    StopStatementNode,
    GobackStatementNode,
    ExitStatementNode,
    CallStatementNode,
    AddStatementNode,
    SubtractStatementNode,
    MultiplyStatementNode,
    DivideStatementNode,
    ComputeStatementNode,
    ExecCicsStatementNode,
)

from cobolscope.rules import (
    GlobalRules,
    EffectiveProgramRules,
    load_rules,
    get_effective_rules,
)

logger = logging.getLogger(__name__)

DEFAULT_KNOWN_ABEND_PROGRAMS: Set[str] = {
    "CEE3ABD",   # IBM Language Environment Abend with dump / options
    "ILBOABN0",  # OS/VS COBOL legacy runtime abend module
    "ABNDPROC",  # Common mainframe custom abend processor
    "ABORT",     # POSIX / Micro Focus abort wrapper
    "CANCL",     # Transaction cancellation runtime
}

_RE_ABEND_NAME = re.compile(
    r"(?:^|[-_])(?:ABEND|FATAL|KILL|CANCEL|ABORT)(?:[-_]|$)", re.IGNORECASE
)
_RE_CRASH_NAME = re.compile(
    r"(?:^|[-_])(?:EXCEPTION|TRIGGER|CRASH|DUMP|S0C7|FAULT|ABEND)(?:[-_]|$)", re.IGNORECASE
)

_S0C7_SOURCE_VALUES = {
    "LOW-VALUES",
    "LOW-VALUE",
    "HIGH-VALUES",
    "HIGH-VALUE",
    "SPACES",
    "SPACE",
    "ALL ' '",
    'ALL " "',
}


def is_s0c7_source_expression(expr: str) -> bool:
    """Returns True if the expression represents non-numeric corruption literals."""
    cleaned = (expr or "").strip().upper()
    return cleaned in _S0C7_SOURCE_VALUES or "LOW-VALUE" in cleaned or "HIGH-VALUE" in cleaned


def is_arithmetic_statement(stmt: AnyStatementNode) -> bool:
    """Returns True if the statement executes arithmetic that would fault on non-numeric data."""
    if isinstance(
        stmt,
        (
            AddStatementNode,
            SubtractStatementNode,
            MultiplyStatementNode,
            DivideStatementNode,
            ComputeStatementNode,
        ),
    ):
        return True
    s_type = (getattr(stmt, "type", "") or "").upper()
    if s_type in ("ADD", "SUBTRACT", "COMPUTE", "MULTIPLY", "DIVIDE"):
        return True
    raw = (getattr(stmt, "raw_text", "") or "").strip().upper()
    return bool(re.match(r"^(?:ADD|SUBTRACT|COMPUTE|MULTIPLY|DIVIDE)\b", raw))


class TerminationClassifier:
    """
    Evaluates COBOL statements, statement sequences, and procedures for fatal termination.
    Supports declarative rules, deliberate hardware abend idioms, and transitive call tree closure.
    """

    def __init__(
        self,
        rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
        program_id: Optional[str] = None,
        config_abend_programs: Optional[Set[str]] = None,
        config_terminal_paras: Optional[Set[str]] = None,
    ):
        if isinstance(rules, EffectiveProgramRules):
            self.effective_rules = rules
        elif isinstance(rules, GlobalRules):
            self.effective_rules = get_effective_rules(rules, program_id=program_id)
        else:
            self.effective_rules = get_effective_rules(load_rules(), program_id=program_id)

        self.known_abend_programs: Set[str] = set(self.effective_rules.runtime_modules)
        if config_abend_programs:
            self.known_abend_programs.update({p.upper().strip() for p in config_abend_programs})

        self.terminal_paragraphs_override: Set[str] = set(self.effective_rules.strict_paragraphs)
        if config_terminal_paras:
            self.terminal_paragraphs_override.update({p.upper().strip() for p in config_terminal_paras})

        self.terminal_paragraphs: Set[str] = set(self.terminal_paragraphs_override)

    def is_s0c7_crash_sequence(
        self, s1: AnyStatementNode, s2: AnyStatementNode
    ) -> bool:
        """
        Layer 3: Identifies the classic IBM mainframe S0C7 Data Exception idiom:
        MOVE LOW-VALUES/SPACES into a field, immediately followed by arithmetic on
        that field, its redefinition, or a related exception-triggering structure.
        """
        if not self.effective_rules.detect_s0c7_idioms:
            return False

        # Step 1: s1 must be a MOVE of non-numeric literal
        is_move = isinstance(s1, MoveStatementNode) or (getattr(s1, "type", "") or "").upper() == "MOVE"
        raw1 = (getattr(s1, "raw_text", "") or "").strip().upper()
        if not is_move and not raw1.startswith("MOVE"):
            return False

        from_expr = getattr(s1, "from_expr", "") or ""
        if not from_expr and raw1:
            m_src = re.search(r"\bMOVE\s+([A-Za-z0-9_\-\'\"]+)\s+TO\b", raw1, re.IGNORECASE)
            if m_src:
                from_expr = m_src.group(1)

        if not is_s0c7_source_expression(from_expr):
            return False

        # Step 2: s2 must be an arithmetic operation
        if not is_arithmetic_statement(s2):
            return False

        # Step 3: Extract targets / operands touched by s1 and s2
        s1_targets: Set[str] = set()
        for t in getattr(s1, "to_targets", []) or []:
            s1_targets.add(t.strip().upper())
        for tid in getattr(s1, "target_field_ids", []) or []:
            tid_up = tid.strip().upper()
            s1_targets.add(tid_up)
            s1_targets.add(tid_up.split("_")[-1])
        if raw1:
            m_to = re.search(r"\bTO\s+([A-Za-z0-9_\-]+)", raw1, re.IGNORECASE)
            if m_to:
                s1_targets.add(m_to.group(1).strip().upper())

        s2_operands: Set[str] = set()
        for t in getattr(s2, "targets", []) or []:
            s2_operands.add(t.strip().upper())
        for t in getattr(s2, "to_targets", []) or []:
            s2_operands.add(t.strip().upper())
        for tid in (getattr(s2, "target_field_ids", []) or []) + (getattr(s2, "source_field_ids", []) or []):
            tid_up = tid.strip().upper()
            s2_operands.add(tid_up)
            s2_operands.add(tid_up.split("_")[-1])
        raw2 = (getattr(s2, "raw_text", "") or "").strip().upper()
        if raw2:
            for token in re.findall(r"[A-Za-z0-9_\-]+", raw2):
                s2_operands.add(token.strip().upper())

        # Check Correlation:
        # A. Direct intersection
        if s1_targets & s2_operands:
            return True

        # B. Prefix or Substring match (e.g. DATA-EXCEPTION and DATA-EXCEPTION-TRIGGER)
        for t1 in s1_targets:
            if len(t1) >= 4:
                for t2 in s2_operands:
                    if len(t2) >= 4 and (t1 in t2 or t2 in t1):
                        return True

        # C. Semantic crash/exception trigger naming
        for t in s1_targets | s2_operands:
            if _RE_CRASH_NAME.search(t):
                return True

        # D. Direct adjacency fallback: in COBOL, moving LOW-VALUES/SPACES immediately
        # before an arithmetic statement is universally an intentional crash.
        return True

    def has_deliberate_s0c7_idiom(
        self, stmts: Union[List[AnyStatementNode], Any]
    ) -> bool:
        """Scans a list of statements or a procedure node for deliberate S0C7 crash sequences."""
        actual_stmts = getattr(stmts, "statements", stmts)
        if not isinstance(actual_stmts, list) or len(actual_stmts) < 2:
            return False

        for i in range(len(actual_stmts) - 1):
            s1 = actual_stmts[i]
            s2 = actual_stmts[i + 1]
            if self.is_s0c7_crash_sequence(s1, s2):
                return True

            # Also inspect window of 2 if a DISPLAY is placed between them
            if i + 2 < len(actual_stmts):
                s_mid = actual_stmts[i + 1]
                s3 = actual_stmts[i + 2]
                if (getattr(s_mid, "type", "") or "").upper() == "DISPLAY":
                    if self.is_s0c7_crash_sequence(s1, s3):
                        return True

        return False

    def is_statement_terminal(
        self, stmt: AnyStatementNode, raw_txt: Optional[str] = None
    ) -> bool:
        """
        Determines whether an individual statement is a fatal sink that halts execution.
        """
        # --- Layer 1: Language Syntax Primitives ---
        if isinstance(stmt, StopStatementNode):
            return self.effective_rules.syntax_primitives.stop_run

        if isinstance(stmt, GobackStatementNode):
            return self.effective_rules.syntax_primitives.goback

        if isinstance(stmt, ExitStatementNode):
            op = (getattr(stmt, "operation", "") or "").upper()
            txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
            if "PROGRAM" in op or "EXIT PROGRAM" in txt:
                return self.effective_rules.syntax_primitives.exit_program

        if isinstance(stmt, ExecCicsStatementNode):
            payload = (getattr(stmt, "raw_payload", "") or "").upper()
            txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
            combined = f"{payload} {txt}"
            if any(h in combined for h in self.effective_rules.cics_exclude_handlers):
                return False
            if re.search(r"\b(?:EXEC\s+CICS\s+)?ABEND\b", combined):
                return self.effective_rules.syntax_primitives.exec_cics_abend
            if re.search(r"\b(?:EXEC\s+CICS\s+)?RETURN\b", combined):
                return self.effective_rules.syntax_primitives.exec_cics_return
            return False

        # --- Layer 2: Well-Known Runtime / OS Abend Modules ---
        if isinstance(stmt, CallStatementNode):
            prog = (
                getattr(stmt, "program", "") or getattr(stmt, "target", "") or ""
            ).strip().strip("'\"").upper()

            if self.effective_rules.is_runtime_abend_module(prog) or prog in self.known_abend_programs:
                return True

            # IMS DL/I Rollback & Terminate
            if prog == "CBLTDLI":
                params = [
                    p.strip().strip("'\"").upper()
                    for p in getattr(stmt, "using_parameters", []) or []
                ]
                txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
                if any(p in ("ROLL", "ROLS") for p in params) or "ROLL" in txt:
                    return True

            txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
            if self.effective_rules.is_runtime_abend_module(txt) or _RE_ABEND_NAME.search(txt):
                return True

        # --- Layer 3: Hardware Arithmetic Exceptions (Literal Divide by Zero) ---
        if self.effective_rules.detect_divide_by_zero and isinstance(
            stmt, (DivideStatementNode, ComputeStatementNode)
        ):
            expr = (getattr(stmt, "expression", "") or "").strip()
            raw = (raw_txt or getattr(stmt, "raw_text", "") or "").strip().upper()
            if re.search(r"\bBY\s+0(?:\s|$|\.)", raw) or re.search(r"\/\s*0(?:\s|$|\.)", expr):
                return True

        # --- Layer 4: Out-of-line Invocations of Terminal Procedures (PERFORM / GO TO) ---
        if isinstance(stmt, (PerformStatementNode, GoToStatementNode)):
            if isinstance(stmt, PerformStatementNode) and stmt.is_inline:
                return False
            tgt = (getattr(stmt, "target", "") or "").strip().upper()
            thru = (getattr(stmt, "thru", "") or "").strip().upper()
            if tgt and (
                tgt in self.terminal_paragraphs
                or self.effective_rules.is_terminal_name(tgt)
            ):
                return True
            if thru and (
                thru in self.terminal_paragraphs
                or self.effective_rules.is_terminal_name(thru)
            ):
                return True
            txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
            if self.effective_rules.is_terminal_name(txt):
                return True

        # Generic fallback
        txt = (raw_txt or getattr(stmt, "raw_text", "") or "").upper()
        if any(h in txt for h in self.effective_rules.cics_exclude_handlers):
            return False
        s_type = (getattr(stmt, "type", "") or "").upper()
        if s_type in ("PERFORM", "CALL", "GO TO", "GOTO", "GENERIC") and self.effective_rules.is_terminal_name(txt):
            return True

        return False

    def get_terminal_label(
        self, stmt: AnyStatementNode, raw_txt: Optional[str] = None
    ) -> str:
        """Produces a clean, human-readable label for terminal CFG display."""
        if isinstance(stmt, (StopStatementNode, GobackStatementNode)):
            txt = (raw_txt or getattr(stmt, "raw_text", "") or "").strip()
            return txt if txt else stmt.type
        if isinstance(stmt, ExitStatementNode):
            return "EXIT PROGRAM"
        if isinstance(stmt, ExecCicsStatementNode):
            payload = (getattr(stmt, "raw_payload", "") or "").upper()
            if "ABEND" in payload:
                return "EXEC CICS ABEND"
            return "EXEC CICS RETURN"
        if isinstance(stmt, CallStatementNode):
            prog = (getattr(stmt, "program", "") or getattr(stmt, "target", "") or "").strip().strip("'\"")
            return f"CALL '{prog}' (ABEND)" if prog else "CALL ABEND"
        if isinstance(stmt, PerformStatementNode):
            tgt = getattr(stmt, "target", "") or ""
            return f"PERFORM {tgt}" if tgt else "PERFORM ABEND"
        if isinstance(stmt, GoToStatementNode):
            tgt = getattr(stmt, "target", "") or ""
            return f"GO TO {tgt}" if tgt else "GO TO ABEND"
        txt = (raw_txt or getattr(stmt, "raw_text", "") or "").strip()
        return txt[:40] if txt else getattr(stmt, "type", "TERMINAL")

    def is_paragraph_terminal(self, para: Union[ParagraphNode, SectionNode]) -> bool:
        """
        Determines whether an entire paragraph or section definitively terminates program flow.
        """
        p_name = para.name.upper().strip()

        # Step 0: Highest precedence check - per-program exclusion overrides
        if self.effective_rules.is_excluded(p_name):
            return False

        if p_name in self.terminal_paragraphs_override:
            return True

        if getattr(para, "is_terminal", False):
            return True

        # Check configured regex patterns
        if self.effective_rules.matches_terminal_pattern(p_name):
            return True

        stmts = getattr(para, "statements", []) or []
        if not stmts:
            return False

        # Layer 3 Check: Deliberate hardware crash sequences
        if self.effective_rules.detect_s0c7_idioms and self.has_deliberate_s0c7_idiom(stmts):
            return True

        # Check last executable statement
        if self.is_statement_terminal(stmts[-1]):
            return True

        # If procedure has ABEND in name and contains terminal or crash calls
        if self.effective_rules.is_terminal_name(p_name):
            for s in stmts:
                if self.is_statement_terminal(s):
                    return True
                if (getattr(s, "type", "") or "").upper() in ("PERFORM", "CALL"):
                    return True

        return False

    @classmethod
    def for_program(
        cls,
        model: ProgramModel,
        rules: Optional[Union[GlobalRules, EffectiveProgramRules]] = None,
        config_abend_programs: Optional[Set[str]] = None,
        config_terminal_paras: Optional[Set[str]] = None,
    ) -> TerminationClassifier:
        """
        Constructs a TerminationClassifier and performs fixed-point reachability
        analysis across the entire ProgramModel to identify all terminal procedures.
        """
        if rules is None:
            rules = load_rules()
        effective = (
            rules
            if isinstance(rules, EffectiveProgramRules)
            else get_effective_rules(rules, program_id=model.program_id)
        )

        classifier = cls(
            rules=effective,
            program_id=model.program_id,
            config_abend_programs=config_abend_programs,
            config_terminal_paras=config_terminal_paras,
        )

        # Pass 1: Base terminal procedures
        for p in model.paragraphs:
            p_name = p.name.upper().strip()
            if classifier.is_paragraph_terminal(p):
                classifier.terminal_paragraphs.add(p_name)

        for s in model.sections:
            s_name = s.name.upper().strip()
            if classifier.is_paragraph_terminal(s):
                classifier.terminal_paragraphs.add(s_name)

        # Pass 2: Iterative Fixed-Point Propagation (if enabled in rules)
        if classifier.effective_rules.transitive_enabled:
            changed = True
            while changed:
                changed = False
                for p in model.paragraphs:
                    p_name = p.name.upper().strip()
                    if (
                        p_name in classifier.terminal_paragraphs
                        or classifier.effective_rules.is_excluded(p_name)
                    ):
                        continue

                    stmts = p.statements
                    if not stmts:
                        continue

                    # Check if last statement unconditionally invokes a terminal procedure
                    last_stmt = stmts[-1]
                    if isinstance(last_stmt, PerformStatementNode) and last_stmt.target:
                        tgt = last_stmt.target.upper().strip()
                        if tgt in classifier.terminal_paragraphs and not (
                            last_stmt.until_condition or last_stmt.varying_expr
                        ):
                            classifier.terminal_paragraphs.add(p_name)
                            changed = True

        return classifier
