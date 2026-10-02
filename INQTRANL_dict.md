# Data Dictionary: `INQTRANL`

**Author:** IBM  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 113 |
| **Level-88 Business Rules** | 6 |
| **Memory Overlays (REDEFINES)** | 6 |
| **Working-Storage Span** | 962 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 6 | 96 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORTCODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 10 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 16 | 8 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 24 | 10 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 34 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 40 | 12 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 52 | 3 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 55 | 40 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 95 | 7 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`HV-QUERY-SORTCODE`**<br/><small>`HV-QUERY-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 102 | 6 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 01 | **`HV-QUERY-ACCNO`**<br/><small>`HV-QUERY-ACCNO`</small> | Alphanumeric (8 chars) | `X(8)` | 108 | 8 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 01 | **`HV-QUERY-FROM-DATE`**<br/><small>`HV-QUERY-FROM-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 116 | 10 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 01 | **`HV-QUERY-TO-DATE`**<br/><small>`HV-QUERY-TO-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 126 | 10 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 01 | **`HV-QUERY-LIMIT`**<br/><small>`HV-QUERY-LIMIT`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 136 | 2 | — | `READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small><br/>&nbsp;<br/>`FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`HV-QUERY-OFFSET`**<br/><small>`HV-QUERY-OFFSET`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 138 | 4 | — | `READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small><br/>&nbsp;<br/>`FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 142 | 0 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 142 | 0 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 142 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 142 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 142 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 146 | 4 | — | — |
| 01 | **`WS-TRANSACTION-COUNT`**<br/><small>`WS-TRANSACTION-COUNT`</small> | Signed Integer (32-bit Binary) | `S9(5)`<br/>*COMP* | 150 | 4 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-FETCH-COUNT`**<br/><small>`WS-FETCH-COUNT`</small> | Signed SmallInt (16-bit Binary) | `S9(3)`<br/>*COMP* | 154 | 2 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`WS-TOTAL-COUNT`**<br/><small>`WS-TOTAL-COUNT`</small> | Signed Integer (32-bit Binary) | `S9(5)`<br/>*COMP* | 156 | 4 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-SKIP-COUNT`**<br/><small>`WS-SKIP-COUNT`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 160 | 4 | **Default:** `0` | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`WS-ROW-COUNT`**<br/><small>`WS-ROW-COUNT`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 164 | 4 | **Default:** `0` | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 168 | 8 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small><br/>*( +2 more)* |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 176 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 184 | 678 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 184 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 184 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 192 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 196 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 204 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 208 | 10 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 218 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 226 | 4 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 230 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 238 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 246 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 254 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 262 | 600 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 862 | 8 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 870 | 10 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 870 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 870 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 872 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 873 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 875 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 876 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 880 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 880 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 880 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 880 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 882 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 884 | 2 | — | `ABEND-ROUTINE`<br/><small>*AR010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-TRAN-ID-PARTS`**<br/><small>`WS-TRAN-ID-PARTS`</small> | Group | *DISPLAY* | 886 | 44 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-SC`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-SC`</small> | Alphanumeric (6 chars) | `X(6)` | 886 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 892 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-NUM`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-NUM`</small> | Alphanumeric (8 chars) | `X(8)` | 893 | 8 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 901 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-DATE`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-DATE`</small> | Alphanumeric (8 chars) | `X(8)` | 902 | 8 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 910 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-TIME`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 911 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-TRAN-ID-PARTS.FILLER`</small> | Alphanumeric (1 chars) | `X` | 917 | 1 | **Default:** `-` | — |
| 03 | &nbsp;&nbsp;`WS-TRAN-ID-REF`<br/><small>`WS-TRAN-ID-PARTS.WS-TRAN-ID-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 918 | 12 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 01 | **`WS-DATE-WORK`**<br/><small>`WS-DATE-WORK`</small> | Group | *DISPLAY* | 930 | 18 | — | — |
| 03 | &nbsp;&nbsp;`WS-DATE-YYYYMMDD`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD`</small> | Numeric Display (8 digits) | `9(8)` | 930 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`WS-DATE-YYYYMMDD-GRP`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP`</small> | Group | *DISPLAY* | 930 | 8 | <mark>REDEFINES WS-DATE-YYYYMMDD</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-YYYY`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-YYYY`</small> | Numeric Display (4 digits) | `9(4)` | 930 | 4 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-MM`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-MM`</small> | Numeric Display (2 digits) | `9(2)` | 934 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-DD`<br/><small>`WS-DATE-WORK.WS-DATE-YYYYMMDD-GRP.WS-DATE-DD`</small> | Numeric Display (2 digits) | `9(2)` | 936 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 03 | &nbsp;&nbsp;`WS-DATE-ISO`<br/><small>`WS-DATE-WORK.WS-DATE-ISO`</small> | Alphanumeric (10 chars) | `X(10)` | 938 | 10 | — | `GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small><br/>&nbsp;<br/>`FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 03 | &nbsp;&nbsp;`WS-DATE-ISO-GRP`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP`</small> | Group | *DISPLAY* | 938 | 10 | <mark>REDEFINES WS-DATE-ISO</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-YYYY`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-YYYY`</small> | Alphanumeric (4 chars) | `X(4)` | 938 | 4 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-SEP1`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-SEP1`</small> | Alphanumeric (1 chars) | `X` | 942 | 1 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-MM`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-MM`</small> | Alphanumeric (2 chars) | `X(2)` | 943 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-SEP2`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-SEP2`</small> | Alphanumeric (1 chars) | `X` | 945 | 1 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-DATE-ISO-DD`<br/><small>`WS-DATE-WORK.WS-DATE-ISO-GRP.WS-DATE-ISO-DD`</small> | Alphanumeric (2 chars) | `X(2)` | 946 | 2 | — | `CONVERT-YYYYMMDD-TO-ISO`<br/><small>*CYI010*</small><br/>&nbsp;<br/>`CONVERT-ISO-TO-YYYYMMDD`<br/><small>*CIY010*</small> |
| 01 | **`WS-SORTCODE-CHAR`**<br/><small>`WS-SORTCODE-CHAR`</small> | Alphanumeric (6 chars) | `X(6)` | 948 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 01 | **`WS-ACCNO-CHAR`**<br/><small>`WS-ACCNO-CHAR`</small> | Alphanumeric (8 chars) | `X(8)` | 954 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 14551 | — | — |
| 03 | &nbsp;&nbsp;`INQTRANL-EYE`<br/><small>`DFHCOMMAREA.INQTRANL-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | • `88 INQTRANL-EYE-VALID`: 'ITRL' | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-SORTCODE`<br/><small>`DFHCOMMAREA.INQTRANL-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 4 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-ACCNO`<br/><small>`DFHCOMMAREA.INQTRANL-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 10 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-FROM-DATE`<br/><small>`DFHCOMMAREA.INQTRANL-FROM-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 18 | 8 | • `88 INQTRANL-NO-FROM-DATE`: '0' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-TO-DATE`<br/><small>`DFHCOMMAREA.INQTRANL-TO-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 26 | 8 | • `88 INQTRANL-NO-TO-DATE`: '99999999' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-TOTAL-COUNT`<br/><small>*GTC010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-LIMIT`<br/><small>`DFHCOMMAREA.INQTRANL-LIMIT`</small> | Numeric Display (3 digits) | `9(3)` | 34 | 3 | • `88 INQTRANL-DEFAULT-LIMIT`: '50' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-OFFSET`<br/><small>`DFHCOMMAREA.INQTRANL-OFFSET`</small> | Numeric Display (5 digits) | `9(5)` | 37 | 5 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-TRANSACTIONS-DB2`<br/><small>*RTD010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-TOTAL-COUNT`<br/><small>`DFHCOMMAREA.INQTRANL-TOTAL-COUNT`</small> | Numeric Display (5 digits) | `9(5)` | 42 | 5 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-RETURNED-COUNT`<br/><small>`DFHCOMMAREA.INQTRANL-RETURNED-COUNT`</small> | Numeric Display (3 digits) | `9(3)` | 47 | 3 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-SUCCESS`<br/><small>`DFHCOMMAREA.INQTRANL-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 50 | 1 | • `88 INQTRANL-SUCCESS-TRUE`: 'Y'<br/>• `88 INQTRANL-SUCCESS-FALSE`: 'N' | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQTRANL-TRANSACTIONS`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS`</small> | Group Array [100] | *DISPLAY* | 51 | 14500 | **OCCURS:** 100 | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-ID`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-ID`</small> | Alphanumeric (50 chars) | `X(50)` | 51 | 50 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-SORTCODE`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 101 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-ACCNO`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 107 | 8 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DATE`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 115 | 8 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DATE-GRP`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 115 | 8 | <mark>REDEFINES INQTRANL-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DATE-YYYY`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DATE-GRP.INQTRANL-TRAN-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 115 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DATE-MM`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DATE-GRP.INQTRANL-TRAN-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 119 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DATE-DD`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DATE-GRP.INQTRANL-TRAN-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 121 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TIME`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 123 | 6 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TIME-GRP`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 123 | 6 | <mark>REDEFINES INQTRANL-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TIME-HH`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TIME-GRP.INQTRANL-TRAN-TIME-HH`</small> | Numeric Display (2 digits) | `99` | 123 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TIME-MM`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TIME-GRP.INQTRANL-TRAN-TIME-MM`</small> | Numeric Display (2 digits) | `99` | 125 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TIME-SS`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TIME-GRP.INQTRANL-TRAN-TIME-SS`</small> | Numeric Display (2 digits) | `99` | 127 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-REF`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 129 | 12 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-TYPE`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 141 | 3 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-DESC`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 144 | 40 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQTRANL-TRAN-AMOUNT`<br/><small>`DFHCOMMAREA.INQTRANL-TRANSACTIONS.INQTRANL-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 184 | 12 | — | `FETCH-TRANSACTION-DATA`<br/><small>*FTD010*</small> |

