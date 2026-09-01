# CobolScope

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Java 17+](https://img.shields.io/badge/java-17+-orange.svg)](https://openjdk.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**CobolScope** is a high-performance COBOL semantic analysis, AST/ASG extraction, memory layout data dictionary generator, and interactive procedure call graph visualizer built on top of the ANTLR4 [ProLeap COBOL Parser](https://github.com/uwol/proleap-cobol-parser).

CobolScope bridges enterprise mainframe COBOL to modern Python data models, enabling automated code intelligence, legacy migration, architecture mapping, and dead code elimination.

---

## Key Features

- **High-Fidelity AST & Semantic Graph IR**: Extracts full compilation unit hierarchies, sections, paragraphs, statements, and symbol cross-references into structured JSON.
- **Exact Binary Memory Layout**: Reconstructs exact byte offsets, lengths, and memory overlays (`REDEFINES`) verified against live IBM/GnuCOBOL compiler symbol tables.
- **Interactive Data Dictionaries**: Exports data definitions into searchable, filterable **HTML reports**, clean **Markdown tables**, **CSV**, and **JSON Schema**.
- **Level-2 Procedure Call Graphs**: Generates clean architectural control flow diagrams with functional clustering, `PERFORM ... THRU` range expansion, and exit collapsing in **SVG**, **Interactive HTML (pan & zoom)**, and **Graphviz DOT**.
- **Pushdown Reachability Analyzer**: Emulates COBOL runtime execution using a Pushdown Automaton to detect dead paragraphs, uncalled abend routines, and unreachable blocks.
- **Open Polymorphic Statement Architecture**: Strongly typed Pydantic models for rich statements (`MOVE`, `PERFORM`, `IF`, `EVALUATE`, `CALL`, `COMPUTE`, `EXEC SQL`, `EXEC CICS`).
- **6-Tier Verification Suite**: Audited against mathematical invariant proofs, live GnuCOBOL compiler listings, the official NIST COBOL-85 conformance suite, and open-source enterprise CICS programs ([IBM Bank-of-Z](https://github.com/IBM/Bank-of-Z)).

---

## Quick Start

### Prerequisites
- **Java 17+ runtime** on your `PATH` (`java`)
- **Python 3.10+**
- *(Optional)* [Graphviz](https://graphviz.org/) (`dot` on your `PATH`) for SVG compilation

### 1. Install
```bash
# The Java parser bridge is already bundled with the package.
pip install -e .
```

To rebuild the bundled Java bridge while developing CobolScope, install a JDK
17+ (`java` and `javac`) and run `python build_java.py`. On Windows,
`./build.ps1` is an equivalent wrapper.

### 2. CLI Usage

#### Parse & Output Canonical AST JSON
```bash
# Print AST IR JSON to stdout
cobolscope path/to/program.cbl -f FIXED

# Save AST IR JSON to file with copybook resolution
cobolscope path/to/program.cbl -I ./copybooks -o output.json
```

#### Generate Data Dictionaries
```bash
# Interactive HTML Report with live search & type filtering
cobolscope path/to/program.cbl --dict --dict-format html -o dictionary.html

# GitHub-Flavored Markdown Table
cobolscope path/to/program.cbl --dict --dict-format md -o dictionary.md

# CSV or JSON export
cobolscope path/to/program.cbl --dict --dict-format csv -o dictionary.csv
```

#### Generate Procedure Call Graphs
```bash
# Interactive pan & zoom HTML Call Graph
cobolscope path/to/program.cbl --graph --graph-format html -o call_graph.html

# Scalable Vector Graphics (SVG)
cobolscope path/to/program.cbl --graph --graph-format svg -o call_graph.svg

# Graphviz DOT format
cobolscope path/to/program.cbl --graph --graph-format dot -o call_graph.dot
```

#### Run Pushdown Reachability Analysis
```bash
cobolscope path/to/program.cbl --reachability
```

---

## Python API

```python
from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.dictionary import DataDictionaryGenerator
from cobolscope.graph import CallGraphGenerator
from cobolscope.reachability import PushdownReachabilityAnalyzer

# 1. Parse COBOL Source
raw_ir = parse("path/to/program.cbl", copybook_dirs=["./copybooks"], format="FIXED")
model = ProgramModel.from_dict(raw_ir)

print(f"Program ID: {model.program_id}")
print(f"Total Paragraphs: {len(model.paragraphs)}")

# 2. Inspect Data Dictionary & Memory Layout
dict_gen = DataDictionaryGenerator(model)
for row in dict_gen.rows:
    print(f"{row.level:02d} {row.name:<30} Offset: {row.byte_offset:<5} Len: {row.byte_length:<4} Type: {row.logical_type}")

# Export Markdown or HTML
md_report = dict_gen.to_markdown()
html_report = dict_gen.to_html()

# 3. Generate Procedure Call Graph
graph_gen = CallGraphGenerator(model)
dot_source = graph_gen.to_dot()
svg_content = graph_gen.to_svg()
html_viewer = graph_gen.to_html()

# 4. Run Reachability & Dead Code Detection
analyzer = PushdownReachabilityAnalyzer(model)
reach_result = analyzer.analyze()
print(f"Reachable Paragraphs: {len(reach_result.reachable_paragraphs)}")
print(f"Dead / Unreachable Code: {reach_result.unreachable_paragraphs}")
```

---

## Example: IBM Bank-of-Z (`XFRFUN.cbl`)

CobolScope includes pre-generated samples from the open-source **IBM Bank-of-Z** enterprise CICS/DB2 funds transfer application ([`XFRFUN.cbl`](tests/fixtures/bank_of_z/cobol/XFRFUN.cbl)):

- **Interactive Procedure Call Graph**: [`examples/XFRFUN_call_graph.html`](examples/XFRFUN_call_graph.html) ([SVG version](examples/XFRFUN_call_graph.svg))
- **Interactive Data Dictionary**: [`examples/XFRFUN_data_dictionary.html`](examples/XFRFUN_data_dictionary.html) ([Markdown version](examples/XFRFUN_data_dictionary.md))

### Sample Data Dictionary Output

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `A010` |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 6 | 88 | — | `UADT010` |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | `A010` |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 42 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 80 | 7 | — | `UADF010`, `UADT010` |

---

## 6-Tier Verification Suite

CobolScope enforces strict mathematical, architectural, and compiler correctness standards:

| Tier | Suite | Purpose |
| :--- | :--- | :--- |
| **Tier 1** | `test_pipeline.py` | End-to-end AST & statement deserialization parity |
| **Tier 2** | `test_data_dictionary.py` | 1:1 Memory layout, overlay offsets, and exporter roundtrip |
| **Tier 3** | `test_invariants.py` | Mathematical proofs (Group Sum, REDEFINES Alignment, Zero Slop) |
| **Tier 4** | `test_asg_parity.py` | Native ProLeap ASG semantic metamodel zero-drop completeness |
| **Tier 5** | `test_call_graph.py` | Procedure call graph topology, cluster partitioning, and exit collapsing |
| **Tier 6** | `test_gnucobol_parity.py`| Live binary GnuCOBOL (`cobc`) compiler symbol table cross-check |
| **Pushdown** | `test_reachability.py` | Interprocedural call stack reachability & dead code detection |
| **NIST** | `test_nist_suite.py` | Official NIST COBOL-85 standard conformance suite (500+ programs) |

To run the full suite:
```powershell
python -m tests.run_all_tests
python -m tests.test_nist_suite
```

---

## Architecture & Project Structure

```
cobolscope/
├── __init__.py                # Core package entrypoints (parse, models)
├── cli.py                     # Unified CLI with subcommands & argument parser
├── models/                    # Typed Pydantic IR data models (AST, DFG, CFG)
├── parser/                    # Java subprocess runner & streaming JSON reader
├── dictionary/                # Data dictionary engine, offsets, & exporters (HTML, MD, CSV)
├── graph/                     # Procedure call graph generator & cluster classifier
├── reachability/              # Pushdown Automaton interprocedural reachability analyzer
└── templates/                 # Jinja2 templates for interactive HTML visualizers

java/
├── ProLeapCliRunner.java      # CLI entrypoint for the ProLeap parser bridge
├── CobolTextCleaner.java      # Preprocessor and comment/directive sanitizer
├── HeaderDivisionExtractor.java # Program identification metadata extractor
├── DataDivisionExtractor.java # Memory layout, PIC sizing, and REDEFINES offset calculator
├── ProcedureDivisionExtractor.java # Paragraphs, CFG edges, and call target extractor
├── StatementMapper.java       # Polymorphic statement mapper (MOVE, PERFORM, SQL, CICS)
├── AsgSemanticAuditor.java    # Metamodel completeness & ASG auditor
├── IrJsonWriter.java          # High-speed streaming JSON serializer
└── IrModel.java               # Intermediate DTO transfer objects
```

---

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.
CobolScope utilizes the [ProLeap COBOL Parser](https://github.com/uwol/proleap-cobol-parser) under the MIT License.
