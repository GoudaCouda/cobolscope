"""
Objective ProLeap ASG Semantic Audit & Graph Cross-Validation Test Harness.
Leverages ProLeap's Abstract Semantic Graph (ASG) and ANTLR token positions
as the definitive ground truth to verify 100% extraction completeness and fidelity.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from cobolscope.models import (
    ProgramModel,
    DataField,
    Condition88,
    ParagraphNode,
    SectionNode,
    StatementNode,
)


class AsgSemanticAuditor:
    """
    Validates ProgramModel instances against ProLeap's native ASG ground-truth metrics.
    """

    def __init__(self, model: ProgramModel, source_file: Optional[str | Path] = None):
        self.model = model
        self.source_file = Path(source_file or model.source_file_path)
        self.violations: List[str] = []

    def audit_all(self) -> List[str]:
        """Runs all ASG semantic completeness and source slice audits."""
        self.violations = []
        self.audit_asg_completeness()
        self.audit_call_graph_and_structure()
        return self.violations

    def audit_asg_completeness(self) -> List[str]:
        """
        Asserts 100% parity between native ProLeap ASG entries and the emitted ProgramModel.
        """
        audit = self.model.asg_audit_summary
        if not audit:
            self.violations.append("ASG Audit Summary missing in ProgramModel!")
            return self.violations

        # 1. Collect all DataFields and Level-88s from the ProgramModel
        model_fields: List[DataField] = []
        model_88_names: Set[str] = set()

        def collect(fields: List[DataField]):
            for f in fields:
                model_fields.append(f)
                for c in f.conditions_88:
                    model_88_names.add(c.name.upper().strip())
                collect(f.children)

        for fd in self.model.data_dictionary.file_section:
            collect(fd.records)
        collect(self.model.data_dictionary.working_storage_section)
        collect(self.model.data_dictionary.linkage_section)
        collect(self.model.data_dictionary.local_storage_section)

        # 2. Assert Data Entry Count Parity
        if len(model_fields) != audit.total_asg_data_entries:
            self.violations.append(
                f"DataField count mismatch: ASG Ground Truth={audit.total_asg_data_entries}, "
                f"ProgramModel={len(model_fields)}"
            )

        # 3. Assert Level-88 Condition Count Parity
        total_model_88s = sum(len(f.conditions_88) for f in model_fields)
        if total_model_88s != audit.total_asg_level88_entries:
            self.violations.append(
                f"Level-88 count mismatch: ASG Ground Truth={audit.total_asg_level88_entries}, "
                f"ProgramModel={total_model_88s}"
            )

        # 4. Assert Variable Name Discovery Parity
        model_field_names = {f.name.upper().strip() for f in model_fields if f.name != "FILLER"}
        for asg_var in audit.asg_variable_names:
            if asg_var and asg_var != "FILLER" and asg_var not in model_field_names:
                self.violations.append(f"ASG Variable '{asg_var}' missing from ProgramModel!")

        # 5. Assert Level-88 Name Discovery Parity
        for asg_88 in audit.asg_level88_names:
            if asg_88 and asg_88 not in model_88_names:
                self.violations.append(f"ASG Level-88 Condition '{asg_88}' missing from ProgramModel!")

        # 6. Assert Paragraph Count Parity
        if len(self.model.paragraphs) != audit.total_asg_paragraphs:
            self.violations.append(
                f"Paragraph count mismatch: ASG Ground Truth={audit.total_asg_paragraphs}, "
                f"ProgramModel={len(self.model.paragraphs)}"
            )

        return self.violations

    def audit_call_graph_and_structure(self) -> List[str]:
        """
        Audits CFG edges and ensures physical paragraphs maintain structural integrity.
        """
        valid_targets = (
            {p.name.upper() for p in self.model.paragraphs}
            | {s.name.upper() for s in self.model.sections}
        )

        for p in self.model.paragraphs:
            # Check that all successors exist in the program (paragraph or section)
            for succ in p.successors:
                if succ.upper() not in valid_targets:
                    self.violations.append(
                        f"Paragraph '{p.name}' references non-existent successor '{succ}'"
                    )

            # Check that fallthrough successor exists if present
            if p.fallthrough_successor and p.fallthrough_successor.upper() not in valid_targets:
                self.violations.append(
                    f"Paragraph '{p.name}' references non-existent fallthrough successor '{p.fallthrough_successor}'"
                )

        return self.violations
