/*
 * Copyright (C) 2017, Ulrich Wolffgang <ulrich.wolffgang@proleap.io>
 * Modifications Copyright (c) 2026 CobolScope Contributors.
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the MIT license. See the LICENSE file for details.
 */

package io.proleap.cobol.preprocessor.sub.document.impl;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Scanner;
import java.util.Stack;

import org.antlr.v4.runtime.BufferedTokenStream;
import org.antlr.v4.runtime.tree.TerminalNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.proleap.cobol.CobolPreprocessorBaseListener;
import io.proleap.cobol.CobolPreprocessorParser;
import io.proleap.cobol.CobolPreprocessorParser.CopySourceContext;
import io.proleap.cobol.CobolPreprocessorParser.ReplaceClauseContext;
import io.proleap.cobol.CobolPreprocessorParser.ReplacingPhraseContext;
import io.proleap.cobol.asg.params.CobolParserParams;
import io.proleap.cobol.preprocessor.CobolPreprocessor;
import io.proleap.cobol.preprocessor.CobolPreprocessorResult;
import io.proleap.cobol.preprocessor.CobolSourceMap;
import io.proleap.cobol.preprocessor.exception.CobolPreprocessorException;
import io.proleap.cobol.preprocessor.impl.CobolPreprocessorImpl;
import io.proleap.cobol.preprocessor.sub.CobolLine;
import io.proleap.cobol.preprocessor.sub.copybook.CobolWordCopyBookFinder;
import io.proleap.cobol.preprocessor.sub.copybook.FilenameCopyBookFinder;
import io.proleap.cobol.preprocessor.sub.copybook.LiteralCopyBookFinder;
import io.proleap.cobol.preprocessor.sub.copybook.impl.CobolWordCopyBookFinderImpl;
import io.proleap.cobol.preprocessor.sub.copybook.impl.FilenameCopyBookFinderImpl;
import io.proleap.cobol.preprocessor.sub.copybook.impl.LiteralCopyBookFinderImpl;
import io.proleap.cobol.preprocessor.sub.document.CobolDocumentParserListener;
import io.proleap.cobol.preprocessor.sub.util.TokenUtils;

/**
 * ANTLR visitor, which preprocesses a given COBOL program by executing COPY and
 * REPLACE statements and tracks exact physical-to-preprocessed source mappings.
 */
