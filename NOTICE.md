# CobolScope Notice & Attribution

**CobolScope**  
Copyright &copy; 2026 CobolScope Contributors.  
Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](file:///C:/Users/austi/cobolscope/LICENSE) for details.

---

## 1. Original Work (Developed from Scratch for CobolScope)

The following components were authored completely from scratch specifically for the CobolScope project and are licensed under the Apache License, Version 2.0:

### Core Python Architecture
- All modules in [`cobolscope/`](file:///C:/Users/austi/cobolscope/cobolscope):
  - Abstract Syntax Tree (AST) hydration and canonical metamodel.
  - Level-2 Procedure Call Graph builder, clusterer, and disentangling engine.
  - Pushdown Automaton (PDA) control-flow reachability analyzer.
  - Level-3 Intra-procedural Control Flow Graph (CFG) engine.
  - Comprehensive Data Dictionary generator with bit-level memory layout calculations.
  - Interactive Documentation Portal generator and command-line interface ([`cli.py`](file:///C:/Users/austi/cobolscope/cobolscope/cli.py)).
- All test suites in [`tests/`](file:///C:/Users/austi/cobolscope/tests) and test harness validation engines in [`tests/harness/`](file:///C:/Users/austi/cobolscope/tests/harness).
- All web visualization templates in [`cobolscope/templates/`](file:///C:/Users/austi/cobolscope/cobolscope/templates).

### Original Java Extraction & Pipeline Classes (`java/`)
- [`java/AsgSemanticAuditor.java`](file:///C:/Users/austi/cobolscope/java/AsgSemanticAuditor.java): Custom AST/ASG verification oracle.
- [`java/CobolTextCleaner.java`](file:///C:/Users/austi/cobolscope/java/CobolTextCleaner.java): Token normalization and COBOL syntax cleaner.
- [`java/DataDivisionExtractor.java`](file:///C:/Users/austi/cobolscope/java/DataDivisionExtractor.java): Data Division, REDEFINES, and memory layout extractor.
- [`java/HeaderDivisionExtractor.java`](file:///C:/Users/austi/cobolscope/java/HeaderDivisionExtractor.java): Identification & Environment Division extractor.
- [`java/IrJsonWriter.java`](file:///C:/Users/austi/cobolscope/java/IrJsonWriter.java): Zero-dependency fast JSON serialization engine.
- [`java/IrModel.java`](file:///C:/Users/austi/cobolscope/java/IrModel.java): Canonical IR Data Transfer Object (DTO) hierarchy.
- [`java/ProcedureDivisionExtractor.java`](file:///C:/Users/austi/cobolscope/java/ProcedureDivisionExtractor.java): Procedure Division hierarchy extractor.
- [`java/ProLeapCliRunner.java`](file:///C:/Users/austi/cobolscope/java/ProLeapCliRunner.java): JVM CLI runner orchestrator and streaming JSON pipeline.
- [`java/StatementMapper.java`](file:///C:/Users/austi/cobolscope/java/StatementMapper.java): Open polymorphic statement mapping engine.
- [`java/io/proleap/cobol/preprocessor/CobolPreprocessorResult.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/CobolPreprocessorResult.java): Preprocessed source and line coordinate container.
- [`java/io/proleap/cobol/preprocessor/CobolSourceMap.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/CobolSourceMap.java): Interval-tree physical line coordinate mapper.
- [`java/io/proleap/cobol/preprocessor/CobolSourceMapContext.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/CobolSourceMapContext.java): Thread-local and global registry for active source maps.

---

## 2. Modified Derivative Works (Adapted from ProLeap COBOL Parser)

This product includes modified software derived from the **ProLeap COBOL Parser** ([proleap-cobol-parser](https://github.com/wrdlbrnft/proleap-cobol-parser)):

> **Copyright &copy; 2017, Ulrich Wolffgang &lt;ulrich.wolffgang@proleap.io&gt;**  
> All rights reserved.  
> Licensed under the **MIT License**.

The following files located in `java/io/proleap/` are modified derivative works adapted to inject CobolScope physical source coordinate mapping across copybook expansions:
- [`java/io/proleap/cobol/asg/runner/impl/CobolParserRunnerImpl.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/asg/runner/impl/CobolParserRunnerImpl.java)
- [`java/io/proleap/cobol/preprocessor/impl/CobolPreprocessorImpl.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/impl/CobolPreprocessorImpl.java)
- [`java/io/proleap/cobol/preprocessor/sub/document/CobolDocumentParserListener.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/sub/document/CobolDocumentParserListener.java)
- [`java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentContext.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentContext.java)
- [`java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentParserImpl.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentParserImpl.java)
- [`java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentParserListenerImpl.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/sub/document/impl/CobolDocumentParserListenerImpl.java)
- [`java/io/proleap/cobol/preprocessor/sub/line/writer/impl/CobolLineWriterImpl.java`](file:///C:/Users/austi/cobolscope/java/io/proleap/cobol/preprocessor/sub/line/writer/impl/CobolLineWriterImpl.java)

*Modifications Copyright &copy; 2026 CobolScope Contributors.*

---

## 3. Third-Party Open Source Components

This product bundles or interacts with the following open-source dependencies:

| Component | Copyright / Authors | License | Purpose |
| :--- | :--- | :--- | :--- |
| **ProLeap COBOL Parser** | Ulrich Wolffgang | MIT | Base COBOL parser & ASG engine |
| **ANTLR 4 Runtime** | Terence Parr, Sam Harwell | BSD 3-Clause | Lexer & Parser runtime |
| **Cytoscape.js** | The Cytoscape Consortium | MIT | Graph visualization engine |
| **Dagre & cytoscape-dagre** | Chris Pettitt | MIT | Directed graph layout library |
| **Eclipse Layout Kernel (ELK)** | Kiel University and others | EPL-2.0 / MIT | Layered graph layout engine |
| **Pydantic** | Samuel Colvin and contributors | MIT | Data validation and metamodels |
| **Jinja2** | Pallets Projects | BSD 3-Clause | HTML template engine |
