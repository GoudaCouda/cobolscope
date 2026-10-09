# Architecture and Testing Standards Rule

## 1. Domain Separation & Zero Test Pollution
* **Production Runtime (`cobolscope/`)**:
  - Must remain 100% clean and free of testing harnesses, compiler bridges, oracles, or temporary debug scripts.
  - Only production data models, parsing subprocess bridges, and exporter utilities live here.
* **Testing Infrastructure (`tests/harness/`)**:
  - All test oracles, validation engines (`invariants.py`), live compiler bridges (`gnucobol_runner.py`), and ground-truth auditors (`asg_auditor.py`) must reside strictly under `tests/harness/`.
* **Test Fixtures (`tests/fixtures/`)**:
  - Synthetic test programs (`TEST-DATA-DICT.cbl`), golden compiler listings, and copybook fixtures belong in `tests/fixtures/`, not in production sample directories.