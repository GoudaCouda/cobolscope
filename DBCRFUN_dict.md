# Data Dictionary: `DBCRFUN`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 207 |
| **Level-88 Business Rules** | 31 |
| **Memory Overlays (REDEFINES)** | 13 |
| **Working-Storage Span** | 201 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small> |
| 77 | `SYSIDERR-RETRY`<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 9 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 9 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 9 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 13 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-KEY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY`</small> | Group | *DISPLAY* | 23 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 23 | 6 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 29 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 37 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 45 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 49 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 59 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 63 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 73 | 10 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 83 | 7 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 90 | 7 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 97 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 97 | 96 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 97 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORT-CODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORT-CODE`</small> | Alphanumeric (6 chars) | `X(6)` | 101 | 6 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-ACC-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-ACC-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 107 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 115 | 10 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 125 | 6 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 131 | 12 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 143 | 3 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 146 | 40 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 186 | 7 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 193 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 193 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 193 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 197 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 132 | — | — |
| 03 | &nbsp;&nbsp;`COMM-ACCNO`<br/><small>`DFHCOMMAREA.COMM-ACCNO`</small> | Alphanumeric (8 chars) | `X(8)` | 0 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>&nbsp;<br/>`WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-AMT`<br/><small>`DFHCOMMAREA.COMM-AMT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 8 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>&nbsp;<br/>`WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SORTC`<br/><small>`DFHCOMMAREA.COMM-SORTC`</small> | Numeric Display (6 digits) | `9(6)` | 20 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-AV-BAL`<br/><small>`DFHCOMMAREA.COMM-AV-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 26 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACT-BAL`<br/><small>`DFHCOMMAREA.COMM-ACT-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 38 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ORIGIN`<br/><small>`DFHCOMMAREA.COMM-ORIGIN`</small> | Group | *DISPLAY* | 50 | 80 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-APPLID`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 50 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-USERID`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-USERID`</small> | Alphanumeric (8 chars) | `X(8)` | 58 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-FACILITY-NAME`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-FACILITY-NAME`</small> | Alphanumeric (8 chars) | `X(8)` | 66 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NETWRK-ID`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-NETWRK-ID`</small> | Alphanumeric (8 chars) | `X(8)` | 74 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-FACILTYPE`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-FACILTYPE`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 82 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>&nbsp;<br/>`WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.FILLER`</small> | Alphanumeric (4 chars) | `X(4)` | 86 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DESCRIPTION`<br/><small>`DFHCOMMAREA.COMM-ORIGIN.COMM-DESCRIPTION`</small> | Alphanumeric (40 chars) | `X(40)` | 90 | 40 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 130 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`DFHCOMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 131 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>*( +2 more)* |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`FILE-RETRY`**<br/><small>`FILE-RETRY`</small> | Numeric Display (3 digits) | `999` | 0 | 3 | — | — |
| 01 | **`WS-EXIT-RETRY-LOOP`**<br/><small>`WS-EXIT-RETRY-LOOP`</small> | Alphanumeric (1 chars) | `X` | 3 | 1 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 4 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 4 | 4 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 8 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 9 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 11 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 12 | 2 | — | — |
| 01 | **`DATA-STORE-TYPE`**<br/><small>`DATA-STORE-TYPE`</small> | Alphanumeric (1 chars) | `X` | 14 | 1 | • `88 DATASTORE-TYPE-DLI`: '1'<br/>• `88 DATASTORE-TYPE-DB2`: '2'<br/>• `88 DATASTORE-TYPE-VSAM`: 'V' | — |
| 01 | **`WS-ACC-DATA`**<br/><small>`WS-ACC-DATA`</small> | Group | *DISPLAY* | 15 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 15 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 15 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 19 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 29 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 29 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 35 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 43 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 51 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 57 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 57 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 57 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 59 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 61 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 65 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 73 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 73 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 73 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 75 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 77 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 81 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 81 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 81 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 83 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 85 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 89 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 101 | 12 | — | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 113 | 12 | **Default:** `0` | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 01 | **`WS-SQLCODE-DISP`**<br/><small>`WS-SQLCODE-DISP`</small> | Numeric Display (9 digits) | `9(9)` | 125 | 9 | **Default:** `0` | — |
| 01 | **`DESIRED-ACC-KEY`**<br/><small>`DESIRED-ACC-KEY`</small> | Group | *DISPLAY* | 134 | 14 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-SORT-CODE`<br/><small>`DESIRED-ACC-KEY.DESIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 134 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`DESIRED-ACC-NO`<br/><small>`DESIRED-ACC-KEY.DESIRED-ACC-NO`</small> | Numeric Display (8 digits) | `9(8)` | 140 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`NEW-ACCOUNT-AVAILABLE-BALANCE`**<br/><small>`NEW-ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 148 | 12 | **Default:** `0` | — |
| 01 | **`NEW-ACCOUNT-ACTUAL-BALANCE`**<br/><small>`NEW-ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 160 | 12 | **Default:** `0` | — |
| 01 | **`WS-ACC-REC-LEN`**<br/><small>`WS-ACC-REC-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 172 | 2 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 174 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 182 | 10 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 182 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 182 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 184 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 185 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 187 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 188 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 192 | 10 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small> |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 192 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 194 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 195 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 197 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 198 | 4 | — | — |
| 01 | **`PROCTRAN-AREA`**<br/><small>`PROCTRAN-AREA`</small> | Group | *DISPLAY* | 202 | 99 | — | — |
| 03 | &nbsp;&nbsp;`PROC-TRAN-DATA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA`</small> | Group | *DISPLAY* | 202 | 99 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-EYE-CATCHER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 202 | 4 | • `88 PROC-TRAN-VALID`: 'PRTR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-AREA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA`</small> | Group | *DISPLAY* | 202 | 4 | <mark>REDEFINES PROC-TRAN-EYE-CATCHER</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-FLAG`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.PROC-TRAN-LOGICAL-DELETE-FLAG`</small> | Alphanumeric (1 chars) | `X` | 202 | 1 | • `88 PROC-TRAN-LOGICALLY-DELETED`: 'X'FF'' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.FILLER`</small> | Alphanumeric (3 chars) | `X(3)` | 203 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-ID`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID`</small> | Group | *DISPLAY* | 206 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-SORT-CODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 206 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-NUMBER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 212 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 220 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 220 | 8 | <mark>REDEFINES PROC-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-YYYY`</small> | Numeric Display (4 digits) | `9999` | 220 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 224 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-DD`</small> | Numeric Display (2 digits) | `99` | 226 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 228 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 228 | 6 | <mark>REDEFINES PROC-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-HH`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 228 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 230 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-SS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 232 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-REF`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 234 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 246 | 3 | • `88 PROC-TY-CHEQUE-ACKNOWLEDGED`: 'CHA'<br/>• `88 PROC-TY-CHEQUE-FAILURE`: 'CHF'<br/>• `88 PROC-TY-CHEQUE-PAID-IN`: 'CHI'<br/>• `88 PROC-TY-CHEQUE-PAID-OUT`: 'CHO'<br/>• `88 PROC-TY-CREDIT`: 'CRE'<br/>• `88 PROC-TY-DEBIT`: 'DEB'<br/>• `88 PROC-TY-WEB-CREATE-ACCOUNT`: 'ICA'<br/>• `88 PROC-TY-WEB-CREATE-CUSTOMER`: 'ICC'<br/>• `88 PROC-TY-WEB-DELETE-ACCOUNT`: 'IDA'<br/>• `88 PROC-TY-WEB-DELETE-CUSTOMER`: 'IDC'<br/>• `88 PROC-TY-BRANCH-CREATE-ACCOUNT`: 'OCA'<br/>• `88 PROC-TY-BRANCH-CREATE-CUSTOMER`: 'OCC'<br/>• `88 PROC-TY-BRANCH-DELETE-ACCOUNT`: 'ODA'<br/>• `88 PROC-TY-BRANCH-DELETE-CUSTOMER`: 'ODC'<br/>• `88 PROC-TY-CREATE-SODD`: 'OCS'<br/>• `88 PROC-TY-PAYMENT-CREDIT`: 'PCR'<br/>• `88 PROC-TY-PAYMENT-DEBIT`: 'PDR'<br/>• `88 PROC-TY-TRANSFER`: 'TFR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 249 | 40 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR`</small> | Group | *DISPLAY* | 249 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-HEADER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-HEADER`</small> | Alphanumeric (26 chars) | `X(26)` | 249 | 26 | • `88 PROC-TRAN-DESC-XFR-FLAG`: 'TRANSFER' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 275 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-ACCOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-ACCOUNT`</small> | Numeric Display (8 digits) | `9(8)` | 281 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC`</small> | Group | *DISPLAY* | 249 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 249 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 259 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 267 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 269 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 271 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 275 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 277 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 279 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 283 | 6 | • `88 PROC-DESC-DELACC-FLAG`: 'DELETE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CREACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC`</small> | Group | *DISPLAY* | 249 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 249 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 259 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 267 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 269 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 271 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 275 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 277 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 279 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 283 | 6 | • `88 PROC-DESC-CREACC-FLAG`: 'CREATE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELCUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS`</small> | Group | *DISPLAY* | 249 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 249 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 255 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 265 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 279 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 283 | 1 | • `88 PROC-DESC-DELCUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 284 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 286 | 1 | • `88 PROC-DESC-DELCUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 287 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CRECUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS`</small> | Group | *DISPLAY* | 249 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 249 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 255 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 265 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 279 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 283 | 1 | • `88 PROC-DESC-CRECUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 284 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 286 | 1 | • `88 PROC-DESC-CRECUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 287 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-AMOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 289 | 12 | — | — |
| 01 | **`WS-PASSED-DATA`**<br/><small>`WS-PASSED-DATA`</small> | Group | *DISPLAY* | 301 | 13 | — | — |
| 02 | &nbsp;&nbsp;`WS-TEST-KEY`<br/><small>`WS-PASSED-DATA.WS-TEST-KEY`</small> | Alphanumeric (4 chars) | `X(4)` | 301 | 4 | — | — |
| 02 | &nbsp;&nbsp;`WS-SORT-CODE`<br/><small>`WS-PASSED-DATA.WS-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 305 | 6 | — | — |
| 02 | &nbsp;&nbsp;`WS-CUSTOMER-RANGE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE`</small> | Group | *DISPLAY* | 311 | 3 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-TOP`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-TOP`</small> | Alphanumeric (1 chars) | `X` | 311 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-MIDDLE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-MIDDLE`</small> | Alphanumeric (1 chars) | `X` | 312 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-BOTTOM`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-BOTTOM`</small> | Alphanumeric (1 chars) | `X` | 313 | 1 | — | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 314 | 4 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 318 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small><br/>&nbsp;<br/>`WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>*( +2 more)* |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 326 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 330 | 1 | **Default:** `N` | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 331 | 20 | — | `CHECK-FOR-STORM-DRAIN-DB2`<br/><small>*CFSDD010*</small> |
| 01 | **`NUMERIC-AMOUNT-DISPLAY`**<br/><small>`NUMERIC-AMOUNT-DISPLAY`</small> | Decimal Display (13, 2) | `+9(10).99` | 351 | 14 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 365 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 365 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 365 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 365 | 2 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 367 | 2 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 369 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 371 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 379 | 678 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 379 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 379 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 387 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 391 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 399 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 403 | 10 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 413 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 421 | 4 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 425 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 433 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 441 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 449 | 8 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 457 | 600 | — | `WRITE-TO-PROCTRAN-DB2`<br/><small>*WTPD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-SUFFICIENT-FUNDS`**<br/><small>`WS-SUFFICIENT-FUNDS`</small> | Alphanumeric (1 chars) | `X` | 1057 | 1 | **Default:** `N` | — |
| 01 | **`WS-DIFFERENCE`**<br/><small>`WS-DIFFERENCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1058 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |

