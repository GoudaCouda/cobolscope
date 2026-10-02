# Data Dictionary: `DELACC`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 253 |
| **Level-88 Business Rules** | 32 |
| **Memory Overlays (REDEFINES)** | 16 |
| **Working-Storage Span** | 1,452 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 01 | **`SYSIDERR-RETRY`**<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILE-RETRY`**<br/><small>`FILE-RETRY`</small> | Numeric Display (3 digits) | `999` | 9 | 3 | — | — |
| 01 | **`WS-EXIT-RETRY-LOOP`**<br/><small>`WS-EXIT-RETRY-LOOP`</small> | Alphanumeric (1 chars) | `X` | 12 | 1 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 13 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 13 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 13 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 17 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 27 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 33 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 41 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 49 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 53 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 63 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 67 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 77 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 87 | 7 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 94 | 7 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 101 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 101 | 96 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 101 | 4 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORT-CODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORT-CODE`</small> | Alphanumeric (6 chars) | `X(6)` | 105 | 6 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-ACC-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-ACC-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 111 | 8 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 119 | 10 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 129 | 6 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 135 | 12 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 147 | 3 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 150 | 40 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 190 | 7 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 197 | 0 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 197 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 205 | 16 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 205 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 209 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-EIBRESP-DISPLAY`<br/><small>`WS-CICS-WORK-AREA.WS-EIBRESP-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 213 | 8 | — | — |
| 01 | **`WS-APPLID`**<br/><small>`WS-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 221 | 8 | — | — |
| 01 | **`EXIT-BROWSE-LOOP`**<br/><small>`EXIT-BROWSE-LOOP`</small> | Alphanumeric (1 chars) | `X` | 229 | 1 | **Default:** `N` | — |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 230 | 98 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 230 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 230 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 234 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 244 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 244 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 250 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 258 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 266 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 272 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 272 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 272 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 274 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 276 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 280 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 288 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 288 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 288 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 290 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 292 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 296 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 296 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 296 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 298 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 300 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 304 | 12 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 316 | 12 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 01 | **`PROCTRAN-AREA`**<br/><small>`PROCTRAN-AREA`</small> | Group | *DISPLAY* | 328 | 99 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`PROC-TRAN-DATA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA`</small> | Group | *DISPLAY* | 328 | 99 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-EYE-CATCHER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 328 | 4 | • `88 PROC-TRAN-VALID`: 'PRTR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-AREA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA`</small> | Group | *DISPLAY* | 328 | 4 | <mark>REDEFINES PROC-TRAN-EYE-CATCHER</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-FLAG`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.PROC-TRAN-LOGICAL-DELETE-FLAG`</small> | Alphanumeric (1 chars) | `X` | 328 | 1 | • `88 PROC-TRAN-LOGICALLY-DELETED`: 'X'FF'' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.FILLER`</small> | Alphanumeric (3 chars) | `X(3)` | 329 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-ID`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID`</small> | Group | *DISPLAY* | 332 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-SORT-CODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 332 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-NUMBER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 338 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 346 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 346 | 8 | <mark>REDEFINES PROC-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-YYYY`</small> | Numeric Display (4 digits) | `9999` | 346 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 350 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-DD`</small> | Numeric Display (2 digits) | `99` | 352 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 354 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 354 | 6 | <mark>REDEFINES PROC-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-HH`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 354 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 356 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-SS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 358 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-REF`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 360 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 372 | 3 | • `88 PROC-TY-CHEQUE-ACKNOWLEDGED`: 'CHA'<br/>• `88 PROC-TY-CHEQUE-FAILURE`: 'CHF'<br/>• `88 PROC-TY-CHEQUE-PAID-IN`: 'CHI'<br/>• `88 PROC-TY-CHEQUE-PAID-OUT`: 'CHO'<br/>• `88 PROC-TY-CREDIT`: 'CRE'<br/>• `88 PROC-TY-DEBIT`: 'DEB'<br/>• `88 PROC-TY-WEB-CREATE-ACCOUNT`: 'ICA'<br/>• `88 PROC-TY-WEB-CREATE-CUSTOMER`: 'ICC'<br/>• `88 PROC-TY-WEB-DELETE-ACCOUNT`: 'IDA'<br/>• `88 PROC-TY-WEB-DELETE-CUSTOMER`: 'IDC'<br/>• `88 PROC-TY-BRANCH-CREATE-ACCOUNT`: 'OCA'<br/>• `88 PROC-TY-BRANCH-CREATE-CUSTOMER`: 'OCC'<br/>• `88 PROC-TY-BRANCH-DELETE-ACCOUNT`: 'ODA'<br/>• `88 PROC-TY-BRANCH-DELETE-CUSTOMER`: 'ODC'<br/>• `88 PROC-TY-CREATE-SODD`: 'OCS'<br/>• `88 PROC-TY-PAYMENT-CREDIT`: 'PCR'<br/>• `88 PROC-TY-PAYMENT-DEBIT`: 'PDR'<br/>• `88 PROC-TY-TRANSFER`: 'TFR' | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 375 | 40 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR`</small> | Group | *DISPLAY* | 375 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-HEADER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-HEADER`</small> | Alphanumeric (26 chars) | `X(26)` | 375 | 26 | • `88 PROC-TRAN-DESC-XFR-FLAG`: 'TRANSFER' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 401 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-ACCOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-ACCOUNT`</small> | Numeric Display (8 digits) | `9(8)` | 407 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC`</small> | Group | *DISPLAY* | 375 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 375 | 10 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 385 | 8 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 393 | 2 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 395 | 2 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 397 | 4 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 401 | 2 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 403 | 2 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 405 | 4 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 409 | 6 | • `88 PROC-DESC-DELACC-FLAG`: 'DELETE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CREACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC`</small> | Group | *DISPLAY* | 375 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 375 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 385 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 393 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 395 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 397 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 401 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 403 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 405 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 409 | 6 | • `88 PROC-DESC-CREACC-FLAG`: 'CREATE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELCUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS`</small> | Group | *DISPLAY* | 375 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 375 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 381 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 391 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 405 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 409 | 1 | • `88 PROC-DESC-DELCUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 410 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 412 | 1 | • `88 PROC-DESC-DELCUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 413 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CRECUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS`</small> | Group | *DISPLAY* | 375 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 375 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 381 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 391 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 405 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 409 | 1 | • `88 PROC-DESC-CRECUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 410 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 412 | 1 | • `88 PROC-DESC-CRECUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 413 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-AMOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 415 | 12 | — | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 427 | 4 | — | — |
| 77 | `PROCTRAN-RETRY`<br/><small>`PROCTRAN-RETRY`</small> | Numeric Display (3 digits) | `999` | 431 | 3 | — | — |
| 01 | **`ACCOUNT-ACT-BAL-STORE`**<br/><small>`ACCOUNT-ACT-BAL-STORE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 434 | 12 | **Default:** `0` | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`RETURNED-DATA`**<br/><small>`RETURNED-DATA`</small> | Group | *DISPLAY* | 446 | 98 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-EYE-CATCHER`<br/><small>`RETURNED-DATA.RETURNED-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 446 | 4 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-CUST-NO`<br/><small>`RETURNED-DATA.RETURNED-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 450 | 10 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-KEY`<br/><small>`RETURNED-DATA.RETURNED-KEY`</small> | Group | *DISPLAY* | 460 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-SORT-CODE`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 460 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-NUMBER`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 466 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-TYPE`<br/><small>`RETURNED-DATA.RETURNED-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 474 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-INTEREST-RATE`<br/><small>`RETURNED-DATA.RETURNED-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 482 | 6 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OPENED`<br/><small>`RETURNED-DATA.RETURNED-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 488 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OVERDRAFT-LIMIT`<br/><small>`RETURNED-DATA.RETURNED-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 496 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-LAST-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 504 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-NEXT-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 512 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-AVAILABLE-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 520 | 12 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-ACTUAL-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 532 | 12 | — | — |
| 01 | **`DESIRED-KEY`**<br/><small>`DESIRED-KEY`</small> | Unsigned BigInt (64-bit Binary) | `9(10)`<br/>*BINARY* | 544 | 8 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 552 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 552 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 556 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 557 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 559 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 560 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 01 | **`DATA-STORE-TYPE`**<br/><small>`DATA-STORE-TYPE`</small> | Alphanumeric (1 chars) | `X` | 562 | 1 | • `88 DATASTORE-TYPE-DB2`: '2'<br/>• `88 DATASTORE-TYPE-VSAM`: 'V' | — |
| 01 | **`DB2-EXIT-LOOP`**<br/><small>`DB2-EXIT-LOOP`</small> | Alphanumeric (1 chars) | `X` | 563 | 1 | — | — |
| 01 | **`FETCH-DATA-CNT`**<br/><small>`FETCH-DATA-CNT`</small> | Unsigned SmallInt (16-bit Binary) | `9(4)`<br/>*COMP* | 564 | 2 | — | — |
| 01 | **`WS-CUST-ALT-KEY-LEN`**<br/><small>`WS-CUST-ALT-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 566 | 2 | **Default:** `+10` | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 568 | 12 | **Default:** `0` | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`ACCOUNT-KEY-RID`**<br/><small>`ACCOUNT-KEY-RID`</small> | Group | *DISPLAY* | 580 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`ACCOUNT-KEY-RID.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 580 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`ACCOUNT-KEY-RID.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 586 | 8 | **Default:** `0` | — |
| 01 | **`MY-TCB`**<br/><small>`MY-TCB`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 594 | 4 | — | — |
| 01 | **`MY-TCB-STRING`**<br/><small>`MY-TCB-STRING`</small> | Alphanumeric (8 chars) | `X(8)` | 598 | 8 | — | — |
| 01 | **`WS-ACC-KEY-LEN`**<br/><small>`WS-ACC-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 606 | 2 | **Default:** `+14` | — |
| 01 | **`WS-ACC-NUM`**<br/><small>`WS-ACC-NUM`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 608 | 2 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 610 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 618 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 618 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 618 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 620 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 621 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 623 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 624 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 628 | 10 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 628 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 630 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 631 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 633 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 634 | 4 | — | — |
| 01 | **`WS-TOKEN`**<br/><small>`WS-TOKEN`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 638 | 4 | — | — |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 642 | 20 | — | — |
| 01 | **`ACCOUNT-CONTROL`**<br/><small>`ACCOUNT-CONTROL`</small> | Group | *DISPLAY* | 662 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-CONTROL-RECORD`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD`</small> | Group | *DISPLAY* | 662 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-EYE-CATCHER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 662 | 4 | • `88 ACCOUNT-CONTROL-EYECATCHER-V`: 'CTRL' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (10 digits) | `9(10)` | 666 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-KEY`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY`</small> | Group | *DISPLAY* | 676 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-SORT-CODE`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY.ACCOUNT-CONTROL-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 676 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-NUMBER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY.ACCOUNT-CONTROL-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 682 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.NUMBER-OF-ACCOUNTS`</small> | Numeric Display (8 digits) | `9(8)` | 690 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`LAST-ACCOUNT-NUMBER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.LAST-ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 698 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-SUCCESS-FLAG`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-SUCCESS-FLAG`</small> | Alphanumeric (1 chars) | `X` | 706 | 1 | • `88 ACCOUNT-CONTROL-SUCCESS`: 'Y' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-FAIL-CODE`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 707 | 1 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Decimal Display (6, 2) | `9(4)V99` | 708 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 714 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 722 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 730 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 738 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 746 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Alphanumeric (2 chars) | `X(2)` | 758 | 2 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 760 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 760 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 760 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 760 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 762 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 764 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 766 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 774 | 678 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 774 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 774 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 782 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 786 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 794 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 798 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 808 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 816 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 820 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 828 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 836 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 844 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 852 | 600 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 122 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-EYE`<br/><small>`DFHCOMMAREA.DELACC-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-CUSTNO`<br/><small>`DFHCOMMAREA.DELACC-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 4 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-SCODE`<br/><small>`DFHCOMMAREA.DELACC-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 14 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-ACCNO`<br/><small>`DFHCOMMAREA.DELACC-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 20 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-ACC-TYPE`<br/><small>`DFHCOMMAREA.DELACC-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 28 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-INT-RATE`<br/><small>`DFHCOMMAREA.DELACC-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 36 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-OPENED`<br/><small>`DFHCOMMAREA.DELACC-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 42 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-OPENED-GROUP`<br/><small>`DFHCOMMAREA.DELACC-OPENED-GROUP`</small> | Group | *DISPLAY* | 42 | 8 | <mark>REDEFINES DELACC-OPENED</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-OPENED-DAY`<br/><small>`DFHCOMMAREA.DELACC-OPENED-GROUP.DELACC-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 42 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-OPENED-MONTH`<br/><small>`DFHCOMMAREA.DELACC-OPENED-GROUP.DELACC-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 44 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-OPENED-YEAR`<br/><small>`DFHCOMMAREA.DELACC-OPENED-GROUP.DELACC-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 46 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-OVERDRAFT`<br/><small>`DFHCOMMAREA.DELACC-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 50 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.DELACC-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 58 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-LAST-STMT-GROUP`<br/><small>`DFHCOMMAREA.DELACC-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 58 | 8 | <mark>REDEFINES DELACC-LAST-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-LAST-STMT-DAY`<br/><small>`DFHCOMMAREA.DELACC-LAST-STMT-GROUP.DELACC-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 58 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-LAST-STMT-MONTH`<br/><small>`DFHCOMMAREA.DELACC-LAST-STMT-GROUP.DELACC-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 60 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-LAST-STMT-YEAR`<br/><small>`DFHCOMMAREA.DELACC-LAST-STMT-GROUP.DELACC-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 62 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.DELACC-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 66 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-NEXT-STMT-GROUP`<br/><small>`DFHCOMMAREA.DELACC-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 66 | 8 | <mark>REDEFINES DELACC-NEXT-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-NEXT-STMT-DAY`<br/><small>`DFHCOMMAREA.DELACC-NEXT-STMT-GROUP.DELACC-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 66 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-NEXT-STMT-MONTH`<br/><small>`DFHCOMMAREA.DELACC-NEXT-STMT-GROUP.DELACC-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`DELACC-NEXT-STMT-YEAR`<br/><small>`DFHCOMMAREA.DELACC-NEXT-STMT-GROUP.DELACC-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 70 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-AVAIL-BAL`<br/><small>`DFHCOMMAREA.DELACC-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 74 | 12 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-ACTUAL-BAL`<br/><small>`DFHCOMMAREA.DELACC-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 86 | 12 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-SUCCESS`<br/><small>`DFHCOMMAREA.DELACC-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 98 | 1 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`DEL-ACCOUNT-DB2`<br/><small>*DADB010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-FAIL-CD`<br/><small>`DFHCOMMAREA.DELACC-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 99 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-DEL-SUCCESS`<br/><small>`DFHCOMMAREA.DELACC-DEL-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 100 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`DEL-ACCOUNT-DB2`<br/><small>*DADB010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-DEL-FAIL-CD`<br/><small>`DFHCOMMAREA.DELACC-DEL-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 101 | 1 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`DEL-ACCOUNT-DB2`<br/><small>*DADB010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-DEL-APPLID`<br/><small>`DFHCOMMAREA.DELACC-DEL-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 102 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-DEL-PCB1`<br/><small>`DFHCOMMAREA.DELACC-DEL-PCB1`</small> | Memory Pointer (4 bytes) | *POINTER* | 110 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-DEL-PCB2`<br/><small>`DFHCOMMAREA.DELACC-DEL-PCB2`</small> | Memory Pointer (4 bytes) | *POINTER* | 114 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-DEL-PCB3`<br/><small>`DFHCOMMAREA.DELACC-DEL-PCB3`</small> | Memory Pointer (4 bytes) | *POINTER* | 118 | 4 | — | — |

