import io.proleap.cobol.asg.metamodel.call.Call;
import io.proleap.cobol.asg.metamodel.call.DataDescriptionEntryCall;
import io.proleap.cobol.asg.metamodel.data.datadescription.DataDescriptionEntry;
import io.proleap.cobol.asg.metamodel.procedure.Statement;
import io.proleap.cobol.asg.metamodel.procedure.accept.AcceptStatement;
import io.proleap.cobol.asg.metamodel.procedure.add.AddStatement;
import io.proleap.cobol.asg.metamodel.procedure.call.CallStatement;
import io.proleap.cobol.asg.metamodel.procedure.close.CloseStatement;
import io.proleap.cobol.asg.metamodel.procedure.compute.ComputeStatement;
import io.proleap.cobol.asg.metamodel.procedure.delete.DeleteStatement;
import io.proleap.cobol.asg.metamodel.procedure.display.DisplayStatement;
import io.proleap.cobol.asg.metamodel.procedure.divide.DivideStatement;
import io.proleap.cobol.asg.metamodel.procedure.evaluate.EvaluateStatement;
import io.proleap.cobol.asg.metamodel.procedure.evaluate.When;
import io.proleap.cobol.asg.metamodel.procedure.evaluate.WhenPhrase;
import io.proleap.cobol.asg.metamodel.procedure.execcics.ExecCicsStatement;
import io.proleap.cobol.asg.metamodel.procedure.execsql.ExecSqlStatement;
import io.proleap.cobol.asg.metamodel.procedure.execsqlims.ExecSqlImsStatement;
import io.proleap.cobol.asg.metamodel.procedure.exit.ExitStatement;
import io.proleap.cobol.asg.metamodel.procedure.goback.GobackStatement;
import io.proleap.cobol.asg.metamodel.procedure.gotostmt.GoToStatement;
import io.proleap.cobol.asg.metamodel.procedure.ifstmt.IfStatement;
import io.proleap.cobol.asg.metamodel.procedure.initialize.InitializeStatement;
import io.proleap.cobol.asg.metamodel.procedure.inspect.InspectStatement;
import io.proleap.cobol.asg.metamodel.procedure.move.MoveStatement;
import io.proleap.cobol.asg.metamodel.procedure.multiply.MultiplyStatement;
import io.proleap.cobol.asg.metamodel.procedure.open.OpenStatement;
import io.proleap.cobol.asg.metamodel.procedure.perform.PerformInlineStatement;
import io.proleap.cobol.asg.metamodel.procedure.perform.PerformProcedureStatement;
import io.proleap.cobol.asg.metamodel.procedure.perform.PerformStatement;
import io.proleap.cobol.asg.metamodel.procedure.perform.PerformType;
import io.proleap.cobol.asg.metamodel.procedure.read.ReadStatement;
import io.proleap.cobol.asg.metamodel.procedure.rewrite.RewriteStatement;
import io.proleap.cobol.asg.metamodel.procedure.search.SearchStatement;
import io.proleap.cobol.asg.metamodel.procedure.set.SetStatement;
import io.proleap.cobol.asg.metamodel.procedure.start.StartStatement;
import io.proleap.cobol.asg.metamodel.procedure.stop.StopStatement;
import io.proleap.cobol.asg.metamodel.procedure.string.StringStatement;
import io.proleap.cobol.asg.metamodel.procedure.subtract.SubtractStatement;
import io.proleap.cobol.asg.metamodel.procedure.unstring.UnstringStatement;
import io.proleap.cobol.asg.metamodel.procedure.write.WriteStatement;

import java.util.*;

/**
 * Maps ProLeap ASG Statements into Canonical IR StatementDto representations,
 * resolving source and target field IDs.
 */
public class StatementMapper {

