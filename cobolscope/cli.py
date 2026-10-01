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
    parse_batch,
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
        nargs="?",
        default=None,
        help="Path to the COBOL source file or copybook to parse (optional if using --init-rules).",
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
    parser.add_argument(
        "--sharepoint",
        "--aspx",
        action="store_true",
        dest="sharepoint",
        help="Generate native SharePoint Online compatible .aspx output artifacts instead of .html.",
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
    mode_group.add_argument(
        "--cfg",
        metavar="PARAGRAPH",
        dest="cfg_target",
        help="Generate Level 3 Intra-Procedural CFG for the specified procedure paragraph or 'all'.",
    )
    mode_group.add_argument(
        "--cfg-format",
        choices=["json", "cytoscape"],
        default="json",
        dest="cfg_format",
        help="Output format for Level 3 CFG (json, cytoscape). Default: json.",
    )
    mode_group.add_argument(
        "--portal",
        metavar="TARGET",
        nargs="?",
        const="",
        dest="portal_target",
        help="Generate or regenerate HTML documentation portal (index.html) from a batch output directory or manifest.json.",
    )

    # ---------------------------------------------------------
    # Data Dictionary Options
    # ---------------------------------------------------------
    dict_group = parser.add_argument_group("Data Dictionary Options (used with --dict)")
    dict_group.add_argument(
        "--dict-format",
        default="markdown",
        choices=["markdown", "md", "html", "aspx", "csv", "json"],
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
        default="html",
        choices=["html", "aspx", "cytoscape", "svg", "dot", "json"],
        help="Output format for Call Graph (html, aspx, cytoscape, svg, dot, json). Default: html.",
    )
    graph_group.add_argument(
        "--graph-engine",
        choices=["cytoscape", "graphviz"],
        default="cytoscape",
        help="Default rendering engine in interactive HTML viewer (cytoscape or graphviz).",
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
    graph_group.add_argument(
        "--show-error-traps",
        action="store_true",
        dest="show_error_traps",
        default=False,
        help="Include error trap / abend handling procedures and relationships in the call graph (hidden by default).",
    )

    # ---------------------------------------------------------
    # Rules & Termination Options
    # ---------------------------------------------------------
    rules_group = parser.add_argument_group("Rules & Abend Options")
    rules_group.add_argument(
        "-r",
        "--rules",
        metavar="FILE",
        dest="rules_file",
        help="Path to custom YAML rules file (defaults to ./cobolscope-rules.yaml or built-in defaults).",
    )
    rules_group.add_argument(
        "--init-rules",
        action="store_true",
        dest="init_rules",
        help="Generate a starter or auto-scanned cobolscope-rules.yaml configuration file.",
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


def _run_batch_directory(
    input_path: Path,
    args: argparse.Namespace,
    rules: Any,
    log_info: Any,
    log_verbose: Any,
    overall_start: float,
) -> int:
    """Execute CobolScope in batch mode on a directory of COBOL programs using a single JVM run."""
    from cobolscope.batch.runner import run_batch_directory

    return run_batch_directory(
        input_path=input_path,
        args=args,
        rules=rules,
        log_info=log_info,
        log_verbose=log_verbose,
        overall_start=overall_start,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main CLI entry point."""
    args = parse_args(argv)
    verbose = args.verbose
    overall_start = time.perf_counter()

    def log_verbose(msg: str) -> None:
        if verbose:
            sys.stderr.write(f"[DEBUG] {msg}\n")
            sys.stderr.flush()

    def log_info(msg: str) -> None:
        sys.stderr.write(f"[COBOLSCOPE] {msg}\n")
        sys.stderr.flush()

    # 0. Handle --init-rules
    if args.init_rules:
        from cobolscope.rules_generator import generate_rules_file
        from cobolscope.models import ProgramModel

        out_path = Path(args.output) if args.output else Path("cobolscope-rules.yaml")
        scan_models = []
        if args.input_file:
            target = Path(args.input_file)
            if target.exists():
                try:
                    log_verbose(f"Scanning target for rules: {target}")
                    raw_dict = parse(
                        input_file=target,
                        format=args.format,
                        copybook_dirs=args.copybook_dirs,
                        copybook_exts=args.copybook_exts,
                        ignore_syntax_errors=args.ignore_syntax_errors,
                        jar_path=args.jar,
                        runner_cp=args.runner_cp,
                        java_exe=args.java_exe,
                        extra_java_args=args.java_args,
                    )
                    scan_models.append(ProgramModel.from_dict(raw_dict))
                except Exception as e:
                    print(f"WARNING: Could not parse target for rules scanning ({e}). Outputting default template.", file=sys.stderr)

        generate_rules_file(out_path, models=scan_models if scan_models else None)
        print(f"Generated rules configuration: {out_path.resolve()}")
        return 0

    # 0b. Handle --portal
    if args.portal_target is not None:
        from cobolscope.portal import generate_portal
        target_str = args.portal_target or args.input_file
        if not target_str:
            print("ERROR: Directory or manifest.json path required for --portal.", file=sys.stderr)
            return 2
        target_path = Path(target_str)
        if not target_path.exists():
            print(f"ERROR: Target path not found for --portal: {target_path}", file=sys.stderr)
            return 2
        try:
            out_target = Path(args.output) if args.output else None
            is_aspx = getattr(args, "sharepoint", False) or (out_target is not None and str(out_target).lower().endswith(".aspx"))
            generate_portal(target_path, output_path=out_target, aspx=is_aspx)
            default_out = "portal.aspx" if is_aspx else "index.html"
            out_file = out_target or (target_path / default_out if target_path.is_dir() else target_path.parent / default_out)
            log_info(f"Documentation portal generated: {out_file.resolve()}")
            return 0
        except Exception as e:
            print(f"ERROR: Failed to generate documentation portal: {e}", file=sys.stderr)
            return 1

    if not args.input_file:
        print("ERROR: input_file is required unless using --init-rules or --portal.", file=sys.stderr)
        return 2

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        return 2

    from cobolscope.rules import load_rules
    rules = load_rules(path=args.rules_file)
    log_verbose(f"Loaded rules (runtime_modules={len(rules.runtime_modules)}, strict_paragraphs={len(rules.paragraph_names.strict)})")

    if input_path.is_dir():
        return _run_batch_directory(input_path, args, rules, log_info, log_verbose, overall_start)

    log_info(f"Target: {input_path.name} (format: {args.format})")
    log_info("Parsing AST via Java ProLeap bridge...")

    # 1. Parse COBOL source via Java parser bridge
    parse_start = time.perf_counter()
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
    para_count = len(raw_dict.get("paragraphs", []))
    log_info(f"AST parsed ({para_count} paragraphs) in {parse_dur:.2f} ms")

    # 2. Dispatch to requested mode
    try:
        source_text = None
        if args.input_file:
            try:
                src_p = Path(args.input_file)
                if src_p.is_file() and src_p.suffix.lower() not in (".json",):
                    source_text = src_p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        # A. Data Dictionary Generation
        if args.generate_dictionary:
            dict_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Data Dictionary...")
            from cobolscope.models import ProgramModel
            from cobolscope.data_dictionary import generate_data_dictionary

            model = ProgramModel.from_dict(raw_dict)
            if source_text:
                model.source_code = source_text
            model_dur = (time.perf_counter() - dict_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            dict_fmt = args.dict_format
            if args.sharepoint and dict_fmt in ("markdown", "md", "html"):
                dict_fmt = "aspx"
            elif args.output and str(args.output).lower().endswith(".aspx"):
                dict_fmt = "aspx"

            log_info(f"Generating Data Dictionary (format={dict_fmt}, hide_fillers={args.hide_fillers})...")
            gen_start = time.perf_counter()
            content = generate_data_dictionary(
                model,
                format=dict_fmt,
                hide_fillers=args.hide_fillers,
                source_code=source_text,
            )
            gen_dur = (time.perf_counter() - gen_start) * 1000
            log_verbose(f"Data Dictionary generated in {gen_dur:.2f} ms")

            write_start = time.perf_counter()
            _write_output(content, args.output)
            write_dur = (time.perf_counter() - write_start) * 1000
            log_verbose(f"Output written in {write_dur:.2f} ms")

            total_dur = (time.perf_counter() - overall_start) * 1000
            out_desc = args.output if args.output else "stdout"
            log_info(f"Data Dictionary completed in {total_dur:.2f} ms -> {out_desc}")
            return 0

        # B. Call Graph Generation
        if args.generate_graph:
            graph_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Call Graph...")
            from cobolscope.models import ProgramModel
            from cobolscope.graph import generate_call_graph

            model = ProgramModel.from_dict(raw_dict)
            if source_text:
                model.source_code = source_text
            elif hasattr(model, "get_source_text"):
                source_text = model.get_source_text()

            model_dur = (time.perf_counter() - graph_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            graph_fmt = args.graph_format
            if args.sharepoint and graph_fmt == "html":
                graph_fmt = "aspx"
            elif args.output and str(args.output).lower().endswith(".aspx"):
                graph_fmt = "aspx"

            log_info(f"Rendering Call Graph (format={graph_fmt})...")
            gen_start = time.perf_counter()
            content = generate_call_graph(
                model,
                format=graph_fmt,
                hide_fallthrough=not args.show_fallthrough,
                collapse_exits=args.collapse_exits,
                enable_clustering=args.enable_clustering,
                cluster_mode=args.cluster_mode,
                compact_nodes=not args.detailed_nodes,
                concentrate=args.concentrate,
                splines=args.splines,
                initial_engine=args.graph_engine,
                rules=rules,
                hide_error_traps=not args.show_error_traps,
                source_code=source_text,
            )
            gen_dur = (time.perf_counter() - gen_start) * 1000
            log_verbose(f"Call Graph rendered in {gen_dur:.2f} ms")

            write_start = time.perf_counter()
            _write_output(content, args.output)
            write_dur = (time.perf_counter() - write_start) * 1000
            log_verbose(f"Output written in {write_dur:.2f} ms")

            total_dur = (time.perf_counter() - overall_start) * 1000
            out_desc = args.output if args.output else "stdout"
            log_info(f"Call Graph completed in {total_dur:.2f} ms -> {out_desc}")
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

            log_info("Running Pushdown Reachability Analysis...")
            an_start = time.perf_counter()
            analyzer = PushdownReachabilityAnalyzer(model, rules=rules)
            reachability_model = analyzer.analyze()
            an_dur = (time.perf_counter() - an_start) * 1000
            log_verbose(f"Pushdown Reachability Analysis completed in {an_dur:.2f} ms")

            if args.save_transitions:
                save_start = time.perf_counter()
                log_verbose(f"Saving serialized transitions to: {args.save_transitions}")
                reachability_model.to_json_file(args.save_transitions)
                save_dur = (time.perf_counter() - save_start) * 1000
                log_verbose(f"Transitions saved in {save_dur:.2f} ms")
                log_info(f"Transitions saved -> {args.save_transitions}")

            if args.generate_reachability:
                content = reachability_model.model_dump_json(indent=2)
                _write_output(content, args.output)

            total_dur = (time.perf_counter() - overall_start) * 1000
            out_desc = args.output if args.output else "stdout"
            log_info(f"Reachability analysis completed in {total_dur:.2f} ms -> {out_desc}")
            return 0

        # D. Level 3 Intra-Procedural CFG Generation
        if args.cfg_target:
            cfg_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Level 3 CFG...")
            from cobolscope.models import ProgramModel, ParagraphNode
            from cobolscope.graph import build_procedure_cfg

            model = ProgramModel.from_dict(raw_dict)
            model_dur = (time.perf_counter() - cfg_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            target_name = args.cfg_target.strip()
            log_info(f"Generating Level 3 CFG (target='{target_name}', format={args.cfg_format})...")
            if target_name.lower() == "all":
                all_cfgs = {}
                for p in model.paragraphs:
                    p_cfg = build_procedure_cfg(model.program_id, p, rules=rules)
                    if args.cfg_format == "cytoscape":
                        all_cfgs[p.name] = p_cfg.to_cytoscape_elements()
                    else:
                        all_cfgs[p.name] = p_cfg.model_dump()
                content = json.dumps(all_cfgs, indent=2)
            else:
                para = model.get_paragraph(target_name)
                if not para:
                    for s in model.sections:
                        if s.name.upper().strip() == target_name.upper():
                            para = ParagraphNode(name=s.name, location=s.location, statements=s.statements)
                            break
                if not para:
                    print(f"ERROR: Procedure '{target_name}' not found in program '{model.program_id}'.", file=sys.stderr)
                    return 2

                p_cfg = build_procedure_cfg(model.program_id, para, rules=rules)
                if args.cfg_format == "cytoscape":
                    content = p_cfg.to_cytoscape_json()
                else:
                    content = p_cfg.model_dump_json(indent=2)

            write_start = time.perf_counter()
            _write_output(content, args.output)
            write_dur = (time.perf_counter() - write_start) * 1000
            log_verbose(f"Output written in {write_dur:.2f} ms")
            total_dur = (time.perf_counter() - overall_start) * 1000
            out_desc = args.output if args.output else "stdout"
            log_info(f"CFG generation completed in {total_dur:.2f} ms -> {out_desc}")
            return 0

        # E. Default Mode: Output Canonical IR JSON
        log_info("Serializing Canonical IR to JSON...")
        json_start = time.perf_counter()
        content = json.dumps(raw_dict, indent=2)
        json_dur = (time.perf_counter() - json_start) * 1000
        log_verbose(f"JSON serialization completed in {json_dur:.2f} ms")

        write_start = time.perf_counter()
        _write_output(content, args.output)
        write_dur = (time.perf_counter() - write_start) * 1000
        log_verbose(f"Output written in {write_dur:.2f} ms")

        total_dur = (time.perf_counter() - overall_start) * 1000
        out_desc = args.output if args.output else "stdout"
        log_info(f"Canonical IR JSON generated in {total_dur:.2f} ms -> {out_desc}")
        return 0

    except Exception as e:
        print(f"ERROR: Pipeline generation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())