public class CobolDocumentParserListenerImpl extends CobolPreprocessorBaseListener
		implements CobolDocumentParserListener {

	private final static Logger LOG = LoggerFactory.getLogger(CobolDocumentParserListenerImpl.class);

	private final Stack<CobolDocumentContext> contexts = new Stack<CobolDocumentContext>();

	private final CobolParserParams params;

	private final BufferedTokenStream tokens;

	private final String sourceFileName;

	private final CobolSourceMap sourceMap;

	private int prepChunkStart = 1;

	private int origChunkStart = 1;

	private final int[] lineMap;

	public CobolDocumentParserListenerImpl(final CobolParserParams params, final BufferedTokenStream tokens) {
		this(params, tokens, "", new CobolSourceMap(""), null);
	}

	public CobolDocumentParserListenerImpl(final CobolParserParams params, final BufferedTokenStream tokens,
			final String sourceFileName, final CobolSourceMap sourceMap) {
		this(params, tokens, sourceFileName, sourceMap, null);
	}

	public CobolDocumentParserListenerImpl(final CobolParserParams params, final BufferedTokenStream tokens,
			final String sourceFileName, final CobolSourceMap sourceMap, final int[] lineMap) {
		this.params = params;
		this.tokens = tokens;
		this.sourceFileName = sourceFileName != null ? sourceFileName : "";
		this.sourceMap = sourceMap != null ? sourceMap : new CobolSourceMap(this.sourceFileName);
		this.sourceMap.setPrimarySourceFile(this.sourceFileName);
		this.lineMap = lineMap;

		contexts.push(new CobolDocumentContext());
	}

	public static void addCodeSegments(final CobolSourceMap sourceMap, final int prepStart, final int prepEnd,
			final int codeStart, final int codeEnd, final String sourceFile, final int[] lineMap) {
		if (prepEnd < prepStart || codeEnd < codeStart) {
			return;
		}

		if (lineMap == null || lineMap.length == 0) {
			sourceMap.addEntry(prepStart, prepEnd, sourceFile, codeStart, codeEnd);
			return;
		}

		int currPrepSegStart = prepStart;
		int currOrigSegStart = (codeStart < lineMap.length && lineMap[codeStart] > 0) ? lineMap[codeStart] : codeStart;
		int prevOrigLine = currOrigSegStart;

		for (int i = 1; i <= (prepEnd - prepStart); i++) {
			int c = codeStart + i;
			int p = prepStart + i;
			int origLine = (c < lineMap.length && lineMap[c] > 0) ? lineMap[c] : c;

			if (origLine != prevOrigLine + 1) {
				sourceMap.addEntry(currPrepSegStart, p - 1, sourceFile, currOrigSegStart, prevOrigLine);
				currPrepSegStart = p;
				currOrigSegStart = origLine;
			}
			prevOrigLine = origLine;
		}

		sourceMap.addEntry(currPrepSegStart, prepEnd, sourceFile, currOrigSegStart, prevOrigLine);
	}

	@Override
	public CobolSourceMap getSourceMap() {
		return sourceMap;
	}

	protected String buildLines(final String text, final String linePrefix) {
		final StringBuffer sb = new StringBuffer(text.length());
		final Scanner scanner = new Scanner(text);
		boolean firstLine = true;

		while (scanner.hasNextLine()) {
			if (!firstLine) {
				sb.append(CobolPreprocessor.NEWLINE);
			}

			final String line = scanner.nextLine();
			final String trimmedLine = line.trim();
			final String prefixedLine = linePrefix + CobolPreprocessor.WS + trimmedLine;
			final String suffixedLine = prefixedLine.replaceAll("(?i)(end-exec)",
					"$1 " + CobolPreprocessor.EXEC_END_TAG);

			sb.append(suffixedLine);
			firstLine = false;
		}

		scanner.close();
		return sb.toString();
	}

	@Override
	public CobolDocumentContext context() {
		return contexts.peek();
	}

	protected CobolWordCopyBookFinder createCobolWordCopyBookFinder() {
		return new CobolWordCopyBookFinderImpl();
	}

	protected FilenameCopyBookFinder createFilenameCopyBookFinder() {
		return new FilenameCopyBookFinderImpl();
	}

	protected LiteralCopyBookFinder createLiteralCopyBookFinder() {
		return new LiteralCopyBookFinderImpl();
	}

	@Override
	public void enterCompilerOptions(final CobolPreprocessorParser.CompilerOptionsContext ctx) {
		push();
	}

	@Override
	public void enterCopyStatement(final CobolPreprocessorParser.CopyStatementContext ctx) {
		if (contexts.size() == 1) {
			int prepCopyStart = context().getLineCount();
			int origCopyStart = ctx.getStart() != null ? ctx.getStart().getLine() : origChunkStart;
			if (prepCopyStart > prepChunkStart && origCopyStart >= origChunkStart) {
				addCodeSegments(sourceMap, prepChunkStart, prepCopyStart - 1, origChunkStart, origCopyStart - 1, sourceFileName, lineMap);
			}
		}

		push();
	}

	@Override
	public void enterEjectStatement(final CobolPreprocessorParser.EjectStatementContext ctx) {
		push();
	}

	@Override
	public void enterExecCicsStatement(final CobolPreprocessorParser.ExecCicsStatementContext ctx) {
		push();
	}

	@Override
	public void enterExecSqlImsStatement(final CobolPreprocessorParser.ExecSqlImsStatementContext ctx) {
		push();
	}

	@Override
	public void enterExecSqlStatement(final CobolPreprocessorParser.ExecSqlStatementContext ctx) {
		push();
	}

	@Override
	public void enterReplaceArea(final CobolPreprocessorParser.ReplaceAreaContext ctx) {
		push();
	}

	@Override
	public void enterReplaceByStatement(final CobolPreprocessorParser.ReplaceByStatementContext ctx) {
		push();
	}

	@Override
	public void enterReplaceOffStatement(final CobolPreprocessorParser.ReplaceOffStatementContext ctx) {
		push();
	}

	@Override
	public void enterSkipStatement(final CobolPreprocessorParser.SkipStatementContext ctx) {
		push();
	}

	@Override
	public void enterTitleStatement(final CobolPreprocessorParser.TitleStatementContext ctx) {
		push();
	}

	@Override
	public void exitCompilerOptions(final CobolPreprocessorParser.CompilerOptionsContext ctx) {
		pop();
	}

	@Override
	public void exitCopyStatement(final CobolPreprocessorParser.CopyStatementContext ctx) {
		pop();
		push();

		/*
		 * replacement phrase
		 */
		for (final ReplacingPhraseContext replacingPhrase : ctx.replacingPhrase()) {
			context().storeReplaceablesAndReplacements(replacingPhrase.replaceClause());
		}

		/*
		 * copy the copy book
		 */
		final CopySourceContext copySource = ctx.copySource();
		final File copyBook = findCopyBook(copySource, params);
		String copyBookContent = null;
		CobolSourceMap childSourceMap = null;

		if (copyBook == null) {
			throw new CobolPreprocessorException("Could not find copy book " + copySource.getText()
					+ " in directory of COBOL input file or copy books param object.");
		} else {
			try {
				final CobolPreprocessorResult childResult = new CobolPreprocessorImpl().processWithSourceMap(copyBook, params);
				copyBookContent = childResult.code;
				childSourceMap = childResult.sourceMap;
			} catch (final IOException e) {
				copyBookContent = null;
				LOG.warn(e.getMessage());
			}
		}

		if (copyBookContent != null) {
			context().write(copyBookContent);
			context().replaceReplaceablesByReplacements(tokens);
		}

		final String content = context().read();
		pop();

		if (contexts.size() == 1) {
			int prepChildStart = context().getLineCount();
			int childLines = 0;
			if (content != null && !content.isEmpty()) {
				childLines = 1;
				for (int i = 0; i < content.length(); i++) {
					if (content.charAt(i) == '\n') childLines++;
				}
			}

			if (childSourceMap != null && !childSourceMap.isEmpty()) {
				sourceMap.spliceChild(prepChildStart, childSourceMap);
			} else if (copyBook != null && childLines > 0) {
				sourceMap.addEntry(prepChildStart, prepChildStart + childLines - 1, copyBook.getName(), 1, childLines);
			}

			context().write(content);

			prepChunkStart = prepChildStart + childLines;
			int origCopyStop = ctx.getStop() != null ? ctx.getStop().getLine() : (ctx.getStart() != null ? ctx.getStart().getLine() : origChunkStart);
			origChunkStart = origCopyStop + 1;
		} else {
			context().write(content);
		}
	}

	@Override
	public void exitStartRule(final CobolPreprocessorParser.StartRuleContext ctx) {
		if (contexts.size() == 1) {
			int totalPrepLines = context().getLineCount();
			if (totalPrepLines >= prepChunkStart) {
				int count = totalPrepLines - prepChunkStart;
				addCodeSegments(sourceMap, prepChunkStart, totalPrepLines, origChunkStart, origChunkStart + count, sourceFileName, lineMap);
			}
		}
	}

	@Override
	public void exitEjectStatement(final CobolPreprocessorParser.EjectStatementContext ctx) {
		pop();
	}

	@Override
	public void exitExecCicsStatement(final CobolPreprocessorParser.ExecCicsStatementContext ctx) {
		pop();
		push();

		final String text = TokenUtils.getTextIncludingHiddenTokens(ctx, tokens);
		final String linePrefix = CobolLine.createBlankSequenceArea(params.getFormat())
				+ CobolPreprocessor.EXEC_CICS_TAG;
		final String lines = buildLines(text, linePrefix);

		context().write(lines);

		final String content = context().read();
		pop();

		context().write(content);
	}

	@Override
	public void exitExecSqlImsStatement(final CobolPreprocessorParser.ExecSqlImsStatementContext ctx) {
		pop();
		push();

		final String text = TokenUtils.getTextIncludingHiddenTokens(ctx, tokens);
		final String linePrefix = CobolLine.createBlankSequenceArea(params.getFormat())
				+ CobolPreprocessor.EXEC_SQLIMS_TAG;
		final String lines = buildLines(text, linePrefix);

		context().write(lines);

		final String content = context().read();
		pop();

		context().write(content);
	}

	@Override
	public void exitExecSqlStatement(final CobolPreprocessorParser.ExecSqlStatementContext ctx) {
		pop();
		push();

		final String text = TokenUtils.getTextIncludingHiddenTokens(ctx, tokens);
		final String linePrefix = CobolLine.createBlankSequenceArea(params.getFormat())
				+ CobolPreprocessor.EXEC_SQL_TAG;
		final String lines = buildLines(text, linePrefix);

		context().write(lines);

		final String content = context().read();
		pop();

		context().write(content);
	}

	@Override
	public void exitReplaceArea(final CobolPreprocessorParser.ReplaceAreaContext ctx) {
		final List<ReplaceClauseContext> replaceClauses = ctx.replaceByStatement().replaceClause();
		context().storeReplaceablesAndReplacements(replaceClauses);

		context().replaceReplaceablesByReplacements(tokens);
		final String content = context().read();

		pop();
		context().write(content);
	}

	@Override
	public void exitReplaceByStatement(final CobolPreprocessorParser.ReplaceByStatementContext ctx) {
		pop();
	}

	@Override
	public void exitReplaceOffStatement(final CobolPreprocessorParser.ReplaceOffStatementContext ctx) {
		pop();
	}

	@Override
	public void exitSkipStatement(final CobolPreprocessorParser.SkipStatementContext ctx) {
		pop();
	}

	@Override
	public void exitTitleStatement(final CobolPreprocessorParser.TitleStatementContext ctx) {
		pop();
	}

	protected File findCopyBook(final CopySourceContext copySource, final CobolParserParams params) {
		final File result;

		if (copySource.cobolWord() != null) {
			result = createCobolWordCopyBookFinder().findCopyBook(params, copySource.cobolWord());
		} else if (copySource.literal() != null) {
			result = createLiteralCopyBookFinder().findCopyBook(params, copySource.literal());
		} else if (copySource.filename() != null) {
			result = createFilenameCopyBookFinder().findCopyBook(params, copySource.filename());
		} else {
			LOG.warn("unknown copy book reference type {}", copySource);
			result = null;
		}

		return result;
	}

	protected String getCopyBookContent(final CopySourceContext copySource, final CobolParserParams params) {
		final File copyBook = findCopyBook(copySource, params);
		String result;

		if (copyBook == null) {
			throw new CobolPreprocessorException("Could not find copy book " + copySource.getText()
					+ " in directory of COBOL input file or copy books param object.");
		} else {
			try {
				result = new CobolPreprocessorImpl().process(copyBook, params);
			} catch (final IOException e) {
				result = null;
				LOG.warn(e.getMessage());
			}
		}

		return result;
	}

	protected CobolDocumentContext pop() {
		return contexts.pop();
	}

	protected CobolDocumentContext push() {
		return contexts.push(new CobolDocumentContext());
	}

	@Override
	public void visitTerminal(final TerminalNode node) {
		final int tokPos = node.getSourceInterval().a;
		context().write(TokenUtils.getHiddenTokensToLeft(tokPos, tokens));

		if (!TokenUtils.isEOF(node)) {
			final String text = node.getText();
			context().write(text);
		}
	}
}
