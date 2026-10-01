import io.proleap.cobol.asg.metamodel.CompilationUnit;
import io.proleap.cobol.asg.metamodel.Program;
import io.proleap.cobol.asg.metamodel.ProgramUnit;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntry;
import io.proleap.cobol.asg.runner.impl.CobolParserRunnerImpl;
import io.proleap.cobol.preprocessor.CobolPreprocessor.CobolSourceFormatEnum;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.util.*;

/**
 * Production Canonical IR CLI Runner and Pipeline Orchestrator.
 * Parses COBOL source files using ProLeap ASG and coordinates division extractors
 * to produce structured Canonical IR JSON output.
 */
public class ProLeapCliRunner {

    // =========================================================================
    // Backwards Compatibility Type Aliases to IrModel
    // =========================================================================
    public static class SourceLocationDto extends IrModel.SourceLocationDto {}
    public static class ProgramModelDto extends IrModel.ProgramModelDto {}
    public static class FileControlEntryDto extends IrModel.FileControlEntryDto {}
    public static class FileDescriptionDto extends IrModel.FileDescriptionDto {}
    public static class DataDictionaryDto extends IrModel.DataDictionaryDto {}
    public static class Condition88Dto extends IrModel.Condition88Dto {}
    public static class DataFieldDto extends IrModel.DataFieldDto {}
    public static class SectionDto extends IrModel.SectionDto {}
    public static class ParagraphDto extends IrModel.ParagraphDto {}
    public static class EvaluateWhenBranchDto extends IrModel.EvaluateWhenBranchDto {}
    public static class StatementDto extends IrModel.StatementDto {}
    public static class JsonWriter extends IrJsonWriter {}

