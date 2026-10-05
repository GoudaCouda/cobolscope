"""
Unit and regression tests for CobolScope Streamlined CLI parsing,
smart format inference, flag normalization, and backwards compatibility.
"""

import unittest
from pathlib import Path
from cobolscope.cli import build_arg_parser, parse_args


class TestCliStreamlining(unittest.TestCase):
    """Verifies that the streamlined CLI correctly parses options and infers formats."""

    def test_clean_help_does_not_contain_suppressed_internals(self):
        """Verifies that internal rendering knobs are hidden from the user-facing --help output."""
        parser = build_arg_parser()
        help_text = parser.format_help()

        # Core options should be visible
        self.assertIn("--graph", help_text)
        self.assertIn("--dict", help_text)
        self.assertIn("--reachability", help_text)
        self.assertIn("--disentangle", help_text)
        self.assertIn("--cluster-mode", help_text)
        self.assertIn("--hide-fillers", help_text)

        # Internal rendering knobs should NOT be visible in help
        self.assertNotIn("--splines", help_text)
        self.assertNotIn("--nodesep", help_text)
        self.assertNotIn("--ranksep", help_text)
        self.assertNotIn("--ranker", help_text)
        self.assertNotIn("--no-concentrate", help_text)
        self.assertNotIn("--no-dynamic-heuristics", help_text)
        self.assertNotIn("--detailed-nodes", help_text)
        self.assertNotIn("--no-collapse-exits", help_text)
        self.assertNotIn("--save-transitions", help_text)

    def test_backwards_compatibility_suppressed_flags_still_work(self):
        """Verifies that legacy/advanced flags still parse cleanly without raising errors."""
        args = parse_args([
            "PROG.cbl",
            "--splines", "ortho",
            "--nodesep", "1.5",
            "--ranksep", "2.0",
            "--ranker", "tight-tree",
            "--no-concentrate",
            "--no-collapse-exits",
            "--no-cluster",
            "--enable-cloning",
            "--clone-mode", "caller",
            "--clone-threshold", "5",
            "--graph-format", "svg",
            "--dict-format", "csv",
            "--save-transitions", "trans.json",
        ])

        self.assertEqual(args.splines, "ortho")
        self.assertEqual(args.nodesep, 1.5)
        self.assertEqual(args.ranksep, 2.0)
        self.assertEqual(args.ranker, "tight-tree")
        self.assertFalse(args.concentrate)
        self.assertFalse(args.collapse_exits)
        self.assertFalse(args.enable_clustering)
        self.assertTrue(args.enable_cloning)
        self.assertEqual(args.clone_mode, "caller")
        self.assertEqual(args.clone_threshold, 5)
        self.assertEqual(args.graph_format, "svg")
        self.assertEqual(args.dict_format, "csv")
        self.assertEqual(args.save_transitions, "trans.json")

    def test_disentangle_flag_defaults_to_section(self):
        """Verifies --disentangle parses cleanly with and without arguments."""
        args_default = parse_args(["PROG.cbl", "--disentangle"])
        self.assertEqual(args_default.disentangle, "section")

        args_caller = parse_args(["PROG.cbl", "--disentangle", "caller"])
        self.assertEqual(args_caller.disentangle, "caller")

    def test_cluster_mode_options(self):
        """Verifies --cluster-mode accepts valid hierarchy settings."""
        for mode in ("auto", "none", "sections", "semantic"):
            args = parse_args(["PROG.cbl", "--cluster-mode", mode])
            self.assertEqual(args.cluster_mode, mode)


if __name__ == "__main__":
    unittest.main()
