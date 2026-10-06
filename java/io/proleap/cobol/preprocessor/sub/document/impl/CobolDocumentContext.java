/*
 * Copyright (C) 2017, Ulrich Wolffgang <ulrich.wolffgang@proleap.io>
 * Modifications Copyright (c) 2026 CobolScope Contributors.
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the MIT license. See the LICENSE file for details.
 */

package io.proleap.cobol.preprocessor.sub.document.impl;

import java.util.Arrays;
import java.util.List;

import org.antlr.v4.runtime.BufferedTokenStream;

import io.proleap.cobol.CobolPreprocessorParser.ReplaceClauseContext;

/**
 * A replacement context that defines, which replaceables should be replaced by
 * which replacements.
 */
public class CobolDocumentContext {

	private CobolReplacementMapping[] currentReplaceableReplacements;

	private StringBuffer outputBuffer = new StringBuffer();

	private int lineCount = 1;

	public String read() {
		return outputBuffer.toString();
	}

	public int getLineCount() {
		return lineCount;
	}

	/**
	 * Replaces replaceables with replacements.
	 */
	public void replaceReplaceablesByReplacements(final BufferedTokenStream tokens) {
		if (currentReplaceableReplacements != null) {
			Arrays.sort(currentReplaceableReplacements);

			for (final CobolReplacementMapping replaceableReplacement : currentReplaceableReplacements) {
				final String currentOutput = outputBuffer.toString();
				final String replacedOutput = replaceableReplacement.replace(currentOutput, tokens);

				outputBuffer = new StringBuffer();
				outputBuffer.append(replacedOutput);
			}

			int count = 1;
			String currentOutput = outputBuffer.toString();
			for (int i = 0; i < currentOutput.length(); i++) {
				if (currentOutput.charAt(i) == '\n') {
					count++;
				}
			}
			lineCount = count;
		}
	}

	public void storeReplaceablesAndReplacements(final List<ReplaceClauseContext> replaceClauses) {
		if (replaceClauses == null) {
			currentReplaceableReplacements = null;
		} else {
			final int length = replaceClauses.size();
			currentReplaceableReplacements = new CobolReplacementMapping[length];

			int i = 0;

			for (final ReplaceClauseContext replaceClause : replaceClauses) {
				final CobolReplacementMapping replaceableReplacement = new CobolReplacementMapping();

				replaceableReplacement.replaceable = replaceClause.replaceable();
				replaceableReplacement.replacement = replaceClause.replacement();

				currentReplaceableReplacements[i] = replaceableReplacement;
				i++;
			}
		}
	}

	public void write(final String text) {
		if (text != null && !text.isEmpty()) {
			outputBuffer.append(text);
			for (int i = 0; i < text.length(); i++) {
				if (text.charAt(i) == '\n') {
					lineCount++;
				}
			}
		}
	}
}
