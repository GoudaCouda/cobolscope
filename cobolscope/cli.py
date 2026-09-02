#!/usr/bin/env python3
"""
Python CLI entry point for ProLeap COBOL Parser, Data Dictionary,
Call Graph Visualizer, and Pushdown Reachability Analyzer.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose telemetry and execution timing for each task/pipeline step.",
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
    graph_group.add_argument(
        "--cluster-mode",
        choices=["auto", "none", "sections", "semantic"],
        default="auto",
        help="Clustering strategy: 'auto' (clusters by SECTION if present, else unclustered hierarchy), 'sections', 'semantic', or 'none'.",
    )
    graph_group.add_argument(
        "--splines",
        choices=["spline", "ortho", "polyline", "curved"],
        default="spline",
        help="Graphviz edge routing style (spline, ortho, polyline, curved).",
    )
    graph_group.add_argument(
        "--detailed-nodes",
        action="store_true",
        dest="detailed_nodes",
        default=False,
        help="Render raw data variable lineage directly on node box face (default keeps boxes compact).",
    )
    graph_group.add_argument(
        "--no-concentrate",
        action="store_false",
        dest="concentrate",
        default=True,
        help="Disable Graphviz edge concentration/trunk merging.",
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
    verbose = args.verbose
    overall_start = time.perf_counter()

    def log_verbose(msg: str) -> None:
        if verbose:
            sys.stderr.write(f"[DEBUG] {msg}\n")
            sys.stderr.flush()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    log_verbose(f"Starting CobolScope CLI on target: {input_path}")
    log_verbose(f"Source format: {args.format}")

    # 1. Parse COBOL source via Java parser bridge
    parse_start = time.perf_counter()
    log_verbose("Invoking ProLeap Java parser bridge...")
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

    parse_dur = (time.perf_counter() - parse_start) * 1000
    log_verbose(f"Java parsing completed in {parse_dur:.2f} ms")

    # 2. Dispatch to requested mode
    try:
        # A. Data Dictionary Generation
        if args.generate_dictionary:
            dict_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Data Dictionary...")
            from cobolscope.models import ProgramModel
            from cobolscope.data_dictionary import generate_data_dictionary

            model = ProgramModel.from_dict(raw_dict)
            model_dur = (time.perf_counter() - dict_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            gen_start = time.perf_counter()
            log_verbose(f"Generating Data Dictionary (format={args.dict_format}, hide_fillers={args.hide_fillers})...")
            content = generate_data_dictionary(
                model,
                format=args.dict_format,
                hide_fillers=args.hide_fillers,
            )
            gen_dur = (time.perf_counter() - gen_start) * 1000
            log_verbose(f"Data Dictionary generated in {gen_dur:.2f} ms")

            write_start = time.perf_counter()
            _write_output(content, args.output)
            write_dur = (time.perf_counter() - write_start) * 1000
            log_verbose(f"Output written in {write_dur:.2f} ms")

            total_dur = (time.perf_counter() - overall_start) * 1000
            log_verbose(f"Total pipeline execution time: {total_dur:.2f} ms")
            return 0

        # B. Call Graph Generation
        if args.generate_graph:
            graph_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Call Graph...")
            from cobolscope.models import ProgramModel
            from cobolscope.graph import generate_call_graph

            model = ProgramModel.from_dict(raw_dict)
            model_dur = (time.perf_counter() - graph_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            gen_start = time.perf_counter()
            log_verbose(f"Rendering Call Graph (format={args.graph_format})...")
            content = generate_call_graph(
                model,
                format=args.graph_format,
                hide_fallthrough=not args.show_fallthrough,
                collapse_exits=args.collapse_exits,
                enable_clustering=args.enable_clustering,
                cluster_mode=args.cluster_mode,
                compact_nodes=not args.detailed_nodes,
                concentrate=args.concentrate,
                splines=args.splines,
            )
            gen_dur = (time.perf_counter() - gen_start) * 1000
            log_verbose(f"Call Graph rendered in {gen_dur:.2f} ms")

            write_start = time.perf_counter()
            _write_output(content, args.output)
            write_dur = (time.perf_counter() - write_start) * 1000
            log_verbose(f"Output written in {write_dur:.2f} ms")

            total_dur = (time.perf_counter() - overall_start) * 1000
            log_verbose(f"Total pipeline execution time: {total_dur:.2f} ms")
            return 0

        # C. Pushdown Reachability Analysis
        if args.generate_reachability or args.save_transitions:
            reach_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Pushdown Reachability...")
            from cobolscope.models import ProgramModel
            from cobolscope.reachability import PushdownReachabilityAnalyzer

            model = ProgramModel.from_dict(raw_dict)
            model_dur = (time.perf_counter() - reach_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            an_start = time.perf_counter()
            log_verbose("Running Pushdown Reachability Analysis...")
            analyzer = PushdownReachabilityAnalyzer(model)
            reachability_model = analyzer.analyze()
            an_dur = (time.perf_counter() - an_start) * 1000
            log_verbose(f"Pushdown Reachability Analysis completed in {an_dur:.2f} ms")

            if args.save_transitions:
                save_start = time.perf_counter()
                log_verbose(f"Saving serialized transitions to: {args.save_transitions}")
                reachability_model.to_json_file(args.save_transitions)
                save_dur = (time.perf_counter() - save_start) * 1000
                log_verbose(f"Transitions saved in {save_dur:.2f} ms")

            if args.generate_reachability:
                content = reachability_model.model_dump_json(indent=2)
                _write_output(content, args.output)

            total_dur = (time.perf_counter() - overall_start) * 1000
            log_verbose(f"Total pipeline execution time: {total_dur:.2f} ms")
            return 0

        # D. Default Mode: Output Canonical IR JSON
        log_verbose("Serializing Canonical IR to JSON...")
        json_start = time.perf_counter()
        content = json.dumps(raw_dict, indent=2)
        json_dur = (time.perf_counter() - json_start) * 1000
        log_verbose(f"JSON serialization completed in {json_dur:.2f} ms")

        write_start = time.perf_counter()
        _write_output(content, args.output)
        write_dur = (time.perf_counter() - write_start) * 1000
        log_verbose(f"Output written in {write_dur:.2f} ms")

        total_dur = (time.perf_counter() - overall_start) * 1000
        log_verbose(f"Total pipeline execution time: {total_dur:.2f} ms")
        return 0

    except Exception as e:
        print(f"ERROR: Pipeline generation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())