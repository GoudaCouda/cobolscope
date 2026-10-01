package io.proleap.cobol.preprocessor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Tracks deterministic mapping between preprocessed ANTLR token line coordinates
 * and original physical source file lines across single, multiple, and nested copybook expansions.
 */
public class CobolSourceMap {

    public static class Entry {
        public final int prepStartLine;
        public final int prepEndLine;
        public final String sourceFile;
        public final int origStartLine;
        public final int origEndLine;

        public Entry(int prepStartLine, int prepEndLine, String sourceFile, int origStartLine, int origEndLine) {
            this.prepStartLine = prepStartLine;
            this.prepEndLine = prepEndLine;
            this.sourceFile = sourceFile != null ? sourceFile : "";
            this.origStartLine = origStartLine;
            this.origEndLine = origEndLine;
        }

        public boolean contains(int prepLine) {
            return prepLine >= prepStartLine && prepLine <= prepEndLine;
        }

        public int resolveLine(int prepLine) {
            return origStartLine + (prepLine - prepStartLine);
        }

        @Override
        public String toString() {
            return String.format("[%d..%d] -> %s:[%d..%d]", prepStartLine, prepEndLine, sourceFile, origStartLine, origEndLine);
        }
    }

    public static class ResolvedLocation {
        public final String sourceFile;
        public final int line;
        public final int column;

        public ResolvedLocation(String sourceFile, int line, int column) {
            this.sourceFile = sourceFile != null ? sourceFile : "";
            this.line = line;
            this.column = column;
        }

        @Override
        public String toString() {
            return sourceFile.isEmpty() ? "L" + line : sourceFile + ":L" + line;
        }
    }

    private final List<Entry> entries = new ArrayList<>();
    private String primarySourceFile = "";

    public CobolSourceMap() {}

    public CobolSourceMap(String primarySourceFile) {
        this.primarySourceFile = primarySourceFile != null ? primarySourceFile : "";
    }

    public void setPrimarySourceFile(String primarySourceFile) {
        this.primarySourceFile = primarySourceFile != null ? primarySourceFile : "";
    }

    public String getPrimarySourceFile() {
        return primarySourceFile;
    }

    public void addEntry(int prepStartLine, int prepEndLine, String sourceFile, int origStartLine, int origEndLine) {
        if (prepEndLine >= prepStartLine) {
            String file = (sourceFile != null && !sourceFile.isEmpty()) ? sourceFile : primarySourceFile;
            entries.add(new Entry(prepStartLine, prepEndLine, file, origStartLine, origEndLine));
        }
    }

    public void spliceChild(int parentPrepStartLine, CobolSourceMap childMap) {
        if (childMap == null || childMap.isEmpty()) {
            return;
        }
        int offset = parentPrepStartLine - 1;
        for (Entry childEntry : childMap.getEntries()) {
            addEntry(
                childEntry.prepStartLine + offset,
                childEntry.prepEndLine + offset,
                childEntry.sourceFile,
                childEntry.origStartLine,
                childEntry.origEndLine
            );
        }
    }

    public List<Entry> getEntries() {
        return Collections.unmodifiableList(entries);
    }

    public boolean isEmpty() {
        return entries.isEmpty();
    }

    public ResolvedLocation resolve(int prepLine, int prepColumn) {
        if (entries.isEmpty()) {
            return new ResolvedLocation(primarySourceFile, prepLine, prepColumn);
        }

        int low = 0;
        int high = entries.size() - 1;

        while (low <= high) {
            int mid = (low + high) >>> 1;
            Entry entry = entries.get(mid);

            if (prepLine < entry.prepStartLine) {
                high = mid - 1;
            } else if (prepLine > entry.prepEndLine) {
                low = mid + 1;
            } else {
                return new ResolvedLocation(entry.sourceFile, entry.resolveLine(prepLine), prepColumn);
            }
        }

        // Boundary clamp fallback
        if (high < 0) {
            Entry first = entries.get(0);
            return new ResolvedLocation(first.sourceFile, first.origStartLine, prepColumn);
        }
        Entry last = entries.get(entries.size() - 1);
        int clampedLine = last.origEndLine + (prepLine - last.prepEndLine);
        return new ResolvedLocation(last.sourceFile, Math.max(1, clampedLine), prepColumn);
    }
}
