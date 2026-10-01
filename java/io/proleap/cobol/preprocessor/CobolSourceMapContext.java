package io.proleap.cobol.preprocessor;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Thread-local and global registry providing AST extractors access to
 * the active CobolSourceMap without altering public ASG interfaces.
 */
public class CobolSourceMapContext {

    private static final ThreadLocal<CobolSourceMap> currentSourceMap = new ThreadLocal<>();
    private static final Map<String, CobolSourceMap> registry = new ConcurrentHashMap<>();

    public static void set(CobolSourceMap sourceMap) {
        currentSourceMap.set(sourceMap);
    }

    public static CobolSourceMap get() {
        return currentSourceMap.get();
    }

    public static void clear() {
        currentSourceMap.remove();
    }

    public static void register(String key, CobolSourceMap sourceMap) {
        if (key != null && sourceMap != null) {
            registry.put(key, sourceMap);
        }
    }

    public static CobolSourceMap getRegistered(String key) {
        return key != null ? registry.get(key) : null;
    }
}
