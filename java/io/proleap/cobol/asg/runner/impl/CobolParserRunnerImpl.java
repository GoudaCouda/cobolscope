/*
 * Copyright (C) 2017, Ulrich Wolffgang <ulrich.wolffgang@proleap.io>
 * Modifications Copyright (c) 2026 CobolScope Contributors.
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the MIT license. See the LICENSE file for details.
 */

package io.proleap.cobol.asg.runner.impl;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

import org.antlr.v4.runtime.BailErrorStrategy;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.DefaultErrorStrategy;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.atn.PredictionMode;
import org.antlr.v4.runtime.misc.ParseCancellationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.proleap.cobol.CobolLexer;
import io.proleap.cobol.CobolParser;
import io.proleap.cobol.CobolParser.StartRuleContext;
import io.proleap.cobol.asg.exception.CobolParserException;
import io.proleap.cobol.asg.metamodel.CompilationUnit;
import io.proleap.cobol.asg.metamodel.Program;
import io.proleap.cobol.asg.metamodel.impl.ProgramImpl;
import io.proleap.cobol.asg.params.CobolParserParams;
import io.proleap.cobol.asg.params.impl.CobolParserParamsImpl;
import io.proleap.cobol.asg.runner.CobolParserRunner;
import io.proleap.cobol.asg.runner.ThrowingErrorListener;
import io.proleap.cobol.asg.util.FilenameUtils;
import io.proleap.cobol.asg.visitor.ParserVisitor;
import io.proleap.cobol.asg.visitor.impl.CobolCompilationUnitVisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolDataDivisionStep1VisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolDataDivisionStep2VisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolFileControlClauseVisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolFileDescriptionEntryClauseVisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolProcedureDivisionVisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolProcedureStatementVisitorImpl;
import io.proleap.cobol.asg.visitor.impl.CobolProgramUnitVisitorImpl;
import io.proleap.cobol.preprocessor.CobolPreprocessor.CobolSourceFormatEnum;
import io.proleap.cobol.preprocessor.CobolPreprocessorResult;
import io.proleap.cobol.preprocessor.CobolSourceMap;
import io.proleap.cobol.preprocessor.CobolSourceMapContext;
import io.proleap.cobol.preprocessor.impl.CobolPreprocessorImpl;

public class CobolParserRunnerImpl implements CobolParserRunner {

	private final static Logger LOG = LoggerFactory.getLogger(CobolParserRunnerImpl.class);

	protected void analyze(final Program program) {
		final boolean profile = "true".equalsIgnoreCase(System.getProperty("cobolscope.profile", System.getenv("COBOLSCOPE_PROFILE")));
		final long tStart = System.nanoTime();

		final long t0 = System.nanoTime();
		analyzeProgramUnits(program);
		final long tUnits = System.nanoTime() - t0;

		final long t1 = System.nanoTime();
		analyzeDataDivisionsStep1(program);
		final long tData1 = System.nanoTime() - t1;

		final long t2 = System.nanoTime();
		analyzeDataDivisionsStep2(program);
		final long tData2 = System.nanoTime() - t2;

		final long t3 = System.nanoTime();
		analyzeFileControlClauses(program);
		final long tFc = System.nanoTime() - t3;

		final long t4 = System.nanoTime();
		analyzeFileDescriptionEntriesClauses(program);
		final long tFd = System.nanoTime() - t4;

		final long t5 = System.nanoTime();
		analyzeProcedureDivisions(program);
		final long tProc = System.nanoTime() - t5;

		final long t6 = System.nanoTime();
		analyzeProcedureStatements(program);
		final long tStmt = System.nanoTime() - t6;

		if (profile) {
			final long tTotal = System.nanoTime() - tStart;
			System.err.printf("[PROFILE-ASG] Total: %.2f ms | units: %.2f ms | data1: %.2f ms | data2: %.2f ms | fc: %.2f ms | fd: %.2f ms | proc: %.2f ms | stmt: %.2f ms%n",
					tTotal / 1e6, tUnits / 1e6, tData1 / 1e6, tData2 / 1e6, tFc / 1e6, tFd / 1e6, tProc / 1e6, tStmt / 1e6);
		}
	}

	@Override
	public Program analyzeCode(final String cobolCode, final String compilationUnitName, final CobolParserParams params)
			throws IOException {
		final Program program = new ProgramImpl();

		parseCode(cobolCode, compilationUnitName, program, params);
		analyze(program);

		return program;
	}

