# CobolScope: Resume & Portfolio Project Showcase

> **Strategic Framing Note**: To prevent being pigeonholed as a legacy "COBOL / Mainframe Developer", this document presents multiple resume listings tailored for **modern Systems, Compiler, Infrastructure, and Full-Stack Developer Tooling** roles. Only **Variation 4** explicitly focuses on COBOL/Mainframe modernization; the other variations showcase your mastery of **compilers, binary memory layout engines, formal graph theory, static program analysis, and developer tooling**.

---

## Quick Reference: Project Overview

| Attribute | Modern Systems & Tooling Framing | Legacy Migration Framing (Optional) |
| :--- | :--- | :--- |
| **Project Title** | **CodeScope / CobolScope** (Compiler-Grade Static Analysis & Code Intelligence Engine) | **CobolScope** (Enterprise Mainframe Migration & Analysis Tool) |
| **Role** | Creator & Lead Systems Architect | Creator & Modernization Engineer |
| **Core Stack** | Python 3.10+, Java 17+, ANTLR4, Pydantic v2, Cytoscape.js, Graphviz, Jinja2, PyYAML | Same + COBOL-85, CICS, DB2 |
| **Key Domains** | Abstract Syntax Trees (AST/ASG), Binary Memory Layouts, Graph Algorithms, Formal Invariant Proofs | Mainframe Refactoring, Core Banking Systems |
| **Scale / Rigor** | 500+ standard conformance programs (NIST suite), live binary compiler symbol tables (`cobc`), 6-tier CI suite | IBM Bank-of-Z Enterprise CICS/DB2 Core Banking |

---

## Tailored Resume Bullet Variations

### Variation 1: Systems / Compiler / Core Infrastructure Engineer (Recommended for Systems / Backend)
*Focuses on parser theory, AST/ASG metamodels, binary memory reconstruction, graph algorithms, and formal proofs. Mentions the target language only as the testbed grammar.*

**CobolScope | Lead Systems & Compiler Tooling Engineer** &nbsp;|&nbsp; *Java 17, Python 3.10+, ANTLR4, Pydantic, Graph Theory*
- Engineered a high-performance static analysis and AST/ASG semantic extraction engine bridging an ANTLR4/Java grammar parser to strongly typed Python Pydantic models via zero-copy streaming JSON serialization.
- Architected a binary memory layout reconstruction engine calculating exact byte offsets, lengths, and memory overlays (`REDEFINES`, bit/nibble-packed decimals), achieving 100% byte-offset parity against live binary compiler symbol tables.
- Implemented formal mathematical proofs into CI (Group Sum, Memory Overlay Alignment, Zero Slop) to mathematically verify struct offsets and composite hierarchies across thousands of data fields.
- Implemented zero-dependency static graph algorithms including Tarjan’s Strongly Connected Components ($O(\|V\| + \|E\|)$), Cooper-Harvey-Kennedy (2001) Dominator Trees, and Lengauer-Tarjan Post-Dominators to resolve cyclic flow and compute control dependence.
- Built an interprocedural Pushdown Automaton (PDA) modeling LIFO call-stack semantics and terminal exit sinks to execute automated dead code detection and unreachable block elimination across 500+ standard test programs.

---

### Variation 2: Software Engineer (Developer Tooling, Infrastructure & Platforms)
*Focuses on developer tools, automated code intelligence, interactive visualization engines, declarative rules, and CLI design.*

**CobolScope | Creator & Lead Developer** &nbsp;|&nbsp; *Python, Java, TypeScript/Cytoscape.js, CLI, Pydantic, PyYAML*
- Designed and built a code intelligence and program analysis platform that ingests complex enterprise codebases to automate architecture mapping, data dictionary extraction, and control flow visualization.
- Built an interactive visualization engine rendering multi-level graph representations (Cytoscape.js pan/zoom HTML, SVG, Graphviz DOT), modeling intra-procedural decision splits (`IF`, branch fanout), loop constructs, and terminal error sinks.
- Developed a declarative YAML rules engine paired with an automated heuristic AST scanner (`--init-rules`) that automatically infers error-handling conventions, system call wrappers, and database exception patterns.
- Produced searchable, filterable HTML/Markdown/CSV data dictionaries indexing business schema types, domain constraint intervals, and cross-file variable reference lineage.
- Enforced software reliability with an automated 6-tier CI test harness validating wire deserialization, AST completeness, memory layout proofs, and external compiler ground truth.

