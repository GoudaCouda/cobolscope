import io.proleap.cobol.asg.metamodel.environment.EnvironmentDivision;
import io.proleap.cobol.asg.metamodel.environment.inputoutput.InputOutputSection;
import io.proleap.cobol.asg.metamodel.environment.inputoutput.filecontrol.FileControlEntry;
import io.proleap.cobol.asg.metamodel.environment.inputoutput.filecontrol.FileControlParagraph;
import io.proleap.cobol.asg.metamodel.identification.IdentificationDivision;

import java.util.List;

/**
 * Extracts Identification Division metadata and Environment Division file controls.
 */
public class HeaderDivisionExtractor {

    public static void extractIdentificationDivision(IdentificationDivision idDiv, IrModel.ProgramModelDto model, String fallbackName) {
        if (idDiv == null) {
            model.programId = fallbackName;
            return;
        }

        if (idDiv.getProgramIdParagraph() != null) {
            model.programId = idDiv.getProgramIdParagraph().getName();
        } else {
            model.programId = fallbackName;
        }

        if (idDiv.getAuthorParagraph() != null && idDiv.getAuthorParagraph().getCtx() != null) {
            model.author = CobolTextCleaner.cleanAuthor(CobolTextCleaner.cleanContextText(idDiv.getAuthorParagraph().getCtx()));
        }
        if (idDiv.getInstallationParagraph() != null && idDiv.getInstallationParagraph().getCtx() != null) {
            model.installation = CobolTextCleaner.cleanInstallation(CobolTextCleaner.cleanContextText(idDiv.getInstallationParagraph().getCtx()));
        }
        if (idDiv.getDateWrittenParagraph() != null && idDiv.getDateWrittenParagraph().getCtx() != null) {
            model.dateWritten = CobolTextCleaner.cleanDateWritten(CobolTextCleaner.cleanContextText(idDiv.getDateWrittenParagraph().getCtx()));
        }
        if (idDiv.getDateCompiledParagraph() != null && idDiv.getDateCompiledParagraph().getCtx() != null) {
            model.dateCompiled = CobolTextCleaner.cleanDateCompiled(CobolTextCleaner.cleanContextText(idDiv.getDateCompiledParagraph().getCtx()));
        }
    }

    public static void extractEnvironmentDivision(EnvironmentDivision envDiv, IrModel.DataDictionaryDto dict) {
        if (envDiv == null) return;

        InputOutputSection ioSection = envDiv.getInputOutputSection();
        if (ioSection == null) return;

        FileControlParagraph fcPara = ioSection.getFileControlParagraph();
        if (fcPara == null) return;

        List<FileControlEntry> entries = fcPara.getFileControlEntries();
        if (entries == null) return;

        for (FileControlEntry entry : entries) {
            IrModel.FileControlEntryDto dto = new IrModel.FileControlEntryDto();
            dto.selectName = entry.getName();
            dto.location = new IrModel.SourceLocationDto(entry.getCtx());

            if (entry.getAssignClause() != null && entry.getAssignClause().getCtx() != null) {
                dto.assignTo = CobolTextCleaner.cleanAssignTo(CobolTextCleaner.cleanContextText(entry.getAssignClause().getCtx()));
            }
            if (entry.getOrganizationClause() != null && entry.getOrganizationClause().getMode() != null) {
                dto.organization = entry.getOrganizationClause().getMode().name();
            } else if (entry.getOrganizationClause() != null && entry.getOrganizationClause().getCtx() != null) {
                dto.organization = CobolTextCleaner.cleanOrganization(CobolTextCleaner.cleanContextText(entry.getOrganizationClause().getCtx()));
            }
            if (entry.getAccessModeClause() != null && entry.getAccessModeClause().getMode() != null) {
                dto.accessMode = entry.getAccessModeClause().getMode().name();
            } else if (entry.getAccessModeClause() != null && entry.getAccessModeClause().getCtx() != null) {
                dto.accessMode = CobolTextCleaner.cleanAccessMode(CobolTextCleaner.cleanContextText(entry.getAccessModeClause().getCtx()));
            }
            if (entry.getFileStatusClause() != null && entry.getFileStatusClause().getCtx() != null) {
                dto.fileStatusVar = CobolTextCleaner.cleanFileStatus(CobolTextCleaner.cleanContextText(entry.getFileStatusClause().getCtx()));
            }
            if (entry.getRecordKeyClause() != null && entry.getRecordKeyClause().getCtx() != null) {
                dto.recordKey = CobolTextCleaner.cleanRecordKey(CobolTextCleaner.cleanContextText(entry.getRecordKeyClause().getCtx()));
            }

            dict.fileControls.add(dto);
        }
    }
}
