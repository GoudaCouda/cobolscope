# CobolScope User Guide & Walkthrough

Welcome to **CobolScope**! This guide is designed for developers, systems architects, business analysts, and modernization teams who want to explore, understand, and document legacy COBOL applications quickly and reliably.

Whether you need to trace an unfamiliar business routine, verify exact variable offsets in a complex `REDEFINES` structure, identify dead code, or document an entire repository of programs, CobolScope turns dense mainframe COBOL into interactive, intuitive visual tools.

---

## Table of Contents

1. [What CobolScope Does](#what-cobolscope-does)
2. [Quick Start Cheat Sheet](#quick-start-cheat-sheet)
3. [The Interactive Procedure Call Graph](#the-interactive-procedure-call-graph)
   - [Navigating the Visual Graph](#navigating-the-visual-graph)
   - [Routine Info Popover](#routine-info-popover)
   - [Split-Screen Source Code View (`Alt+C`)](#split-screen-source-code-view-altc)
   - [Level 3 Intra-Procedure CFGs & Linear Traces](#level-3-intra-procedure-cfgs--linear-traces)
4. [The Interactive Data Dictionary](#the-interactive-data-dictionary)
   - [Understanding the Memory Layout](#understanding-the-memory-layout)
   - [Filtering & Searching Data Items](#filtering--searching-data-items)
   - [Side Split Code Panel & Variable Highlighting](#side-split-code-panel--variable-highlighting)
   - [Where-Used Routine Navigation](#where-used-routine-navigation)
5. [Occurrence Highlighting Across Code Viewers](#occurrence-highlighting-across-code-viewers)
6. [Multi-Program Documentation Portal](#multi-program-documentation-portal)
7. [Custom Rules & Terminal Traps (`cobolscope-rules.yaml`)](#custom-rules--terminal-traps)
8. [Tips & Keyboard Shortcuts](#tips--keyboard-shortcuts)

---

## What CobolScope Does

Mainframe COBOL programs often span thousands of lines, with deep paragraph fall-throughs, `PERFORM ... THRU` ranges, complex memory overlays, and legacy abnormal termination routines.

CobolScope parses COBOL using a rigorous, compiler-grade AST parser (ProLeap) and provides:

- **Architectural Call Graphs**: See the routine hierarchy, execution flows, and functional clusters without getting lost in the code.
- **Binary Memory Data Dictionaries**: See exact byte offsets, lengths, data types, and `REDEFINES` overlays verified against compiler symbol tables.
- **Embedded Source Code Split Views**: Inspect the actual COBOL lines alongside the diagrams and tables—with automatic line positioning and identifier occurrence highlighting.
- **Dead Code & Reachability Analysis**: Discover dead or uncalled paragraphs using a Pushdown Automaton.
- **Multi-Program Portals**: Generate a unified browsable website for an entire folder of COBOL programs.

---

## Quick Start Cheat Sheet

### 1. Inspect a Single Program
```bash
# Generate an interactive HTML Call Graph
cobolscope program.cbl --graph -o program_graph.html

# Generate an interactive HTML Data Dictionary
cobolscope program.cbl --dict --dict-format html -o program_dict.html

# Export Data Dictionary to GitHub-flavored Markdown or CSV
cobolscope program.cbl --dict --dict-format md -o program_dict.md
cobolscope program.cbl --dict --dict-format csv -o program_dict.csv
```

### 2. Generate a Complete Documentation Portal for a Folder
If you have a folder with multiple COBOL files and copybooks:
```bash
cobolscope path/to/cobol_folder/ -I path/to/copybooks/ -o docs_portal/ --portal
```
Open `docs_portal/index.html` in any web browser to access all programs, call graphs, source code, and data dictionaries in a single interface.

---

## The Interactive Procedure Call Graph

Open any generated `*_graph.html` file in your browser to view the visual procedure hierarchy.

```
+-------------------------------------------------------------------------------+
| COBOLSCOPE / HELLO-SPLIT          [Routine Info] [Split Code Alt+C] [Fit] [⚙] |
+---------------------------------------+---------------------------------------+
|                                       | SOURCE CODE        [ROUTINE] 1000-CALC |
|       [0000-MAIN]                     | ------------------------------------- |
|            |                          | 003200 1000-CALC.                     |
|            v                          | 003201     MOVE 'N' TO EOF-FLAG.      |
|      [1000-CALC]                      | 003202     PERFORM 2000-PROCESS.      |
|            |                          |                                       |
|            v                          |                                       |
|     [2000-PROCESS]                    |                                       |
|                                       |                                       |
+---------------------------------------+---------------------------------------+
```

### Navigating the Visual Graph
- **Pan & Zoom**: Click and drag on the canvas to pan. Use your mouse scroll wheel (or trackpad pinch) to zoom in and out.
- **Routine Selection**: Click on any paragraph box on the canvas to inspect its details and highlight incoming/outgoing call paths.
- **Fit to Screen**: Click the **Fit** button in the top toolbar to re-center and frame the entire graph.

### Routine Info Popover
Clicking on the program name or the **Info** icon in the header reveals a clean routine summary popover showing:
- **Routine Name & Enclosing Section**
- **Physical Line Range** (e.g., lines 120–165)
- **Cyclomatic Complexity (CC)**: Number of independent branch paths.
- **Statement Count & Functional Subsystem Cluster**

### Split-Screen Source Code View (`Alt+C`)
- Click the **Code** button in the header (or press **Alt+C**) to open the split code view.
- Click any node on the graph, then click **View Routine Code** to slide open the source view directly centered on that paragraph's lines.
- **Resizable Splitter**: Click and drag the vertical divider between the graph and code panel to adjust width to your preference.
- **Jump by Line or Search**: Use the search input at the top of the code pane to jump to any line number (e.g., `450`) or search for any text.

### Level 3 Intra-Procedure CFGs & Linear Traces
When a procedure has complex internal logic (multiple `IF`, `EVALUATE`, or loop constructs):
- Click **View Procedure CFG** to open the statement-level flowchart showing decision diamonds, branches, and terminal exit nodes.
- For linear, non-branching procedures, click **View Statement Trace** to view a clean step-by-step table of all operations and subroutine calls.

---

## The Interactive Data Dictionary

Open any generated `*_dict.html` file to inspect data items and memory layout.

### Understanding the Memory Layout
The dictionary displays every field declared in `WORKING-STORAGE`, `LINKAGE`, `FILE SECTION`, and `LOCAL-STORAGE`:

| Column | What It Tells You |
| :--- | :--- |
| **Lvl** | COBOL level number (`01`, `05`, `77`, `88`, etc.). |
| **Field Name / Structure** | Field name indented by hierarchy depth, with qualified parent path, `REDEFINES` targets, `OCCURS` bounds, and default `VALUE`. |
| **Business Type** | Human-readable logical type (e.g., `Alphanumeric(10)`, `Signed Decimal(9, 2) Packed`, `SmallInt (16-bit)`, `Group Array [10]`). |
| **PIC / Usage** | Raw COBOL `PICTURE` string and `USAGE` clause (`DISPLAY`, `COMP-3`, `COMP`, `INDEX`, etc.). |
| **Offset** | Exact starting byte offset in memory from the beginning of the section. |
| **Length** | Total size of the field in bytes (including array expansions). |
| **Where-Used** | Every procedure paragraph that reads, writes, or references this field. |

### Filtering & Searching Data Items
- **Search Bar**: Type any field name, qualified path, or procedure name to filter instantly as you type.
- **Section Dropdown**: Filter to `WORKING-STORAGE`, `LINKAGE SECTION`, `FILE SECTION`, or view `ALL`.
- **Type Dropdown**: Filter by logical type (e.g., view only packed decimals, alphanumeric strings, or level-88 rules).
- **Column Sorting**: Click any column header (`Lvl`, `Field Name`, `Offset`, `Length`) to sort ascending or descending.

### Side Split Code Panel & Variable Highlighting
- **Click any variable row in the table**:
  1. A split code panel slides open smoothly on the right (without navigating away from your dictionary).
  2. The code panel automatically scrolls to the exact line where the variable is defined.
  3. The definition line is highlighted in blue.
  4. All occurrences of that variable across the entire program are subtly highlighted in soft amber.
- **Easy Dismiss**: Close the code panel anytime by clicking the **✕** button or pressing the **Escape** key.
- **Adjust Width**: Drag the divider between the table and code pane to customize your view.

### Where-Used Routine Navigation
In the **Where-Used (Paragraphs)** column:
- Click any routine breadcrumb (e.g., `READ-RECORD > 0100-FETCH`):
  1. The split code panel pops open and jumps straight to that routine's procedure code.
  2. The variable you were inspecting remains highlighted, allowing you to instantly see how that variable is manipulated inside that routine!
- *(Pro Tip)*: Hold **Ctrl** (or **Cmd**) when clicking a Where-Used routine to jump directly into the full Call Graph visualization.

---

## Occurrence Highlighting Across Code Viewers

All code viewers in CobolScope (Data Dictionary code pane, Call Graph split view, and the Portal code viewer) support **interactive occurrence highlighting**:

1. **Click any word or variable** in the code pane.
2. Every occurrence of that identifier in the file is instantly highlighted with a subtle yellow badge (`.var-highlight`).
3. **Click the word again** (or click empty space) to clear the highlight.

This makes it effortless to track variable assignments, loop counters, and procedure calls at a glance without needing manual browser searches.

---

## Multi-Program Documentation Portal

When running on an entire repository (`--portal`), CobolScope generates a standalone documentation portal (`index.html`):

- **Sidebar Explorer**: Filter and select any COBOL program in the system.
- **Top Navigation Tabs**:
  - **Call Graph**: Interactive visual architecture and procedure flow.
  - **Source Code**: Full source viewer with line numbers, COBOL column guides (Area A/B), and instant line jumping.
  - **Data Dictionary**: The complete binary memory layout and Where-Used cross-reference.
- **Deep Linking**: Share URLs with colleagues using hash links (e.g., `portal.html#program=INQCUST&tab=dictionary`), which automatically opens the exact program and tab.

---

## Custom Rules & Terminal Traps

Mainframe programs often use site-specific macros, runtime modules (`CEE3ABD`, `ILBOABN0`), or database checks (`SQLCODE NOT = 0`) to handle fatal errors. By default, CobolScope treats these as abnormal termination sinks (terminal traps).

### Generating a Starter Rules File
Run CobolScope with `--init-rules` to automatically scan your programs and generate a customized `cobolscope-rules.yaml`:
```bash
cobolscope --init-rules path/to/program.cbl -o cobolscope-rules.yaml
```

### Applying Rules
Pass `-r cobolscope-rules.yaml` to any command:
```bash
cobolscope path/to/program.cbl --graph -r cobolscope-rules.yaml -o graph.html
```

---

## Tips & Keyboard Shortcuts

| Shortcut / Action | Where | What It Does |
| :--- | :--- | :--- |
| **`Alt + C`** | Call Graph | Toggles the Split-Screen Source Code Viewer open or closed. |
| **`Esc`** | Data Dictionary & Call Graph | Closes the side split code panel or active modal. |
| **Click Row** | Data Dictionary | Opens split code panel, focuses definition line, and highlights variable. |
| **Click Breadcrumb** | Data Dictionary Where-Used | Opens split code panel, focuses procedure, and highlights variable usage. |
| **`Ctrl + Click` Breadcrumb** | Data Dictionary Where-Used | Navigates directly to that routine in the companion Call Graph. |
| **Click any Word** | Any Code Viewer | Highlights all occurrences of that variable/identifier across the code. |
| **Enter (in Code Search)** | Code Viewer Toolbar | Type a line number (e.g. `245`) or word to jump directly to it. |