---

### Variation 3: Ultra-Concise SWE Format (For General 1-Page Resumes)
*Balanced, high-impact, language-agnostic. Emphasizes systems programming, algorithms, and developer tooling.*

**CobolScope | Creator & Lead Engineer** &nbsp;|&nbsp; *Python, Java 17, ANTLR4, Pydantic, Cytoscape.js, Graph Theory*
- Engineered a compiler-grade static analysis engine extracting AST/ASG intermediate representations into strongly typed Python models, validated against 500+ conformance test programs.
- Reconstructed physical binary memory layouts and overlapping data structures with formal mathematical proofs, matching live binary compiler symbol tables with 100% byte-offset parity.
- Implemented Tarjan's SCC and a Pushdown Automaton analyzer to simulate LIFO call stacks, automating dead code pruning and rendering interactive Cytoscape.js control flow graphs.

---

### Variation 4: Enterprise Modernization & FinTech Migration Specialist
*ONLY use this variation when explicitly applying for Mainframe Modernization, Cloud Migration (AWS Blu Age, Google Cloud Dual Run), or FinTech Banking Core positions.*

**CobolScope | Mainframe Code Intelligence & Modernization Engine** &nbsp;|&nbsp; *Mainframe Modernization, COBOL, CICS, DB2, Python, Java*
- Architected an automated code intelligence and migration platform to de-risk multi-million-dollar legacy refactoring initiatives across core banking and enterprise financial systems.
- Reconstructed exact physical memory layouts, packed decimal structures (`COMP-3`), and `REDEFINES` overlays from COBOL data divisions into modern relational schemas and JSON dictionaries.
- Mapped complex procedural control flow across IBM Bank-of-Z CICS transaction programs and DB2 SQL interfaces, isolating critical business logic from obsolete runtime abend routines (`CEE3ABD`, `ILBOABN0`).
- Implemented Pushdown Automaton reachability analysis to identify dead paragraphs, uncalled abend sinks, and fallthrough execution paths, accelerating refactoring into cloud-native microservices.

---

## Strategic Resume Framing: How to Avoid the "Legacy Dev" Trap

### 1. The Resume Title / Subtitle
- **Avoid:** *"COBOL Programmer"*, *"Mainframe Developer"*, or *"COBOL Software Engineer"*.
- **Use:**
  - **Software Engineer - Compilers & Developer Tooling**
  - **Systems Software Engineer - Program Analysis & Infrastructure**
  - **Backend / Platform Engineer - Code Intelligence**

### 2. If You Want to Disguise the Name
If you are applying to general modern startups or FAANG companies where seeing "COBOL" in a project name might trigger recruiter bias, you can list the project as:
> **CodeScope (or ScopeIR)** — *Compiler-Grade Static Analysis & Binary Memory Layout Engine*

In the description, explain that it was built to solve the hardest static analysis challenges found in real-world computing: complex binary overlays, non-local control flow, and multi-language compiler interop.

---

## System Architecture & Technical Deep Dive

```
                             TARGET SOURCE PROGRAM
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │       Java 17 Compiler Bridge       │
                    │   - ANTLR4 Parser & Semantic Graph  │
                    │   - Comment & Directive Sanitizer   │
                    │   - Physical Memory Byte Layout     │
                    │   - Streaming JSON IR Emitter       │
                    └──────────────────┬──────────────────┘
                                       │ Streaming JSON IR
                                       ▼
                    ┌─────────────────────────────────────┐
                    │     Python 3.10+ Analysis Core      │
                    │   - Strongly Typed Pydantic IR      │
                    │   - Open Polymorphic Statement AST  │
                    │   - Declarative YAML Rules Engine   │
                    └──────┬───────────┬───────────┬──────┘
                           │           │           │
         ┌─────────────────┘           │           └─────────────────┐
         ▼                             ▼                             ▼
┌────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────┐
│ Memory Layout Core │   │   Graph & Static Analysis │   │ Pushdown Reachability │
│ - Mathematical     │   │ - Tarjan's SCC ($O(V+E)$) │   │ - LIFO Worklist Engine│
│   Invariant Proofs │   │ - Cooper Dominator Tree   │   │ - Dead Code Pruner    │
│ - Live `cobc`      │   │ - Level-2 Procedure Graph │   │ - Uncalled Sink Finder│
│   Compiler Parity  │   │ - Level-3 Cytoscape CFG   │   │                       │
└────────────────────┘   └───────────────────────────┘   └───────────────────────┘
```

