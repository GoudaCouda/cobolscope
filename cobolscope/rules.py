"""
cobolscope.rules
~~~~~~~~~~~~~~~~

Declarative YAML rules engine for abnormal termination (ABEND), exit point classification,
custom paragraph patterns, runtime modules, database/condition checks, and per-program overrides.
"""

from __future__ import annotations

import logging
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel, Field
import yaml

logger = logging.getLogger(__name__)

DEFAULT_RUNTIME_MODULES: List[str] = [
    "CEE3ABD",   # IBM Language Environment Abend
    "ILBOABN0",  # OS/VS COBOL Legacy Abend
    "ABNDPROC",  # Custom mainframe abend processor
    "ABORT",     # POSIX / Micro Focus abort wrapper
    "CANCL",     # Transaction cancellation runtime
]

DEFAULT_STRICT_PARAGRAPHS: List[str] = [
    "999-ABEND",
    "999-ABEND-EXIT",
    "9999-ABEND",
    "ABEND-ROUTINE",
    "ABEND-HANDLING",
    "FATAL-ERROR",
]

DEFAULT_PARAGRAPH_PATTERNS: List[str] = [
    r"^.*-ABEND(?:-EXIT)?$",
    r"^.*-FATAL(?:-ERROR)?$",
    r"^.*-KILL$",
    r"^.*-ABORT$",
    r"^.*-CANCEL$",
]

DEFAULT_EXCLUDE_CICS_HANDLERS: List[str] = [
    "HANDLE ABEND",
    "HANDLE CONDITION",
    "IGNORE CONDITION",
    "PUSH HANDLE",
    "POP HANDLE",
]


class ParagraphNamingRules(BaseModel):
    strict: List[str] = Field(default_factory=lambda: list(DEFAULT_STRICT_PARAGRAPHS))
    patterns: List[str] = Field(default_factory=lambda: list(DEFAULT_PARAGRAPH_PATTERNS))


class SyntaxPrimitivesRules(BaseModel):
    stop_run: bool = True
    goback: bool = True
    exit_program: bool = True
    exec_cics_return: bool = True
    exec_cics_abend: bool = True


class CicsOptionsRules(BaseModel):
    exclude_handlers: List[str] = Field(default_factory=lambda: list(DEFAULT_EXCLUDE_CICS_HANDLERS))


class HardwareExceptionRules(BaseModel):
    detect_s0c7_idioms: bool = True
    detect_divide_by_zero: bool = True


class AbendConditionRule(BaseModel):
    condition_pattern: str
    description: Optional[str] = None
    action: str = "ABEND"


DEFAULT_ABEND_CONDITIONS: List[AbendConditionRule] = [
    AbendConditionRule(
        condition_pattern=r"SQLCODE\s*(?:NOT\s*=\s*0|IS\s+NOT\s+EQUAL\s+TO\s+ZERO|<)",
        description="DB2 SQL Error Condition",
    ),
    AbendConditionRule(
        condition_pattern=r"(?:FILE-STATUS|FSCODE)\s*(?:NOT\s*=\s*['\"]00['\"]|IS\s+NOT\s+EQUAL\s+TO\s+['\"]00['\"])",
        description="File Status Error Condition",
    ),
    AbendConditionRule(
        condition_pattern=r"CONNECT-FAILED",
        description="Database Connection Failure",
    ),
]


class ConditionalCheckRules(BaseModel):
    abend_conditions: List[AbendConditionRule] = Field(
        default_factory=lambda: [r.model_copy() for r in DEFAULT_ABEND_CONDITIONS]
    )
    auto_classify_abend_branches: bool = True


class StatementRules(BaseModel):
    syntax_primitives: SyntaxPrimitivesRules = Field(default_factory=SyntaxPrimitivesRules)
    cics_options: CicsOptionsRules = Field(default_factory=CicsOptionsRules)
    hardware_exceptions: HardwareExceptionRules = Field(default_factory=HardwareExceptionRules)
    conditional_checks: ConditionalCheckRules = Field(default_factory=ConditionalCheckRules)


