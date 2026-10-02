# Data Dictionary: `CREACC`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 389 |
| **Level-88 Business Rules** | 34 |
| **Memory Overlays (REDEFINES)** | 26 |
| **Working-Storage Span** | 410 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`ENQ-NAMED-COUNTER`<br/><small>*ENC010*</small><br/>*( +4 more)* |
| 77 | `SYSIDERR-RETRY`<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 9 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 9 | 88 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 9 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 13 | 10 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 23 | 6 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 29 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 37 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 45 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 49 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED-GROUP`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 49 | 10 | <mark>REDEFINES HV-ACCOUNT-OPENED</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-OPENED-DAY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP.HV-ACCOUNT-OPENED-DAY`</small> | Alphanumeric (2 chars) | `XX` | 49 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-OPENED-DELIM1`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP.HV-ACCOUNT-OPENED-DELIM1`</small> | Alphanumeric (1 chars) | `X` | 51 | 1 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-OPENED-MONTH`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP.HV-ACCOUNT-OPENED-MONTH`</small> | Alphanumeric (2 chars) | `XX` | 52 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-OPENED-DELIM2`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP.HV-ACCOUNT-OPENED-DELIM2`</small> | Alphanumeric (1 chars) | `X` | 54 | 1 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-OPENED-YEAR`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED-GROUP.HV-ACCOUNT-OPENED-YEAR`</small> | Alphanumeric (4 chars) | `X(4)` | 55 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 59 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 63 | 10 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-GROUP`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 63 | 10 | <mark>REDEFINES HV-ACCOUNT-LAST-STMT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-DAY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP.HV-ACCOUNT-LAST-STMT-DAY`</small> | Alphanumeric (2 chars) | `XX` | 63 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-DELIM1`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP.HV-ACCOUNT-LAST-STMT-DELIM1`</small> | Alphanumeric (1 chars) | `X` | 65 | 1 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-MONTH`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP.HV-ACCOUNT-LAST-STMT-MONTH`</small> | Alphanumeric (2 chars) | `XX` | 66 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-DELIM2`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP.HV-ACCOUNT-LAST-STMT-DELIM2`</small> | Alphanumeric (1 chars) | `X` | 68 | 1 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT-YEAR`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT-GROUP.HV-ACCOUNT-LAST-STMT-YEAR`</small> | Alphanumeric (4 chars) | `X(4)` | 69 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 73 | 10 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-GROUP`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 73 | 10 | <mark>REDEFINES HV-ACCOUNT-NEXT-STMT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-DAY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP.HV-ACCOUNT-NEXT-STMT-DAY`</small> | Alphanumeric (2 chars) | `XX` | 73 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-DELIM1`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP.HV-ACCOUNT-NEXT-STMT-DELIM1`</small> | Alphanumeric (1 chars) | `X` | 75 | 1 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-MONTH`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP.HV-ACCOUNT-NEXT-STMT-MONTH`</small> | Alphanumeric (2 chars) | `XX` | 76 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-DELIM2`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP.HV-ACCOUNT-NEXT-STMT-DELIM2`</small> | Alphanumeric (1 chars) | `X` | 78 | 1 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT-YEAR`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT-GROUP.HV-ACCOUNT-NEXT-STMT-YEAR`</small> | Alphanumeric (4 chars) | `X(4)` | 79 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 83 | 7 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 90 | 7 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 97 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 105 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 105 | 96 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 105 | 4 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORT-CODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORT-CODE`</small> | Alphanumeric (6 chars) | `X(6)` | 109 | 6 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-ACC-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-ACC-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 115 | 8 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 123 | 10 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 133 | 6 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 139 | 12 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 151 | 3 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 154 | 40 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 194 | 7 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`HOST-CONTROL-ROW`**<br/><small>`HOST-CONTROL-ROW`</small> | Group | *DISPLAY* | 201 | 76 | — | — |
| 03 | &nbsp;&nbsp;`HV-CONTROL-NAME`<br/><small>`HOST-CONTROL-ROW.HV-CONTROL-NAME`</small> | Alphanumeric (32 chars) | `X(32)` | 201 | 32 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 03 | &nbsp;&nbsp;`HV-CONTROL-VALUE-NUM`<br/><small>`HOST-CONTROL-ROW.HV-CONTROL-VALUE-NUM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 233 | 4 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 03 | &nbsp;&nbsp;`HV-CONTROL-VALUE-STR`<br/><small>`HOST-CONTROL-ROW.HV-CONTROL-VALUE-STR`</small> | Alphanumeric (40 chars) | `X(40)` | 237 | 40 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 277 | 0 | — | — |
| 01 | **`PROCTRAN-AREA`**<br/><small>`PROCTRAN-AREA`</small> | Group | *DISPLAY* | 277 | 99 | — | — |
| 03 | &nbsp;&nbsp;`PROC-TRAN-DATA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA`</small> | Group | *DISPLAY* | 277 | 99 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-EYE-CATCHER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 277 | 4 | • `88 PROC-TRAN-VALID`: 'PRTR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-AREA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA`</small> | Group | *DISPLAY* | 277 | 4 | <mark>REDEFINES PROC-TRAN-EYE-CATCHER</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-FLAG`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.PROC-TRAN-LOGICAL-DELETE-FLAG`</small> | Alphanumeric (1 chars) | `X` | 277 | 1 | • `88 PROC-TRAN-LOGICALLY-DELETED`: 'X'FF'' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.FILLER`</small> | Alphanumeric (3 chars) | `X(3)` | 278 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-ID`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID`</small> | Group | *DISPLAY* | 281 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-SORT-CODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 281 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-NUMBER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 287 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 295 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 295 | 8 | <mark>REDEFINES PROC-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-YYYY`</small> | Numeric Display (4 digits) | `9999` | 295 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 299 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-DD`</small> | Numeric Display (2 digits) | `99` | 301 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 303 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 303 | 6 | <mark>REDEFINES PROC-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-HH`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 303 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 305 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-SS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 307 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-REF`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 309 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 321 | 3 | • `88 PROC-TY-CHEQUE-ACKNOWLEDGED`: 'CHA'<br/>• `88 PROC-TY-CHEQUE-FAILURE`: 'CHF'<br/>• `88 PROC-TY-CHEQUE-PAID-IN`: 'CHI'<br/>• `88 PROC-TY-CHEQUE-PAID-OUT`: 'CHO'<br/>• `88 PROC-TY-CREDIT`: 'CRE'<br/>• `88 PROC-TY-DEBIT`: 'DEB'<br/>• `88 PROC-TY-WEB-CREATE-ACCOUNT`: 'ICA'<br/>• `88 PROC-TY-WEB-CREATE-CUSTOMER`: 'ICC'<br/>• `88 PROC-TY-WEB-DELETE-ACCOUNT`: 'IDA'<br/>• `88 PROC-TY-WEB-DELETE-CUSTOMER`: 'IDC'<br/>• `88 PROC-TY-BRANCH-CREATE-ACCOUNT`: 'OCA'<br/>• `88 PROC-TY-BRANCH-CREATE-CUSTOMER`: 'OCC'<br/>• `88 PROC-TY-BRANCH-DELETE-ACCOUNT`: 'ODA'<br/>• `88 PROC-TY-BRANCH-DELETE-CUSTOMER`: 'ODC'<br/>• `88 PROC-TY-CREATE-SODD`: 'OCS'<br/>• `88 PROC-TY-PAYMENT-CREDIT`: 'PCR'<br/>• `88 PROC-TY-PAYMENT-DEBIT`: 'PDR'<br/>• `88 PROC-TY-TRANSFER`: 'TFR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 324 | 40 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR`</small> | Group | *DISPLAY* | 324 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-HEADER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-HEADER`</small> | Alphanumeric (26 chars) | `X(26)` | 324 | 26 | • `88 PROC-TRAN-DESC-XFR-FLAG`: 'TRANSFER' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 350 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-ACCOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-ACCOUNT`</small> | Numeric Display (8 digits) | `9(8)` | 356 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC`</small> | Group | *DISPLAY* | 324 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 324 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 334 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 342 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 344 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 346 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 350 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 352 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 354 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 358 | 6 | • `88 PROC-DESC-DELACC-FLAG`: 'DELETE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CREACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC`</small> | Group | *DISPLAY* | 324 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 324 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 334 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 342 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 344 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 346 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 350 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 352 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 354 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 358 | 6 | • `88 PROC-DESC-CREACC-FLAG`: 'CREATE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELCUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS`</small> | Group | *DISPLAY* | 324 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 324 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 330 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 340 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 354 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 358 | 1 | • `88 PROC-DESC-DELCUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 359 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 361 | 1 | • `88 PROC-DESC-DELCUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 362 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CRECUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS`</small> | Group | *DISPLAY* | 324 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 324 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 330 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 340 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 354 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 358 | 1 | • `88 PROC-DESC-CRECUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 359 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 361 | 1 | • `88 PROC-DESC-CRECUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 362 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-AMOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 364 | 12 | — | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 376 | 4 | — | — |
| 01 | **`PROCTRAN-RETRY`**<br/><small>`PROCTRAN-RETRY`</small> | Numeric Display (3 digits) | `999` | 380 | 3 | — | — |
| 01 | **`WS-EXIT-RETRY-LOOP`**<br/><small>`WS-EXIT-RETRY-LOOP`</small> | Alphanumeric (1 chars) | `X` | 383 | 1 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 384 | 16 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 384 | 4 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`ENQ-NAMED-COUNTER`<br/><small>*ENC010*</small><br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 388 | 4 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;`WS-EIBRESP-DISPLAY`<br/><small>`WS-CICS-WORK-AREA.WS-EIBRESP-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 392 | 8 | — | — |
| 01 | **`WS-CUSTOMER-NO-NUM`**<br/><small>`WS-CUSTOMER-NO-NUM`</small> | Numeric Display (10 digits) | `9(10)` | 400 | 10 | — | — |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 100 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-EYECATCHER`<br/><small>`DFHCOMMAREA.COMM-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.COMM-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 4 | 10 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CUSTOMER-ACCOUNT-COUNT`<br/><small>*CAC010*</small> |
| 03 | &nbsp;&nbsp;`COMM-KEY`<br/><small>`DFHCOMMAREA.COMM-KEY`</small> | Group | *DISPLAY* | 14 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-SORTCODE`<br/><small>`DFHCOMMAREA.COMM-KEY.COMM-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 14 | 6 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NUMBER`<br/><small>`DFHCOMMAREA.COMM-KEY.COMM-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 20 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`DFHCOMMAREA.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 28 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`ACCOUNT-TYPE-CHECK`<br/><small>*ATC010*</small> |
| 03 | &nbsp;&nbsp;`COMM-INT-RT`<br/><small>`DFHCOMMAREA.COMM-INT-RT`</small> | Decimal Display (6, 2) | `9(4)V99` | 36 | 6 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-OPENED`<br/><small>`DFHCOMMAREA.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 42 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 42 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 42 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 44 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 46 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-OVERDR-LIM`<br/><small>`DFHCOMMAREA.COMM-OVERDR-LIM`</small> | Numeric Display (8 digits) | `9(8)` | 50 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 58 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-LAST-STMNT-GROUP`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP`</small> | Group | *DISPLAY* | 58 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-DAY`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-DAY`</small> | Numeric Display (2 digits) | `99` | 58 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-MONTH`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-MONTH`</small> | Numeric Display (2 digits) | `99` | 60 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-YEAR`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-YEAR`</small> | Numeric Display (4 digits) | `9999` | 62 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 66 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-NEXT-STMNT-GROUP`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP`</small> | Group | *DISPLAY* | 66 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-DAY`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-DAY`</small> | Numeric Display (2 digits) | `99` | 66 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-MONTH`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-MONTH`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-YEAR`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-YEAR`</small> | Numeric Display (4 digits) | `9999` | 70 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`DFHCOMMAREA.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 74 | 12 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACT-BAL`<br/><small>`DFHCOMMAREA.COMM-ACT-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 86 | 12 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 98 | 1 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`ENQ-NAMED-COUNTER`<br/><small>*ENC010*</small><br/>*( +3 more)* |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`DFHCOMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 99 | 1 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`ENQ-NAMED-COUNTER`<br/><small>*ENC010*</small><br/>*( +3 more)* |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`FILE-RETRY`**<br/><small>`FILE-RETRY`</small> | Numeric Display (3 digits) | `999` | 0 | 3 | — | — |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 3 | 98 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 3 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 3 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 7 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 17 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 17 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 23 | 8 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 31 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 39 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 45 | 8 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 45 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 45 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 47 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 49 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 53 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 61 | 8 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 61 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 61 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 63 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 65 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 69 | 8 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 69 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 69 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 71 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 73 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 77 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 89 | 12 | — | — |
| 01 | **`OUTPUTC-DATA`**<br/><small>`OUTPUTC-DATA`</small> | Group | *DISPLAY* | 101 | 397 | — | — |
| 03 | &nbsp;&nbsp;`CUSTOMER-RECORD`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD`</small> | Group | *DISPLAY* | 101 | 397 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-EYECATCHER`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 101 | 4 | • `88 CUSTOMER-EYECATCHER-VALUE`: 'CUST' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-KEY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-KEY`</small> | Group | *DISPLAY* | 105 | 16 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-SORTCODE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 105 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 111 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NAME`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-NAME`</small> | Group | *DISPLAY* | 121 | 110 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-TITLE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 121 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-FIRST-NAME`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 131 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-LAST-NAME`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 181 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-DOB`</small> | Group | *DISPLAY* | 231 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-DAY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 231 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-MONTH`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 233 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-YEAR`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 235 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-PHONE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 239 | 20 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDRESS`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS`</small> | Group | *DISPLAY* | 259 | 210 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE1`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 259 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE2`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 309 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CITY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 359 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-POSTCODE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 409 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-COUNTRY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 419 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-STATUS`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 469 | 10 | • `88 CUSTOMER-STATUS-ACTIVE`: 'ACTIVE'<br/>• `88 CUSTOMER-STATUS-INACTIVE`: 'INACTIVE'<br/>• `88 CUSTOMER-STATUS-SUSPENDED`: 'SUSPENDED' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DATE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE`</small> | Group | *DISPLAY* | 479 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DAY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 479 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-MONTH`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 481 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-YEAR`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 483 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREDIT-SCORE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 487 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DATE`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 490 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DAY`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 490 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-MONTH`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 492 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-YEAR`<br/><small>`OUTPUTC-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 494 | 4 | — | — |
| 01 | **`RETURN-DATA`**<br/><small>`RETURN-DATA`</small> | Group | *DISPLAY* | 498 | 242 | — | — |
| 03 | &nbsp;&nbsp;`RETURN-DATA-EYECATCHER`<br/><small>`RETURN-DATA.RETURN-DATA-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 498 | 4 | — | — |
| 03 | &nbsp;&nbsp;`RETURN-DATA-NUMBER`<br/><small>`RETURN-DATA.RETURN-DATA-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 502 | 10 | — | — |
| 03 | &nbsp;&nbsp;`RETURN-DATA-NAME`<br/><small>`RETURN-DATA.RETURN-DATA-NAME`</small> | Alphanumeric (60 chars) | `X(60)` | 512 | 60 | — | — |
| 03 | &nbsp;&nbsp;`RETURN-DATA-ADDRESS`<br/><small>`RETURN-DATA.RETURN-DATA-ADDRESS`</small> | Alphanumeric (160 chars) | `X(160)` | 572 | 160 | — | — |
| 03 | &nbsp;&nbsp;`RETURN-DATA-DATE-OF-BIRTH`<br/><small>`RETURN-DATA.RETURN-DATA-DATE-OF-BIRTH`</small> | Numeric Display (8 digits) | `9(8)` | 732 | 8 | — | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 740 | 16 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 740 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-CUST-NUMBER`<br/><small>`CUSTOMER-KY.REQUIRED-CUST-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 746 | 10 | **Default:** `0` | — |
| 01 | **`ACCOUNT-KY`**<br/><small>`ACCOUNT-KY`</small> | Group | *DISPLAY* | 756 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE2`<br/><small>`ACCOUNT-KY.REQUIRED-SORT-CODE2`</small> | Numeric Display (6 digits) | `9(6)` | 756 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUMBER`<br/><small>`ACCOUNT-KY.REQUIRED-ACC-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 762 | 8 | **Default:** `0` | — |
| 01 | **`RANDOM-CUSTOMER`**<br/><small>`RANDOM-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 770 | 10 | **Default:** `0` | — |
| 01 | **`HIGHEST-CUST-NUMBER`**<br/><small>`HIGHEST-CUST-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 780 | 10 | **Default:** `0` | — |
| 01 | **`EXIT-VSAM-READ`**<br/><small>`EXIT-VSAM-READ`</small> | Alphanumeric (1 chars) | `X` | 790 | 1 | **Default:** `N` | — |
| 01 | **`EXIT-DB2-READ`**<br/><small>`EXIT-DB2-READ`</small> | Alphanumeric (1 chars) | `X` | 791 | 1 | **Default:** `N` | — |
| 01 | **`WS-V-RETRIED`**<br/><small>`WS-V-RETRIED`</small> | Alphanumeric (1 chars) | `X` | 792 | 1 | **Default:** `N` | — |
| 01 | **`WS-D-RETRIED`**<br/><small>`WS-D-RETRIED`</small> | Alphanumeric (1 chars) | `X` | 793 | 1 | **Default:** `N` | — |
| 01 | **`WS-ERROR`**<br/><small>`WS-ERROR`</small> | Alphanumeric (40 chars) | `X(40)` | 794 | 40 | **Default:** `ALL '#'` | — |
| 01 | **`NCS-ACC-NO-STUFF`**<br/><small>`NCS-ACC-NO-STUFF`</small> | Group | *DISPLAY* | 834 | 35 | — | — |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-NAME`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME`</small> | Group | *DISPLAY* | 834 | 17 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-ACT-NAME`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-ACT-NAME`</small> | Alphanumeric (9 chars) | `X(9)` | 834 | 9 | **Default:** `BANKZACCT` | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-TEST-SORT`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-TEST-SORT`</small> | Alphanumeric (6 chars) | `X(6)` | 843 | 6 | — | `ENQ-NAMED-COUNTER`<br/><small>*ENC010*</small><br/>&nbsp;<br/>`DEQ-NAMED-COUNTER`<br/><small>*DNC010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-FILL`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-FILL`</small> | Alphanumeric (2 chars) | `XX` | 849 | 2 | — | — |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-INC`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-INC`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 851 | 8 | **Default:** `0` | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-VALUE`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-VALUE`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 859 | 8 | **Default:** `0` | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-RESP`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-RESP`</small> | Alphanumeric (2 chars) | `XX` | 867 | 2 | **Default:** `00` | — |
| 01 | **`WS-DISP-CUST-NO-VAL`**<br/><small>`WS-DISP-CUST-NO-VAL`</small> | Signed Numeric Display (18 digits) | `S9(18)` | 869 | 18 | — | — |
| 01 | **`WS-ACC-REC-LEN`**<br/><small>`WS-ACC-REC-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 887 | 2 | **Default:** `0` | — |
| 01 | **`NCS-UPDATED`**<br/><small>`NCS-UPDATED`</small> | Alphanumeric (1 chars) | `X` | 889 | 1 | **Default:** `N` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 890 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 898 | 10 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 898 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 898 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 900 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 901 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 903 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 904 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`DONT-CARE`**<br/><small>`DONT-CARE`</small> | Unsigned Integer (32-bit Binary) | `9(8)`<br/>*BINARY* | 908 | 4 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`LEAP-YEAR`**<br/><small>`LEAP-YEAR`</small> | Unsigned Integer (32-bit Binary) | `9(8)`<br/>*BINARY* | 912 | 4 | — | `CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 916 | 10 | — | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 916 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 918 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 919 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 921 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 922 | 4 | — | — |
| 01 | **`WS-STDT-X`**<br/><small>`WS-STDT-X`</small> | Alphanumeric (8 chars) | `X(8)` | 926 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-STDT-9`**<br/><small>`WS-STDT-9`</small> | Group | *DISPLAY* | 926 | 8 | <mark>REDEFINES WS-STDT-X</mark> | — |
| 03 | &nbsp;&nbsp;`WS-STDT-9-NUM`<br/><small>`WS-STDT-9.WS-STDT-9-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 926 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-STDT-9-NUMERIC`**<br/><small>`WS-STDT-9-NUMERIC`</small> | Numeric Display (8 digits) | `9(8)` | 934 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-INTEGER`**<br/><small>`WS-INTEGER`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 942 | 4 | **Default:** `0` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-FUTURE-DATE`**<br/><small>`WS-FUTURE-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 946 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`CALCULATE-DATES`<br/><small>*CD010*</small> |
| 01 | **`WS-FUT`**<br/><small>`WS-FUT`</small> | Group | *DISPLAY* | 946 | 8 | <mark>REDEFINES WS-FUTURE-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-FUTURE-YY`<br/><small>`WS-FUT.WS-FUTURE-YY`</small> | Numeric Display (4 digits) | `9(4)` | 946 | 4 | — | — |
| 03 | &nbsp;&nbsp;`WS-FUTURE-MM`<br/><small>`WS-FUT.WS-FUTURE-MM`</small> | Numeric Display (2 digits) | `99` | 950 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-FUTURE-DD`<br/><small>`WS-FUT.WS-FUTURE-DD`</small> | Numeric Display (2 digits) | `99` | 952 | 2 | — | — |
| 01 | **`WS-FUTURE-CONV`**<br/><small>`WS-FUTURE-CONV`</small> | Group | *DISPLAY* | 954 | 8 | — | — |
| 03 | &nbsp;&nbsp;`WS-FUT-9`<br/><small>`WS-FUTURE-CONV.WS-FUT-9`</small> | Numeric Display (8 digits) | `9(8)` | 954 | 8 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 03 | &nbsp;&nbsp;`WS-FUT-X`<br/><small>`WS-FUTURE-CONV.WS-FUT-X`</small> | Group | *DISPLAY* | 954 | 8 | <mark>REDEFINES WS-FUT-9</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-FUT-X-YY`<br/><small>`WS-FUTURE-CONV.WS-FUT-X.WS-FUT-X-YY`</small> | Alphanumeric (4 chars) | `X(4)` | 954 | 4 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-FUT-X-MM`<br/><small>`WS-FUTURE-CONV.WS-FUT-X.WS-FUT-X-MM`</small> | Alphanumeric (2 chars) | `XX` | 958 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-FUT-X-DD`<br/><small>`WS-FUTURE-CONV.WS-FUT-X.WS-FUT-X-DD`</small> | Alphanumeric (2 chars) | `XX` | 960 | 2 | — | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 01 | **`NCS-ACC-NO-DISP`**<br/><small>`NCS-ACC-NO-DISP`</small> | Numeric Display (16 digits) | `9(16)` | 962 | 16 | **Default:** `0` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 01 | **`STORED-SORTCODE`**<br/><small>`STORED-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 978 | 6 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small> |
| 01 | **`STORED-CUSTNO`**<br/><small>`STORED-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 984 | 10 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`STORED-ACCTYPE`**<br/><small>`STORED-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 994 | 8 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`STORED-LST-STMT`**<br/><small>`STORED-LST-STMT`</small> | Alphanumeric (8 chars) | `X(8)` | 1002 | 8 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`STORED-NXT-STMT`**<br/><small>`STORED-NXT-STMT`</small> | Alphanumeric (8 chars) | `X(8)` | 1010 | 8 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`STORED-ACCNO`**<br/><small>`STORED-ACCNO`</small> | Alphanumeric (8 chars) | `X(8)` | 1018 | 8 | **Default:** `SPACES` | `WRITE-ACCOUNT-DB2`<br/><small>*WAD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 1026 | 12 | **Default:** `0` | `WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 01 | **`ACCOUNT-KY3`**<br/><small>`ACCOUNT-KY3`</small> | Group | *DISPLAY* | 1038 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE3`<br/><small>`ACCOUNT-KY3.REQUIRED-SORT-CODE3`</small> | Numeric Display (6 digits) | `9(6)` | 1038 | 6 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`REQUIRED-ACCT-NUMBER3`<br/><small>`ACCOUNT-KY3.REQUIRED-ACCT-NUMBER3`</small> | Numeric Display (8 digits) | `9(8)` | 1044 | 8 | **Default:** `0` | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small> |
| 01 | **`ACCOUNT-KY3-BYTES`**<br/><small>`ACCOUNT-KY3-BYTES`</small> | Alphanumeric (14 chars) | `X(14)` | 1038 | 14 | <mark>REDEFINES ACCOUNT-KY3</mark> | — |
| 01 | **`INQCUST-COMMAREA`**<br/><small>`INQCUST-COMMAREA`</small> | Group | *DISPLAY* | 1052 | 403 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-EYE`<br/><small>`INQCUST-COMMAREA.INQCUST-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 1052 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-SCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 1056 | 6 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CUSTNO`<br/><small>`INQCUST-COMMAREA.INQCUST-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 1062 | 10 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME`</small> | Group | *DISPLAY* | 1072 | 110 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-TITLE`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 1072 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-FIRST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 1082 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-LAST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 1132 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-DOB`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB`</small> | Group | *DISPLAY* | 1182 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 1182 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 1184 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1186 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PHONE`<br/><small>`INQCUST-COMMAREA.INQCUST-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 1190 | 20 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-ADDR`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR`</small> | Group | *DISPLAY* | 1210 | 210 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE1`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 1210 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE2`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 1260 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CITY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 1310 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-POSTCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 1360 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-COUNTRY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 1370 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-STATUS`<br/><small>`INQCUST-COMMAREA.INQCUST-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 1420 | 10 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREATED-DATE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE`</small> | Group | *DISPLAY* | 1430 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-DD`</small> | Numeric Display (2 digits) | `99` | 1430 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-MM`</small> | Numeric Display (2 digits) | `99` | 1432 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1434 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREDIT-SCORE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 1438 | 3 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CS-REVIEW-DT`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT`</small> | Group | *DISPLAY* | 1441 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-DD`</small> | Numeric Display (2 digits) | `99` | 1441 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-MM`</small> | Numeric Display (2 digits) | `99` | 1443 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1445 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-SUCCESS`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1449 | 1 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-FAIL-CD`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 1450 | 1 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PCB-POINTER`<br/><small>`INQCUST-COMMAREA.INQCUST-PCB-POINTER`</small> | Alphanumeric (4 chars) | `X(4)` | 1451 | 4 | — | — |
| 01 | **`INQACCCU-COMMAREA`**<br/><small>`INQACCCU-COMMAREA`</small> | Group | *DISPLAY* | 1455 | 1981 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`INQACCCU-COMMAREA.NUMBER-OF-ACCOUNTS`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 1455 | 4 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`CUSTOMER-ACCOUNT-COUNT`<br/><small>*CAC010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`INQACCCU-COMMAREA.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 1459 | 10 | — | `CUSTOMER-ACCOUNT-COUNT`<br/><small>*CAC010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`INQACCCU-COMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1469 | 1 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`INQACCCU-COMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 1470 | 1 | — | — |
| 03 | &nbsp;&nbsp;`CUSTOMER-FOUND`<br/><small>`INQACCCU-COMMAREA.CUSTOMER-FOUND`</small> | Alphanumeric (1 chars) | `X` | 1471 | 1 | — | — |
| 03 | &nbsp;&nbsp;`COMM-PCB-POINTER`<br/><small>`INQACCCU-COMMAREA.COMM-PCB-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 1472 | 4 | — | `CUSTOMER-ACCOUNT-COUNT`<br/><small>*CAC010*</small> |
| 03 | &nbsp;&nbsp;`ACCOUNT-DETAILS`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS`</small> | Group Array [20] | *DISPLAY* | 1476 | 1960 | **OCCURS:** 1 TO 20 (DEPENDING ON NUMBER-OF-ACCOUNTS IN INQACCCU-COMMAREA) | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-EYE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 1476 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 1480 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-SCODE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 1490 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACCNO`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 1496 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1504 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-INT-RATE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 1512 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 1518 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 1518 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 1518 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 1520 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1522 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OVERDRAFT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 1526 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1534 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 1534 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 1534 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 1536 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1538 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1542 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 1542 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 1542 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 1544 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1546 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1550 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACTUAL-BAL`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1562 | 12 | — | — |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 3436 | 20 | — | — |
| 01 | **`ACCOUNT-CONTROL`**<br/><small>`ACCOUNT-CONTROL`</small> | Group | *DISPLAY* | 3456 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-CONTROL-RECORD`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD`</small> | Group | *DISPLAY* | 3456 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-EYE-CATCHER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 3456 | 4 | • `88 ACCOUNT-CONTROL-EYECATCHER-V`: 'CTRL' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (10 digits) | `9(10)` | 3460 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-KEY`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY`</small> | Group | *DISPLAY* | 3470 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-SORT-CODE`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY.ACCOUNT-CONTROL-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 3470 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-NUMBER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-KEY.ACCOUNT-CONTROL-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 3476 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.NUMBER-OF-ACCOUNTS`</small> | Numeric Display (8 digits) | `9(8)` | 3484 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`LAST-ACCOUNT-NUMBER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.LAST-ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 3492 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-SUCCESS-FLAG`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-SUCCESS-FLAG`</small> | Alphanumeric (1 chars) | `X` | 3500 | 1 | • `88 ACCOUNT-CONTROL-SUCCESS`: 'Y' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CONTROL-FAIL-CODE`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.ACCOUNT-CONTROL-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 3501 | 1 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Decimal Display (6, 2) | `9(4)V99` | 3502 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 3508 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 3516 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 3524 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Numeric Display (8 digits) | `9(8)` | 3532 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 3540 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`ACCOUNT-CONTROL.ACCOUNT-CONTROL-RECORD.FILLER`</small> | Alphanumeric (2 chars) | `X(2)` | 3552 | 2 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 3554 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 3554 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 3554 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 3554 | 2 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 3556 | 2 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 3558 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 3560 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 3568 | 678 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 3568 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 3568 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 3576 | 4 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 3580 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 3588 | 4 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 3592 | 10 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 3602 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 3610 | 4 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 3614 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 3622 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 3630 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 3638 | 8 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 3646 | 600 | — | `FIND-NEXT-ACCOUNT`<br/><small>*FNA010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-DB2`<br/><small>*WPD010*</small> |