---

## Key Algorithmic Innovations (Great for System Design & Coding Interviews)

### 1. Mathematical Memory Invariant Proofs
Rather than trusting heuristic offsets, the engine mathematically enforces consistency across composite memory buffers:
- **Group Sum Invariant**: $\text{Length}(\text{parent}) \equiv \sum \text{Length}(\text{child}_i) \times \text{occurs}_i$
- **Overlay Alignment Invariant**: $\text{Offset}(\text{overlay\_field}) \equiv \text{Offset}(\text{target\_field})$
- **Zero-Slop Continuous Layout**: $\text{Offset}(\text{child}_{i+1}) \equiv \text{Offset}(\text{child}_i) + \text{Length}(\text{child}_i)$
- **Compiler Parity**: Automated test harness compiles the input with GnuCOBOL (`cobc -ftsymbols -Xref`), parses the binary listing, and verifies a 100% match.

### 2. Zero-Dependency Static Graph Algorithms
- **Tarjan's Strongly Connected Components (SCC)**: Implemented with an explicit iterative state machine to prevent Python recursion depth limits on deeply nested cyclic control-flow graphs.
- **Cooper-Harvey-Kennedy (2001) Dominator Tree (`idom`)**: Computes forward dominance frontiers efficiently for compiler optimization and dead code reachability.
- **Lengauer-Tarjan Post-Dominator Tree (`ipdom`)**: Analyzes convergence on common procedure exits, virtual exits, and terminal sink nodes.

### 3. Pushdown Automaton Interprocedural Call-Stack Analysis
Simulates program execution using a LIFO worklist algorithm:
- Tracks call-frame pushes and returns across non-local procedure invocations.
- Accurately differentiates natural fallthrough execution from subroutine returns, preventing the false-positive paths common in basic DFS/BFS traversal.
- Detects uncalled error routines and genuinely dead execution blocks.

---

## Technical Interview Talking Points ("Tell Me About a Challenging Project")

### The Pitch (30-second summary)
> *"I built a compiler-grade static program analysis and memory layout reconstruction engine. It bridges an ANTLR4 Java parser to a modern Python analysis core, reconstructing physical binary memory layouts with formal mathematical proofs and 100% parity against native compiler symbol tables. I also implemented zero-dependency graph algorithms—including Tarjan’s SCC and a Pushdown Automaton—to model LIFO call stacks, eliminate dead code, and render interactive multi-level control flow graphs."*

### Deep-Dive Question 1: *"Why did you choose this problem?"*
> *"I wanted to tackle a domain with real systems-level complexity. Many modern languages abstract away physical memory behind virtual machines and garbage collectors. Legacy enterprise systems, by contrast, rely on raw physical memory overlays (`REDEFINES`), custom byte/nibble packing (`COMP-3`), and non-local control flow. Building an engine that mathematically models this memory and control flow required solving genuine compiler and graph theory problems."*

### Deep-Dive Question 2: *"What was the most challenging algorithmic problem you encountered?"*
> *"Handling control-flow reachability with non-local jumps and implicit returns. In standard procedural languages, functions have explicit return semantics. In this grammar, routines can be called via sub-procedure calls (`PERFORM`), jumped to permanently (`GO TO`), or naturally fallen into sequentially. A normal graph DFS results in false paths because it doesn't model the return stack. I designed a Pushdown Automaton with a LIFO call stack worklist that accurately simulates execution states, identifying dead blocks that no execution path could ever reach."*

### Deep-Dive Question 3: *"How did you verify correctness?"*
> *"I built a 6-tier test harness. Tier 1 checks AST wire deserialization. Tier 2 verifies data dictionary memory layouts. Tier 3 executes formal mathematical invariant proofs (Group Sum, Overlay Alignment, Zero Slop). Tier 4 tests ASG metamodel completeness. Tier 5 validates graph topologies. And Tier 6 uses a live GnuCOBOL compiler (`cobc`) as a test oracle, asserting 100% byte offset and length parity across hundreds of fields."*
