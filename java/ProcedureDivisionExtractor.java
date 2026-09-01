import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntry;
import io.proleap.cobol.asg.metamodel.procedure.Paragraph;
import io.proleap.cobol.asg.metamodel.procedure.ProcedureDivision;
import io.proleap.cobol.asg.metamodel.procedure.Section;
import io.proleap.cobol.asg.metamodel.procedure.Statement;

import java.util.*;

/**
 * Extracts Procedure Division sections and paragraphs, collecting all nested statements
 * and resolving the complete Control Flow Graph (successors, calledBy, terminal, fallthrough).
 */
public class ProcedureDivisionExtractor {

    public static void extractProcedureDivision(
            ProcedureDivision procDiv,
            IrModel.ProgramModelDto model,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        if (procDiv == null) return;

        // Extract Standard Sections
        if (procDiv.getSections() != null) {
            for (Section sec : procDiv.getSections()) {
                IrModel.SectionDto secDto = new IrModel.SectionDto();
                secDto.name = sec.getName();
                secDto.location = new IrModel.SourceLocationDto(sec.getCtx());

                if (sec.getStatements() != null) {
                    for (Statement stmt : sec.getStatements()) {
                        IrModel.StatementDto stmtDto = StatementMapper.mapStatement(stmt, entryToIdMap, nameToIdMap);
                        if (stmtDto != null) secDto.statements.add(stmtDto);
                    }
                }

                if (sec.getParagraphs() != null) {
                    for (Paragraph p : sec.getParagraphs()) {
                        secDto.paragraphNames.add(p.getName());
                    }
                }
                model.sections.add(secDto);
            }
        }

        // Extract Declaratives Sections
        if (procDiv.getDeclaratives() != null) {
            try {
                Object decls = procDiv.getDeclaratives();
                java.lang.reflect.Method getDeclsM = decls.getClass().getMethod("getDeclaratives");
                List<?> declList = (List<?>) getDeclsM.invoke(decls);
                if (declList != null) {
                    for (Object decl : declList) {
                        IrModel.SectionDto secDto = new IrModel.SectionDto();
                        String secName = null;
                        try {
                            java.lang.reflect.Method getHeaderM = decl.getClass().getMethod("getDeclarativeSectionHeader");
                            Object header = getHeaderM.invoke(decl);
                            if (header != null) {
                                secName = (String) header.getClass().getMethod("getName").invoke(header);
                            }
                        } catch (Exception ignored) {}
                        if (secName == null) {
                            try {
                                java.lang.reflect.Method getNameM = decl.getClass().getMethod("getName");
                                secName = (String) getNameM.invoke(decl);
                            } catch (Exception ignored) {}
                        }
                        if (secName == null) {
                            secName = "DECLARATIVES-SECTION";
                        }
                        secDto.name = secName;
                        try {
                            java.lang.reflect.Method getCtxM = decl.getClass().getMethod("getCtx");
                            org.antlr.v4.runtime.ParserRuleContext ctx = (org.antlr.v4.runtime.ParserRuleContext) getCtxM.invoke(decl);
                            secDto.location = new IrModel.SourceLocationDto(ctx);
                        } catch (Exception ignored) {}
                        try {
                            java.lang.reflect.Method getParasM = decl.getClass().getMethod("getParagraphs");
                            List<?> pList = (List<?>) getParasM.invoke(decl);
                            if (pList != null) {
                                for (Object p : pList) {
                                    secDto.paragraphNames.add((String) p.getClass().getMethod("getName").invoke(p));
                                }
                            }
                        } catch (Exception ignored) {}
                        model.sections.add(secDto);
                    }
                }
            } catch (Exception ignored) {}
        }

        // Extract all Paragraphs in explicit physical execution order
        if (procDiv.getParagraphs() != null) {
            Map<String, IrModel.ParagraphDto> paragraphMap = new LinkedHashMap<>();
            List<IrModel.ParagraphDto> pList = new ArrayList<>();

            for (Paragraph p : procDiv.getParagraphs()) {
                IrModel.ParagraphDto pDto = new IrModel.ParagraphDto();
                pDto.name = p.getName();
                pDto.location = new IrModel.SourceLocationDto(p.getCtx());
                if (p.getSection() != null) {
                    pDto.sectionParent = p.getSection().getName();
                } else {
                    for (IrModel.SectionDto sec : model.sections) {
                        if (sec.paragraphNames.contains(p.getName())) {
                            pDto.sectionParent = sec.name;
                            break;
                        }
                    }
                    if (pDto.sectionParent == null && !model.sections.isEmpty()) {
                        if (pDto.location != null && pDto.location.startLine > 0) {
                            for (IrModel.SectionDto sec : model.sections) {
                                if (sec.location != null && sec.location.startLine > 0 && sec.location.endLine > 0) {
                                    if (pDto.location.startLine >= sec.location.startLine && pDto.location.endLine <= sec.location.endLine) {
                                        pDto.sectionParent = sec.name;
                                        if (!sec.paragraphNames.contains(p.getName())) {
                                            sec.paragraphNames.add(p.getName());
                                        }
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }

                if (p.getStatements() != null) {
                    for (Statement stmt : p.getStatements()) {
                        IrModel.StatementDto stmtDto = StatementMapper.mapStatement(stmt, entryToIdMap, nameToIdMap);
                        if (stmtDto != null) {
                            pDto.statements.add(stmtDto);
                        }
                    }
                }

                // Phase 1A: Collect ALL nested statements recursively (including inside IF/EVALUATE/PERFORM)
                List<IrModel.StatementDto> allStmts = new ArrayList<>();
                for (IrModel.StatementDto s : pDto.statements) {
                    collectAllNestedStatements(s, allStmts);
                }

                // Phase 1B: Extract successors and terminal status across all nested statements
                for (IrModel.StatementDto stmtDto : allStmts) {
                    if ("PERFORM".equals(stmtDto.type) && stmtDto.target != null) {
                        if (!pDto.successors.contains(stmtDto.target)) {
                            pDto.successors.add(stmtDto.target);
                        }
                    } else if ("GO_TO".equals(stmtDto.type)) {
                        if (stmtDto.target != null && !pDto.successors.contains(stmtDto.target)) {
                            pDto.successors.add(stmtDto.target);
                        }
                        if (stmtDto.dependingOn != null) {
                            String beforeDep = stmtDto.dependingOn.split("(?i)DEPENDING")[0];
                            String[] tokens = beforeDep.trim().split("[\\s,]+");
                            for (String token : tokens) {
                                if (!token.isEmpty() && !pDto.successors.contains(token)) {
                                    pDto.successors.add(token);
                                }
                            }
                        }
                    }
                }

                // Terminal status check
                if (!pDto.statements.isEmpty()) {
                    IrModel.StatementDto lastTopStmt = pDto.statements.get(pDto.statements.size() - 1);
                    if ("GOBACK".equals(lastTopStmt.type) || "STOP".equals(lastTopStmt.type)) {
                        pDto.isTerminal = true;
                    }
                }

                pList.add(pDto);
                if (p.getName() != null) {
                    paragraphMap.put(p.getName().toUpperCase(), pDto);
                }
            }

            // Phase 2: Compute fallthroughSuccessor & bidirectional calledBy links across all paragraphs
            for (int i = 0; i < pList.size(); i++) {
                IrModel.ParagraphDto caller = pList.get(i);

                // Compute fallthrough successor
                if (i + 1 < pList.size()) {
                    boolean isTerminalOrGoto = Boolean.TRUE.equals(caller.isTerminal);
                    if (!caller.statements.isEmpty()) {
                        IrModel.StatementDto lastStmt = caller.statements.get(caller.statements.size() - 1);
                        if ("GO_TO".equals(lastStmt.type) && lastStmt.target != null && lastStmt.dependingOn == null) {
                            isTerminalOrGoto = true;
                        }
                    }
                    if (!isTerminalOrGoto) {
                        caller.fallthroughSuccessor = pList.get(i + 1).name;
                    }
                }

                // Compute calledBy across all nested statements in caller
                List<IrModel.StatementDto> allCallerStmts = new ArrayList<>();
                for (IrModel.StatementDto s : caller.statements) {
                    collectAllNestedStatements(s, allCallerStmts);
                }

                for (IrModel.StatementDto stmt : allCallerStmts) {
                    if ("PERFORM".equals(stmt.type) && stmt.target != null) {
                        String target = stmt.target;
                        String thru = stmt.thru;

                        if (thru != null) {
                            boolean inRange = false;
                            for (IrModel.ParagraphDto candidate : pList) {
                                if (candidate.name.equalsIgnoreCase(target)) {
                                    inRange = true;
                                }
                                if (inRange) {
                                    if (!candidate.calledBy.contains(caller.name)) {
                                        candidate.calledBy.add(caller.name);
                                    }
                                    if (candidate.name.equalsIgnoreCase(thru)) {
                                        break;
                                    }
                                }
                            }
                        } else if (paragraphMap.containsKey(target.toUpperCase())) {
                            IrModel.ParagraphDto targetDto = paragraphMap.get(target.toUpperCase());
                            if (!targetDto.calledBy.contains(caller.name)) {
                                targetDto.calledBy.add(caller.name);
                            }
                        }
                    } else if ("GO_TO".equals(stmt.type)) {
                        List<String> targets = new ArrayList<>();
                        if (stmt.target != null) {
                            targets.add(stmt.target);
                        }
                        if (stmt.dependingOn != null) {
                            String beforeDep = stmt.dependingOn.split("(?i)DEPENDING")[0];
                            String[] tokens = beforeDep.trim().split("[\\s,]+");
                            for (String token : tokens) {
                                if (!token.isEmpty() && paragraphMap.containsKey(token.toUpperCase())) {
                                    targets.add(token);
                                }
                            }
                        }
                        for (String target : targets) {
                            if (paragraphMap.containsKey(target.toUpperCase())) {
                                IrModel.ParagraphDto targetDto = paragraphMap.get(target.toUpperCase());
                                if (!targetDto.calledBy.contains(caller.name)) {
                                    targetDto.calledBy.add(caller.name);
                                }
                            }
                        }
                    }
                }
            }

            model.paragraphs.addAll(pList);
        }
    }

    public static void collectAllNestedStatements(IrModel.StatementDto stmt, List<IrModel.StatementDto> acc) {
        if (stmt == null) return;
        acc.add(stmt);
        if (stmt.thenStatements != null) {
            for (IrModel.StatementDto s : stmt.thenStatements) collectAllNestedStatements(s, acc);
        }
        if (stmt.elseStatements != null) {
            for (IrModel.StatementDto s : stmt.elseStatements) collectAllNestedStatements(s, acc);
        }
        if (stmt.nestedStatements != null) {
            for (IrModel.StatementDto s : stmt.nestedStatements) collectAllNestedStatements(s, acc);
        }
        if (stmt.whenBranches != null) {
            for (IrModel.EvaluateWhenBranchDto b : stmt.whenBranches) {
                if (b.statements != null) {
                    for (IrModel.StatementDto s : b.statements) collectAllNestedStatements(s, acc);
                }
            }
        }
        if (stmt.whenOtherStatements != null) {
            for (IrModel.StatementDto s : stmt.whenOtherStatements) collectAllNestedStatements(s, acc);
        }
    }
}
