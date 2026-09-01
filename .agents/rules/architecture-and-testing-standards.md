# Architecture and Testing Standards Rule

## 1. Domain Separation & Zero Test Pollution
* **Production Runtime (`cobolscope/`)**:
  - Must remain 100% clean and free of testing harnesses, compiler bridges, oracles, or temporary debug scripts.
  - Only production data models, parsing subprocess bridges, and exporter utilities live here.
* **Testing Infrastructure (`tests/harness/`)**:
  - All test oracles, validation engines (`invariants.py`), live compiler bridges (`gnucobol_runner.py`), and ground-truth auditors (`asg_auditor.py`) must reside strictly under `tests/harness/`.
* **Test Fixtures (`tests/fixtures/`)**:
  - Synthetic test programs (`TEST-DATA-DICT.cbl`), golden compiler listings, and copybook fixtures belong in `tests/fixtures/`, not in production sample directories.

---

## 2. Open Polymorphic Statement Architecture
* High-value structured statements (`MOVE`, `PERFORM`, `IF`, `EVALUATE`, `CALL`, `COMPUTE`, arithmetic, and embedded SQL/CICS) maintain dedicated typed Pydantic models.
* All other standard COBOL verbs (`SORT`, `RELEASE`, `RETURN`, `ALTER`, `USE`, etc.) and dialect extensions gracefully normalize into `GenericStatementNode`.
* **Fallback Logging**: Any statement falling back to `GenericStatementNode` must be logged with line coordinates and original verb to ensure complete auditability.

---

## 3. Four-Tier Verification Requirement
Before committing changes to the IR, Data Dictionary, or Java runners, all 4 verification tiers must pass with 100% success:
1. **Tier 1 (E2E Pipeline & AST)**: `python tests/test_pipeline.py`
2. **Tier 2 (Mathematical Invariants)**: `python tests/test_invariants.py`
3. **Tier 3 (GnuCOBOL Compiler Parity)**: `python tests/test_gnucobol_parity.py`
4. **Tier 4 (Native ProLeap ASG Parity)**: `python tests/test_asg_parity.py`
5. **NIST Conformance**: `python tests/test_nist_suite.py`
