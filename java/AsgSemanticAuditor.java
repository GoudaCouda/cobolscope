import io.proleap.cobol.asg.metamodel.CompilationUnit;
import io.proleap.cobol.asg.metamodel.Program;
import io.proleap.cobol.asg.metamodel.ProgramUnit;
import io.proleap.cobol.asg.metamodel.call.Call;
import io.proleap.cobol.asg.metamodel.data.DataDivision;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntry;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntryCondition;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntryGroup;
import io.proleap.cobol.asg.metamodel.data.file.FileDescriptionEntry;
import io.proleap.cobol.asg.metamodel.procedure.Paragraph;
import io.proleap.cobol.asg.metamodel.procedure.ProcedureDivision;
import io.proleap.cobol.asg.metamodel.procedure.Section;

import java.util.*;

/**
 * Objective Native ASG Semantic Auditor.
 * Traverses ProLeap's native Metamodel Abstract Semantic Graph (ASG) directly,
 * collecting objective ground-truth metrics, symbol inventories, and call graphs.
 */
public class AsgSemanticAuditor {

    public static IrModel.AsgAuditSummaryDto auditProgramUnit(ProgramUnit programUnit) {
        if (programUnit == null) return null;

        IrModel.AsgAuditSummaryDto audit = new IrModel.AsgAuditSummaryDto();
        Set<DataDescriptionEntry> visitedEntries = new HashSet<>();

        // 1. Audit Data Division ASG Metamodel
        DataDivision dataDiv = programUnit.getDataDivision();
        if (dataDiv != null) {
            // File Section
            if (dataDiv.getFileSection() != null && dataDiv.getFileSection().getFileDescriptionEntries() != null) {
                for (FileDescriptionEntry fd : dataDiv.getFileSection().getFileDescriptionEntries()) {
                    if (fd.getDataDescriptionEntries() != null) {
                        for (DataDescriptionEntry entry : fd.getDataDescriptionEntries()) {
                            auditDataEntryFlat(entry, audit, visitedEntries);
                        }
                    }
                }
            }

            // Working-Storage Section
            if (dataDiv.getWorkingStorageSection() != null && dataDiv.getWorkingStorageSection().getDataDescriptionEntries() != null) {
                for (DataDescriptionEntry entry : dataDiv.getWorkingStorageSection().getDataDescriptionEntries()) {
                    auditDataEntryFlat(entry, audit, visitedEntries);
                }
            }

            // Linkage Section
            if (dataDiv.getLinkageSection() != null && dataDiv.getLinkageSection().getDataDescriptionEntries() != null) {
                for (DataDescriptionEntry entry : dataDiv.getLinkageSection().getDataDescriptionEntries()) {
                    auditDataEntryFlat(entry, audit, visitedEntries);
                }
            }

            // Local-Storage Section
            if (dataDiv.getLocalStorageSection() != null && dataDiv.getLocalStorageSection().getDataDescriptionEntries() != null) {
                for (DataDescriptionEntry entry : dataDiv.getLocalStorageSection().getDataDescriptionEntries()) {
                    auditDataEntryFlat(entry, audit, visitedEntries);
                }
            }
        }

        // 2. Audit Procedure Division ASG Metamodel
        ProcedureDivision procDiv = programUnit.getProcedureDivision();
        if (procDiv != null) {
            // Sections
            if (procDiv.getSections() != null) {
                for (Section sec : procDiv.getSections()) {
                    if (sec.getStatements() != null) {
                        audit.totalAsgStatements += sec.getStatements().size();
                    }
                }
            }

            // Paragraphs
            if (procDiv.getParagraphs() != null) {
                for (Paragraph p : procDiv.getParagraphs()) {
                    audit.totalAsgParagraphs++;
                    if (p.getStatements() != null) {
                        audit.totalAsgStatements += p.getStatements().size();
                    }

                    if (p.getCalls() != null && !p.getCalls().isEmpty()) {
                        List<String> callerNames = new ArrayList<>();
                        for (Call call : p.getCalls()) {
                            if (call.getCtx() != null) {
                                callerNames.add(call.getCtx().getText());
                            }
                        }
                        if (!callerNames.isEmpty()) {
                            audit.asgParagraphCalls.put(p.getName(), callerNames);
                        }
                    }
                }
            }
        }

        return audit;
    }

    private static void auditDataEntryFlat(
            DataDescriptionEntry entry,
            IrModel.AsgAuditSummaryDto audit,
            Set<DataDescriptionEntry> visited) {

        if (entry == null || !visited.add(entry)) return;

        Integer level = entry.getLevelNumber();
        String name = entry.getName();

        if (entry instanceof DataDescriptionEntryCondition || (level != null && level == 88)) {
            audit.totalAsgLevel88Entries++;
            if (name != null && !name.trim().isEmpty()) {
                audit.asgLevel88Names.add(name.trim().toUpperCase());
            }
        } else {
            audit.totalAsgDataEntries++;
            if (name != null && !name.trim().isEmpty()) {
                audit.asgVariableNames.add(name.trim().toUpperCase());
            }
            if (entry.getCalls() != null) {
                audit.totalAsgCalls += entry.getCalls().size();
            }
        }
    }
}
