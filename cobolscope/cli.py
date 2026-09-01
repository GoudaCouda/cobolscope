#!/usr/bin/env python3
"""
Python CLI entry point for ProLeap COBOL Parser, Data Dictionary,
Call Graph Visualizer, and Pushdown Reachability Analyzer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from cobolscope.parser import (
    VALID_FORMATS,
    check_java_available,
    find_jar,
    find_runner_classpath,
    parse,
)


def build_arg_parser() -> argparse.ArgumentParser:
    """Constructs the unified CLI argument parser with organized option groups."""
    parser = argparse.ArgumentParser(
        prog="cobolscope",
        description="Unified CLI for CobolScope COBOL Parsing, Data Dictionaries, Call Graphs, and Reachability.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # ---------------------------------------------------------
    # Core Positional & Format Arguments
    # ---------------------------------------------------------
    parser.add_argument(
        "input_file",
        help="Path to the COBOL source file or copybook to parse.",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="FIXED",
        choices=VALID_FORMATS,
        type=str.upper,
        help="COBOL source format (FIXED, TANDEM, VARIABLE).",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output destination path (defaults to stdout).",
    )

    # ---------------------------------------------------------
    # Preprocessor & Copybook Resolution
    # ---------------------------------------------------------
    prep_group = parser.add_argument_group("Preprocessor & Copybook Options")
    prep_group.add_argument(
        "-I",
        "--copybook-dir",
        action="append",
        dest="copybook_dirs",
        metavar="DIR",
        help="Directory containing copybooks to resolve (repeatable).",
    )
    prep_group.add_argument(
        "--copybook-ext",
        action="append",
        dest="copybook_exts",
        metavar="EXT",
        help="Custom copybook file extensions without leading dot (e.g. 'cpy', 'cbl').",
    )
    prep_group.add_argument(
        "--ignore-errors",
        "--ignore-syntax-errors",
        action="store_true",
        dest="ignore_syntax_errors",
        help="Ignore minor syntax errors during ASG construction.",
    )

    # ---------------------------------------------------------
    # Output Modes (Subsystem Triggers)
    # ---------------------------------------------------------
    mode_group = parser.add_argument_group("Output Modes (Default: Canonical IR JSON)")
    mode_group.add_argument(
        "--dict",
        "--dictionary",
        action="store_true",
        dest="generate_dictionary",
        help="Generate a comprehensive Data Dictionary instead of raw IR JSON.",
    )
    mode_group.add_argument(
        "--graph",
        "--call-graph",
        action="store_true",
        dest="generate_graph",
        help="Generate a Level-2 Procedure Call Graph visualization.",
    )
    mode_group.add_argument(
        "--reachability",
        action="store_true",
        dest="generate_reachability",
        help="Run Pushdown Reachability Analysis and output verified transitions.",
    )

    # ---------------------------------------------------------
    # Data Dictionary Options
    # ---------------------------------------------------------
    dict_group = parser.add_argument_group("Data Dictionary Options (used with --dict)")
    dict_group.add_argument(
        "--dict-format",
        default="markdown",
        choices=["markdown", "md", "html", "csv", "json"],
        help="Output format for Data Dictionary.",
    )
    dict_group.add_argument(
        "--hide-fillers",
        action="store_true",
        help="Hide FILLER fields in Data Dictionary outputs.",
    )

    # ---------------------------------------------------------
    # Call Graph Options
    # ---------------------------------------------------------
    graph_group = parser.add_argument_group("Call Graph Options (used with --graph)")
    graph_group.add_argument(
        "--graph-format",
        default="svg",
        choices=["svg", "dot", "html", "json"],
        help="Output format for Call Graph.",
    )
    graph_group.add_argument(
        "--show-fallthrough",
        action="store_true",
        dest="show_fallthrough",
        default=False,
        help="Include physical sequential fall-through connectors in the call graph.",
    )
    graph_group.add_argument(
        "--no-collapse-exits",
        action="store_false",
        dest="collapse_exits",
        default=True,
        help="Disable automatic collapsing of dummy *-EXIT return paragraphs.",
    )
    graph_group.add_argument(
        "--no-cluster",
        action="store_false",
        dest="enable_clustering",
        default=True,
        help="Disable functional subsystem clustering subgraphs.",
    )

    # ---------------------------------------------------------
    # Reachability Options
    # ---------------------------------------------------------
    reach_group = parser.add_argument_group("Reachability Options")
    reach_group.add_argument(
        "--save-transitions",
        dest="save_transitions",
        metavar="FILE",
        help="Save serialized Pushdown State Transitions and Reachability model to file.",
    )

    # ---------------------------------------------------------
    # Java & Execution Environment
    # ---------------------------------------------------------
    env_group = parser.add_argument_group("JVM & Environment Options")
    env_group.add_argument(
        "--jar",
        help="Path to proleap-cobol-parser.jar (overrides PROLEAP_JAR env var).",
    )
    env_group.add_argument(
        "--runner-cp",
        help="Classpath entry containing compiled ProLeapCliRunner.class.",
    )
    env_group.add_argument(
        "--java-exe",
        default="java",
        help="Name or path of Java runtime executable.",
    )
    env_group.add_argument(
        "--java-arg",
        action="append",
        dest="java_args",
        metavar="ARG",
        help="Extra JVM argument (repeatable), e.g. --java-arg -Xmx2g.",
    )

    return parser


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parses command line arguments."""
    return build_arg_parser().parse_args(argv)


