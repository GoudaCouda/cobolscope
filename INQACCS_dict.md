# Data Dictionary: `INQACCS`

**Author:** Bank of Z  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 96 |
| **Level-88 Business Rules** | 0 |
| **Memory Overlays (REDEFINES)** | 5 |
| **Working-Storage Span** | 861 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 6 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 20 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 26 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 34 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 42 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 46 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 56 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 60 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 70 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 80 | 7 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 87 | 7 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 01 | **`EIBRCODE-NICE`**<br/><small>`EIBRCODE-NICE`</small> | Group | *DISPLAY* | 94 | 6 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-FIRST`<br/><small>`EIBRCODE-NICE.EIBRCODE-FIRST`</small> | Alphanumeric (1 chars) | `X` | 94 | 1 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-SECOND`<br/><small>`EIBRCODE-NICE.EIBRCODE-SECOND`</small> | Alphanumeric (1 chars) | `X` | 95 | 1 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-THIRD`<br/><small>`EIBRCODE-NICE.EIBRCODE-THIRD`</small> | Alphanumeric (1 chars) | `X` | 96 | 1 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-FOURTH`<br/><small>`EIBRCODE-NICE.EIBRCODE-FOURTH`</small> | Alphanumeric (1 chars) | `X` | 97 | 1 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-FIFTH`<br/><small>`EIBRCODE-NICE.EIBRCODE-FIFTH`</small> | Alphanumeric (1 chars) | `X` | 98 | 1 | — | — |
| 03 | &nbsp;&nbsp;`EIBRCODE-SIXTH`<br/><small>`EIBRCODE-NICE.EIBRCODE-SIXTH`</small> | Alphanumeric (1 chars) | `X` | 99 | 1 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 100 | 0 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 100 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 100 | 8 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 100 | 4 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 104 | 4 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 108 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 108 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 112 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 113 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 115 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 116 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 118 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 126 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 130 | 1 | **Default:** `N` | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 131 | 20 | — | `CHECK-FOR-STORM-DRAIN-DB2`<br/><small>*CFSDD010*</small> |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 151 | 8 | — | — |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 159 | 10 | — | — |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 159 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 159 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 161 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 162 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 164 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 165 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 169 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 169 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 169 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 169 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 171 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 173 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 175 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 183 | 678 | — | — |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 183 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 183 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 191 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 195 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 203 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 207 | 10 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 217 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 225 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 229 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 237 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 245 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 253 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 261 | 600 | — | — |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 1970 | — | — |
| 03 | &nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`DFHCOMMAREA.NUMBER-OF-ACCOUNTS`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 0 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 4 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`DFHCOMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 5 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-PCB-POINTER`<br/><small>`DFHCOMMAREA.COMM-PCB-POINTER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DETAILS`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS`</small> | Group Array [20] | *DISPLAY* | 10 | 1960 | **OCCURS:** 1 TO 20 (DEPENDING ON NUMBER-OF-ACCOUNTS) | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-EYE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 10 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 14 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-SCODE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 24 | 6 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACCNO`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 30 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 38 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-INT-RATE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 46 | 6 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 52 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 52 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 52 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 54 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 56 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OVERDRAFT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 60 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 68 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 68 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 70 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 72 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 76 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 76 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 76 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 78 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 80 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 84 | 12 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACTUAL-BAL`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 96 | 12 | — | `FETCH-DATA`<br/><small>*FD010*</small> |

