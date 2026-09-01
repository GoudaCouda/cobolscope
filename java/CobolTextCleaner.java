import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.misc.Interval;

/**
 * Text and keyword extraction / cleaning utilities for COBOL AST nodes.
 */
public class CobolTextCleaner {

    public static String cleanAuthor(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^AUTHOR\\.?\\s*", "").trim();
    }

    public static String cleanInstallation(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^INSTALLATION\\.?\\s*", "").trim();
    }

    public static String cleanDateWritten(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^DATE-WRITTEN\\.?\\s*", "").trim();
    }

    public static String cleanDateCompiled(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^DATE-COMPILED\\.?\\s*", "").trim();
    }

    public static String cleanAssignTo(String raw) {
        if (raw == null) return null;
        String s = raw.replaceAll("(?i)^ASSIGN\\s+(TO\\s+)?", "").trim();
        return s.replaceAll("^['\"]|['\"]$", "").trim();
    }

    public static String cleanFileStatus(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^FILE\\s+STATUS\\s+(IS\\s+)?", "").trim();
    }

    public static String cleanRecordKey(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^RECORD\\s+KEY\\s+(IS\\s+)?", "").trim();
    }

    public static String cleanOrganization(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^ORGANIZATION\\s+(IS\\s+)?", "").trim();
    }

    public static String cleanAccessMode(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^ACCESS(\\s+MODE)?\\s+(IS\\s+)?", "").trim();
    }

    public static String cleanValue(String raw) {
        if (raw == null) return null;
        String s = raw.replaceAll("(?i)^VALUES?\\s+(ARE|IS)?\\s*", "").trim();
        // Strip enclosing single quotes or double quotes while unescaping internal quotes
        if ((s.startsWith("'") && s.endsWith("'")) || (s.startsWith("\"") && s.endsWith("\""))) {
            if (s.length() >= 2) {
                s = s.substring(1, s.length() - 1).trim();
                s = s.replace("''", "'").replace("\"\"", "\"");
            }
        }
        return s;
    }

    public static String cleanRedefines(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^REDEFINES\\s+", "").trim();
    }

    public static String cleanDependingOn(String raw) {
        if (raw == null) return null;
        return raw.replaceAll("(?i)^DEPENDING\\s+(ON\\s+)?", "").trim();
    }

    public static String cleanContextText(ParserRuleContext ctx) {
        if (ctx == null) return "";
        if (ctx.getStart() != null && ctx.getStop() != null && ctx.getStart().getInputStream() != null) {
            int a = ctx.getStart().getStartIndex();
            int b = ctx.getStop().getStopIndex();
            if (a <= b) {
                return ctx.getStart().getInputStream().getText(new Interval(a, b))
                        .replaceAll("[\\r\\n]+", " ")
                        .replaceAll("\\s+", " ")
                        .trim();
            }
        }
        return ctx.getText().replaceAll("\\s+", " ").trim();
    }
}
