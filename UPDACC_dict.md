# Data Dictionary: `UPDACC`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 129 |
| **Level-88 Business Rules** | 1 |
| **Memory Overlays (REDEFINES)** | 8 |
| **Working-Storage Span** | 113 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small> |
| 77 | `SYSIDERR-RETRY`<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 9 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 9 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 9 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 13 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-KEY`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY`</small> | Group | *DISPLAY* | 23 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 23 | 6 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-KEY.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 29 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 37 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 45 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 49 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 59 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 63 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 73 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 83 | 7 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 90 | 7 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 97 | 0 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 97 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 105 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 105 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 109 | 4 | — | — |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 99 | — | — |
| 03 | &nbsp;&nbsp;`COMM-EYE`<br/><small>`DFHCOMMAREA.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 4 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SCODE`<br/><small>`DFHCOMMAREA.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 14 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACCNO`<br/><small>`DFHCOMMAREA.COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 20 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`DFHCOMMAREA.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 28 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-INT-RATE`<br/><small>`DFHCOMMAREA.COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 36 | 6 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-OPENED`<br/><small>`DFHCOMMAREA.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 42 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 42 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 42 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 44 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`DFHCOMMAREA.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 46 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-OVERDRAFT`<br/><small>`DFHCOMMAREA.COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 50 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 58 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-LAST-STMNT-GROUP`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP`</small> | Group | *DISPLAY* | 58 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-DAY`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-DAY`</small> | Numeric Display (2 digits) | `99` | 58 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-MONTH`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-MONTH`</small> | Numeric Display (2 digits) | `99` | 60 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LASTST-YEAR`<br/><small>`DFHCOMMAREA.COMM-LAST-STMNT-GROUP.COMM-LASTST-YEAR`</small> | Numeric Display (4 digits) | `9999` | 62 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 66 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-NEXT-STMNT-GROUP`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP`</small> | Group | *DISPLAY* | 66 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-DAY`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-DAY`</small> | Numeric Display (2 digits) | `99` | 66 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-MONTH`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-MONTH`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXTST-YEAR`<br/><small>`DFHCOMMAREA.COMM-NEXT-STMNT-GROUP.COMM-NEXTST-YEAR`</small> | Numeric Display (4 digits) | `9999` | 70 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`DFHCOMMAREA.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 74 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ACTUAL-BAL`<br/><small>`DFHCOMMAREA.COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 86 | 12 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 98 | 1 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 0 | 10 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 0 | 4 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 4 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 5 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 7 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 8 | 2 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`WS-ACC-DATA`**<br/><small>`WS-ACC-DATA`</small> | Group | *DISPLAY* | 10 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 10 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 10 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 14 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 24 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 24 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 30 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 38 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 46 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 52 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 52 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 52 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 54 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 56 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 60 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 68 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 68 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 70 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 72 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 76 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 76 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 76 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 78 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 80 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 84 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`WS-ACC-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 96 | 12 | — | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 108 | 12 | **Default:** `0` | — |
| 01 | **`WS-SQLCODE-DISP`**<br/><small>`WS-SQLCODE-DISP`</small> | Numeric Display (9 digits) | `9(9)` | 120 | 9 | **Default:** `0` | — |
| 01 | **`DESIRED-ACC-KEY`**<br/><small>`DESIRED-ACC-KEY`</small> | Group | *DISPLAY* | 129 | 14 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-SORT-CODE`<br/><small>`DESIRED-ACC-KEY.DESIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 129 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 03 | &nbsp;&nbsp;`DESIRED-ACC-NO`<br/><small>`DESIRED-ACC-KEY.DESIRED-ACC-NO`</small> | Numeric Display (8 digits) | `9(8)` | 135 | 8 | — | `UPDATE-ACCOUNT-DB2`<br/><small>*UAD010*</small> |
| 01 | **`NEW-ACCOUNT-AVAILABLE-BALANCE`**<br/><small>`NEW-ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 143 | 12 | **Default:** `0` | — |
| 01 | **`NEW-ACCOUNT-ACTUAL-BALANCE`**<br/><small>`NEW-ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 155 | 12 | **Default:** `0` | — |
| 01 | **`WS-ACC-REC-LEN`**<br/><small>`WS-ACC-REC-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 167 | 2 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 169 | 8 | — | — |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 177 | 10 | — | — |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 177 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 177 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 179 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 180 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 182 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 183 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 187 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 187 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 189 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 190 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 192 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 193 | 4 | — | — |
| 01 | **`REJ-REASON`**<br/><small>`REJ-REASON`</small> | Alphanumeric (2 chars) | `XX` | 197 | 2 | **Default:** `SPACES` | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 199 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 199 | 6 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`CUSTOMER-KY.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 205 | 8 | **Default:** `0` | — |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 213 | 20 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 233 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 233 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 233 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 233 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 235 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 237 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 239 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 247 | 678 | — | — |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 247 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 247 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 255 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 259 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 267 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 271 | 10 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 281 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 289 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 293 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 301 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 309 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 317 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 325 | 600 | — | — |

