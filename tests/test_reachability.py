"""
tests.test_reachability
~~~~~~~~~~~~~~~~~~~~~~~

Unit and integration tests for the Interprocedural Pushdown Reachability Analyzer.
Validates LIFO call stack worklist exploration, PERFORM return boundaries,
true intra-range fallthroughs, and state transition graph serialization.
"""

import sys
import unittest
from pathlib import Path

# Ensure repository root is in sys.path
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from cobolscope.reachability import PushdownReachabilityAnalyzer, TransitionKind
from tests.harness.test_cache import get_test_model


class TestPushdownReachability(unittest.TestCase):

    def test_reachability_graph_edge_cases(self):
        """Validates interprocedural pushdown reachability on synthetic graph edge cases."""
        model = get_test_model("tests/fixtures/TEST-GRAPH-EDGE-CASES.cbl")
        analyzer = PushdownReachabilityAnalyzer(model)
        res = analyzer.analyze()

        self.assertEqual(res.entrypoint, "0000-START")
        self.assertIn("0000-START", res.reachable_paragraphs)
        self.assertIn("2000-FIRST-PARA", res.reachable_paragraphs)
        self.assertIn("3000-ROUTINE", res.reachable_paragraphs)
        self.assertIn("4000-DISPATCH", res.reachable_paragraphs)
        self.assertIn("4100-NEW-ACCT", res.reachable_paragraphs)
        self.assertIn("4200-UPDATE-ACCT", res.reachable_paragraphs)
        self.assertIn("4300-CLOSE-ACCT", res.reachable_paragraphs)

        # Uncalled declaratives, isolated routines, and post-jump dead code are unreachable
        self.assertIn("ERROR-LOG-PARA", res.unreachable_paragraphs)
        self.assertIn("1000-TERMINATE", res.unreachable_paragraphs)
        self.assertIn("1100-OBSOLETE-CLEANUP", res.unreachable_paragraphs)
        self.assertIn("3100-SKIPPED-LOGIC", res.unreachable_paragraphs)

        # State transition sanity
        self.assertGreater(len(res.state_transitions), 5)
        kinds = {t.kind for t in res.state_transitions}
        self.assertIn(TransitionKind.CALL_PERFORM, kinds)
        self.assertIn(TransitionKind.TERMINATE, kinds)

    def test_reachability_bank_of_z_xfrfun(self):
        """Validates pushdown reachability and dead code detection on Bank-of-Z XFRFUN.cbl."""
        model = get_test_model("tests/fixtures/bank_of_z/cobol/XFRFUN.cbl")
        analyzer = PushdownReachabilityAnalyzer(model)
        res = analyzer.analyze()

        self.assertEqual(res.entrypoint, "A010")
        self.assertIn("A010", res.reachable_paragraphs)
        self.assertIn("CFSDD010", res.reachable_paragraphs)
        self.assertIn("PTD010", res.reachable_paragraphs)
        self.assertIn("UAD010", res.reachable_paragraphs)

        # Uncalled abend handlers are correctly flagged as unreachable
        self.assertIn("A999", res.unreachable_paragraphs)
        self.assertIn("GMOOH999", res.unreachable_paragraphs)
        self.assertIn("AH010", res.unreachable_paragraphs)
        self.assertIn("AH999", res.unreachable_paragraphs)

    def test_reachability_bank_of_z_inqcust(self):
        """Validates pushdown reachability across 20 routines in Bank-of-Z INQCUST.cbl."""
        model = get_test_model("tests/fixtures/bank_of_z/cobol/INQCUST.cbl")
        analyzer = PushdownReachabilityAnalyzer(model)
        res = analyzer.analyze()

        self.assertEqual(res.entrypoint, "P010")
        self.assertEqual(len(res.reachable_paragraphs), 20)
        self.assertEqual(len(res.unreachable_paragraphs), 0)


if __name__ == "__main__":
    unittest.main()
