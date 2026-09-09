"""
tests.test_termination
~~~~~~~~~~~~~~~~~~~~~~

Comprehensive verification suite for the multi-layer TerminationClassifier.
Validates:
- Layer 1: Language syntax primitives (STOP RUN, GOBACK, EXIT PROGRAM, EXEC CICS ABEND/RETURN).
- Layer 2: Well-known runtime abend modules (CEE3ABD, ILBOABN0, ABORT, CANCL, CBLTDLI ROLL).
- Layer 3: Deliberate hardware crash sequence detection (IBM S0C7 Data Exception idiom).
- Layer 4: Interprocedural fixed-point propagation across routine call graphs.
- Integration: Accurate detection on real-world mainframe fixtures (TU6852RM.cbl).
"""

import sys
import unittest
from pathlib import Path

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.models import (
    CallStatementNode,
    ExecCicsStatementNode,
    ExitStatementNode,
    GobackStatementNode,
    IfStatementNode,
    MoveStatementNode,
    ParagraphNode,
    PerformStatementNode,
    ProgramModel,
    SourceLocation,
    StopStatementNode,
    GenericStatementNode,
    AddStatementNode,
)
from cobolscope.graph.termination import TerminationClassifier
from tests.harness.test_cache import get_test_model


def _loc() -> SourceLocation:
    return SourceLocation(start_line=1, end_line=1, start_column=1, end_column=10, source_file="TEST.cbl")


class TestTerminationClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = TerminationClassifier()

    def test_layer1_syntax_primitives(self):
        """Layer 1: Standard language verbs that unconditionally terminate execution."""
        stop_node = StopStatementNode(type="STOP", location=_loc(), raw_text="STOP RUN", target_field_ids=[], source_field_ids=[], statement="STOP RUN")
        goback_node = GobackStatementNode(type="GOBACK", location=_loc(), raw_text="GOBACK", target_field_ids=[], source_field_ids=[])
        exit_prog = ExitStatementNode(type="EXIT", location=_loc(), raw_text="EXIT PROGRAM", target_field_ids=[], source_field_ids=[], operation="EXIT PROGRAM")
        plain_exit = ExitStatementNode(type="EXIT", location=_loc(), raw_text="EXIT", target_field_ids=[], source_field_ids=[], operation="EXIT")

        self.assertTrue(self.classifier.is_statement_terminal(stop_node))
        self.assertTrue(self.classifier.is_statement_terminal(goback_node))
        self.assertTrue(self.classifier.is_statement_terminal(exit_prog))
        self.assertFalse(self.classifier.is_statement_terminal(plain_exit))

        # CICS primitives
        cics_abend = ExecCicsStatementNode(type="EXEC_CICS", location=_loc(), raw_text="EXEC CICS ABEND ABCODE('HROL') END-EXEC", target_field_ids=[], source_field_ids=[], raw_payload="EXEC CICS ABEND ABCODE('HROL') END-EXEC")
        cics_return = ExecCicsStatementNode(type="EXEC_CICS", location=_loc(), raw_text="EXEC CICS RETURN END-EXEC", target_field_ids=[], source_field_ids=[], raw_payload="EXEC CICS RETURN END-EXEC")
        cics_handle = ExecCicsStatementNode(type="EXEC_CICS", location=_loc(), raw_text="EXEC CICS HANDLE ABEND LABEL(ERR-ROUTINE) END-EXEC", target_field_ids=[], source_field_ids=[], raw_payload="EXEC CICS HANDLE ABEND LABEL(ERR-ROUTINE) END-EXEC")
        cics_cond = ExecCicsStatementNode(type="EXEC_CICS", location=_loc(), raw_text="EXEC CICS HANDLE CONDITION ERROR(ERR-ROUTINE) END-EXEC", target_field_ids=[], source_field_ids=[], raw_payload="EXEC CICS HANDLE CONDITION ERROR(ERR-ROUTINE) END-EXEC")

        self.assertTrue(self.classifier.is_statement_terminal(cics_abend))
        self.assertTrue(self.classifier.is_statement_terminal(cics_return))
        # Non-fatal error-handler declarations must NOT be flagged as terminal
        self.assertFalse(self.classifier.is_statement_terminal(cics_handle))
        self.assertFalse(self.classifier.is_statement_terminal(cics_cond))

    def test_layer2_runtime_abend_modules(self):
        """Layer 2: Standard mainframe runtime modules that trigger abends."""
        call_cee = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'CEE3ABD' USING CEE3ABD-CODE", target_field_ids=[], source_field_ids=[], program="CEE3ABD")
        call_ilbo = CallStatementNode(type="CALL", location=_loc(), raw_text='CALL "ILBOABN0" USING ABEND-CODE', target_field_ids=[], source_field_ids=[], program="ILBOABN0")
        call_abort = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'ABORT'", target_field_ids=[], source_field_ids=[], program="ABORT")
        call_cancl = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'CANCL'", target_field_ids=[], source_field_ids=[], program="CANCL")
        call_ims_roll = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'CBLTDLI' USING 'ROLL' PCB-MASK", target_field_ids=[], source_field_ids=[], program="CBLTDLI", using_parameters=["'ROLL'", "PCB-MASK"])
        call_ims_get = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'CBLTDLI' USING 'GU' PCB-MASK", target_field_ids=[], source_field_ids=[], program="CBLTDLI", using_parameters=["'GU'", "PCB-MASK"])
        call_normal = CallStatementNode(type="CALL", location=_loc(), raw_text="CALL 'FORMAT-DATE' USING DATE-REC", target_field_ids=[], source_field_ids=[], program="FORMAT-DATE")

        self.assertTrue(self.classifier.is_statement_terminal(call_cee))
        self.assertTrue(self.classifier.is_statement_terminal(call_ilbo))
        self.assertTrue(self.classifier.is_statement_terminal(call_abort))
        self.assertTrue(self.classifier.is_statement_terminal(call_cancl))
        self.assertTrue(self.classifier.is_statement_terminal(call_ims_roll))
        self.assertFalse(self.classifier.is_statement_terminal(call_ims_get))
        self.assertFalse(self.classifier.is_statement_terminal(call_normal))

    def test_layer3_s0c7_hardware_crash_idiom(self):
        """Layer 3: Deliberate data exception sequence (MOVE LOW-VALUES + ADD 1)."""
        s1 = MoveStatementNode(
            type="MOVE", location=_loc(), raw_text="MOVE LOW-VALUES TO DATA-EXCEPTION",
            target_field_ids=["DATA-EXCEPTION"], source_field_ids=[],
            from_expr="LOW-VALUES", to_targets=["DATA-EXCEPTION"]
        )
        s2 = AddStatementNode(
            type="ADD", location=_loc(), raw_text="ADD 1 TO DATA-EXCEPTION-TRIGGER",
            target_field_ids=["DATA-EXCEPTION-TRIGGER"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO DATA-EXCEPTION-TRIGGER"
        )
        self.assertTrue(self.classifier.is_s0c7_crash_sequence(s1, s2))

        # Also works with SPACES
        s1_spaces = MoveStatementNode(
            type="MOVE", location=_loc(), raw_text="MOVE SPACES TO CRASH-FLD",
            target_field_ids=["CRASH-FLD"], source_field_ids=[],
            from_expr="SPACES", to_targets=["CRASH-FLD"]
        )
        s2_spaces = AddStatementNode(
            type="ADD", location=_loc(), raw_text="ADD 1 TO CRASH-FLD",
            target_field_ids=["CRASH-FLD"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO CRASH-FLD"
        )
        self.assertTrue(self.classifier.is_s0c7_crash_sequence(s1_spaces, s2_spaces))

        # Non-crash normal moves must return False
        s1_norm = MoveStatementNode(
            type="MOVE", location=_loc(), raw_text="MOVE 10 TO WS-TOTAL",
            target_field_ids=["WS-TOTAL"], source_field_ids=[],
            from_expr="10", to_targets=["WS-TOTAL"]
        )
        s2_norm = AddStatementNode(
            type="ADD", location=_loc(), raw_text="ADD 1 TO WS-TOTAL",
            target_field_ids=["WS-TOTAL"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO WS-TOTAL"
        )
        self.assertFalse(self.classifier.is_s0c7_crash_sequence(s1_norm, s2_norm))

        # Paragraph check
        p_crash = ParagraphNode(
            name="999-ABEND", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=False, fallthrough_successor=None,
            statements=[
                GenericStatementNode(type="UNKNOWN", location=_loc(), raw_text="DISPLAY 'ABEND'", target_field_ids=[], source_field_ids=[], details={"original_type": "DISPLAY"}),
                s1,
                s2,
            ]
        )
        self.assertTrue(self.classifier.has_deliberate_s0c7_idiom(p_crash))
        self.assertTrue(self.classifier.is_paragraph_terminal(p_crash))

    def test_layer4_transitive_propagation(self):
        """Layer 4: Procedures that unconditionally invoke terminal routines become terminal."""
        s1 = MoveStatementNode(
            type="MOVE", location=_loc(), raw_text="MOVE LOW-VALUES TO DATA-EXCEPTION",
            target_field_ids=["DATA-EXCEPTION"], source_field_ids=[],
            from_expr="LOW-VALUES", to_targets=["DATA-EXCEPTION"]
        )
        s2 = AddStatementNode(
            type="ADD", location=_loc(), raw_text="ADD 1 TO DATA-EXCEPTION-TRIGGER",
            target_field_ids=["DATA-EXCEPTION-TRIGGER"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO DATA-EXCEPTION-TRIGGER"
        )
        # Root crash routine
        p_root_crash = ParagraphNode(
            name="ABEND-ROUTINE", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=False, fallthrough_successor=None,
            statements=[s1, s2]
        )

        # Unconditional caller of ABEND-ROUTINE
        p_fatal_handler = ParagraphNode(
            name="HANDLE-FATAL-ERROR", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=False, fallthrough_successor=None,
            statements=[
                GenericStatementNode(type="UNKNOWN", location=_loc(), raw_text="DISPLAY 'FATAL ERROR'", target_field_ids=[], source_field_ids=[], details={"original_type": "DISPLAY"}),
                PerformStatementNode(type="PERFORM", location=_loc(), raw_text="PERFORM ABEND-ROUTINE", target_field_ids=[], source_field_ids=[], target="ABEND-ROUTINE", is_inline=False),
            ]
        )

        # Conditional caller (should NOT be marked terminal)
        p_conditional_caller = ParagraphNode(
            name="PROCESS-DATA", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=False, fallthrough_successor=None,
            statements=[
                IfStatementNode(
                    type="IF", location=_loc(), raw_text="IF ERR = 'Y' PERFORM ABEND-ROUTINE END-IF",
                    target_field_ids=[], source_field_ids=[], condition="ERR = 'Y'",
                    then_statements=[
                        PerformStatementNode(type="PERFORM", location=_loc(), raw_text="PERFORM ABEND-ROUTINE", target_field_ids=[], source_field_ids=[], target="ABEND-ROUTINE", is_inline=False)
                    ],
                    else_statements=[]
                ),
                GenericStatementNode(type="UNKNOWN", location=_loc(), raw_text="DISPLAY 'CONTINUING'", target_field_ids=[], source_field_ids=[], details={"original_type": "DISPLAY"}),
            ]
        )

        # Normal routine
        p_normal = ParagraphNode(
            name="NORMAL-ROUTINE", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=False, fallthrough_successor=None,
            statements=[
                GenericStatementNode(type="UNKNOWN", location=_loc(), raw_text="DISPLAY 'HELLO'", target_field_ids=[], source_field_ids=[], details={"original_type": "DISPLAY"})
            ]
        )

        dummy_model = ProgramModel(
            program_id="TESTTERM",
            paragraphs=[p_root_crash, p_fatal_handler, p_conditional_caller, p_normal],
            sections=[],
            data_division_summary=None,
            source_file="TESTTERM.cbl"
        )

        prog_classifier = TerminationClassifier.for_program(dummy_model)
        self.assertIn("ABEND-ROUTINE", prog_classifier.terminal_paragraphs)
        self.assertIn("HANDLE-FATAL-ERROR", prog_classifier.terminal_paragraphs)
        self.assertNotIn("PROCESS-DATA", prog_classifier.terminal_paragraphs)
        self.assertNotIn("NORMAL-ROUTINE", prog_classifier.terminal_paragraphs)

    def test_tu6852_deliberate_crash_detection(self):
        """Validates detection of 999-ABEND deliberate crash from user TU6852 specification."""
        s_disp = GenericStatementNode(
            type="UNKNOWN", location=_loc(),
            raw_text="DISPLAY 'REQUIRED RECORD NOT FOUND ON TU-TABLES FOR PROGRAM TU6852P0'",
            target_field_ids=[], source_field_ids=[], details={"original_type": "DISPLAY"}
        )
        s_move = MoveStatementNode(
            type="MOVE", location=_loc(), raw_text="MOVE LOW-VALUES TO DATA-EXCEPTION",
            target_field_ids=["DATA-EXCEPTION"], source_field_ids=[],
            from_expr="LOW-VALUES", to_targets=["DATA-EXCEPTION"]
        )
        s_add = AddStatementNode(
            type="ADD", location=_loc(), raw_text="ADD 1 TO DATA-EXCEPTION-TRIGGER",
            target_field_ids=["DATA-EXCEPTION-TRIGGER"], source_field_ids=[],
            operation="ADD", expression="ADD 1 TO DATA-EXCEPTION-TRIGGER"
        )
        p_abend = ParagraphNode(
            name="999-ABEND", section_parent=None, location=_loc(),
            called_by=["PROCESS-CONTROLS-INTERFACE", "PROCESS-CONTROL-RECORD"],
            successors=[], is_terminal=False, fallthrough_successor="999-ABEND-EXIT",
            statements=[s_disp, s_move, s_add]
        )
        p_normal = ParagraphNode(
            name="WRITE-SUMMARY-RPT", section_parent=None, location=_loc(),
            called_by=["PROCESS-CONTROLS-INTERFACE"], successors=[], is_terminal=False,
            fallthrough_successor=None,
            statements=[
                GenericStatementNode(type="UNKNOWN", location=_loc(), raw_text="WRITE CONTROL-REC", target_field_ids=[], source_field_ids=[], details={"original_type": "WRITE"})
            ]
        )
        model = ProgramModel(
            program_id="TU6852RM",
            paragraphs=[p_abend, p_normal],
            sections=[],
            data_division_summary=None,
            source_file="TU6852RM.cbl"
        )
        prog_classifier = TerminationClassifier.for_program(model)

        self.assertIn("999-ABEND", prog_classifier.terminal_paragraphs)
        self.assertTrue(prog_classifier.is_paragraph_terminal(p_abend))
        self.assertNotIn("WRITE-SUMMARY-RPT", prog_classifier.terminal_paragraphs)
        self.assertFalse(prog_classifier.is_paragraph_terminal(p_normal))

    def test_bank_of_z_real_fixtures(self):
        """Validates termination classification across real-world Bank-of-Z benchmarks."""
        model_xfr = get_test_model("tests/fixtures/bank_of_z/cobol/XFRFUN.cbl")
        clf_xfr = TerminationClassifier.for_program(model_xfr)
        self.assertIn("GMOOH010", clf_xfr.terminal_paragraphs)

        model_inq = get_test_model("tests/fixtures/bank_of_z/cobol/INQCUST.cbl")
        clf_inq = TerminationClassifier.for_program(model_inq)
        self.assertIn("GMOFH010", clf_inq.terminal_paragraphs)

    def test_goto_terminal_statement(self):
        """GO TO referencing an abend paragraph is recognized as a terminal statement."""
        from cobolscope.models import GoToStatementNode
        goto_abend = GoToStatementNode(
            type="GO_TO", location=_loc(), raw_text="GO TO 999-ABEND",
            target_field_ids=[], source_field_ids=[], target="999-ABEND"
        )
        goto_normal = GoToStatementNode(
            type="GO_TO", location=_loc(), raw_text="GO TO 100-PROCESS",
            target_field_ids=[], source_field_ids=[], target="100-PROCESS"
        )
        p_abend = ParagraphNode(
            name="999-ABEND", section_parent=None, location=_loc(),
            called_by=[], successors=[], is_terminal=True, fallthrough_successor=None,
            statements=[StopStatementNode(type="STOP", location=_loc(), raw_text="STOP RUN", target_field_ids=[], source_field_ids=[])]
        )
        model = ProgramModel(
            program_id="TESTGOTO",
            paragraphs=[p_abend],
            sections=[],
            data_division_summary=None,
            source_file="TESTGOTO.cbl"
        )
        clf = TerminationClassifier.for_program(model)
        self.assertTrue(clf.is_statement_terminal(goto_abend))
        self.assertFalse(clf.is_statement_terminal(goto_normal))
        self.assertEqual(clf.get_terminal_label(goto_abend), "GO TO 999-ABEND")


if __name__ == "__main__":
    unittest.main()
