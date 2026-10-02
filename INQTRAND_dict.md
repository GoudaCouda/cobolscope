# Data Dictionary: `INQTRAND`

**Author:** IBM  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 96 |
| **Level-88 Business Rules** | 5 |
| **Memory Overlays (REDEFINES)** | 6 |
| **Working-Storage Span** | 890 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 6 | 96 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORTCODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 10 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 16 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 24 | 10 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 34 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 40 | 12 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 52 | 3 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 55 | 40 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 95 | 7 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 102 | 0 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 102 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 102 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 102 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 106 | 4 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 110 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small><br/>&nbsp;<br/>`ABEND-ROUTINE`<br/><small>*AR010*</small> |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 118 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 126 | 678 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 126 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 126 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 134 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 138 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 146 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 150 | 10 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 160 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 168 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 172 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 180 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 188 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 196 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 204 | 600 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 804 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 812 | 10 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 812 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 812 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 814 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 815 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 817 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 818 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 822 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 822 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 822 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 822 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 824 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 826 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-TRAN-ID-PARTS`**<br/><small>`WS-TRAN-ID-PARTS`</small> | Group | *DISPLAY* | 828 | 44 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-SC`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-SC`</small> | Alphanumeric (6 chars) | `X(6)` | 828 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 834 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-NUM`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-NUM`</small> | Alphanumeric (8 chars) | `X(8)` | 835 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 843 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-DATE`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-DATE`</small> | Alphanumeric (8 chars) | `X(8)` | 844 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 852 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-TIME`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 853 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 859 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-REF`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 860 | 12 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 01 | **`WS-DATE-WORK`**<br/><small>`WS-DATE-WORK`</small> | Group | *DISPLAY* | 872 | 18 | — | — |
| 03 | &nbsp;&nbsp;`WS-DATE-YYYYMMDD`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD`</small> | Numeric Display (8 digits) | `9(8)` | 872 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`WS-DATE-YYYYMMDD-GRP`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP`</small> | Group | *DISPLAY* | 872 | 8 | <mark>REDEFINES WS-DATE-YYYYMMDD</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-YYYY`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-YYYY`</small> | Numeric Display (4 digits) | `9(4)` | 872 | 4 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-MM`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-MM`</small> | Numeric Display (2 digits) | `9(2)` | 876 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-DD`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-DD`</small> | Numeric Display (2 digits) | `9(2)` | 878 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 03 | &nbsp;&nbsp;`WS-DATE-ISO`<br/><small>`WS-DATE-WORK.WS-DATE-ISO`</small> | Alphanumeric (10 chars) | `X(10)` | 880 | 10 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`WS-DATE-ISO-GRP`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP`</small> | Group | *DISPLAY* | 880 | 10 | <mark>REDEFINES WS-DATE-ISO</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-YYYY`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-YYYY`</small> | Alphanumeric (4 chars) | `X(4)` | 880 | 4 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-SEP1`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-SEP1`</small> | Alphanumeric (1 chars) | `X` | 884 | 1 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-MM`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-MM`</small> | Alphanumeric (2 chars) | `X(2)` | 885 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-SEP2`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-SEP2`</small> | Alphanumeric (1 chars) | `X` | 887 | 1 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-DD`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-DD`</small> | Alphanumeric (2 chars) | `X(2)` | 888 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 191 | — | — |
| 03 | &nbsp;&nbsp;`INQTRAND-EYE`<br/><small>`DFHCOMMAREA.INQTRAND-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | • `88 INQTRAND-EYE-VALID`: 'ITRD' | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-SORTCODE`<br/><small>`DFHCOMMAREA.INQTRAND-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 4 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-ACCNO`<br/><small>`DFHCOMMAREA.INQTRAND-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 10 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-DATE`<br/><small>`DFHCOMMAREA.INQTRAND-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 18 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TIME`<br/><small>`DFHCOMMAREA.INQTRAND-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 26 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-REF`<br/><small>`DFHCOMMAREA.INQTRAND-REF`</small> | Numeric Display (12 digits) | `9(12)` | 32 | 12 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-SUCCESS`<br/><small>`DFHCOMMAREA.INQTRAND-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 44 | 1 | • `88 INQTRAND-SUCCESS-TRUE`: 'Y'<br/>• `88 INQTRAND-SUCCESS-FALSE`: 'N' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-FOUND`<br/><small>`DFHCOMMAREA.INQTRAND-FOUND`</small> | Alphanumeric (1 chars) | `X` | 45 | 1 | • `88 INQTRAND-FOUND-TRUE`: 'Y'<br/>• `88 INQTRAND-FOUND-FALSE`: 'N' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-ID`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-ID`</small> | Alphanumeric (50 chars) | `X(50)` | 46 | 50 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-SORTCODE`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 96 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-ACCNO`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 102 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-DATE`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 110 | 8 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-DATE-GRP`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 110 | 8 | <mark>REDEFINES INQTRAND-TRAN-DATE</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-DATE-YYYY`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DATE-GRP.INQTRAND-TRAN-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 110 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-DATE-MM`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DATE-GRP.INQTRAND-TRAN-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 114 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-DATE-DD`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DATE-GRP.INQTRAND-TRAN-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 116 | 2 | — | — |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-TIME`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 118 | 6 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-TIME-GRP`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 118 | 6 | <mark>REDEFINES INQTRAND-TRAN-TIME</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-TIME-HH`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TIME-GRP.INQTRAND-TRAN-TIME-HH`</small> | Numeric Display (2 digits) | `99` | 118 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-TIME-MM`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TIME-GRP.INQTRAND-TRAN-TIME-MM`</small> | Numeric Display (2 digits) | `99` | 120 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRAND-TRAN-TIME-SS`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TIME-GRP.INQTRAND-TRAN-TIME-SS`</small> | Numeric Display (2 digits) | `99` | 122 | 2 | — | — |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-REF`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 124 | 12 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-TYPE`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 136 | 3 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-DESC`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 139 | 40 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRAND-TRAN-AMOUNT`<br/><small>`DFHCOMMAREA.INQTRAND-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 179 | 12 | — | `READ-TRANSACTION-DB2`<br/><small>*RTD010*</small> |

