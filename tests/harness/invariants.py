"""
Automated Invariant Validation Engine for COBOL Data Dictionaries.
Performs rigorous mathematical self-consistency checks across group sums,
REDEFINES memory overlays, continuous byte layout, and Level-88 domain rules.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from cobolscope.models import ProgramModel, DataField, Condition88


@dataclass
class InvariantViolation:
    rule_name: str
    severity: str  # "ERROR" or "WARNING"
    section: str
    field_id: str
    field_name: str
    message: str
    expected: Any
    actual: Any

    def __str__(self) -> str:
        return (
            f"[{self.severity}] {self.rule_name} in {self.section} on '{self.field_name}' ({self.field_id}): "
            f"{self.message} (Expected: {self.expected}, Got: {self.actual})"
        )


class DataDictionaryValidator:
    """
    Validates mathematical self-consistency invariants on parsed ProgramModel instances.
    """

    def __init__(self):
        self.violations: List[InvariantViolation] = []

    def validate(self, model: ProgramModel) -> List[InvariantViolation]:
        """
        Runs all 4 mathematical invariant rules across all data sections.
        Returns a list of any detected InvariantViolation instances.
        """
        self.violations = []
        dd = model.data_dictionary

        # Build symbol map of all fields for target resolution
        name_map: Dict[str, DataField] = {}
        def index_names(fields: List[DataField]):
            for f in fields:
                name_map[f.name.upper()] = f
                if f.qualified_name:
                    name_map[f.qualified_name.upper()] = f
                index_names(f.children)

        for fd in dd.file_section:
            index_names(fd.records)
        index_names(dd.working_storage_section)
        index_names(dd.linkage_section)
        index_names(dd.local_storage_section)

        # 1. FILE SECTION
        for fd in dd.file_section:
            sec_name = f"FILE: {fd.name}"
            self._validate_section_fields(fd.records, sec_name, sequential_roots=False, name_map=name_map)

        # 2. WORKING-STORAGE SECTION (Sequential contiguous roots)
        self._validate_section_fields(dd.working_storage_section, "WORKING-STORAGE", sequential_roots=True, name_map=name_map)

        # 3. LINKAGE SECTION (Each 01 parameter has independent base offset 0)
        self._validate_section_fields(dd.linkage_section, "LINKAGE", sequential_roots=False, name_map=name_map)

        # 4. LOCAL-STORAGE SECTION (Sequential contiguous stack roots)
        self._validate_section_fields(dd.local_storage_section, "LOCAL-STORAGE", sequential_roots=True, name_map=name_map)

        return self.violations

    def _validate_section_fields(
        self,
        fields: List[DataField],
        section: str,
        sequential_roots: bool,
        name_map: Dict[str, DataField],
    ) -> None:
        if not fields:
            return

        # Check continuous layout across 01 root records if section is sequential
        if sequential_roots:
            self._check_continuous_siblings(fields, section, is_root=True)

        for field in fields:
            self._validate_field_recursive(field, section, name_map, parent=None)

    def _validate_field_recursive(
        self,
        field: DataField,
        section: str,
        name_map: Dict[str, DataField],
        parent: Optional[DataField] = None,
    ) -> None:
        # Rule 1: The Group Sum Invariant
        if field.children:
            child_sum = 0
            for child in field.children:
                if child.redefines is None:
                    child_sum += child.byte_length

            multiplier = field.occurs_max if (field.occurs_max and field.occurs_max > 0) else 1
            expected_parent_len = child_sum * multiplier

            if field.byte_length != expected_parent_len:
                self.violations.append(
                    InvariantViolation(
                        rule_name="Group Sum Invariant",
                        severity="ERROR",
                        section=section,
                        field_id=field.id or "",
                        field_name=field.name,
                        message=f"Group byte length does not equal sum of non-redefined children ({child_sum}) × occurrences ({multiplier})",
                        expected=expected_parent_len,
                        actual=field.byte_length,
                    )
                )

            # Rule 3: Continuous Layout (Zero Slop) among children
            self._check_continuous_siblings(field.children, section, is_root=False)

            for child in field.children:
                self._validate_field_recursive(child, section, name_map, parent=field)

        # Rule 2: The REDEFINES Alignment Invariant
        if field.redefines:
            target_name = field.redefines.upper().strip()
            target = None
            if parent:
                for sib in parent.children:
                    if sib.name.upper() == target_name:
                        target = sib
                        break
            if not target and field.qualified_name:
                parts = field.qualified_name.split(".")
                if len(parts) > 1:
                    q_target = ".".join(parts[:-1] + [target_name]).upper()
                    target = name_map.get(q_target)
            if not target:
                target = name_map.get(target_name)

            if target:
                if field.byte_offset != target.byte_offset:
                    self.violations.append(
                        InvariantViolation(
                            rule_name="REDEFINES Alignment Invariant",
                            severity="ERROR",
                            section=section,
                            field_id=field.id or "",
                            field_name=field.name,
                            message=f"Redefining field byte offset does not match target '{target_name}' base offset",
                            expected=target.byte_offset,
                            actual=field.byte_offset,
                        )
                    )
                if field.byte_length > target.byte_length:
                    self.violations.append(
                        InvariantViolation(
                            rule_name="REDEFINES Length Invariant",
                            severity="WARNING",
                            section=section,
                            field_id=field.id or "",
                            field_name=field.name,
                            message=f"Redefining field byte length ({field.byte_length}) exceeds target '{field.redefines}' length ({target.byte_length})",
                            expected=f"<= {target.byte_length}",
                            actual=field.byte_length,
                        )
                    )
            else:
                self.violations.append(
                    InvariantViolation(
                        rule_name="REDEFINES Target Resolution",
                        severity="ERROR",
                        section=section,
                        field_id=field.id or "",
                        field_name=field.name,
                        message=f"REDEFINES target field '{field.redefines}' could not be resolved in symbol table",
                        expected="Valid DataField",
                        actual=None,
                    )
                )

        # Rule 4: Level-88 Conditions Invariant
        for c88 in field.conditions_88:
            if not c88.values:
                self.violations.append(
                    InvariantViolation(
                        rule_name="Level-88 Rule Invariant",
                        severity="WARNING",
                        section=section,
                        field_id=field.id or "",
                        field_name=c88.name,
                        message=f"Level-88 condition '{c88.name}' has no defined valid values",
                        expected="Non-empty values list",
                        actual=[],
                    )
                )

        # Recurse children
        for child in field.children:
            self._validate_field_recursive(child, section, name_map)

    def _check_continuous_siblings(
        self,
        siblings: List[DataField],
        section: str,
        is_root: bool,
    ) -> None:
        """Verifies that consecutive non-redefining siblings form a continuous contiguous memory span."""
        prev_field: Optional[DataField] = None
        running_high_water_mark = 0

        for current in siblings:
            if current.redefines is not None:
                # Overlays share base offset with redefined item, but may extend high water mark
                overlay_end = current.byte_offset + current.byte_length
                if overlay_end > running_high_water_mark:
                    running_high_water_mark = overlay_end
                continue

            if prev_field is not None:
                expected_abs_offset = prev_field.byte_offset + prev_field.byte_length
                if current.byte_offset != expected_abs_offset and current.byte_offset < expected_abs_offset:
                    self.violations.append(
                        InvariantViolation(
                            rule_name="Continuous Layout Invariant",
                            severity="ERROR",
                            section=section,
                            field_id=current.id or "",
                            field_name=current.name,
                            message=f"Non-redefining sibling starts at {current.byte_offset}, overlapping prior sibling '{prev_field.name}' end {expected_abs_offset}",
                            expected=expected_abs_offset,
                            actual=current.byte_offset,
                        )
                    )

                if not is_root:
                    expected_rel_offset = prev_field.relative_offset + prev_field.byte_length
                    if current.relative_offset != expected_rel_offset:
                        self.violations.append(
                            InvariantViolation(
                                rule_name="Continuous Relative Layout Invariant",
                                severity="ERROR",
                                section=section,
                                field_id=current.id or "",
                                field_name=current.name,
                                message=f"Child relative offset ({current.relative_offset}) does not match prior child end ({expected_rel_offset})",
                                expected=expected_rel_offset,
                                actual=current.relative_offset,
                            )
                        )

            prev_field = current
            running_high_water_mark = max(running_high_water_mark, current.byte_offset + current.byte_length)