def _write_output(content: str, output_path: Optional[str]) -> None:
    """Helper to write content to a file or standard output."""
    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
    else:
        try:
            sys.stdout.write(content if content.endswith("\n") else content + "\n")
            sys.stdout.flush()
        except BrokenPipeError:
            pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main CLI entry point."""
    args = parse_args(argv)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    # 1. Parse COBOL source via Java parser bridge
    try:
        raw_dict = parse(
            input_file=input_path,
            format=args.format,
            copybook_dirs=args.copybook_dirs,
            copybook_exts=args.copybook_exts,
            ignore_syntax_errors=args.ignore_syntax_errors,
            jar_path=args.jar,
            runner_cp=args.runner_cp,
            java_exe=args.java_exe,
            extra_java_args=args.java_args,
        )
    except (FileNotFoundError, EnvironmentError) as e:
        print(f"ERROR: Environment setup error: {e}", file=sys.stderr)
        return 5
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: Parsing failed: {e}", file=sys.stderr)
        return 1

    # 2. Dispatch to requested mode
    try:
        # A. Data Dictionary Generation
        if args.generate_dictionary:
            from cobolscope.models import ProgramModel
            from cobolscope.data_dictionary import generate_data_dictionary

            model = ProgramModel.from_dict(raw_dict)
            content = generate_data_dictionary(
                model,
                format=args.dict_format,
                hide_fillers=args.hide_fillers,
            )
            _write_output(content, args.output)
            return 0

        # B. Call Graph Generation
        if args.generate_graph:
            from cobolscope.models import ProgramModel
            from cobolscope.graph import generate_call_graph

            model = ProgramModel.from_dict(raw_dict)
            content = generate_call_graph(
                model,
                format=args.graph_format,
                hide_fallthrough=not args.show_fallthrough,
                collapse_exits=args.collapse_exits,
                enable_clustering=args.enable_clustering,
            )
            _write_output(content, args.output)
            return 0

        # C. Pushdown Reachability Analysis
        if args.generate_reachability or args.save_transitions:
            from cobolscope.models import ProgramModel
            from cobolscope.reachability import PushdownReachabilityAnalyzer

            model = ProgramModel.from_dict(raw_dict)
            analyzer = PushdownReachabilityAnalyzer(model)
            reachability_model = analyzer.analyze()

            if args.save_transitions:
                reachability_model.to_json_file(args.save_transitions)

            if args.generate_reachability:
                content = reachability_model.model_dump_json(indent=2)
                _write_output(content, args.output)
            return 0

        # D. Default Mode: Output Canonical IR JSON
        content = json.dumps(raw_dict, indent=2)
        _write_output(content, args.output)
        return 0

    except Exception as e:
        print(f"ERROR: Pipeline generation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())