    public static IrModel.StatementDto mapStatement(
            Statement stmt,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        if (stmt == null) return null;

        IrModel.StatementDto dto = new IrModel.StatementDto();
        dto.location = new IrModel.SourceLocationDto(stmt.getCtx());
        dto.type = stmt.getStatementType() != null ? stmt.getStatementType().toString() : "UNKNOWN";
        if (stmt.getCtx() != null) {
            dto.rawText = CobolTextCleaner.cleanContextText(stmt.getCtx());
        }

        // 1. MOVE Statement
        if (stmt instanceof MoveStatement) {
            MoveStatement move = (MoveStatement) stmt;
            dto.type = "MOVE";
            if (move.getMoveToStatement() != null) {
                var moveTo = move.getMoveToStatement();
                if (moveTo.getSendingArea() != null && moveTo.getSendingArea().getCtx() != null) {
                    dto.fromExpr = CobolTextCleaner.cleanContextText(moveTo.getSendingArea().getCtx());
                    addResolvedFieldIds(dto.fromExpr, nameToIdMap, dto.sourceFieldIds);
                }
                List<String> targets = new ArrayList<>();
                if (moveTo.getReceivingAreaCalls() != null) {
                    for (Call call : moveTo.getReceivingAreaCalls()) {
                        String name = call.getName() != null ? call.getName() : CobolTextCleaner.cleanContextText(call.getCtx());
                        targets.add(name);
                        String fid = resolveFieldId(call, entryToIdMap, nameToIdMap);
                        if (fid != null && !dto.targetFieldIds.contains(fid)) {
                            dto.targetFieldIds.add(fid);
                        }
                    }
                }
                dto.toTargets = targets;
            } else if (move.getMoveCorrespondingToStatement() != null) {
                dto.isCorresponding = true;
                if (move.getMoveCorrespondingToStatement().getCtx() != null) {
                    dto.correspondingText = CobolTextCleaner.cleanContextText(move.getMoveCorrespondingToStatement().getCtx());
                    addResolvedFieldIds(dto.correspondingText, nameToIdMap, dto.sourceFieldIds);
                }
            }
        }
        // 2. PERFORM Statement
        else if (stmt instanceof PerformStatement) {
            PerformStatement perf = (PerformStatement) stmt;
            dto.type = "PERFORM";

            if (perf.getPerformProcedureStatement() != null) {
                PerformProcedureStatement proc = perf.getPerformProcedureStatement();
                List<String> targets = new ArrayList<>();
                if (proc.getCalls() != null) {
                    for (Call c : proc.getCalls()) {
                        targets.add(c.getName() != null ? c.getName() : CobolTextCleaner.cleanContextText(c.getCtx()));
                    }
                }
                if (!targets.isEmpty()) {
                    dto.target = targets.get(0);
                    if (targets.size() > 1) {
                        dto.thru = targets.get(targets.size() - 1);
                    }
                }
                if (proc.getPerformType() != null) {
                    mapPerformType(proc.getPerformType(), dto, nameToIdMap);
                }
            } else if (perf.getPerformInlineStatement() != null) {
                PerformInlineStatement inline = perf.getPerformInlineStatement();
                dto.isInline = true;
                if (inline.getPerformType() != null) {
                    mapPerformType(inline.getPerformType(), dto, nameToIdMap);
                }
                if (inline.getStatements() != null && !inline.getStatements().isEmpty()) {
                    dto.nestedStatements = new ArrayList<>();
                    for (Statement nested : inline.getStatements()) {
                        IrModel.StatementDto nestedDto = mapStatement(nested, entryToIdMap, nameToIdMap);
                        if (nestedDto != null) dto.nestedStatements.add(nestedDto);
                    }
                }
            }
        }
        // 3. IF Statement
        else if (stmt instanceof IfStatement) {
            IfStatement ifStmt = (IfStatement) stmt;
            dto.type = "IF";
            if (ifStmt.getCondition() != null && ifStmt.getCondition().getCtx() != null) {
                dto.condition = CobolTextCleaner.cleanContextText(ifStmt.getCondition().getCtx());
                addResolvedFieldIds(dto.condition, nameToIdMap, dto.sourceFieldIds);
            }
            if (ifStmt.getThen() != null && ifStmt.getThen().getStatements() != null) {
                dto.thenStatements = new ArrayList<>();
                for (Statement thenStmt : ifStmt.getThen().getStatements()) {
                    IrModel.StatementDto s = mapStatement(thenStmt, entryToIdMap, nameToIdMap);
                    if (s != null) dto.thenStatements.add(s);
                }
            }
            if (ifStmt.getElse() != null && ifStmt.getElse().getStatements() != null) {
                dto.elseStatements = new ArrayList<>();
                for (Statement elseStmt : ifStmt.getElse().getStatements()) {
                    IrModel.StatementDto s = mapStatement(elseStmt, entryToIdMap, nameToIdMap);
                    if (s != null) dto.elseStatements.add(s);
                }
            }
        }
        // 4. EVALUATE Statement
        else if (stmt instanceof EvaluateStatement) {
            EvaluateStatement eval = (EvaluateStatement) stmt;
            dto.type = "EVALUATE";
            List<String> subjects = new ArrayList<>();
            if (eval.getSelect() != null && eval.getSelect().getCtx() != null) {
                String subText = CobolTextCleaner.cleanContextText(eval.getSelect().getCtx());
                subjects.add(subText);
                addResolvedFieldIds(subText, nameToIdMap, dto.sourceFieldIds);
            }
            if (eval.getAlsoSelects() != null) {
                for (var also : eval.getAlsoSelects()) {
                    if (also.getCtx() != null) {
                        String alsoText = CobolTextCleaner.cleanContextText(also.getCtx());
                        subjects.add(alsoText);
                        addResolvedFieldIds(alsoText, nameToIdMap, dto.sourceFieldIds);
                    }
                }
            }
            dto.subjects = subjects;

            if (eval.getWhenPhrases() != null) {
                dto.whenBranches = new ArrayList<>();
                for (WhenPhrase wp : eval.getWhenPhrases()) {
                    IrModel.EvaluateWhenBranchDto branch = new IrModel.EvaluateWhenBranchDto();
                    if (wp.getWhens() != null) {
                        for (When w : wp.getWhens()) {
                            if (w.getCtx() != null) {
                                String wText = CobolTextCleaner.cleanContextText(w.getCtx());
                                branch.conditions.add(wText);
                                addResolvedFieldIds(wText, nameToIdMap, dto.sourceFieldIds);
                            }
                        }
                    }
                    if (wp.getStatements() != null) {
                        for (Statement s : wp.getStatements()) {
                            IrModel.StatementDto mapped = mapStatement(s, entryToIdMap, nameToIdMap);
                            if (mapped != null) branch.statements.add(mapped);
                        }
                    }
                    dto.whenBranches.add(branch);
                }
            }

            if (eval.getWhenOther() != null && eval.getWhenOther().getStatements() != null) {
                dto.whenOtherStatements = new ArrayList<>();
                for (Statement s : eval.getWhenOther().getStatements()) {
                    IrModel.StatementDto mapped = mapStatement(s, entryToIdMap, nameToIdMap);
                    if (mapped != null) dto.whenOtherStatements.add(mapped);
                }
            }
        }
        // 5. CALL Statement
        else if (stmt instanceof CallStatement) {
            CallStatement call = (CallStatement) stmt;
            dto.type = "CALL";
            if (call.getProgramValueStmt() != null && call.getProgramValueStmt().getCtx() != null) {
                dto.program = CobolTextCleaner.cleanContextText(call.getProgramValueStmt().getCtx());
            }
            if (call.getUsingPhrase() != null && call.getUsingPhrase().getUsingParameters() != null) {
                dto.usingParameters = new ArrayList<>();
                for (var p : call.getUsingPhrase().getUsingParameters()) {
                    if (p.getCtx() != null) {
                        String pText = CobolTextCleaner.cleanContextText(p.getCtx());
                        dto.usingParameters.add(pText);
                        addResolvedFieldIds(pText, nameToIdMap, dto.sourceFieldIds);
                    }
                }
            }
            if (call.getGivingPhrase() != null && call.getGivingPhrase().getCtx() != null) {
                dto.giving = CobolTextCleaner.cleanContextText(call.getGivingPhrase().getCtx());
                addResolvedFieldIds(dto.giving, nameToIdMap, dto.targetFieldIds);
            }
            if (call.getOnExceptionClause() != null && call.getOnExceptionClause().getStatements() != null) {
                dto.onExceptionStatements = mapStatements(call.getOnExceptionClause().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (call.getNotOnExceptionClause() != null && call.getNotOnExceptionClause().getStatements() != null) {
                dto.notOnExceptionStatements = mapStatements(call.getNotOnExceptionClause().getStatements(), entryToIdMap, nameToIdMap);
            }
        }
        // 6. COMPUTE Statement
        else if (stmt instanceof ComputeStatement) {
            ComputeStatement comp = (ComputeStatement) stmt;
            dto.type = "COMPUTE";
            if (comp.getArithmeticExpression() != null && comp.getArithmeticExpression().getCtx() != null) {
                dto.expression = CobolTextCleaner.cleanContextText(comp.getArithmeticExpression().getCtx());
                addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            }
            List<String> targets = new ArrayList<>();
            if (comp.getStores() != null) {
                for (var store : comp.getStores()) {
                    if (store.getCtx() != null) targets.add(CobolTextCleaner.cleanContextText(store.getCtx()));
                    String fid = resolveFieldId(store.getStoreCall(), entryToIdMap, nameToIdMap);
                    if (fid != null && !dto.targetFieldIds.contains(fid)) {
                        dto.targetFieldIds.add(fid);
                    }
                }
            }
            dto.targets = targets;
            if (comp.getOnSizeErrorPhrase() != null && comp.getOnSizeErrorPhrase().getStatements() != null) {
                dto.onSizeErrorStatements = mapStatements(comp.getOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (comp.getNotOnSizeErrorPhrase() != null && comp.getNotOnSizeErrorPhrase().getStatements() != null) {
                dto.notOnSizeErrorStatements = mapStatements(comp.getNotOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        }
        // 7. Arithmetic Statements (ADD, SUBTRACT, MULTIPLY, DIVIDE)
        else if (stmt instanceof AddStatement) {
            AddStatement add = (AddStatement) stmt;
            dto.type = "ADD";
            dto.operation = "ADD";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (add.getOnSizeErrorPhrase() != null && add.getOnSizeErrorPhrase().getStatements() != null) {
                dto.onSizeErrorStatements = mapStatements(add.getOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (add.getNotOnSizeErrorPhrase() != null && add.getNotOnSizeErrorPhrase().getStatements() != null) {
                dto.notOnSizeErrorStatements = mapStatements(add.getNotOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof SubtractStatement) {
            SubtractStatement sub = (SubtractStatement) stmt;
            dto.type = "SUBTRACT";
            dto.operation = "SUBTRACT";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (sub.getOnSizeErrorPhrase() != null && sub.getOnSizeErrorPhrase().getStatements() != null) {
                dto.onSizeErrorStatements = mapStatements(sub.getOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (sub.getNotOnSizeErrorPhrase() != null && sub.getNotOnSizeErrorPhrase().getStatements() != null) {
                dto.notOnSizeErrorStatements = mapStatements(sub.getNotOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof MultiplyStatement) {
            MultiplyStatement mul = (MultiplyStatement) stmt;
            dto.type = "MULTIPLY";
            dto.operation = "MULTIPLY";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (mul.getOnSizeErrorPhrase() != null && mul.getOnSizeErrorPhrase().getStatements() != null) {
                dto.onSizeErrorStatements = mapStatements(mul.getOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (mul.getNotOnSizeErrorPhrase() != null && mul.getNotOnSizeErrorPhrase().getStatements() != null) {
                dto.notOnSizeErrorStatements = mapStatements(mul.getNotOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof DivideStatement) {
            DivideStatement div = (DivideStatement) stmt;
            dto.type = "DIVIDE";
            dto.operation = "DIVIDE";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (div.getRemainder() != null && div.getRemainder().getCtx() != null) {
                dto.remainder = CobolTextCleaner.cleanContextText(div.getRemainder().getCtx());
                addResolvedFieldIds(dto.remainder, nameToIdMap, dto.targetFieldIds);
            }
            if (div.getOnSizeErrorPhrase() != null && div.getOnSizeErrorPhrase().getStatements() != null) {
                dto.onSizeErrorStatements = mapStatements(div.getOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (div.getNotOnSizeErrorPhrase() != null && div.getNotOnSizeErrorPhrase().getStatements() != null) {
                dto.notOnSizeErrorStatements = mapStatements(div.getNotOnSizeErrorPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        }
        // 8. I/O Statements (READ, WRITE, REWRITE, DELETE, OPEN, CLOSE, START)
        else if (stmt instanceof ReadStatement) {
            ReadStatement read = (ReadStatement) stmt;
            dto.type = "READ";
            dto.operation = "READ";
            if (read.getFileCall() != null) {
                dto.file = read.getFileCall().getName() != null ? read.getFileCall().getName() : CobolTextCleaner.cleanContextText(read.getFileCall().getCtx());
            }
            if (read.getInto() != null && read.getInto().getCtx() != null) {
                dto.into = CobolTextCleaner.cleanContextText(read.getInto().getCtx());
                addResolvedFieldIds(dto.into, nameToIdMap, dto.targetFieldIds);
            }
            if (read.getKey() != null && read.getKey().getCtx() != null) {
                dto.key = CobolTextCleaner.cleanContextText(read.getKey().getCtx());
                addResolvedFieldIds(dto.key, nameToIdMap, dto.sourceFieldIds);
            }
            if (read.getAtEnd() != null && read.getAtEnd().getStatements() != null) {
                dto.atEndStatements = mapStatements(read.getAtEnd().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (read.getNotAtEndPhrase() != null && read.getNotAtEndPhrase().getStatements() != null) {
                dto.notAtEndStatements = mapStatements(read.getNotAtEndPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (read.getInvalidKeyPhrase() != null && read.getInvalidKeyPhrase().getStatements() != null) {
                dto.invalidKeyStatements = mapStatements(read.getInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (read.getNotInvalidKeyPhrase() != null && read.getNotInvalidKeyPhrase().getStatements() != null) {
                dto.notInvalidKeyStatements = mapStatements(read.getNotInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof WriteStatement) {
            WriteStatement write = (WriteStatement) stmt;
            dto.type = "WRITE";
            dto.operation = "WRITE";
            if (write.getRecordCall() != null) {
                dto.record = write.getRecordCall().getName() != null ? write.getRecordCall().getName() : CobolTextCleaner.cleanContextText(write.getRecordCall().getCtx());
                String fid = resolveFieldId(write.getRecordCall(), entryToIdMap, nameToIdMap);
                if (fid != null && !dto.targetFieldIds.contains(fid)) {
                    dto.targetFieldIds.add(fid);
                }
            }
            if (write.getFrom() != null && write.getFrom().getCtx() != null) {
                dto.fromExpr = CobolTextCleaner.cleanContextText(write.getFrom().getCtx());
                addResolvedFieldIds(dto.fromExpr, nameToIdMap, dto.sourceFieldIds);
            }
            if (write.getInvalidKeyPhrase() != null && write.getInvalidKeyPhrase().getStatements() != null) {
                dto.invalidKeyStatements = mapStatements(write.getInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (write.getNotInvalidKeyPhrase() != null && write.getNotInvalidKeyPhrase().getStatements() != null) {
                dto.notInvalidKeyStatements = mapStatements(write.getNotInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (write.getAtEndOfPagePhrase() != null && write.getAtEndOfPagePhrase().getStatements() != null) {
                dto.endOfPageStatements = mapStatements(write.getAtEndOfPagePhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (write.getNotAtEndOfPagePhrase() != null && write.getNotAtEndOfPagePhrase().getStatements() != null) {
                dto.notEndOfPageStatements = mapStatements(write.getNotAtEndOfPagePhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof RewriteStatement) {
            RewriteStatement rewrite = (RewriteStatement) stmt;
            dto.type = "REWRITE";
            dto.operation = "REWRITE";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (rewrite.getInvalidKeyPhrase() != null && rewrite.getInvalidKeyPhrase().getStatements() != null) {
                dto.invalidKeyStatements = mapStatements(rewrite.getInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (rewrite.getNotInvalidKeyPhrase() != null && rewrite.getNotInvalidKeyPhrase().getStatements() != null) {
                dto.notInvalidKeyStatements = mapStatements(rewrite.getNotInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof DeleteStatement) {
            DeleteStatement del = (DeleteStatement) stmt;
            dto.type = "DELETE";
            dto.operation = "DELETE";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (del.getInvalidKeyPhrase() != null && del.getInvalidKeyPhrase().getStatements() != null) {
                dto.invalidKeyStatements = mapStatements(del.getInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (del.getNotInvalidKeyPhrase() != null && del.getNotInvalidKeyPhrase().getStatements() != null) {
                dto.notInvalidKeyStatements = mapStatements(del.getNotInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof OpenStatement) {
            dto.type = "OPEN";
            dto.operation = "OPEN";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
        } else if (stmt instanceof CloseStatement) {
            dto.type = "CLOSE";
            dto.operation = "CLOSE";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
        } else if (stmt instanceof StartStatement) {
            StartStatement start = (StartStatement) stmt;
            dto.type = "START";
            dto.operation = "START";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            if (start.getInvalidKeyPhrase() != null && start.getInvalidKeyPhrase().getStatements() != null) {
                dto.invalidKeyStatements = mapStatements(start.getInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (start.getNotInvalidKeyPhrase() != null && start.getNotInvalidKeyPhrase().getStatements() != null) {
                dto.notInvalidKeyStatements = mapStatements(start.getNotInvalidKeyPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        }
        // 9. GO TO Statement
        else if (stmt instanceof GoToStatement) {
            GoToStatement gotoStmt = (GoToStatement) stmt;
            dto.type = "GO_TO";
            dto.operation = "GO_TO";
            if (gotoStmt.getSimple() != null && gotoStmt.getSimple().getProcedureCall() != null) {
                dto.target = gotoStmt.getSimple().getProcedureCall().getName();
            } else if (gotoStmt.getDependingOnPhrase() != null && gotoStmt.getDependingOnPhrase().getCtx() != null) {
                dto.dependingOn = CobolTextCleaner.cleanContextText(gotoStmt.getDependingOnPhrase().getCtx());
                addResolvedFieldIds(dto.dependingOn, nameToIdMap, dto.sourceFieldIds);
            }
        }
        // 10. DISPLAY / ACCEPT / INITIALIZE / SET
        else if (stmt instanceof DisplayStatement) {
            DisplayStatement disp = (DisplayStatement) stmt;
            dto.type = "DISPLAY";
            List<String> ops = new ArrayList<>();
            if (disp.getOperands() != null) {
                for (var op : disp.getOperands()) {
                    if (op.getCtx() != null) {
                        String opText = CobolTextCleaner.cleanContextText(op.getCtx());
                        ops.add(opText);
                        addResolvedFieldIds(opText, nameToIdMap, dto.sourceFieldIds);
                    }
                }
            }
            dto.operands = ops;
        } else if (stmt instanceof AcceptStatement) {
            dto.type = "ACCEPT";
            dto.operation = "ACCEPT";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.targetFieldIds);
        } else if (stmt instanceof InitializeStatement) {
            InitializeStatement init = (InitializeStatement) stmt;
            dto.type = "INITIALIZE";
            List<String> targets = new ArrayList<>();
            if (init.getDataItemCalls() != null) {
                for (Call c : init.getDataItemCalls()) {
                    targets.add(c.getName() != null ? c.getName() : CobolTextCleaner.cleanContextText(c.getCtx()));
                    String fid = resolveFieldId(c, entryToIdMap, nameToIdMap);
                    if (fid != null && !dto.targetFieldIds.contains(fid)) {
                        dto.targetFieldIds.add(fid);
                    }
                }
            }
            dto.targets = targets;
        } else if (stmt instanceof SetStatement) {
            dto.type = "SET";
            dto.operation = "SET";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
        }
        // 11. STRING / UNSTRING / INSPECT / SEARCH
        else if (stmt instanceof StringStatement) {
            StringStatement strStmt = (StringStatement) stmt;
            dto.type = "STRING";
            dto.operation = "STRING";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (strStmt.getOnOverflowPhrase() != null && strStmt.getOnOverflowPhrase().getStatements() != null) {
                dto.onOverflowStatements = mapStatements(strStmt.getOnOverflowPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (strStmt.getNotOnOverflowPhrase() != null && strStmt.getNotOnOverflowPhrase().getStatements() != null) {
                dto.notOnOverflowStatements = mapStatements(strStmt.getNotOnOverflowPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof UnstringStatement) {
            UnstringStatement unstr = (UnstringStatement) stmt;
            dto.type = "UNSTRING";
            dto.operation = "UNSTRING";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (unstr.getOnOverflowPhrase() != null && unstr.getOnOverflowPhrase().getStatements() != null) {
                dto.onOverflowStatements = mapStatements(unstr.getOnOverflowPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (unstr.getNotOnOverflowPhrase() != null && unstr.getNotOnOverflowPhrase().getStatements() != null) {
                dto.notOnOverflowStatements = mapStatements(unstr.getNotOnOverflowPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
        } else if (stmt instanceof InspectStatement) {
            dto.type = "INSPECT";
            dto.operation = "INSPECT";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
        } else if (stmt instanceof SearchStatement) {
            SearchStatement search = (SearchStatement) stmt;
            dto.type = "SEARCH";
            dto.operation = "SEARCH";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
            addResolvedFieldIds(dto.expression, nameToIdMap, dto.sourceFieldIds);
            if (search.getAtEndPhrase() != null && search.getAtEndPhrase().getStatements() != null) {
                dto.atEndStatements = mapStatements(search.getAtEndPhrase().getStatements(), entryToIdMap, nameToIdMap);
            }
            if (search.getWhenPhrases() != null) {
                dto.searchWhenBranches = new ArrayList<>();
                for (var wp : search.getWhenPhrases()) {
                    IrModel.SearchWhenBranchDto branch = new IrModel.SearchWhenBranchDto();
                    if (wp.getCondition() != null && wp.getCondition().getCtx() != null) {
                        branch.condition = CobolTextCleaner.cleanContextText(wp.getCondition().getCtx());
                        addResolvedFieldIds(branch.condition, nameToIdMap, dto.sourceFieldIds);
                    }
                    if (wp.getStatements() != null) {
                        branch.statements = mapStatements(wp.getStatements(), entryToIdMap, nameToIdMap);
                        if (branch.statements == null) branch.statements = new ArrayList<>();
                    }
                    dto.searchWhenBranches.add(branch);
                }
            }
        }
        // 12. Flow Termination Statements
        else if (stmt instanceof GobackStatement) {
            dto.type = "GOBACK";
            dto.operation = "GOBACK";
        } else if (stmt instanceof StopStatement) {
            dto.type = "STOP";
            dto.operation = "STOP";
            dto.expression = CobolTextCleaner.cleanContextText(stmt.getCtx());
        } else if (stmt instanceof ExitStatement) {
            dto.type = "EXIT";
            dto.operation = "EXIT";
        }
        // 13. Embedded Subsystems (EXEC SQL / EXEC CICS / EXEC SQLIMS)
        else if (stmt instanceof ExecSqlStatement) {
            ExecSqlStatement sql = (ExecSqlStatement) stmt;
            dto.type = "EXEC_SQL";
            dto.subsystem = "SQL";
            dto.rawPayload = sql.getExecSqlText() != null ? sql.getExecSqlText() : CobolTextCleaner.cleanContextText(sql.getCtx());
        } else if (stmt instanceof ExecCicsStatement) {
            ExecCicsStatement cics = (ExecCicsStatement) stmt;
            dto.type = "EXEC_CICS";
            dto.subsystem = "CICS";
            dto.rawPayload = cics.getExecCicsText() != null ? cics.getExecCicsText() : CobolTextCleaner.cleanContextText(cics.getCtx());
        } else if (stmt instanceof ExecSqlImsStatement) {
            dto.type = "EXEC_SQLIMS";
            dto.subsystem = "SQLIMS";
            dto.rawPayload = CobolTextCleaner.cleanContextText(stmt.getCtx());
        }

        return dto;
    }

    private static List<IrModel.StatementDto> mapStatements(
            List<Statement> stmts,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {
        if (stmts == null || stmts.isEmpty()) return null;
        List<IrModel.StatementDto> result = new ArrayList<>();
        for (Statement s : stmts) {
            IrModel.StatementDto mapped = mapStatement(s, entryToIdMap, nameToIdMap);
            if (mapped != null) result.add(mapped);
        }
        return result.isEmpty() ? null : result;
    }

    public static String resolveFieldId(
            Call call,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        if (call == null) return null;
        Call unwrapped = call.unwrap() != null ? call.unwrap() : call;
        if (unwrapped instanceof DataDescriptionEntryCall && entryToIdMap != null) {
            DataDescriptionEntry dde = ((DataDescriptionEntryCall) unwrapped).getDataDescriptionEntry();
            if (dde != null && entryToIdMap.containsKey(dde)) {
                return entryToIdMap.get(dde);
            }
        }
        if (nameToIdMap != null) {
            String name = call.getName();
            if (name != null && nameToIdMap.containsKey(name.toUpperCase().trim())) {
                return nameToIdMap.get(name.toUpperCase().trim());
            }
            if (call.getCtx() != null) {
                String text = CobolTextCleaner.cleanContextText(call.getCtx()).toUpperCase().trim();
                if (nameToIdMap.containsKey(text)) {
                    return nameToIdMap.get(text);
                }
            }
        }
        return null;
    }

    public static void addResolvedFieldIds(
            String text,
            Map<String, String> nameToIdMap,
            List<String> targetList) {

        if (text == null || nameToIdMap == null || targetList == null) return;
        String clean = text.trim();
        if (clean.isEmpty() || clean.startsWith("'") || clean.startsWith("\"")) return;

        String[] tokens = clean.split("[^a-zA-Z0-9_-]+");
        for (String token : tokens) {
            String t = token.toUpperCase().trim();
            if (t.isEmpty() || t.matches("^-?[0-9]+(\\.[0-9]+)?$")) continue;
            if (nameToIdMap.containsKey(t)) {
                String fid = nameToIdMap.get(t);
                if (!targetList.contains(fid)) {
                    targetList.add(fid);
                }
            }
        }
    }

    public static void mapPerformType(
            PerformType type,
            IrModel.StatementDto dto,
            Map<String, String> nameToIdMap) {

        if (type == null || dto == null) return;
        if (type.getPerformTypeType() != null) {
            dto.performType = type.getPerformTypeType().name();
        }
        if (type.getTimes() != null && type.getTimes().getCtx() != null) {
            dto.timesExpr = CobolTextCleaner.cleanContextText(type.getTimes().getCtx());
            addResolvedFieldIds(dto.timesExpr, nameToIdMap, dto.sourceFieldIds);
        }
        if (type.getUntil() != null && type.getUntil().getCtx() != null) {
            dto.untilCondition = CobolTextCleaner.cleanContextText(type.getUntil().getCtx());
            addResolvedFieldIds(dto.untilCondition, nameToIdMap, dto.sourceFieldIds);
        }
        if (type.getVarying() != null && type.getVarying().getCtx() != null) {
            dto.varyingExpr = CobolTextCleaner.cleanContextText(type.getVarying().getCtx());
            addResolvedFieldIds(dto.varyingExpr, nameToIdMap, dto.sourceFieldIds);
        }
    }
}
