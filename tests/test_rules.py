"""
tests.test_rules
~~~~~~~~~~~~~~~~

Comprehensive verification test suite for the declarative YAML rules engine,
effective program rule derivation, per-program overrides/exclusions,
conditional checks, and automated codebase rule generation.
"""

from pathlib import Path
import tempfile
import unittest

from cobolscope.rules import (
    GlobalRules,
    ParagraphNamingRules,
    ProgramOverrideRules,
    AbendConditionRule,
    get_default_rules,
    get_effective_rules,
    load_rules,
    save_rules,
    rules_to_yaml_string,
)
from cobolscope.rules_generator import (
    scan_program_for_rules,
    generate_rules_from_models,
    generate_rules_file,
)
from cobolscope.graph.termination import TerminationClassifier
from cobolscope.models import (
    ProgramModel,
    ParagraphNode,
    SectionNode,
    StopStatementNode,
    GobackStatementNode,
    CallStatementNode,
    PerformStatementNode,
    MoveStatementNode,
    AddStatementNode,
)
from tests.harness.test_cache import get_test_model


class TestRulesEngine(unittest.TestCase):
    """Tests declarative YAML rules loading, overrides, and evaluation."""

    def test_default_rules(self):
        rules = get_default_rules()
        self.assertEqual(rules.version, "1.0")
        self.assertIn("CEE3ABD", rules.runtime_modules)
        self.assertIn("ILBOABN0", rules.runtime_modules)
        self.assertIn("ABNDPROC", rules.runtime_modules)
        self.assertIn("999-ABEND", rules.paragraph_names.strict)
        self.assertTrue(rules.statement_rules.syntax_primitives.stop_run)
        self.assertTrue(rules.statement_rules.hardware_exceptions.detect_s0c7_idioms)

        effective = get_effective_rules(rules)
        self.assertTrue(effective.is_strict_terminal("999-ABEND"))
        self.assertTrue(effective.matches_terminal_pattern("MY-ERR-ABEND"))
        self.assertTrue(effective.is_runtime_abend_module("CEE3ABD"))
        self.assertFalse(effective.is_excluded("999-ABEND"))

    def test_custom_yaml_rules_roundtrip(self):
        custom_yaml = """
version: "1.0"
runtime_modules:
  - SITE_ABEND_SVC
  - CRASH_NOW
paragraph_names:
  strict:
    - ERR-HALT-01
  patterns:
    - "^KILL-.*$"
statement_rules:
  syntax_primitives:
    stop_run: true
    goback: false
    exit_program: true
    exec_cics_return: true
    exec_cics_abend: true
  cics_options:
    exclude_handlers:
      - HANDLE ABEND
  hardware_exceptions:
    detect_s0c7_idioms: false
    detect_divide_by_zero: true
  conditional_checks:
    abend_conditions:
      - condition_pattern: "DB-STATUS\\\\s*NOT\\\\s*=\\\\s*OK"
        description: "Custom DB failure"
        action: "ABEND"
    auto_classify_abend_branches: true
transitive_propagation:
  enabled: true
  unconditional_only: true
programs:
  TESTPGM:
    terminal_paragraphs:
      - SPECIAL-FINISH
    non_terminal_paragraphs:
      - KILL-RETRY
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8") as f:
            f.write(custom_yaml)
            tmp_path = Path(f.name)

        try:
            loaded = load_rules(path=tmp_path)
            self.assertIn("SITE_ABEND_SVC", loaded.runtime_modules)
            self.assertFalse(loaded.statement_rules.syntax_primitives.goback)
            self.assertFalse(loaded.statement_rules.hardware_exceptions.detect_s0c7_idioms)

            # Check effective rules without program_id
            eff_global = get_effective_rules(loaded)
            self.assertTrue(eff_global.is_strict_terminal("ERR-HALT-01"))
            self.assertTrue(eff_global.matches_terminal_pattern("KILL-ME"))
            self.assertTrue(eff_global.is_runtime_abend_module("SITE_ABEND_SVC"))

            # Check effective rules for TESTPGM
            eff_pgm = get_effective_rules(loaded, program_id="TESTPGM")
            # Program-specific addition
            self.assertTrue(eff_pgm.is_strict_terminal("SPECIAL-FINISH"))
            # Program-specific exclusion (highest precedence: should override KILL- pattern!)
            self.assertTrue(eff_pgm.is_excluded("KILL-RETRY"))
            self.assertFalse(eff_pgm.matches_terminal_pattern("KILL-RETRY"))
            self.assertFalse(eff_pgm.is_terminal_name("KILL-RETRY"))

            # But for another program, KILL-RETRY is NOT excluded!
            eff_other = get_effective_rules(loaded, program_id="OTHERPGM")
            self.assertFalse(eff_other.is_excluded("KILL-RETRY"))
            self.assertTrue(eff_other.matches_terminal_pattern("KILL-RETRY"))
            self.assertFalse(eff_other.is_terminal_name("SPECIAL-FINISH"))

            # Conditional check
            self.assertTrue(eff_pgm.matches_abend_condition("DB-STATUS NOT = OK"))
            self.assertFalse(eff_pgm.matches_abend_condition("DB-STATUS = OK"))
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_termination_classifier_respects_exclusions(self):
        """Verify that a program override non_terminal_paragraphs forces a routine to be non-terminal."""
        rules = get_default_rules()
        rules.programs["PGM1"] = ProgramOverrideRules(
            non_terminal_paragraphs=["999-ABEND"]  # Force exclusion of normally-strict abend paragraph
        )

        clf_pgm1 = TerminationClassifier(rules=rules, program_id="PGM1")
        clf_pgm2 = TerminationClassifier(rules=rules, program_id="PGM2")

        p_abend = ParagraphNode(name="999-ABEND", statements=[StopStatementNode()])

        # In PGM1, exclusion override prevents it from being marked terminal by name
        self.assertTrue(clf_pgm1.effective_rules.is_excluded("999-ABEND"))
        self.assertFalse(clf_pgm1.is_paragraph_terminal(p_abend))

        # In PGM2, it terminates normally
        self.assertFalse(clf_pgm2.effective_rules.is_excluded("999-ABEND"))
        self.assertTrue(clf_pgm2.is_paragraph_terminal(p_abend))

    def test_termination_classifier_per_program_custom_paragraph(self):
        """Verify that a one-off program exception is recognized without editing global rules."""
        rules = get_default_rules()
        rules.programs["XFRFUN"] = ProgramOverrideRules(
            terminal_paragraphs=["GMOOH010"]
        )

        clf_xfr = TerminationClassifier(rules=rules, program_id="XFRFUN")
        clf_other = TerminationClassifier(rules=rules, program_id="OTHER")

        p_gmooh = ParagraphNode(name="GMOOH010", statements=[])

        self.assertTrue(clf_xfr.is_paragraph_terminal(p_gmooh))
        self.assertFalse(clf_other.is_paragraph_terminal(p_gmooh))

    def test_rule_scanner_and_generator(self):
        """Verify scanning real AST models and producing clean YAML rules."""
        model_xfr = get_test_model("tests/fixtures/bank_of_z/cobol/XFRFUN.cbl")
        scan_res = scan_program_for_rules(model_xfr)

        self.assertEqual(scan_res["program_id"], "XFRFUN")
        self.assertIn("ABEND-HANDLING", scan_res["global_strict_paragraphs"])
        self.assertIn("GMOOH010", scan_res["program_terminal_paragraphs"])
        self.assertIn("AH010", scan_res["program_terminal_paragraphs"])

        generated_rules = generate_rules_from_models([model_xfr])
        self.assertIn("XFRFUN", generated_rules.programs)
        self.assertIn("GMOOH010", generated_rules.programs["XFRFUN"].terminal_paragraphs)

        yaml_str = rules_to_yaml_string(generated_rules)
        self.assertIn("GMOOH010", yaml_str)
        self.assertIn("XFRFUN", yaml_str)


if __name__ == "__main__":
    unittest.main()