    // =========================================================================
    // CLI Entry Point
    // =========================================================================

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java ProLeapCliRunner <inputFileOrDir> [format] [outputFileOrDir] [options]");
            System.err.println("Options:");
            System.err.println("  --batch                     Process folder or list of files in a single JVM run");
            System.err.println("  --manifest <manifestFile>   File containing list of input COBOL files to parse");
            System.err.println("  --output-dir <dir>          Directory to write parsed JSON files");
            System.err.println("  -I, --copybook-dir <dir>    Directory containing copybooks (repeatable or delimiter-separated)");
            System.err.println("  --copybook-ext <exts>       Comma-separated copybook extensions (default: cpy,cbl,cob,copy,inc,txt)");
            System.err.println("  --ignore-syntax-errors      Ignore minor syntax errors during ASG construction");
            System.err.println("Formats: FIXED, TANDEM, VARIABLE");
            System.exit(1);
        }

        String inputPath = null;
        String formatArg = null;
        String outputPath = null;
        String manifestPath = null;
        File outputDir = null;
        boolean isBatch = false;
        List<File> copyBookDirs = new ArrayList<>();
        List<String> copyBookExts = new ArrayList<>();
        boolean ignoreSyntaxErrors = false;

        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if ("-I".equals(arg) || "--copybook-dir".equals(arg) || "-cp-dir".equals(arg)) {
                if (i + 1 < args.length) {
                    String[] paths = args[++i].split("[;,]");
                    for (String p : paths) {
                        if (!p.trim().isEmpty()) copyBookDirs.add(new File(p.trim()));
                    }
                }
            } else if ("--copybook-ext".equals(arg) || "-cp-ext".equals(arg)) {
                if (i + 1 < args.length) {
                    String[] exts = args[++i].split("[,;]");
                    for (String ext : exts) {
                        if (!ext.trim().isEmpty()) copyBookExts.add(ext.trim().replaceAll("^\\.", ""));
                    }
                }
            } else if ("--ignore-syntax-errors".equals(arg)) {
                ignoreSyntaxErrors = true;
            } else if ("--batch".equals(arg)) {
                isBatch = true;
            } else if ("--manifest".equals(arg) && i + 1 < args.length) {
                manifestPath = args[++i];
                isBatch = true;
            } else if ("--output-dir".equals(arg) && i + 1 < args.length) {
                outputDir = new File(args[++i]);
                isBatch = true;
            } else if (inputPath == null && !arg.startsWith("-")) {
                inputPath = arg;
            } else if (formatArg == null && !arg.startsWith("-")) {
                formatArg = arg.toUpperCase();
            } else if (outputPath == null && !arg.startsWith("-")) {
                outputPath = arg;
            }
        }

        if (formatArg == null) {
            formatArg = "FIXED";
        }

        CobolSourceFormatEnum format;
        try {
            format = CobolSourceFormatEnum.valueOf(formatArg);
        } catch (IllegalArgumentException e) {
            System.err.println("ERROR: Unknown format '" + formatArg + "'. Valid: FIXED, TANDEM, VARIABLE");
            System.exit(3);
            return;
        }

        File inputFile = inputPath != null ? new File(inputPath) : null;
        if (inputFile != null && inputFile.isDirectory()) {
            isBatch = true;
        }

        if (!isBatch && manifestPath == null) {
            if (inputFile == null || !inputFile.exists()) {
                System.err.println("ERROR: Input file does not exist: " + inputPath);
                System.exit(2);
                return;
            }

            try {
                io.proleap.cobol.asg.params.impl.CobolParserParamsImpl params = new io.proleap.cobol.asg.params.impl.CobolParserParamsImpl();
                params.setFormat(format);
                params.setIgnoreSyntaxErrors(ignoreSyntaxErrors);

                if (!copyBookDirs.isEmpty()) {
                    params.setCopyBookDirectories(copyBookDirs);
                }
                if (!copyBookExts.isEmpty()) {
                    params.setCopyBookExtensions(copyBookExts);
                } else {
                    params.setCopyBookExtensions(Arrays.asList("cpy", "cbl", "cob", "copy", "inc", "txt", ""));
                }

                Program program = new CobolParserRunnerImpl().analyzeFile(inputFile, params);
                IrModel.ProgramModelDto model = extractProgramModel(program, inputFile, format);

                String jsonOutput = IrJsonWriter.toJson(model);

                if (outputPath != null && !outputPath.equals("-")) {
                    try (PrintWriter writer = new PrintWriter(new FileWriter(outputPath))) {
                        writer.print(jsonOutput);
                    }
                } else {
                    System.out.println(jsonOutput);
                }

            } catch (Exception e) {
                System.err.println("ERROR: Extraction failed: " + e.getMessage());
                e.printStackTrace(System.err);
                System.exit(4);
            }
            return;
        }

        // --- Batch Execution Mode ---
        if (outputDir == null) {
            outputDir = (outputPath != null) ? new File(outputPath) : new File(".");
        }
        outputDir.mkdirs();

        List<File> filesToProcess = new ArrayList<>();
        if (manifestPath != null) {
            try {
                List<String> lines = Files.readAllLines(new File(manifestPath).toPath());
                for (String line : lines) {
                    line = line.trim();
                    if (!line.isEmpty() && !line.startsWith("#")) {
                        filesToProcess.add(new File(line));
                    }
                }
            } catch (Exception e) {
                System.err.println("ERROR: Could not read manifest " + manifestPath + ": " + e.getMessage());
                System.exit(2);
                return;
            }
        } else if (inputFile != null && inputFile.isDirectory()) {
            File[] listed = inputFile.listFiles();
            if (listed != null) {
                for (File f : listed) {
                    if (f.isFile()) {
                        String name = f.getName().toLowerCase();
                        if (name.endsWith(".cbl") || name.endsWith(".cob") || name.endsWith(".cobol")) {
                            filesToProcess.add(f);
                        }
                    }
                }
            }
        }

        if (filesToProcess.isEmpty()) {
            System.err.println("WARNING: No COBOL source files found to process.");
            return;
        }

        final List<String> effectiveExts = !copyBookExts.isEmpty()
            ? copyBookExts
            : Arrays.asList("cpy", "cbl", "cob", "copy", "inc", "txt", "");
        final File finalOutputDir = outputDir;
        final boolean finalIgnoreSyntaxErrors = ignoreSyntaxErrors;
        final java.util.concurrent.atomic.AtomicInteger processedCounter = new java.util.concurrent.atomic.AtomicInteger(0);
        final int totalFiles = filesToProcess.size();

        // Process all files in parallel within the single JVM instance
        filesToProcess.parallelStream().forEach(file -> {
            if (!file.exists() || !file.isFile()) {
                System.err.println("WARNING: File not found: " + file.getAbsolutePath());
                System.err.flush();
                return;
            }
            long t0 = System.currentTimeMillis();
            try {
                io.proleap.cobol.asg.params.impl.CobolParserParamsImpl params = new io.proleap.cobol.asg.params.impl.CobolParserParamsImpl();
                params.setFormat(format);
                params.setIgnoreSyntaxErrors(finalIgnoreSyntaxErrors);
                if (!copyBookDirs.isEmpty()) {
                    params.setCopyBookDirectories(copyBookDirs);
                }
                params.setCopyBookExtensions(effectiveExts);

                Program program = new CobolParserRunnerImpl().analyzeFile(file, params);
                IrModel.ProgramModelDto model = extractProgramModel(program, file, format);
                String jsonOutput = IrJsonWriter.toJson(model);

                String baseName = file.getName().replaceFirst("\\.[^.]+$", "");
                File outFile = new File(finalOutputDir, baseName + ".json");
                try (PrintWriter writer = new PrintWriter(new FileWriter(outFile))) {
                    writer.print(jsonOutput);
                }
                long elapsed = System.currentTimeMillis() - t0;
                int current = processedCounter.incrementAndGet();
                int paraCount = model.paragraphs != null ? model.paragraphs.size() : 0;
                System.out.println("PARSED: [" + current + "/" + totalFiles + "] " + file.getName() + " in " + elapsed + "ms (" + paraCount + " paragraphs)");
                System.out.flush();
            } catch (Exception e) {
                int current = processedCounter.incrementAndGet();
                System.err.println("ERROR: [" + current + "/" + totalFiles + "] " + file.getName() + ": " + e.getMessage());
                System.err.flush();
            }
        });
    }

    // =========================================================================
    // Core Pipeline Orchestration
    // =========================================================================

    public static IrModel.ProgramModelDto extractProgramModel(Program program, File inputFile, CobolSourceFormatEnum format) {
        IrModel.ProgramModelDto model = new IrModel.ProgramModelDto();
        model.sourceFile = null;
        model.format = format.name();

        List<CompilationUnit> cus = program.getCompilationUnits();
        if (cus == null || cus.isEmpty()) {
            return model;
        }

        CompilationUnit cu = cus.get(0);
        ProgramUnit pu = cu.getProgramUnit();
        if (pu == null) {
            model.programId = cu.getName();
            return model;
        }

        // Maps to hold resolved ASG DataDescriptionEntry -> Field ID mapping and Name -> Field ID mapping
        Map<DataDescriptionEntry, String> entryToIdMap = new IdentityHashMap<>();
        Map<String, String> nameToIdMap = new LinkedHashMap<>();

        // 1. Identification Division
        HeaderDivisionExtractor.extractIdentificationDivision(pu.getIdentificationDivision(), model, cu.getName());

        // 2. Environment Division
        HeaderDivisionExtractor.extractEnvironmentDivision(pu.getEnvironmentDivision(), model.dataDictionary);

        // 3. Data Division & Layout Calculation
        DataDivisionExtractor.extractDataDivision(pu.getDataDivision(), model.dataDictionary, entryToIdMap, nameToIdMap);

        // 4. Procedure Division & Symbol Resolution
        ProcedureDivisionExtractor.extractProcedureDivision(pu.getProcedureDivision(), model, entryToIdMap, nameToIdMap);

        // 5. Objective Native ASG Ground-Truth Audit
        model.asgAuditSummary = AsgSemanticAuditor.auditProgramUnit(pu);

        return model;
    }
}