class TransitiveRules(BaseModel):
    enabled: bool = True
    unconditional_only: bool = True


class ProgramOverrideRules(BaseModel):
    terminal_paragraphs: List[str] = Field(default_factory=list)
    non_terminal_paragraphs: List[str] = Field(default_factory=list)
    runtime_modules: List[str] = Field(default_factory=list)
    abend_conditions: List[AbendConditionRule] = Field(default_factory=list)


class GlobalRules(BaseModel):
    version: str = "1.0"
    runtime_modules: List[str] = Field(default_factory=lambda: list(DEFAULT_RUNTIME_MODULES))
    paragraph_names: ParagraphNamingRules = Field(default_factory=ParagraphNamingRules)
    statement_rules: StatementRules = Field(default_factory=StatementRules)
    transitive_propagation: TransitiveRules = Field(default_factory=TransitiveRules)
    programs: Dict[str, ProgramOverrideRules] = Field(default_factory=dict)


class EffectiveProgramRules:
    """
    Optimized, pre-compiled evaluation rule view for a specific program (or global fallback).
    """

    def __init__(self, rules: GlobalRules, program_id: Optional[str] = None):
        self.program_id: Optional[str] = program_id.upper().strip() if program_id else None
        prog_override = rules.programs.get(self.program_id or "", ProgramOverrideRules())

        # Exclusions (highest precedence)
        self.excluded_paragraphs: Set[str] = {
            p.upper().strip() for p in prog_override.non_terminal_paragraphs
        }

        # Strict paragraphs (global + program override)
        self.strict_paragraphs: Set[str] = {
            p.upper().strip() for p in rules.paragraph_names.strict
        } | {p.upper().strip() for p in prog_override.terminal_paragraphs}

        # Compiled paragraph regexes
        self.compiled_patterns: List[re.Pattern] = []
        for pat in rules.paragraph_names.patterns:
            try:
                self.compiled_patterns.append(re.compile(pat, re.IGNORECASE))
            except re.error as e:
                logger.warning(f"Invalid regex pattern in rules: '{pat}': {e}")

        # Runtime modules
        self.runtime_modules: Set[str] = {
            m.upper().strip() for m in rules.runtime_modules
        } | {m.upper().strip() for m in prog_override.runtime_modules}

        # Statement and CICS rules
        self.statement_rules = rules.statement_rules
        self.syntax_primitives = rules.statement_rules.syntax_primitives
        self.cics_exclude_handlers: Set[str] = {
            h.upper().strip() for h in rules.statement_rules.cics_options.exclude_handlers
        }
        self.detect_s0c7_idioms = rules.statement_rules.hardware_exceptions.detect_s0c7_idioms
        self.detect_divide_by_zero = rules.statement_rules.hardware_exceptions.detect_divide_by_zero

        # Compiled abend conditions
        self.compiled_abend_conditions: List[Tuple[re.Pattern, str]] = []
        all_conditions = (
            rules.statement_rules.conditional_checks.abend_conditions
            + prog_override.abend_conditions
        )
        for cond in all_conditions:
            try:
                self.compiled_abend_conditions.append(
                    (re.compile(cond.condition_pattern, re.IGNORECASE), cond.action)
                )
            except re.error as e:
                logger.warning(f"Invalid condition pattern in rules: '{cond.condition_pattern}': {e}")

        # Transitive propagation
        self.transitive_enabled = rules.transitive_propagation.enabled
        self.unconditional_only = rules.transitive_propagation.unconditional_only

    def is_excluded(self, name: str) -> bool:
        """Returns True if the routine is explicitly configured as non-terminal in overrides."""
        return name.upper().strip() in self.excluded_paragraphs

    def is_strict_terminal(self, name: str) -> bool:
        """Returns True if the routine matches strict paragraph names."""
        clean = name.upper().strip()
        if self.is_excluded(clean):
            return False
        return clean in self.strict_paragraphs

    def matches_terminal_pattern(self, name: str) -> bool:
        """Returns True if the routine matches configured terminal regex patterns."""
        clean = name.upper().strip()
        if self.is_excluded(clean):
            return False
        return any(pat.search(clean) for pat in self.compiled_patterns)

    def is_terminal_name(self, name: str) -> bool:
        """Returns True if the routine name is terminal via strict or regex rules."""
        return self.is_strict_terminal(name) or self.matches_terminal_pattern(name)

    def is_runtime_abend_module(self, module_name: str) -> bool:
        """Returns True if the called module name is an abend runtime program."""
        clean = module_name.upper().strip().strip("'\"")
        if clean in self.runtime_modules:
            return True
        # Generic heuristic regex fallback
        return bool(re.search(r"(?:^|[-_])(?:ABEND|FATAL|KILL|CANCEL|ABORT)(?:[-_]|$)", clean))

    def matches_abend_condition(self, condition_expr: str) -> bool:
        """Returns True if the condition expression indicates a fatal abend check."""
        clean = (condition_expr or "").strip().upper()
        if not clean:
            return False
        return any(pat.search(clean) for pat, _ in self.compiled_abend_conditions)


