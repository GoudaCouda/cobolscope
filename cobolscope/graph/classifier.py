"""
cobolscope.graph.classifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Heuristic subsystem classifier and cluster visual themes for COBOL procedures.
"""

from __future__ import annotations
import re
from typing import Dict

from cobolscope.models import (
    ParagraphNode,
    ReadStatementNode,
    WriteStatementNode,
    RewriteStatementNode,
    DeleteStatementNode,
    OpenStatementNode,
    CloseStatementNode,
    ExecSqlStatementNode,
    ExecCicsStatementNode,
    ExecSqlImsStatementNode,
    SearchStatementNode,
    StopStatementNode,
    GobackStatementNode,
    ExitStatementNode,
)
from .models import GraphNodeType

CLUSTER_THEMES: Dict[GraphNodeType, Dict[str, str]] = {
    GraphNodeType.MAIN_DRIVER: {
        "id": "cluster_main_driver",
        "name": "Main Control & Driver",
        "color": "#1A365D",
        "fill_color": "#EBF4FF",
        "text_color": "#1A365D",
    },
    GraphNodeType.INITIALIZATION: {
        "id": "cluster_init",
        "name": "Initialization & Housekeeping",
        "color": "#2C5282",
        "fill_color": "#EBF8FF",
        "text_color": "#2C5282",
    },
    GraphNodeType.BUSINESS_LOGIC: {
        "id": "cluster_logic",
        "name": "Business & Transaction Logic",
        "color": "#0078D4",
        "fill_color": "#F0F8FF",
        "text_color": "#004B87",
    },
    GraphNodeType.FILE_IO: {
        "id": "cluster_file_io",
        "name": "File I/O Operations",
        "color": "#107C41",
        "fill_color": "#F2F9F4",
        "text_color": "#0B5A2F",
    },
    GraphNodeType.DATABASE_IO: {
        "id": "cluster_database_io",
        "name": "Database & Subsystem Access",
        "color": "#008272",
        "fill_color": "#F0FDFB",
        "text_color": "#005A4E",
    },
    GraphNodeType.TABLE_LOOKUP: {
        "id": "cluster_table",
        "name": "Table & Memory Lookups",
        "color": "#5C2D91",
        "fill_color": "#FAF5FF",
        "text_color": "#441D6A",
    },
    GraphNodeType.ERROR_HANDLING: {
        "id": "cluster_error",
        "name": "Error Handling & Traps",
        "color": "#DC2626",
        "fill_color": "#FEF2F2",
        "text_color": "#991B1B",
    },
    GraphNodeType.TERMINATION: {
        "id": "cluster_termination",
        "name": "Program Termination & Wrap-Up",
        "color": "#475569",
        "fill_color": "#F8FAFC",
        "text_color": "#1E293B",
    },
    GraphNodeType.ROUTINE_EXIT: {
        "id": "cluster_exit",
        "name": "Routine Return Points",
        "color": "#605E5C",
        "fill_color": "#F8F8F8",
        "text_color": "#323130",
    },
    GraphNodeType.GENERIC: {
        "id": "cluster_generic",
        "name": "General Procedures",
        "color": "#4A5568",
        "fill_color": "#F7FAFC",
        "text_color": "#2D3748",
    },
}


