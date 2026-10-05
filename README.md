# CobolScope

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen?logo=github&style=for-the-badge)](https://goudacouda.github.io/cobolscope/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Java 17+](https://img.shields.io/badge/java-17+-orange.svg)](https://openjdk.org/)
[![GnuCOBOL Parity](https://img.shields.io/badge/GnuCOBOL-verified-brightgreen.svg)](https://gnucobol.sourceforge.io/)
[![NIST Conformance](https://img.shields.io/badge/NIST%20COBOL--85-audited-success.svg)](https://www.itl.nist.gov/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

**CobolScope** is a developer tool that turns COBOL programs into interactive call graphs, memory layout data dictionaries, and searchable static HTML documentation.

Built on the [ProLeap ANTLR4 Parser](https://github.com/uwol/proleap-cobol-parser) with a Python semantic engine, it runs completely locally with no database or server requirements.

> **Live Demo**: [https://goudacouda.github.io/cobolscope/](https://goudacouda.github.io/cobolscope/)

---

[![CobolScope Documentation Portal](docs/images/portal_overview.png)](https://goudacouda.github.io/cobolscope/)

---

## What Does It Do?

Reading thousands of lines of legacy COBOL is tedious. Deep paragraph fall-throughs, `PERFORM ... THRU` ranges, complex `REDEFINES` memory overlays, and dead code make it hard to see what a program actually does.

CobolScope helps you make sense of it:

- **Procedure Call Graphs**: Interactive hierarchy of routines, control flow, and branch targets.
- **Memory Layout Dictionaries**: Exact byte offsets, field sizes, and `REDEFINES` overlays without doing the math by hand.
- **Split Code View (`Alt+C`)**: Jump straight from graph nodes or data dictionary rows to the source line, with identifier occurrence highlighting.
- **Dead Code Detection**: Pushdown reachability analyzer that flags uncalled paragraphs and stranded logic.
- **Static Documentation Portal**: Point it at a directory of COBOL files and copybooks to generate a self-contained `index.html` website you can open directly in any browser.

---

## The Default Way to Use CobolScope

CobolScope is designed to be used out of the box with **`--graph` and `--dict`** on a folder of programs or a single file to produce a complete, interactive **HTML portal**:

```bash
# Recommended default: Generate Call Graphs, Data Dictionaries, and the Web Portal
cobolscope path/to/cobol_folder/ -I path/to/copybooks/ --graph --dict -o docs_portal/
```

### What This Generates:
1. **`docs_portal/index.html`**: A standalone, zero-CORS documentation portal you can open in any browser (`open docs_portal/index.html` or double-click).
2. **Interactive Call Graphs** for each program with functional clustering, zoom/pan controls, and split code inspection.
3. **Binary Data Dictionaries** with live search, column sorting, type filtering, Where-Used cross-references, and sliding code drawers.
4. **Syntax-Highlighted Source Code** with COBOL standard column indicators (Area A, Area B, Sequence area).
5. **`docs_portal/manifest.json`**: Machine-readable metadata and program inventory.

> 💡 **See the exact output live**: Test the fully generated portal deployed on GitHub Pages: **[https://goudacouda.github.io/cobolscope/](https://goudacouda.github.io/cobolscope/)**.

---

## Feature Showcase

### 1. Multi-Program Documentation Portal
Browse all programs in a directory from a sidebar with routine counters, status badges, search filtering, and deep-linkable URLs (e.g. `#program=INQCUST&tab=call_graph`).

[![CobolScope Portal Overview](docs/images/portal_overview.png)](https://goudacouda.github.io/cobolscope/)

---

### 2. Level-2 Procedure Call Graphs with Wide Split-Screen Code (`Alt+C`)
Understand the structure of complex programs at a glance with a clean, unclustered routine hierarchy. Graph nodes display routine names, entry points, cyclomatic complexity (CC), statement counts, and data flow lineage with directed control transfer edges. Press **`Alt+C`** or click **View Routine Code** to open the spacious, wide-aspect split-screen source code viewer centered directly on the selected procedure.

![Call Graph Split Code](docs/images/call_graph_split_code.png)

---

### 3. Level-3 Intra-Procedural CFG Flowcharts
Drill down into complex procedures with branching logic. For procedures with conditional splits (`IF`, `EVALUATE`) or loop iterations (`PERFORM UNTIL`), CobolScope generates fine-grained statement-level flowcharts modeling decision diamonds, execution paths, basic block operations, and terminal exits.

![Level 3 CFG Flowchart](docs/images/level3_flowchart.png)

---

### 4. Binary Data Dictionaries with Sliding Code Drawer
Inspect every field across `WORKING-STORAGE`, `LINKAGE`, and `FILE SECTION`. Click any variable row to slide open the source code drawer, which instantly highlights the field definition line in blue and highlights the variable in yellow.

![Data Dictionary Split View](docs/images/data_dictionary_split.png)

- **Exact Byte Offsets & Lengths**: Accurately tracks base offsets and memory overlay starting points.
- **Where-Used Cross-References**: See every paragraph that references a variable. Click a routine breadcrumb to jump directly to its procedure code.
- **Type & Section Filters**: Instantly filter down to packed decimals, alphanumeric fields, or specific divisions.

---


## Quick Start

### Prerequisites
- **Python 3.10+**
- **Java 17+** runtime (`java` on your `PATH`)
- *(Optional)* [Graphviz](https://graphviz.org/) (`dot` on your `PATH`) if exporting static SVG/DOT diagrams

### Installation
The Java parser bridge is pre-compiled and bundled directly with the repository:

```bash
# Clone the repository
git clone https://github.com/GoudaCouda/cobolscope.git
cd cobolscope

# Install the Python package in editable mode
pip install -e .
```

---

## How to Use CobolScope

### 1. Repository-Level Batch Processing (Recommended)

Process an entire directory of COBOL programs in a single, high-speed JVM run:

```bash
# Full build with interactive call graphs, data dictionaries, and web portal
cobolscope ./src/cobol -I ./src/copybooks --graph --dict -o ./dist/portal/

# Include dead code reachability analysis and CFG flowcharts
cobolscope ./src/cobol -I ./src/copybooks --graph --dict --reachability --cfg all -o ./dist/portal/
```

Open `./dist/portal/index.html` directly in your browser. No web server is required.

---

### 2. Single-Program Analysis

Run analysis on individual programs and output specific artifacts:

#### Call Graphs
```bash
# Standalone interactive HTML Call Graph
cobolscope program.cbl -I copy/ --graph -o call_graph.html

# Scalable Vector Graphics (SVG) or Graphviz DOT format
cobolscope program.cbl --graph --graph-format svg -o call_graph.svg
cobolscope program.cbl --graph --graph-format dot -o call_graph.dot
```

#### Data Dictionaries
```bash
# Standalone interactive HTML Data Dictionary
cobolscope program.cbl -I copy/ --dict --dict-format html -o dictionary.html

# GitHub-Flavored Markdown table
cobolscope program.cbl --dict --dict-format md -o dictionary.md

# CSV export (for spreadsheets or databases)
cobolscope program.cbl --dict --dict-format csv -o dictionary.csv
```

#### Pushdown Reachability & Dead Code Detection
```bash
# Find dead paragraphs and uncalled execution paths
cobolscope program.cbl --reachability

# Save verified state transitions to JSON
cobolscope program.cbl --reachability --save-transitions transitions.json
```

#### Canonical AST IR Export
```bash
# Stream complete semantic AST JSON to file
cobolscope program.cbl -I copy/ -o program_ast.json
```

---

### 3. Declarative Rules Engine (`cobolscope-rules.yaml`)

Mainframe environments often use proprietary macros or runtime modules (`CEE3ABD`, `ILBOABN0`, `ABEND`) to handle fatal errors. CobolScope features a declarative YAML rules engine to model these semantics:

```bash
# Automatically scan a codebase and generate a starter rules file
cobolscope --init-rules ./src/cobol -o cobolscope-rules.yaml

# Apply the rules file to any analysis or portal build
cobolscope ./src/cobol --graph --dict -r cobolscope-rules.yaml -o ./dist/portal/
```

---

## Architecture Overview

CobolScope follows a clean, decoupled architecture that pairs a high-performance Java semantic parser with a Python modeling and rendering pipeline:

```mermaid
flowchart LR
    A["COBOL Sources<br/>& Copybooks"] --> B["Java ProLeap Bridge<br/>(ANTLR4 AST & Symbol Table)"]
    B --> C["Streaming AST IR<br/>(JSON)"]
    C --> D["Python Semantic Core<br/>(Pydantic Models)"]
    D --> E["Data Dictionary Engine<br/>(Byte Offsets & Overlays)"]
    D --> F["Call Graph & CFG Engine<br/>(Clustering & Topologies)"]
    D --> G["Pushdown Reachability<br/>(Dead Code Detection)"]
    E --> H["Interactive Web Portal<br/>(index.html & Standalone HTMLs)"]
    F --> H
    G --> H
```

### Key Architectural Components

- **Java Parser Bridge (`java/`)**: Invokes the ANTLR4 ProLeap parser in a single JVM instance to preprocess copybooks, evaluate `REDEFINES` byte calculations, and extract semantic symbols with streaming JSON serialization.
- **Strongly-Typed Semantic IR (`cobolscope/models/`)**: Hydrates the raw AST into rich Pydantic models with dedicated representations for structured verbs (`MOVE`, `PERFORM`, `IF`, `EVALUATE`, `CALL`, `EXEC SQL`, `EXEC CICS`) and graceful fallbacks for extended dialects.
- **Memory Layout Engine (`cobolscope/dictionary/`)**: Calculates exact starting byte offsets, group bounds, and memory overlays.
- **Graph & CFG Engine (`cobolscope/graph/`)**: Builds Level-2 procedure call graphs with functional clustering and Level-3 intra-procedural flowcharts using Cytoscape.js and Graphviz.
- **Portal & HTML Generator (`cobolscope/portal/`)**: Assembles static HTML, CSS, and vanilla JS into self-contained, responsive documentation portals with zero external runtime dependencies.

---

## Python API

You can also use CobolScope programmatically as a Python library:

```python
from cobolscope.parser import parse
from cobolscope.models import ProgramModel
from cobolscope.data_dictionary import generate_data_dictionary
from cobolscope.graph import generate_call_graph
from cobolscope.reachability import PushdownReachabilityAnalyzer

# 1. Parse COBOL source with copybook resolution
raw_ir = parse("program.cbl", copybook_dirs=["./copybooks"], format="FIXED")
model = ProgramModel.from_dict(raw_ir)

print(f"Program: {model.program_id} ({len(model.paragraphs)} routines)")

# 2. Generate Interactive Data Dictionary
html_dict = generate_data_dictionary(model, format="html")

# 3. Generate Interactive Call Graph
html_graph = generate_call_graph(model, format="html")

# 4. Run Dead Code / Reachability Analysis
analyzer = PushdownReachabilityAnalyzer(model)
reach_result = analyzer.analyze()
print(f"Reachable: {len(reach_result.reachable_paragraphs)}")
print(f"Dead Code: {reach_result.unreachable_paragraphs}")
```

---

## 6-Tier Verification & Quality Standards

CobolScope enforces strict verification standards across every component:

| Verification Tier | Focus Area | Verification Strategy |
| :--- | :--- | :--- |
| **Tier 1: Pipeline E2E** | AST Deserialization | Complete roundtrip parity across all statements |
| **Tier 2: Data Dictionary** | Memory Layout | Exact byte offsets, group boundaries, and overlay alignments |
| **Tier 3: Invariants** | Mathematical Proofs | Group Sum consistency, REDEFINES alignment, and zero-slop checks |
| **Tier 4: ASG Parity** | Semantic Completeness | Zero-drop audit against native ProLeap ASG metamodels |
| **Tier 5: Call Graph** | Graph Topology | Cluster boundaries, exit collapsing, and acyclic/cyclic flows |
| **Tier 6: GnuCOBOL Parity** | Compiler Truth | 1:1 symbol table cross-checks against live `cobc` compiler listings |
| **NIST COBOL-85** | Language Standard | Audited against official 500+ program NIST conformance suite |

To run the verification suite:
```bash
python -m tests.run_all_tests
python -m tests.test_nist_suite
```

---

## Keyboard Shortcuts

| Shortcut | Context | Action |
| :--- | :--- | :--- |
| **`Alt + C`** | Call Graph | Toggle split-screen source code viewer |
| **`Esc`** | Any Viewer | Close code drawer, routine inspector, or active modal |
| **Click Row** | Data Dictionary | Slide open split code drawer focused on variable definition |
| **Click Breadcrumb** | Data Dictionary | Jump directly to routine procedure code |
| **`Ctrl + Click` Breadcrumb** | Data Dictionary | Jump straight to routine in Call Graph |
| **Click Any Identifier** | Code Viewers | Highlight all occurrences of that variable across code |

---

## Additional Documentation

- 📖 **[User Guide & Visual Walkthrough](USER_GUIDE.md)**: In-depth guide on graph navigation, occurrence highlighting, and split-screen features.
- 📐 **[Agent & Architecture Guidelines](AGENTS.md)**: Engineering guidelines, ProLeap-first principles, and domain separation standards.

---

## License

This project is licensed under the **Apache License, Version 2.0** - see the [LICENSE](LICENSE) file for details.  
CobolScope utilizes the [ProLeap COBOL Parser](https://github.com/uwol/proleap-cobol-parser) under the MIT License.
