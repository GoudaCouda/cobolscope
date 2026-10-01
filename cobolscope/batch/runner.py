"""
cobolscope.batch.runner
~~~~~~~~~~~~~~~~~~~~~~~

Batch processing engine for multi-program COBOL repositories and directories.
Orchestrates parallel or single-JVM ProLeap parsing, artifact generation (Call Graphs,
Data Dictionaries, Pushdown Reachability, CFGs), manifest synthesis, and documentation portal assembly.
"""

from __future__ import annotations
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from cobolscope.parser.runner import parse_batch
from cobolscope.models import ProgramModel, ParagraphNode
from cobolscope.data_dictionary import generate_data_dictionary
from cobolscope.graph import generate_call_graph, build_procedure_cfg
from cobolscope.graph.cfg_builder import compute_cyclomatic_complexity
from cobolscope.portal import generate_portal

logger = logging.getLogger(__name__)


def run_batch_directory(
    input_path: Union[str, Path],
    args: Any,
    rules: Optional[Any] = None,
    log_info: Optional[Callable[[str], None]] = None,
    log_verbose: Optional[Callable[[str], None]] = None,
    overall_start: Optional[float] = None,
) -> int:
    """
    Execute CobolScope in batch mode on a directory of COBOL programs using a single JVM run.

    Args:
        input_path: Path to the directory containing COBOL source files.
        args: Command arguments or configuration object carrying formatting and artifact flags.
        rules: Optional parsed business/abend rules.
        log_info: Optional callback for user-facing progress messages.
        log_verbose: Optional callback for debug/verbose messages.
        overall_start: Optional starting timestamp for duration calculation.

    Returns:
        0 on complete success, 1 on partial failures, >1 on fatal setup/execution errors.
    """
    if log_info is None:
        log_info = lambda msg: logger.info(msg)
    if log_verbose is None:
        log_verbose = lambda msg: logger.debug(msg)
    if overall_start is None:
        overall_start = time.perf_counter()

    input_path = Path(input_path).resolve()
    cobol_exts = (".cbl", ".cob", ".cobol")
    cobol_files = sorted([
        p for p in input_path.rglob("*")
        if p.is_file() and p.suffix.lower() in cobol_exts
    ])
    if not cobol_files:
        print(f"ERROR: No COBOL source files (*.cbl, *.cob, *.cobol) found in {input_path}", file=sys.stderr)
        return 2

    out_dir = (Path(args.output) if getattr(args, "output", None) else Path("output") / input_path.name).resolve()
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
            format=getattr(args, "format", "FIXED"),
            copybook_dirs=getattr(args, "copybook_dirs", None),
            copybook_exts=getattr(args, "copybook_exts", None),
            ignore_syntax_errors=getattr(args, "ignore_syntax_errors", False),
            jar_path=getattr(args, "jar", None),
            runner_cp=getattr(args, "runner_cp", None),
            java_exe=getattr(args, "java_exe", None),
            extra_java_args=getattr(args, "java_args", None),
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

    manifest_programs = []
    success_count = 0
    fail_count = 0

    active_modes = []
    if getattr(args, "generate_graph", False):
        active_modes.append(f"Call Graph ({getattr(args, 'graph_format', 'html')})")
    if getattr(args, "generate_dictionary", False):
        active_modes.append(f"Data Dict ({getattr(args, 'dict_format', 'markdown')})")
    if getattr(args, "generate_reachability", False) or getattr(args, "save_transitions", False):
        active_modes.append("Reachability")
    if getattr(args, "cfg_target", None):
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
            if getattr(args, "generate_dictionary", False):
                dict_fmt = getattr(args, "dict_format", "markdown")
                ext = "md" if dict_fmt in ("markdown", "md") else dict_fmt
                dict_filename = f"{prog_id}_dict.{ext}"
                dict_path = out_dir / dict_filename
                dict_content = generate_data_dictionary(
                    model,
                    format=dict_fmt,
                    hide_fillers=getattr(args, "hide_fillers", False),
                    source_code=source_text,
                )
                dict_path.write_text(dict_content, encoding="utf-8")
                artifacts["data_dictionary"] = dict_filename

                html_dict_text = dict_content if dict_fmt == "html" else None

                # Also generate interactive HTML data dictionary for portal embedding if not already HTML
                if dict_fmt != "html":
                    html_dict_filename = f"{prog_id}_dict.html"
                    html_dict_path = out_dir / html_dict_filename
                    html_dict_text = generate_data_dictionary(
                        model,
                        format="html",
                        hide_fillers=getattr(args, "hide_fillers", False),
                        source_code=source_text,
                    )
                    html_dict_path.write_text(html_dict_text, encoding="utf-8")
                    artifacts["data_dictionary_html"] = html_dict_filename

                # Generate companion ASPX data dictionary for native SharePoint execution
                if html_dict_text:
                    aspx_dict_filename = f"{prog_id}_dict.aspx"
                    aspx_dict_path = out_dir / aspx_dict_filename
                    aspx_dict_path.write_text('<%@ Page Language="C#" %>\n' + html_dict_text, encoding="utf-8")
                    artifacts["data_dictionary_aspx"] = aspx_dict_filename

            # B. Call Graph Generation
            if getattr(args, "generate_graph", False):
                graph_fmt = getattr(args, "graph_format", "html")
                graph_filename = f"{prog_id}.{graph_fmt}"
                graph_path = out_dir / graph_filename
                graph_content = generate_call_graph(
                    model,
                    format=graph_fmt,
                    hide_fallthrough=not getattr(args, "show_fallthrough", False),
                    collapse_exits=getattr(args, "collapse_exits", False),
                    enable_clustering=getattr(args, "enable_clustering", True),
                    cluster_mode=getattr(args, "cluster_mode", "section"),
                    compact_nodes=not getattr(args, "detailed_nodes", False),
                    concentrate=getattr(args, "concentrate", True),
                    splines=getattr(args, "splines", "ortho"),
                    initial_engine=getattr(args, "graph_engine", "cytoscape"),
                    rules=rules,
                    hide_error_traps=not getattr(args, "show_error_traps", False),
                    source_code=source_text,
                )
                graph_path.write_text(graph_content, encoding="utf-8")
                artifacts["call_graph"] = graph_filename

                # Generate companion ASPX call graph for native SharePoint execution
                if graph_fmt == "html":
                    aspx_graph_filename = f"{prog_id}.aspx"
                    aspx_graph_path = out_dir / aspx_graph_filename
                    aspx_graph_path.write_text('<%@ Page Language="C#" %>\n' + graph_content, encoding="utf-8")
                    artifacts["call_graph_aspx"] = aspx_graph_filename

            # C. Reachability
            if getattr(args, "generate_reachability", False) or getattr(args, "save_transitions", False):
                from cobolscope.reachability import PushdownReachabilityAnalyzer
                analyzer = PushdownReachabilityAnalyzer(model, rules=rules)
                reachability_model = analyzer.analyze()
                reach_filename = f"{prog_id}_reachability.json"
                reach_path = out_dir / reach_filename
                reach_path.write_text(reachability_model.model_dump_json(indent=2), encoding="utf-8")
                artifacts["reachability"] = reach_filename

            # D. Level 3 CFG
            cfg_target = getattr(args, "cfg_target", None)
            if cfg_target:
                target_name = cfg_target.strip()
                cfg_filename = f"{prog_id}_cfg.json"
                cfg_path = out_dir / cfg_filename
                cfg_fmt = getattr(args, "cfg_format", "cytoscape")
                if target_name.lower() == "all":
                    all_cfgs = {}
                    for p in model.paragraphs:
                        p_cfg = build_procedure_cfg(model.program_id, p, rules=rules)
                        all_cfgs[p.name] = p_cfg.to_cytoscape_elements() if cfg_fmt == "cytoscape" else p_cfg.model_dump()
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
                        content = p_cfg.to_cytoscape_json() if cfg_fmt == "cytoscape" else p_cfg.model_dump_json(indent=2)
                        cfg_path.write_text(content, encoding="utf-8")
                artifacts["cfg"] = cfg_filename

            # Stats calculation
            total_stmts = sum(len(p.statements) for p in model.paragraphs)

            prog_entry = {
                "program_id": prog_id,
                "total_paragraphs": len(model.paragraphs),
                "total_statements": total_stmts,
                "status": "SUCCESS",
                "artifacts": artifacts,
            }
            if source_text is not None:
                prog_entry["source_code"] = source_text
            manifest_programs.append(prog_entry)
            success_count += 1
            generated_list = [k for k in artifacts if k != "ir"]
            summary_str = f"generated {', '.join(generated_list)}" if generated_list else "IR saved"
            log_info(f"  -> [{idx}/{len(cobol_files)}] {prog_id}: {summary_str}")

        except Exception as e:
            fail_count += 1
            manifest_programs.append({
                "program_id": cobol_file.stem,
                "status": "ERROR",
                "error": str(e),
                "artifacts": {},
            })
            log_info(f"  [ERR] [{idx}/{len(cobol_files)}] {cobol_file.name}: {e}")

    total_dur_ms = round((time.perf_counter() - overall_start) * 1000, 2)
    manifest = {
        "batch_summary": {
            "total_programs_found": len(cobol_files),
            "succeeded": success_count,
            "failed": fail_count,
            "format": getattr(args, "format", "FIXED"),
            "duration_ms": total_dur_ms,
        },
        "programs": manifest_programs,
    }
    manifest_file = out_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    portal_file = out_dir / "index.html"
    try:
        generate_portal(manifest, output_path=portal_file)
        manifest["batch_summary"]["portal"] = portal_file.name
        if (out_dir / "portal.aspx").exists():
            manifest["batch_summary"]["portal_aspx"] = "portal.aspx"
        manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        portal_note = f", portal: {portal_file.name} (SharePoint: portal.aspx)"
    except Exception as e:
        log_verbose(f"Failed to generate documentation portal: {e}")
        portal_note = ""

    # Generate SharePoint deployment instructions guide
    sp_guide = out_dir / "SHAREPOINT_DEPLOYMENT.md"
    try:
        sp_guide.write_text(
            "# SharePoint Online Deployment Guide\n\n"
            "This folder contains pre-configured, native `.aspx` documentation artifacts ready for hosting on SharePoint Online (e.g., `coboldocs.sharepoint.com`).\n\n"
            "## 3-Step Deployment\n\n"
            "1. **Upload Folder to SharePoint Library**:\n"
            "   - Navigate to your SharePoint Document Library (e.g. `Site Assets` or `Documents`).\n"
            "   - Drag and drop this entire output directory into the SharePoint library.\n\n"
            "2. **Open the Documentation Portal**:\n"
            "   - Click on `portal.aspx` inside SharePoint.\n"
            "   - SharePoint will render `portal.aspx` directly in the browser as an interactive web application without prompting for downloads.\n\n"
            "3. **Navigation & Offline Parity**:\n"
            "   - All call graphs (`[PROGRAM].aspx`), data dictionaries (`[PROGRAM]_dict.aspx`), and source code viewers are pre-configured to execute inline within SharePoint frames.\n"
            "   - If hosting on standard web servers (Apache, Nginx, GitHub Pages), use `index.html`.\n",
            encoding="utf-8"
        )
    except Exception as e:
        log_verbose(f"Failed to write SharePoint deployment guide: {e}")

    total_s = total_dur_ms / 1000.0
    log_info(f"Batch completed: {success_count}/{len(cobol_files)} programs processed in {total_s:.2f}s -> {out_dir.resolve()} (manifest: {manifest_file.name}{portal_note})")
    return 0 if fail_count == 0 else 1
