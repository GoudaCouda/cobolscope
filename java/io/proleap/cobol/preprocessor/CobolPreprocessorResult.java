package io.proleap.cobol.preprocessor;

public class CobolPreprocessorResult {
    public final String code;
    public final CobolSourceMap sourceMap;

    public CobolPreprocessorResult(String code, CobolSourceMap sourceMap) {
        this.code = code;
        this.sourceMap = sourceMap;
    }
}
