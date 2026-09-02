import org.antlr.v4.runtime.ParserRuleContext;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntry;

import java.util.*;

/**
 * Canonical COBOL Intermediate Representation (IR) DTOs.
 */
public class IrModel {

    public static class SourceLocationDto {
        public int startLine;
        public int endLine;
        public int startColumn;
        public int endColumn;

        public SourceLocationDto() {}

        public SourceLocationDto(ParserRuleContext ctx) {
            if (ctx != null && ctx.getStart() != null) {
                this.startLine = ctx.getStart().getLine();
                this.startColumn = ctx.getStart().getCharPositionInLine();
                if (ctx.getStop() != null) {
                    this.endLine = ctx.getStop().getLine();
                    this.endColumn = ctx.getStop().getCharPositionInLine();
                } else {
                    this.endLine = this.startLine;
                    this.endColumn = this.startColumn;
                }
            }
        }
    }

    public static class ProgramModelDto {
        public String programId;
        public String author;
        public String installation;
        public String dateWritten;
        public String dateCompiled;
        public String sourceFile;
        public String format;
        public DataDictionaryDto dataDictionary = new DataDictionaryDto();
        public List<SectionDto> sections = new ArrayList<>();
        public List<ParagraphDto> paragraphs = new ArrayList<>();
        public AsgAuditSummaryDto asgAuditSummary;
    }

    public static class AsgAuditSummaryDto {
        public int totalAsgDataEntries;
        public int totalAsgLevel88Entries;
        public int totalAsgParagraphs;
        public int totalAsgStatements;
        public int totalAsgCalls;
        public List<String> asgVariableNames = new ArrayList<>();
        public List<String> asgLevel88Names = new ArrayList<>();
        public Map<String, List<String>> asgParagraphCalls = new LinkedHashMap<>();
    }

    public static class FileControlEntryDto {
        public String selectName;
        public String assignTo;
        public String organization;
        public String accessMode;
        public String fileStatusVar;
        public String recordKey;
        public List<String> alternateRecordKeys = new ArrayList<>();
        public SourceLocationDto location;
    }

    public static class FileDescriptionDto {
        public String name;
        public String selectName;
        public String recordingMode;
        public SourceLocationDto location;
        public List<DataFieldDto> records = new ArrayList<>();
    }

    public static class DataDictionaryDto {
        public List<FileControlEntryDto> fileControls = new ArrayList<>();
        public List<FileDescriptionDto> fileSection = new ArrayList<>();
        public List<DataFieldDto> workingStorageSection = new ArrayList<>();
        public List<DataFieldDto> linkageSection = new ArrayList<>();
        public List<DataFieldDto> localStorageSection = new ArrayList<>();
        public int workingStorageBytes;
    }

    public static class Condition88Dto {
        public String name;
        public List<String> values = new ArrayList<>();
        public SourceLocationDto location;
    }

    public static class DataFieldDto {
        public String id;
        public String qualifiedName;
        public int level;
        public String name;
        public String pic;
        public String usage;
        public String value;
        public String redefines;
        public String logicalType;
        public int byteOffset;
        public int relativeOffset;
        public int byteLength;
        public int elementByteLength;
        public Integer occursMin;
        public Integer occursMax;
        public String dependingOn;
        public List<String> indexedBy = new ArrayList<>();
        public Boolean isFiller;
        public Boolean isJustified;
        public Boolean isBlankWhenZero;
        public Boolean isSynchronized;
        public Boolean isSignSeparate;
        public List<Condition88Dto> conditions88 = new ArrayList<>();
        public List<DataFieldDto> children = new ArrayList<>();
        public SourceLocationDto location;

        public transient DataDescriptionEntry asgEntry;
    }

    public static class SectionDto {
        public String name;
        public SourceLocationDto location;
        public List<StatementDto> statements = new ArrayList<>();
        public List<String> paragraphNames = new ArrayList<>();
    }

    public static class ParagraphDto {
        public String name;
        public String sectionParent;
        public SourceLocationDto location;
        public List<String> calledBy = new ArrayList<>();
        public List<String> successors = new ArrayList<>();
        public Boolean isTerminal;
        public String fallthroughSuccessor;
        public List<StatementDto> statements = new ArrayList<>();
    }

    public static class EvaluateWhenBranchDto {
        public List<String> conditions = new ArrayList<>();
        public List<StatementDto> statements = new ArrayList<>();
    }

    public static class SearchWhenBranchDto {
        public String condition;
        public List<StatementDto> statements = new ArrayList<>();
    }

    public static class StatementDto {
        public String type;
        public SourceLocationDto location;
        public String rawText;

        public List<String> sourceFieldIds = new ArrayList<>();
        public List<String> targetFieldIds = new ArrayList<>();

        // MOVE
        public String fromExpr;
        public List<String> toTargets;
        public Boolean isCorresponding;
        public String correspondingText;

        // PERFORM
        public String target;
        public String thru;
        public String performType;
        public String timesExpr;
        public String untilCondition;
        public String varyingExpr;
        public Boolean isInline;
        public List<StatementDto> nestedStatements;

        // IF
        public String condition;
        public List<StatementDto> thenStatements;
        public List<StatementDto> elseStatements;

        // EVALUATE
        public List<String> subjects;
        public List<EvaluateWhenBranchDto> whenBranches;
        public List<StatementDto> whenOtherStatements;

        // CALL
        public String program;
        public List<String> usingParameters;
        public String giving;
        public List<StatementDto> onExceptionStatements;
        public List<StatementDto> notOnExceptionStatements;

        // COMPUTE & ARITHMETIC
        public String operation;
        public String expression;
        public List<String> targets;
        public String remainder;
        public List<StatementDto> onSizeErrorStatements;
        public List<StatementDto> notOnSizeErrorStatements;

        // I/O & CONTROL
        public String file;
        public String record;
        public String into;
        public String key;
        public String dependingOn;
        public List<StatementDto> atEndStatements;
        public List<StatementDto> notAtEndStatements;
        public List<StatementDto> invalidKeyStatements;
        public List<StatementDto> notInvalidKeyStatements;
        public List<StatementDto> endOfPageStatements;
        public List<StatementDto> notEndOfPageStatements;

        // SEARCH
        public List<SearchWhenBranchDto> searchWhenBranches;

        // STRING / UNSTRING
        public List<StatementDto> onOverflowStatements;
        public List<StatementDto> notOnOverflowStatements;

        // DISPLAY
        public List<String> operands;

        // EXEC SQL / CICS / SQLIMS
        public String subsystem;
        public String rawPayload;

        // Fallback for custom/unhandled properties
        public Map<String, Object> details;
    }
}
