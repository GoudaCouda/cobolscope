# ProLeap-First Tooling & Built-in Capability Rule

## Core Directive
Before implementing any new tooling, parsers, extractors, validators, or test harnesses, **always first check if the built-in ProLeap COBOL parser (`io.proleap.cobol.*`) already provides the required capability**.

* **For Test Suites & Ground-Truth Oracles (Strict)**: Always utilize ProLeap's native Abstract Semantic Graph (ASG) metamodel, ANTLR token streams, and symbol resolvers rather than writing ad-hoc regexes or secondary parsers.
* **For Production Runtime / CLI (Pragmatic)**: Leverage Java extraction for complex AST/ASG resolution during parsing, then transfer into optimized Pydantic v2 in-memory models for fast $O(1)$ querying and lightweight CLI execution.

---

## ProLeap Built-In Capabilities & Function Inventory

| Category | ProLeap Class / Method | One-Sentence Summary |
| :--- | :--- | :--- |
| **Pipeline Runner** | `CobolParserRunner.analyzeFile(...)` | Runs preprocessing, ANTLR lexing/parsing, and 2-phase semantic graph resolution in a single call. |
| **Metamodel Root** | `CompilationUnit.getProgram()` / `getProgramUnits()` | Provides access to all programs, subprograms, and divisions defined within the compilation unit. |
| **Variable Lineage** | `DataDescriptionEntry.getCalls()` | Returns the complete list of statement references and call-sites accessing a variable across the entire program. |
| **Routine Call Graph** | `Paragraph.getCalls()` / `Section.getCalls()` | Returns all calling routines and `PERFORM`/`GO TO` statements that invoke a specific paragraph or section. |
| **Statement DFG** | `Statement.getCalledDataDescriptionEntries()` | Returns the collection of all data entries accessed (read or modified) by that individual statement. |
| **REDEFINES Target** | `RedefinesClause.getRedefinesDataDescriptionEntry()` | Directly resolves the exact target AST `DataDescriptionEntry` of a `REDEFINES` clause without manual symbol search. |
| **OCCURS Metadata** | `DataDescriptionEntry.getOccursClause()` | Provides min/max bounds, `DEPENDING ON` variables, and `INDEXED BY` symbols directly from the AST. |
| **Level-88 Intervals** | `DataDescriptionEntryCondition.getValueIntervals()` | Extracts all condition literals and continuous value intervals (`FROM ... THRU ...`) for boolean domain validation. |
| **Group Hierarchy** | `DataDescriptionEntryGroup.getDataDescriptionEntries()` | Traverses child AST hierarchies and records without manual level-number string parsing. |
| **Statement Typing** | `Statement.getStatementType()` | Enum-based classification for all 45+ standard COBOL verbs (`MOVE`, `PERFORM`, `IF`, `EVALUATE`, `CALL`, etc.). |
| **Copybook Expansion** | `CobolPreprocessor.process(...)` | Handles multi-directory copybook discovery, `REPLACING` phrase token substitution, and comment stripping. |
| **Line Normalization** | `CobolLineReader` | Parses standard `FIXED` (Cols 1-6 seq, Col 7 indicator, Cols 8-72 Area A/B), `TANDEM`, and `VARIABLE` line formats. |
| **Symbol Resolution** | `NameResolver.resolveDataDescriptionEntry(...)` | Resolves qualified identifiers (`FIELD OF GROUP`) and shadowed variables across local and global scopes. |
| **Source Tracking** | `ASGElement.getCtx()` | Exposes ANTLR `ParserRuleContext` containing exact line numbers, token indexes, character offsets, and source streams. |

---

## Workflow When Adding New Features

1. **Search ProLeap First**: Search `proleap-cobol-parser/src/main/java/io/proleap/cobol/` for relevant metamodel classes (`asg.metamodel.*`), resolvers (`asg.resolver.*`), or preprocessor tools.
2. **Extract via Java Model**: If ProLeap supports it, add the property to `IrModel.java` and extract it in `DataDivisionExtractor`, `ProcedureDivisionExtractor`, or `StatementMapper`.
3. **Expose in Pydantic IR**: Add the corresponding typed attribute to `cobolscope/models.py`.
4. **Validate with ASG Auditor**: Cross-verify extraction completeness against native ASG metrics in `tests/harness/asg_auditor.py`.
