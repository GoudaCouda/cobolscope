package io.proleap.cobol.preprocessor.sub.line.writer.impl;

import java.util.ArrayList;
import java.util.List;

import io.proleap.cobol.preprocessor.CobolPreprocessor;
import io.proleap.cobol.preprocessor.sub.CobolLine;
import io.proleap.cobol.preprocessor.sub.CobolLineTypeEnum;
import io.proleap.cobol.preprocessor.sub.line.writer.CobolLineWriter;

public class CobolLineWriterImpl implements CobolLineWriter {

	public static class SerializationResult {
		public final String code;
		public final int[] lineMap;

		public SerializationResult(final String code, final int[] lineMap) {
			this.code = code;
			this.lineMap = lineMap;
		}
	}

	public SerializationResult serializeWithLineMap(final List<CobolLine> lines) {
		final StringBuffer sb = new StringBuffer();
		final List<Integer> map = new ArrayList<>(lines.size() + 1);
		map.add(0); // 1-indexed padding

		for (final CobolLine line : lines) {
			final boolean notContinuationLine = !CobolLineTypeEnum.CONTINUATION.equals(line.getType());

			if (notContinuationLine) {
				if (line.getNumber() > 0) {
					sb.append(CobolPreprocessor.NEWLINE);
				}

				sb.append(line.getBlankSequenceArea());
				sb.append(line.getIndicatorArea());
				map.add(line.getNumber() + 1);
			}

			sb.append(line.getContentArea());
		}

		final int[] lineMap = new int[map.size()];
		for (int i = 0; i < map.size(); i++) {
			lineMap[i] = map.get(i);
		}

		return new SerializationResult(sb.toString(), lineMap);
	}

	@Override
	public String serialize(final List<CobolLine> lines) {
		return serializeWithLineMap(lines).code;
	}
}
