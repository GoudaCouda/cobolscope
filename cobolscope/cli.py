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
        default="html",
        choices=["html", "cytoscape", "svg", "dot", "json"],
        help="Output format for Call Graph (html, cytoscape, svg, dot, json). Default: html.",
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
    cobol_exts = (".cbl", ".cob", ".cobol")
    cobol_files = sorted([
        p for p in input_path.rglob("*")
        if p.is_file() and p.suffix.lower() in cobol_exts
    ])
    if not cobol_files:
        print(f"ERROR: No COBOL source files (*.cbl, *.cob, *.cobol) found in {input_path}", file=sys.stderr)
        return 2

    out_dir = (Path(args.output) if args.output else Path("output") / input_path.name).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    ir_dir = out_dir / "ir"
    ir_dir.mkdir(parents=True, exist_ok=True)

    log_info(f"Target directory: {input_path.resolve()} ({len(cobol_files)} COBOL programs found)")
    log_info("Parsing COBOL sources via single-JVM ProLeap bridge (streaming)...")

    def on_parser_progress(channel: str, line: str) -> None:
        if line.startswith("PARSED: "):
            info = line[len("PARSED: "):]
            log_info(f"  [OK] {info}")
        elif line.startswith("ERROR: "):
            err = line[len("ERROR: "):]
            log_info(f"  [ERR] {err}")
        elif line.startswith("WARNING: "):
            warn = line[len("WARNING: "):]
            log_info(f"  [WARN] {warn}")
        else:
            log_verbose(f"[Java {channel}] {line}")

    parse_start = time.perf_counter()
    try:
        batch_results = parse_batch(
            input_files=cobol_files,
            output_dir=ir_dir,
            format=args.format,
            copybook_dirs=args.copybook_dirs,
            copybook_exts=args.copybook_exts,
            ignore_syntax_errors=args.ignore_syntax_errors,
            jar_path=args.jar,
            runner_cp=args.runner_cp,
            java_exe=args.java_exe,
            extra_java_args=args.java_args,
            on_progress=on_parser_progress,
        )
    except (FileNotFoundError, EnvironmentError) as e:
        print(f"ERROR: Environment setup error: {e}", file=sys.stderr)
        return 5
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: Batch parsing failed: {e}", file=sys.stderr)
        return 1

    parse_dur = (time.perf_counter() - parse_start) * 1000
    log_info(f"Java batch parsing completed in {parse_dur:.2f} ms ({len(batch_results)}/{len(cobol_files)} succeeded)")

    from cobolscope.models import ProgramModel

    manifest_programs = []
    success_count = 0
    fail_count = 0

    active_modes = []
    if args.generate_graph:
        active_modes.append(f"Call Graph ({args.graph_format})")
    if args.generate_dictionary:
        active_modes.append(f"Data Dict ({args.dict_format})")
    if args.generate_reachability or args.save_transitions:
        active_modes.append("Reachability")
    if args.cfg_target:
        active_modes.append(f"CFG ({args.cfg_target})")
    if not active_modes:
        active_modes.append("Canonical IR")

    log_info(f"Generating artifacts [{', '.join(active_modes)}] for {len(batch_results)} programs...")

    for idx, cobol_file in enumerate(cobol_files, 1):
        src_key = str(cobol_file.resolve())
        json_file = batch_results.get(src_key)

        if not json_file or not json_file.exists():
            fail_count += 1
            manifest_programs.append({
                "program_id": cobol_file.stem,
                "source_file": cobol_file.name,
                "relative_source": str(cobol_file.relative_to(input_path)).replace("\\", "/"),
                "status": "FAILED",
                "error": "Failed during Java AST extraction or missing copybook",
                "artifacts": {},
            })
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                raw_dict = json.load(f)
            model = ProgramModel.from_dict(raw_dict)
            prog_id = model.program_id or cobol_file.stem

            source_text = None
            artifacts_source = None
            try:
                source_text = cobol_file.read_text(encoding="utf-8", errors="replace")
                model.source_code = source_text
                source_filename = f"{prog_id}.cbl"
                (out_dir / source_filename).write_text(source_text, encoding="utf-8")
                artifacts_source = source_filename
            except Exception:
                pass

            artifacts = {
                "ir": str(json_file.relative_to(out_dir)).replace("\\", "/")
            }
            if artifacts_source:
                artifacts["source"] = artifacts_source

            # A. Data Dictionary Generation
            if args.generate_dictionary:
                from cobolscope.data_dictionary import generate_data_dictionary
                ext = "md" if args.dict_format in ("markdown", "md") else args.dict_format
                dict_filename = f"{prog_id}_dict.{ext}"
                dict_path = out_dir / dict_filename
                dict_content = generate_data_dictionary(
                    model,
                    format=args.dict_format,
                    hide_fillers=args.hide_fillers,
                )
                dict_path.write_text(dict_content, encoding="utf-8")
                artifacts["data_dictionary"] = dict_filename

                # Also generate interactive HTML data dictionary for portal embedding if not already HTML
                if args.dict_format != "html":
                    html_dict_filename = f"{prog_id}_dict.html"
                    html_dict_path = out_dir / html_dict_filename
                    html_dict_content = generate_data_dictionary(
                        model,
                        format="html",
                        hide_fillers=args.hide_fillers,
                    )
                    html_dict_path.write_text(html_dict_content, encoding="utf-8")
                    artifacts["data_dictionary_html"] = html_dict_filename

            # B. Call Graph Generation
            if args.generate_graph:
                from cobolscope.graph import generate_call_graph
                ext = args.graph_format
                graph_filename = f"{prog_id}.{ext}"
                graph_path = out_dir / graph_filename
                graph_content = generate_call_graph(
                    model,
                    format=args.graph_format,
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
                graph_path.write_text(graph_content, encoding="utf-8")
                artifacts["call_graph"] = graph_filename

            # C. Reachability
            if args.generate_reachability or args.save_transitions:
                from cobolscope.reachability import PushdownReachabilityAnalyzer
                analyzer = PushdownReachabilityAnalyzer(model, rules=rules)
                reachability_model = analyzer.analyze()
                reach_filename = f"{prog_id}_reachability.json"
                reach_path = out_dir / reach_filename
                reach_path.write_text(reachability_model.model_dump_json(indent=2), encoding="utf-8")
                artifacts["reachability"] = reach_filename

            # D. Level 3 CFG
            if args.cfg_target:
                from cobolscope.graph import build_procedure_cfg
                from cobolscope.models import ParagraphNode
                target_name = args.cfg_target.strip()
                cfg_filename = f"{prog_id}_cfg.json"
                cfg_path = out_dir / cfg_filename
                if target_name.lower() == "all":
                    all_cfgs = {}
                    for p in model.paragraphs:
                        p_cfg = build_procedure_cfg(model.program_id, p, rules=rules)
                        all_cfgs[p.name] = p_cfg.to_cytoscape_elements() if args.cfg_format == "cytoscape" else p_cfg.model_dump()
                    cfg_path.write_text(json.dumps(all_cfgs, indent=2), encoding="utf-8")
                else:
                    para = model.get_paragraph(target_name)
                    if not para:
                        for s in model.sections:
                            if s.name.upper().strip() == target_name.upper():
                                para = ParagraphNode(name=s.name, location=s.location, statements=s.statements)
                                break
                    if para:
                        p_cfg = build_procedure_cfg(model.program_id, para, rules=rules)
                        content = p_cfg.to_cytoscape_json() if args.cfg_format == "cytoscape" else p_cfg.model_dump_json(indent=2)
                        cfg_path.write_text(content, encoding="utf-8")
                artifacts["cfg"] = cfg_filename

            # Stats calculation
            from cobolscope.graph.cfg_builder import compute_cyclomatic_complexity
            total_stmts = sum(len(p.statements) for p in model.paragraphs)
            max_cc = max((compute_cyclomatic_complexity(p.statements) for p in model.paragraphs), default=1)

            manifest_programs.append({
                "program_id": prog_id,
                "source_file": cobol_file.name,
                "relative_source": str(cobol_file.relative_to(input_path)).replace("\\", "/"),
                "total_paragraphs": len(model.paragraphs),
                "total_statements": total_stmts,
                "max_cyclomatic_complexity": max_cc,
                "entry_point": model.paragraphs[0].name if model.paragraphs else None,
                "status": "SUCCESS",
                "artifacts": artifacts,
            })
            success_count += 1
            generated_list = [k for k in artifacts if k != "ir"]
            summary_str = f"generated {', '.join(generated_list)}" if generated_list else "IR saved"
            log_info(f"  -> [{idx}/{len(cobol_files)}] {prog_id}: {summary_str}")

        except Exception as e:
            fail_count += 1
            manifest_programs.append({
                "program_id": cobol_file.stem,
                "source_file": cobol_file.name,
                "relative_source": str(cobol_file.relative_to(input_path)).replace("\\", "/"),
                "status": "ERROR",
                "error": str(e),
                "artifacts": {},
            })
            log_info(f"  [ERR] [{idx}/{len(cobol_files)}] {cobol_file.name}: {e}")

    total_dur_ms = round((time.perf_counter() - overall_start) * 1000, 2)
    manifest = {
        "batch_summary": {
            "source_directory": str(input_path.resolve()),
            "total_programs_found": len(cobol_files),
            "succeeded": success_count,
            "failed": fail_count,
            "format": args.format,
            "duration_ms": total_dur_ms,
        },
        "programs": manifest_programs,
    }
    manifest_file = out_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    portal_file = out_dir / "index.html"
    try:
        from cobolscope.portal import generate_portal
        generate_portal(manifest, output_path=portal_file)
        manifest["batch_summary"]["portal"] = portal_file.name
        manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        portal_note = f", portal: {portal_file.name}"
    except Exception as e:
        log_verbose(f"Failed to generate documentation portal: {e}")
        portal_note = ""

    total_s = total_dur_ms / 1000.0
    log_info(f"Batch completed: {success_count}/{len(cobol_files)} programs processed in {total_s:.2f}s -> {out_dir.resolve()} (manifest: {manifest_file.name}{portal_note})")
    return 0 if fail_count == 0 else 1


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
            generate_portal(target_path, output_path=out_target)
            out_file = out_target or (target_path / "index.html" if target_path.is_dir() else target_path.parent / "index.html")
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
        # A. Data Dictionary Generation
        if args.generate_dictionary:
            dict_start = time.perf_counter()
            log_verbose("Hydrating canonical ProgramModel for Data Dictionary...")
            from cobolscope.models import ProgramModel
            from cobolscope.data_dictionary import generate_data_dictionary

            model = ProgramModel.from_dict(raw_dict)
            model_dur = (time.perf_counter() - dict_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            log_info(f"Generating Data Dictionary (format={args.dict_format}, hide_fillers={args.hide_fillers})...")
            gen_start = time.perf_counter()
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
            source_text = None
            if args.input_file:
                try:
                    src_p = Path(args.input_file)
                    if src_p.is_file() and src_p.suffix.lower() not in (".json",):
                        source_text = src_p.read_text(encoding="utf-8", errors="replace")
                        model.source_code = source_text
                except Exception:
                    pass
            if not source_text and hasattr(model, "get_source_text"):
                source_text = model.get_source_text()

            model_dur = (time.perf_counter() - graph_start) * 1000
            log_verbose(f"ProgramModel hydrated in {model_dur:.2f} ms")

            log_info(f"Rendering Call Graph (format={args.graph_format})...")
            gen_start = time.perf_counter()
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