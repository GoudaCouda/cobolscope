# CobolScope Verification & Test Suite

This directory contains the comprehensive, multi-layer verification test suite and test harness infrastructure for the CobolScope COBOL Semantic Analysis, AST Extraction, and Procedure Call Graph engine.

---

## 1. Directory Structure

```
tests/
├── harness/                           # Dedicated Verification Engines & Oracles
│   ├── __init__.py                    # Test harness package exports
│   ├── asg_auditor.py                 # Native ProLeap ASG Metamodel Ground-Truth Auditor
│   ├── call_graph_validator.py        # Level-2 Call Graph Topology & Invariant Validator
│   ├── gnucobol_runner.py             # Live GnuCOBOL (cobc) Compiler Bridge & Listing Parser
│   ├── invariants.py                  # Mathematical Self-Consistency Invariant Verifiers
│   └── test_cache.py                  # Session Warm Cache & Fixture Resolver
│
├── fixtures/                          # Test Fixtures & Pre-computed Golden Listings
│   ├── TEST-DATA-DICT.cbl             # Synthetic Edge-Case Gauntlet Stress-Test Program
│   ├── TEST-GRAPH-EDGE-CASES.cbl      # Topology Stress-Test Program (Clusters, Cycles, Fallthroughs)
│   ├── bank_of_z/                     # Open-Source IBM Bank-of-Z Enterprise CICS/DB2 Programs & Copybooks
│   └── gnucobol_golden_listings/      # Official GnuCOBOL 3.2 Compiler Symbol Listings
│       └── TEST-DATA-DICT.listing.txt
│
├── nistcobol85/                       # Official NIST COBOL-85 Standard Test Suite
│   └── src/                           # 500+ Official Conformance CBL Programs & Copybooks
│
├── run_all_tests.py                   # Master Unified Multi-Tier Verification Runner
├── test_pipeline.py                   # Tier 1: E2E Java-to-Python AST Wire Deserialization
├── test_data_dictionary.py            # Tier 2: Data Dictionary 1:1 Reconciliation & Exporters
├── test_invariants.py                 # Tier 3: Automated Mathematical Invariant Proofs
├── test_asg_parity.py                 # Tier 4: Native ProLeap ASG Metamodel Semantic Parity
├── test_call_graph.py                 # Tier 5: Level-2 Call Graph & Visual Exporters
├── test_gnucobol_parity.py            # Tier 6: GnuCOBOL (cobc) Live Compiler Parity
├── test_cfg.py                        # Level-3 Cytoscape Intra-Procedural CFG Suite
├── test_rules.py                      # Declarative Rules Engine & Discovery Scanner Suite
├── test_termination.py                # ABEND & Terminal Procedure Classifier Suite
├── test_reachability.py               # Pushdown Automaton Interprocedural Reachability
└── test_nist_suite.py                 # NIST COBOL-85 Standard Conformance Suite
```

---

## 2. Test Suites & Verification Methodologies

### 1. End-to-End AST Pipeline (`test_pipeline.py`)
- **Methodology**: Black-Box Java-to-Python Wire Deserialization
- **Coverage**: Audits statement discriminated unions (`MoveStatementNode`, `PerformStatementNode`, `IfStatementNode`, `EvaluateStatementNode`), Paragraph CFG resolution (`calledBy`, `successors`, `isTerminal`, `fallthroughSuccessor`), and statement Data Flow Graph (DFG) symbol resolution (`sourceFieldIds`, `targetFieldIds`).

### 2. Data Dictionary Reconciliation (`test_data_dictionary.py`)
- **Methodology**: 1:1 In-Memory Attribute Reconciliation & Exporter Roundtrip
- **Coverage**: Validates exact physical memory layout, Level-88 domain rules, referencing procedure indexing, and roundtrip serialization across **Markdown (`.md`)**, **HTML (`.html`)**, **CSV (`.csv`)**, and **JSON (`.json`)**.

### 3. Mathematical Invariant Suite (`test_invariants.py`)
- **Methodology**: Formal Mathematical Consistency Proofs on Memory Layout
- **Invariants Checked**:
  1. **Group Sum Invariant**: $\text{byte\_length}(\text{parent}) = \sum \text{byte\_length}(\text{children}) \times \text{occurs}$
  2. **REDEFINES Alignment Invariant**: $\text{byte\_offset}(\text{field}) == \text{byte\_offset}(\text{target})$
  3. **Continuous Layout (Zero Slop) Invariant**: $\text{byte\_offset}(\text{child}_{i+1}) == \text{byte\_offset}(\text{child}_i) + \text{byte\_length}(\text{child}_i)$
  4. **Level-88 Invariant**: Level-88 flags allocate 0 bytes and maintain valid non-empty condition intervals.

### 4. GnuCOBOL Compiler Parity (`test_gnucobol_parity.py`)
- **Methodology**: Binary Compiler Cross-Verification
- **Coverage**: Invokes `cobc -fsyntax-only -std=ibm -ftsymbols -Xref -T` to assert 100% byte offset and length parity between GnuCOBOL's compiled layout and ProLeap's Data Dictionary.

### 5. Native ProLeap ASG Semantic Parity (`test_asg_parity.py`)
- **Methodology**: Direct Native ASG Metamodel Auditing (`CompilationUnit`)
- **Coverage**: Traverses ProLeap's internal `DataDescriptionEntry`, `ValueInterval`, and `Paragraph.getCalls()` graphs to ensure 100% zero-drop completeness.

### 6. NIST COBOL-85 Conformance Suite (`test_nist_suite.py`)
- **Methodology**: Standard Industry Conformance Testing
- **Coverage**: Executes the parser across official NIST COBOL-85 programs in `tests/nistcobol85/src/` (covering core language modules: `NC` Nucleus, `IF` Sequential I/O, `IX` Indexed I/O, `RL` Relative I/O, `ST` String/Unstring, `SM` Source Text Manipulation).

### 7. Level-3 Intra-Procedural CFGs (`test_cfg.py`)
- **Methodology**: Fine-Grained Intra-Paragraph Flow Topology Testing
- **Coverage**: Validates statement linear sequencing, decision branch fanout (`IF`/`EVALUATE`), merge nodes, and dead-end terminal sink pruning for abnormal termination routines.

### 8. Declarative YAML Rules Engine (`test_rules.py`)
- **Methodology**: Schema Validation, Rule Merging, and Discovery Testing
- **Coverage**: Validates `cobolscope-rules.yaml` loading, program-level override cascades, `--init-rules` automated scanner discovery, and edge case fallbacks.

### 9. ABEND & Terminal Procedure Classifier (`test_termination.py`)
- **Methodology**: Multi-Heuristic Pattern Matching & Semantic Classification
- **Coverage**: Audits strict paragraph naming, regex matching, runtime module invocations (`CEE3ABD`, etc.), S0C7 hardware exceptions, and database status check patterns.

---

## 3. Running the Test Suites

### Run Full Test Suite via Unittest
```powershell
python -m unittest discover -s tests
```

### Run All Standard Verification Tiers (Unified Runner)
```powershell
python tests/run_all_tests.py
```

### Run NIST COBOL-85 Conformance Suite
```powershell
python tests/test_nist_suite.py
```