	protected void analyzeDataDivisionsStep1(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolDataDivisionStep1VisitorImpl(program);

			LOG.info("Analyzing data divisions of compilation unit {} in step 1.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected void analyzeDataDivisionsStep2(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolDataDivisionStep2VisitorImpl(program);

			LOG.info("Analyzing data divisions of compilation unit {} in step 2.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	@Override
	public Program analyzeFile(final File inputFile, final CobolParserParams params) throws IOException {
		final boolean profile = "true".equalsIgnoreCase(System.getProperty("cobolscope.profile", System.getenv("COBOLSCOPE_PROFILE")));
		final long tStart = System.nanoTime();

		final Program program = new ProgramImpl();

		final long tParse0 = System.nanoTime();
		parseFile(inputFile, program, params);
		final long tParse = System.nanoTime() - tParse0;

		final long tAnalyze0 = System.nanoTime();
		analyze(program);
		final long tAnalyze = System.nanoTime() - tAnalyze0;

		if (profile) {
			final long tTotal = System.nanoTime() - tStart;
			System.err.printf("[PROFILE-FILE] File: %s | Total: %.2f ms | Parse+Preprocess: %.2f ms | ASG Analyze: %.2f ms%n",
					inputFile.getName(), tTotal / 1e6, tParse / 1e6, tAnalyze / 1e6);
		}

		return program;
	}

	@Override
	public Program analyzeFile(final File cobolFile, final CobolSourceFormatEnum format) throws IOException {
		final CobolParserParams params = createDefaultParams(format, cobolFile);
		return analyzeFile(cobolFile, params);
	}

	protected void analyzeFileControlClauses(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolFileControlClauseVisitorImpl(program);

			LOG.info("Analyzing file control clauses of compilation unit {}.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected void analyzeFileDescriptionEntriesClauses(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolFileDescriptionEntryClauseVisitorImpl(program);

			LOG.info("Analyzing file description entries of compilation unit {}.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected void analyzeProcedureDivisions(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolProcedureDivisionVisitorImpl(program);

			LOG.info("Analyzing procedure divisions of compilation unit {}.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected void analyzeProcedureStatements(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolProcedureStatementVisitorImpl(program);

			LOG.info("Analyzing statements of compilation unit {}.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected void analyzeProgramUnits(final Program program) {
		for (final CompilationUnit compilationUnit : program.getCompilationUnits()) {
			final ParserVisitor visitor = new CobolProgramUnitVisitorImpl(compilationUnit);

			LOG.info("Analyzing program units of compilation unit {}.", compilationUnit.getName());
			visitor.visit(compilationUnit.getCtx());
		}
	}

	protected String capitalize(final String line) {
		return Character.toUpperCase(line.charAt(0)) + line.substring(1);
	}

	protected CobolParserParams createDefaultParams() {
		return new CobolParserParamsImpl();
	}

	protected CobolParserParams createDefaultParams(final CobolSourceFormatEnum format, final File cobolFile) {
		final CobolParserParams result = createDefaultParams();
		result.setFormat(format);

		final File copyBooksDirectory = cobolFile.getParentFile();
		result.setCopyBookDirectories(Arrays.asList(copyBooksDirectory));

		return result;
	}

	protected String getCompilationUnitName(final File cobolFile) {
		return capitalize(FilenameUtils.removeExtension(cobolFile.getName()));
	}

	protected void parseCode(final String cobolCode, final String compilationUnitName, final Program program,
			final CobolParserParams params) throws IOException {
		LOG.info("Parsing compilation unit {}.", compilationUnitName);

		// preprocess input stream
		final CobolSourceMap sourceMap = new CobolSourceMap("");
		final CobolPreprocessorResult prepResult = new CobolPreprocessorImpl().processInternal(cobolCode, params, "", sourceMap);
		CobolSourceMapContext.set(prepResult.sourceMap);
		CobolSourceMapContext.register(compilationUnitName, prepResult.sourceMap);

		parsePreprocessInput(prepResult.code, compilationUnitName, program, params);
	}

	protected void parseFile(final File cobolFile, final Program program, final CobolParserParams params)
			throws IOException {
		if (!cobolFile.isFile()) {
			throw new CobolParserException("Could not find file " + cobolFile.getAbsolutePath());
		} else {
			// determine the copy book name
			final String compilationUnitName = getCompilationUnitName(cobolFile);

			LOG.info("Parsing compilation unit {}.", compilationUnitName);

			// preprocess input stream
			final CobolPreprocessorResult prepResult = new CobolPreprocessorImpl().processWithSourceMap(cobolFile, params);
			CobolSourceMapContext.set(prepResult.sourceMap);
			CobolSourceMapContext.register(compilationUnitName, prepResult.sourceMap);
			CobolSourceMapContext.register(cobolFile.getAbsolutePath(), prepResult.sourceMap);
			CobolSourceMapContext.register(cobolFile.getName(), prepResult.sourceMap);

			parsePreprocessInput(prepResult.code, compilationUnitName, program, params);
		}
	}

	protected void parsePreprocessInput(final String preProcessedInput, final String compilationUnitName,
			final Program program, final CobolParserParams params) throws IOException {
		final boolean profile = "true".equalsIgnoreCase(System.getProperty("cobolscope.profile", System.getenv("COBOLSCOPE_PROFILE")));
		final long t0 = System.nanoTime();

		// run the lexer
		final CobolLexer lexer = new CobolLexer(CharStreams.fromString(preProcessedInput));

		if (!params.getIgnoreSyntaxErrors()) {
			// register an error listener, so that preprocessing stops on errors
			lexer.removeErrorListeners();
			lexer.addErrorListener(new ThrowingErrorListener());
		}

		// get a list of matched tokens
		final CommonTokenStream tokens = new CommonTokenStream(lexer);

		// pass the tokens to the parser
		final CobolParser parser = new CobolParser(tokens);

		final long tParse0 = System.nanoTime();
		StartRuleContext ctx = null;

		// Stage 1: Fast SLL prediction mode with BailErrorStrategy
		try {
			parser.getInterpreter().setPredictionMode(PredictionMode.SLL);
			parser.removeErrorListeners();
			parser.setErrorHandler(new BailErrorStrategy());

			ctx = parser.startRule();
		} catch (final ParseCancellationException | RecognitionException ex) {
			// Fast path failed on ambiguous or invalid rule: rewind and fall back to full LL
			tokens.seek(0);
			parser.reset();
			parser.getInterpreter().setPredictionMode(PredictionMode.LL);

			if (!params.getIgnoreSyntaxErrors()) {
				parser.removeErrorListeners();
				parser.addErrorListener(new ThrowingErrorListener());
			} else {
				parser.setErrorHandler(new DefaultErrorStrategy());
			}

			ctx = parser.startRule();
		} catch (final Exception ex) {
			// Any unexpected parser exception during SLL: rewind and fall back to LL
			tokens.seek(0);
			parser.reset();
			parser.getInterpreter().setPredictionMode(PredictionMode.LL);

			if (!params.getIgnoreSyntaxErrors()) {
				parser.removeErrorListeners();
				parser.addErrorListener(new ThrowingErrorListener());
			} else {
				parser.setErrorHandler(new DefaultErrorStrategy());
			}

			ctx = parser.startRule();
		}

		final long tParse = System.nanoTime() - tParse0;

		final long tSplit0 = System.nanoTime();
		final List<String> lines = splitLines(preProcessedInput);
		final long tSplit = System.nanoTime() - tSplit0;

		final long tCu0 = System.nanoTime();
		final ParserVisitor visitor = new CobolCompilationUnitVisitorImpl(compilationUnitName, lines, tokens, program);
		visitor.visit(ctx);
		final long tCu = System.nanoTime() - tCu0;

		if (profile) {
			final long tTotal = System.nanoTime() - t0;
			System.err.printf("[PROFILE-PARSE] Total: %.2f ms | ANTLR parse: %.2f ms | splitLines: %.2f ms | CU Visitor: %.2f ms%n",
					tTotal / 1e6, tParse / 1e6, tSplit / 1e6, tCu / 1e6);
		}
	}

	protected List<String> splitLines(final String preProcessedInput) {
		if (preProcessedInput == null || preProcessedInput.isEmpty()) {
			return new ArrayList<String>();
		}

		final List<String> result = new ArrayList<String>();
		final int len = preProcessedInput.length();
		int start = 0;

		for (int i = 0; i < len; i++) {
			final char c = preProcessedInput.charAt(i);
			if (c == '\r') {
				result.add(preProcessedInput.substring(start, i));
				if (i + 1 < len && preProcessedInput.charAt(i + 1) == '\n') {
					i++; // consume \n if CRLF
				}
				start = i + 1;
			} else if (c == '\n') {
				result.add(preProcessedInput.substring(start, i));
				start = i + 1;
			}
		}

		result.add(preProcessedInput.substring(start));
		return result;
	}
}