class ParagraphClassifier:
    """Heuristic subsystem classifier mapping paragraph names and contents to architectural clusters."""

    _RE_MAIN = re.compile(r"^(?:0*(?:000|010|100)(?:[-_]|$)|(?:MAIN|DRIVER|MAINLINE|ENTRY|ALT-ENTRY)(?:[-_]|$)|0000-)", re.IGNORECASE)
    _RE_INIT = re.compile(r"(?:^|[-_])(?:HSKP|HOUSEKEEP|INIT|OPEN|SETUP|START-UP|STARTUP|PREP)(?:[-_]|$)", re.IGNORECASE)
    _RE_ERROR = re.compile(r"(?:^|[-_])(?:ERROR|ERR|EXCEPTION|RECOVERY|SYS-ERR|TRAP|DIAG|ERROR-LOG)(?:[-_]|$)", re.IGNORECASE)
    _RE_ABEND = re.compile(r"(?:^|[-_])(?:ABEND|FATAL|KILL|CANCEL)(?:[-_]|$)", re.IGNORECASE)
    _RE_WRAPUP = re.compile(r"(?:^|[-_])(?:WRAP-UP|WRAPUP|CLOSE-PROCESS|CLEANUP|SHUTDOWN|FINISH)(?:[-_]|$)", re.IGNORECASE)
    _RE_FILE_IO = re.compile(r"(?:^|[-_])(?:READ|WRITE|REWRITE|DELETE|FETCH|GET|PUT|CLOSE|FILE|REPORT|HEADING|DETAIL)(?:[-_]|$)", re.IGNORECASE)
    _RE_DB_IO = re.compile(r"(?:^|[-_])(?:ADABAS|SQL|CICS|DB2|IMS|FIND|SELECT|INSERT|UPDATE-DB)(?:[-_]|$)", re.IGNORECASE)
    _RE_TABLE = re.compile(r"(?:^|[-_])(?:TBL|TABLE|SEARCH|LOOKUP|GENTBL|GEN-TBL|DECODE|LOAD-TBL)(?:[-_]|$)", re.IGNORECASE)

    @classmethod
    def classify(cls, para: ParagraphNode) -> GraphNodeType:
        name = (para.name or "").strip().upper()
        sec = (para.section_parent or "").strip().upper()

        # 1. Exit nodes
        if name.endswith("-EXIT") or name.endswith("_EXIT") or sec.endswith("-EXIT"):
            return GraphNodeType.ROUTINE_EXIT
        if len(para.statements) == 1 and isinstance(para.statements[0], ExitStatementNode):
            return GraphNodeType.ROUTINE_EXIT

        # 2. Error Handling & Abend (Declaratives, Error routines)
        if (cls._RE_ABEND.search(name) or cls._RE_ERROR.search(name) or "ERROR" in name
                or cls._RE_ABEND.search(sec) or cls._RE_ERROR.search(sec) or "ERROR" in sec):
            return GraphNodeType.ERROR_HANDLING

        # 3. Main Driver & Secondary Entrypoints
        if ((cls._RE_MAIN.search(name) or "ALT-ENTRY" in name or name.startswith("0000-")
                or cls._RE_MAIN.search(sec) or sec in ("PREMIERE", "MAIN", "MAINLINE", "MAIN-LOGIC"))
                and "EXIT" not in name and "EXIT" not in sec):
            return GraphNodeType.MAIN_DRIVER

        # 4. Wrap-up / Clean Termination
        if cls._RE_WRAPUP.search(name) or cls._RE_WRAPUP.search(sec):
            return GraphNodeType.TERMINATION
        if para.is_terminal and any(isinstance(s, (StopStatementNode, GobackStatementNode)) for s in para.statements):
            return GraphNodeType.TERMINATION

        # 5. Initialization / Housekeeping
        if cls._RE_INIT.search(name) or cls._RE_INIT.search(sec):
            return GraphNodeType.INITIALIZATION

        # 6. Database / Subsystem Access
        has_sql_cics = any(
            isinstance(s, (ExecSqlStatementNode, ExecCicsStatementNode, ExecSqlImsStatementNode))
            for s in para.statements
        )
        if has_sql_cics or cls._RE_DB_IO.search(name) or cls._RE_DB_IO.search(sec):
            return GraphNodeType.DATABASE_IO

        # 7. Table / Memory Lookups
        has_search = any(isinstance(s, SearchStatementNode) for s in para.statements)
        if has_search or cls._RE_TABLE.search(name) or cls._RE_TABLE.search(sec):
            return GraphNodeType.TABLE_LOOKUP

        # 8. File I/O
        has_file_io = any(
            isinstance(s, (ReadStatementNode, WriteStatementNode, RewriteStatementNode, DeleteStatementNode, OpenStatementNode, CloseStatementNode))
            for s in para.statements
        )
        if has_file_io or cls._RE_FILE_IO.search(name) or cls._RE_FILE_IO.search(sec):
            return GraphNodeType.FILE_IO

        # 9. Default Business Logic
        return GraphNodeType.BUSINESS_LOGIC
