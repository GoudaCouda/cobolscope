# Data Dictionary: `XFRFUN`

**Source File:** `C:\Users\austi\cobolscope\tests\fixtures\bank_of_z\cobol\XFRFUN.cbl`  
**Author:** *>CE Jon Collett. *>CE  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 261 |
| **Level-88 Business Rules** | 29 |
| **Memory Overlays (REDEFINES)** | 16 |
| **Working-Storage Span** | 192 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | <small>*PREMIERE*</small><br/>`A010` |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 6 | 88 | — | <small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | <small>*PREMIERE*</small><br/>`A010` |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-KEY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY`</small> | Group | *DISPLAY* | 20 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 20 | 6 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 26 | 8 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 34 | 8 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 42 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 46 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 56 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 60 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 70 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 80 | 7 | — | <small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 87 | 7 | — | <small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 94 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 94 | 96 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 94 | 4 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORT-CODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORT-CODE`</small> | Alphanumeric (6 chars) | `X(6)` | 98 | 6 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-ACC-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-ACC-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 104 | 8 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 112 | 10 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 122 | 6 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 128 | 12 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 140 | 3 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 143 | 40 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 183 | 7 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 190 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 190 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 190 | 4 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>&nbsp;<br/><small>*ABEND-HANDLING*</small><br/>`AH010` |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 194 | 4 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>&nbsp;<br/><small>*ABEND-HANDLING*</small><br/>`AH010` |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 90 | — | — |
| 03 | &nbsp;&nbsp;`COMM-FACCNO`<br/><small>`DFHCOMMAREA.COMM-FACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 0 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>&nbsp;<br/><small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`COMM-FSCODE`<br/><small>`DFHCOMMAREA.COMM-FSCODE`</small> | Numeric Display (6 digits) | `9(6)` | 8 | 6 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-TACCNO`<br/><small>`DFHCOMMAREA.COMM-TACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 14 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>&nbsp;<br/><small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`COMM-TSCODE`<br/><small>`DFHCOMMAREA.COMM-TSCODE`</small> | Numeric Display (6 digits) | `9(6)` | 22 | 6 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-AMT`<br/><small>`DFHCOMMAREA.COMM-AMT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 28 | 12 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-FAVBAL`<br/><small>`DFHCOMMAREA.COMM-FAVBAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 40 | 12 | — | <small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010` |
| 03 | &nbsp;&nbsp;`COMM-FACTBAL`<br/><small>`DFHCOMMAREA.COMM-FACTBAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 52 | 12 | — | <small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010` |
| 03 | &nbsp;&nbsp;`COMM-TAVBAL`<br/><small>`DFHCOMMAREA.COMM-TAVBAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 64 | 12 | — | <small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 03 | &nbsp;&nbsp;`COMM-TACTBAL`<br/><small>`DFHCOMMAREA.COMM-TACTBAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 76 | 12 | — | <small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`DFHCOMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 88 | 1 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>*( +3 more)* |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 89 | 1 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>*( +3 more)* |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`SYSIDERR-RETRY`**<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 0 | 3 | — | — |
| 01 | **`FILE-RETRY`**<br/><small>`FILE-RETRY`</small> | Numeric Display (3 digits) | `999` | 3 | 3 | — | — |
| 01 | **`WS-EXIT-RETRY-LOOP`**<br/><small>`WS-EXIT-RETRY-LOOP`</small> | Alphanumeric (1 chars) | `X` | 6 | 1 | — | — |
| 01 | **`DB2-DEADLOCK-RETRY`**<br/><small>`DB2-DEADLOCK-RETRY`</small> | Numeric Display (3 digits) | `999` | 7 | 3 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 10 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 10 | 4 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 14 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 15 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 17 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 18 | 2 | — | — |
| 01 | **`WS-ACC-DATA`**<br/><small>`WS-ACC-DATA`</small> | Group | *DISPLAY* | 20 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 20 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 20 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 24 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 34 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 34 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 40 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 48 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 56 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 62 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 62 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 62 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 64 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 66 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 70 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 78 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 78 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 78 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 80 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 82 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 86 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 86 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 86 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 88 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 90 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 94 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 106 | 12 | — | — |
| 01 | **`WS-ACC-DATA2`**<br/><small>`WS-ACC-DATA2`</small> | Group | *DISPLAY* | 118 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 118 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 118 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 122 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 132 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 132 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 138 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 146 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 154 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 160 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 160 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 160 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 162 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 164 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 168 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 176 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 176 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 176 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 178 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 180 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 184 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 184 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 184 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 186 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 188 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 192 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`WS-ACC-DATA2.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 204 | 12 | — | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 216 | 12 | **Default:** `0` | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 01 | **`WS-SQLCODE-DISP`**<br/><small>`WS-SQLCODE-DISP`</small> | Numeric Display (9 digits) | `9(9)` | 228 | 9 | **Default:** `0` | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 01 | **`DESIRED-ACC-KEY`**<br/><small>`DESIRED-ACC-KEY`</small> | Group | *DISPLAY* | 237 | 14 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-SORT-CODE`<br/><small>`DESIRED-ACC-KEY.DESIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 237 | 6 | — | <small>*PREMIERE*</small><br/>`A010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`DESIRED-ACC-NO`<br/><small>`DESIRED-ACC-KEY.DESIRED-ACC-NO`</small> | Numeric Display (8 digits) | `9(8)` | 243 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-FROM*</small><br/>`UADF010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010` |
| 01 | **`NEW-ACCOUNT-AVAILABLE-BALANCE`**<br/><small>`NEW-ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 251 | 12 | **Default:** `0` | — |
| 01 | **`NEW-ACCOUNT-ACTUAL-BALANCE`**<br/><small>`NEW-ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 263 | 12 | **Default:** `0` | — |
| 01 | **`WS-ACC-REC-LEN`**<br/><small>`WS-ACC-REC-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 275 | 2 | **Default:** `0` | — |
| 01 | **`NEW-ACCOUNT-AVAILABLE-BALANCE2`**<br/><small>`NEW-ACCOUNT-AVAILABLE-BALANCE2`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 277 | 12 | **Default:** `0` | — |
| 01 | **`NEW-ACCOUNT-ACTUAL-BALANCE2`**<br/><small>`NEW-ACCOUNT-ACTUAL-BALANCE2`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 289 | 12 | **Default:** `0` | — |
| 01 | **`WS-ACC-REC-LEN2`**<br/><small>`WS-ACC-REC-LEN2`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 301 | 2 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 303 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 311 | 10 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 311 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 311 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 313 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 314 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 316 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 317 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 321 | 10 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 321 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 323 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 324 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 326 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 327 | 4 | — | — |
| 01 | **`REJ-REASON`**<br/><small>`REJ-REASON`</small> | Alphanumeric (2 chars) | `XX` | 331 | 2 | **Default:** `SPACES` | — |
| 01 | **`PROCTRAN-AREA`**<br/><small>`PROCTRAN-AREA`</small> | Group | *DISPLAY* | 333 | 99 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`PROC-TRAN-DATA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA`</small> | Group | *DISPLAY* | 333 | 99 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-EYE-CATCHER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 333 | 4 | • `88 PROC-TRAN-VALID`: 'PRTR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-AREA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA`</small> | Group | *DISPLAY* | 333 | 4 | <mark>REDEFINES PROC-TRAN-EYE-CATCHER</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-FLAG`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.PROC-TRAN-LOGICAL-DELETE-FLAG`</small> | Alphanumeric (1 chars) | `X` | 333 | 1 | • `88 PROC-TRAN-LOGICALLY-DELETED`: 'X'FF'' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.FILLER`</small> | Alphanumeric (3 chars) | `X(3)` | 334 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-ID`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID`</small> | Group | *DISPLAY* | 337 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-SORT-CODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 337 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-NUMBER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 343 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 351 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 351 | 8 | <mark>REDEFINES PROC-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-YYYY`</small> | Numeric Display (4 digits) | `9999` | 351 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 355 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-DD`</small> | Numeric Display (2 digits) | `99` | 357 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 359 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 359 | 6 | <mark>REDEFINES PROC-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-HH`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 359 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 361 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-SS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 363 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-REF`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 365 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 377 | 3 | • `88 PROC-TY-CHEQUE-ACKNOWLEDGED`: 'CHA'<br/>• `88 PROC-TY-CHEQUE-FAILURE`: 'CHF'<br/>• `88 PROC-TY-CHEQUE-PAID-IN`: 'CHI'<br/>• `88 PROC-TY-CHEQUE-PAID-OUT`: 'CHO'<br/>• `88 PROC-TY-CREDIT`: 'CRE'<br/>• `88 PROC-TY-DEBIT`: 'DEB'<br/>• `88 PROC-TY-WEB-CREATE-ACCOUNT`: 'ICA'<br/>• `88 PROC-TY-WEB-CREATE-CUSTOMER`: 'ICC'<br/>• `88 PROC-TY-WEB-DELETE-ACCOUNT`: 'IDA'<br/>• `88 PROC-TY-WEB-DELETE-CUSTOMER`: 'IDC'<br/>• `88 PROC-TY-BRANCH-CREATE-ACCOUNT`: 'OCA'<br/>• `88 PROC-TY-BRANCH-CREATE-CUSTOMER`: 'OCC'<br/>• `88 PROC-TY-BRANCH-DELETE-ACCOUNT`: 'ODA'<br/>• `88 PROC-TY-BRANCH-DELETE-CUSTOMER`: 'ODC'<br/>• `88 PROC-TY-CREATE-SODD`: 'OCS'<br/>• `88 PROC-TY-PAYMENT-CREDIT`: 'PCR'<br/>• `88 PROC-TY-PAYMENT-DEBIT`: 'PDR'<br/>• `88 PROC-TY-TRANSFER`: 'TFR' | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 380 | 40 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR`</small> | Group | *DISPLAY* | 380 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-HEADER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-HEADER`</small> | Alphanumeric (26 chars) | `X(26)` | 380 | 26 | • `88 PROC-TRAN-DESC-XFR-FLAG`: 'TRANSFER' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 406 | 6 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-ACCOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-ACCOUNT`</small> | Numeric Display (8 digits) | `9(8)` | 412 | 8 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC`</small> | Group | *DISPLAY* | 380 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 380 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 390 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 398 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 400 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 402 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 406 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 408 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 410 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 414 | 6 | • `88 PROC-DESC-DELACC-FLAG`: 'DELETE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CREACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC`</small> | Group | *DISPLAY* | 380 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 380 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 390 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 398 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 400 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 402 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 406 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 408 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 410 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 414 | 6 | • `88 PROC-DESC-CREACC-FLAG`: 'CREATE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELCUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS`</small> | Group | *DISPLAY* | 380 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 380 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 386 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 396 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 410 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 414 | 1 | • `88 PROC-DESC-DELCUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 415 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 417 | 1 | • `88 PROC-DESC-DELCUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 418 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CRECUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS`</small> | Group | *DISPLAY* | 380 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 380 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 386 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 396 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 410 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 414 | 1 | • `88 PROC-DESC-CRECUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 415 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 417 | 1 | • `88 PROC-DESC-CRECUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 418 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-AMOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 420 | 12 | — | — |
| 01 | **`REJTRAN-RIDFLD`**<br/><small>`REJTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 432 | 4 | — | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 436 | 4 | — | — |
| 01 | **`WS-REJ-REAS`**<br/><small>`WS-REJ-REAS`</small> | Group | *DISPLAY* | 440 | 40 | — | — |
| 03 | &nbsp;&nbsp;`WS-REASON-TEXT`<br/><small>`WS-REJ-REAS.WS-REASON-TEXT`</small> | Alphanumeric (26 chars) | `X(26)` | 440 | 26 | **Default:** `SPACES` | — |
| 03 | &nbsp;&nbsp;`WS-TO-ACC`<br/><small>`WS-REJ-REAS.WS-TO-ACC`</small> | Numeric Display (14 digits) | `9(14)` | 466 | 14 | **Default:** `0` | — |
| 01 | **`WS-PROC-REAS`**<br/><small>`WS-PROC-REAS`</small> | Group | *DISPLAY* | 480 | 40 | — | — |
| 03 | &nbsp;&nbsp;`WS-PROC-TEXT`<br/><small>`WS-PROC-REAS.WS-PROC-TEXT`</small> | Alphanumeric (26 chars) | `X(26)` | 480 | 26 | **Default:** `SPACES` | — |
| 03 | &nbsp;&nbsp;`WS-PROC-TO`<br/><small>`WS-PROC-REAS.WS-PROC-TO`</small> | Numeric Display (14 digits) | `9(14)` | 506 | 14 | **Default:** `0` | — |
| 01 | **`WS-TESTING-DB-NAME`**<br/><small>`WS-TESTING-DB-NAME`</small> | Group | *DISPLAY* | 520 | 13 | — | — |
| 03 | &nbsp;&nbsp;`WS-TESTING-TYPE`<br/><small>`WS-TESTING-DB-NAME.WS-TESTING-TYPE`</small> | Alphanumeric (9 chars) | `X(9)` | 520 | 9 | **Default:** `STTESTER.` | — |
| 03 | &nbsp;&nbsp;`WS-TESTING-TABLE-NAME`<br/><small>`WS-TESTING-DB-NAME.WS-TESTING-TABLE-NAME`</small> | Alphanumeric (4 chars) | `X(4)` | 529 | 4 | **Default:** `PLOP` | — |
| 01 | **`WS-SQLCODE1`**<br/><small>`WS-SQLCODE1`</small> | Numeric Display (15 digits) | `9(15)` | 533 | 15 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 548 | 0 | — | — |
| 01 | **`STMTBUF`**<br/><small>`STMTBUF`</small> | Group | *DISPLAY* | 548 | 80 | — | — |
| 49 | &nbsp;&nbsp;`STMTLEN`<br/><small>`STMTBUF.STMTLEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 548 | 2 | **Default:** `+78` | — |
| 49 | &nbsp;&nbsp;`STMTTXT`<br/><small>`STMTBUF.STMTTXT`</small> | Alphanumeric (78 chars) | `X(78)` | 550 | 78 | — | — |
| 01 | **`STMTBUF2`**<br/><small>`STMTBUF2`</small> | Group | *DISPLAY* | 628 | 83 | — | — |
| 49 | &nbsp;&nbsp;`STMTLEN2`<br/><small>`STMTBUF2.STMTLEN2`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 628 | 2 | **Default:** `+81` | — |
| 49 | &nbsp;&nbsp;`STMTTXT2`<br/><small>`STMTBUF2.STMTTXT2`</small> | Alphanumeric (81 chars) | `X(81)` | 630 | 81 | — | — |
| 01 | **`DISP-LOT`**<br/><small>`DISP-LOT`</small> | Group | *DISPLAY* | 711 | 5 | — | — |
| 03 | &nbsp;&nbsp;`DISP-SIGN`<br/><small>`DISP-LOT.DISP-SIGN`</small> | Alphanumeric (1 chars) | `X` | 711 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DISP-SQLCD`<br/><small>`DISP-LOT.DISP-SQLCD`</small> | Numeric Display (4 digits) | `9999` | 712 | 4 | — | — |
| 01 | **`WS-WANTED`**<br/><small>`WS-WANTED`</small> | Group | *DISPLAY* | 716 | 80 | — | — |
| 03 | &nbsp;&nbsp;`VAR-LEN`<br/><small>`WS-WANTED.VAR-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 716 | 2 | **Default:** `+78` | — |
| 03 | &nbsp;&nbsp;`VAR-TXT`<br/><small>`WS-WANTED.VAR-TXT`</small> | Alphanumeric (78 chars) | `X(78)` | 718 | 78 | — | — |
| 01 | **`WS-WANTED2`**<br/><small>`WS-WANTED2`</small> | Group | *DISPLAY* | 796 | 83 | — | — |
| 03 | &nbsp;&nbsp;`VAR-LEN2`<br/><small>`WS-WANTED2.VAR-LEN2`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 796 | 2 | **Default:** `+81` | — |
| 03 | &nbsp;&nbsp;`VAR-TXT2`<br/><small>`WS-WANTED2.VAR-TXT2`</small> | Alphanumeric (81 chars) | `X(81)` | 798 | 81 | — | — |
| 01 | **`WS-INPUT-TAB-NAME`**<br/><small>`WS-INPUT-TAB-NAME`</small> | Alphanumeric (4 chars) | `X(4)` | 879 | 4 | — | — |
| 01 | **`WS-INPUT-TAB-NAME2`**<br/><small>`WS-INPUT-TAB-NAME2`</small> | Alphanumeric (7 chars) | `X(7)` | 883 | 7 | — | — |
| 01 | **`WS-PASSED-DATA`**<br/><small>`WS-PASSED-DATA`</small> | Group | *DISPLAY* | 890 | 13 | — | — |
| 02 | &nbsp;&nbsp;`WS-TEST-KEY`<br/><small>`WS-PASSED-DATA.WS-TEST-KEY`</small> | Alphanumeric (4 chars) | `X(4)` | 890 | 4 | — | — |
| 02 | &nbsp;&nbsp;`WS-SORT-CODE`<br/><small>`WS-PASSED-DATA.WS-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 894 | 6 | — | — |
| 02 | &nbsp;&nbsp;`WS-CUSTOMER-RANGE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE`</small> | Group | *DISPLAY* | 900 | 3 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-TOP`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-TOP`</small> | Alphanumeric (1 chars) | `X` | 900 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-MIDDLE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-MIDDLE`</small> | Alphanumeric (1 chars) | `X` | 901 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-BOTTOM`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-BOTTOM`</small> | Alphanumeric (1 chars) | `X` | 902 | 1 | — | — |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 903 | 4 | — | <small>*ABEND-HANDLING*</small><br/>`AH010` |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 907 | 1 | **Default:** `N` | <small>*ABEND-HANDLING*</small><br/>`AH010` |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 908 | 20 | — | <small>*CHECK-FOR-STORM-DRAIN-DB2*</small><br/>`CFSDD010` |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 928 | 8 | — | <small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>&nbsp;<br/><small>*CHECK-FOR-STORM-DRAIN-DB2*</small><br/>`CFSDD010`<br/>&nbsp;<br/><small>*ABEND-HANDLING*</small><br/>`AH010` |
| 01 | **`NUMERIC-AMOUNT-DISPLAY`**<br/><small>`NUMERIC-AMOUNT-DISPLAY`</small> | Decimal Display (13, 2) | `+9(10).99` | 936 | 14 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 950 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 950 | 6 | — | <small>*WRITE-TO-PROCTRAN-DB2*</small><br/>`WTPD010` |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 950 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 950 | 2 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 952 | 2 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 954 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 956 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 964 | 678 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 964 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 964 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 972 | 4 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 976 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 984 | 4 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 988 | 10 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 998 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 1006 | 4 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 1010 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1018 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1026 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1034 | 8 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 1042 | 600 | — | <small>*UPDATE-ACCOUNT-DB2*</small><br/>`UAD010`<br/>&nbsp;<br/><small>*UPDATE-ACCOUNT-DB2-TO*</small><br/>`UADT010`<br/>*( +2 more)* |