def get_default_rules() -> GlobalRules:
    """Returns a fresh instance of the default GlobalRules."""
    return GlobalRules()


def get_effective_rules(
    rules: Optional[GlobalRules] = None, program_id: Optional[str] = None
) -> EffectiveProgramRules:
    """Derives EffectiveProgramRules for a specific program, falling back to default rules."""
    if rules is None:
        rules = load_rules()
    return EffectiveProgramRules(rules, program_id=program_id)


DEFAULT_RULE_FILENAMES = [
    "cobolscope-rules.yaml",
    ".cobolscope-rules.yaml",
    "cobolscope.yaml",
    ".cobolscope.yaml",
]


def find_rules_file(cwd: Optional[Path] = None) -> Optional[Path]:
    """Searches current or parent directories for a standard CobolScope rules file."""
    search_dir = (cwd or Path.cwd()).resolve()
    for name in DEFAULT_RULE_FILENAMES:
        cand = search_dir / name
        if cand.is_file():
            return cand

    # Check parent directory
    parent = search_dir.parent
    if parent != search_dir:
        for name in DEFAULT_RULE_FILENAMES:
            cand = parent / name
            if cand.is_file():
                return cand

    return None


def load_rules(
    path: Optional[Union[str, Path]] = None, cwd: Optional[Path] = None
) -> GlobalRules:
    """
    Loads GlobalRules from a YAML file if specified or found in the workspace.
    Falls back to built-in default GlobalRules if no file exists.
    """
    target_path: Optional[Path] = None
    if path is not None:
        target_path = Path(path).resolve()
        if not target_path.is_file():
            raise FileNotFoundError(f"Specified rules file not found: {target_path}")
    else:
        target_path = find_rules_file(cwd=cwd)

    if target_path is None:
        return get_default_rules()

    try:
        data = yaml.safe_load(target_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            logger.warning(f"Rules file '{target_path}' is empty or invalid. Using defaults.")
            return get_default_rules()
        return GlobalRules.model_validate(data)
    except Exception as e:
        logger.error(f"Error loading rules from '{target_path}': {e}. Falling back to default rules.")
        return get_default_rules()


def rules_to_yaml_string(rules: GlobalRules) -> str:
    """Renders GlobalRules to a formatted, well-commented YAML document."""
    d = rules.model_dump(exclude_none=True)

    header = (
        "# ==============================================================================\n"
        "# CobolScope Terminal & Abend Rules Configuration\n"
        "#\n"
        "# This configuration governs abnormal termination (ABEND) detection,\n"
        "# control flow graph (CFG) terminal node placement, and call graph reachability.\n"
        "# You can customize global defaults or add program-specific overrides.\n"
        "# ==============================================================================\n\n"
    )
    body = yaml.dump(d, default_flow_style=False, sort_keys=False)
    return header + body


def save_rules(rules: GlobalRules, path: Union[str, Path]) -> None:
    """Saves GlobalRules to disk as a formatted YAML file."""
    out_file = Path(path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(rules_to_yaml_string(rules), encoding="utf-8")
