# Data Dictionary: `ABNDPROC`

**Author:** JONCOLLETT  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 72 |
| **Level-88 Business Rules** | 3 |
| **Memory Overlays (REDEFINES)** | 1 |
| **Working-Storage Span** | 690 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 0 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 0 | 4 | — | `PREMIERE`<br/><small>*A010*</small> |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 4 | 4 | — | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-ABND-AREA`**<br/><small>`WS-ABND-AREA`</small> | Group | *DISPLAY* | 8 | 678 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`WS-ABND-AREA.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 8 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`WS-ABND-AREA.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 8 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`WS-ABND-AREA.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 16 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`WS-ABND-AREA.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 20 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`WS-ABND-AREA.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 28 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`WS-ABND-AREA.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 32 | 10 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`WS-ABND-AREA.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 42 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`WS-ABND-AREA.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 50 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`WS-ABND-AREA.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 54 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`WS-ABND-AREA.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 62 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`WS-ABND-AREA.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 70 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`WS-ABND-AREA.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 78 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`WS-ABND-AREA.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 86 | 600 | — | — |
| 01 | **`WS-ABND-KEY-LEN`**<br/><small>`WS-ABND-KEY-LEN`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 686 | 4 | **Default:** `+12` | — |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 678 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`COMM-VSAM-KEY`<br/><small>`DFHCOMMAREA.COMM-VSAM-KEY`</small> | Group | *DISPLAY* | 0 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-UTIME-KEY`<br/><small>`DFHCOMMAREA.COMM-VSAM-KEY.COMM-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 0 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-TASKNO-KEY`<br/><small>`DFHCOMMAREA.COMM-VSAM-KEY.COMM-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 8 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-APPLID`<br/><small>`DFHCOMMAREA.COMM-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 12 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-TRANID`<br/><small>`DFHCOMMAREA.COMM-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 20 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-DATE`<br/><small>`DFHCOMMAREA.COMM-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 24 | 10 | — | — |
| 03 | &nbsp;&nbsp;`COMM-TIME`<br/><small>`DFHCOMMAREA.COMM-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 34 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-CODE`<br/><small>`DFHCOMMAREA.COMM-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 42 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-PROGRAM`<br/><small>`DFHCOMMAREA.COMM-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 46 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-RESPCODE`<br/><small>`DFHCOMMAREA.COMM-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 54 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-RESP2CODE`<br/><small>`DFHCOMMAREA.COMM-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 62 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-SQLCODE`<br/><small>`DFHCOMMAREA.COMM-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 70 | 8 | — | — |
| 03 | &nbsp;&nbsp;`COMM-FREEFORM`<br/><small>`DFHCOMMAREA.COMM-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 78 | 600 | — | — |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 0 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 0 | 4 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 4 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 5 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 7 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 8 | 2 | — | — |
| 01 | **`DATA-STORE-TYPE`**<br/><small>`DATA-STORE-TYPE`</small> | Alphanumeric (1 chars) | `X` | 10 | 1 | • `88 DATASTORE-TYPE-DLI`: '1'<br/>• `88 DATASTORE-TYPE-DB2`: '2'<br/>• `88 DATASTORE-TYPE-VSAM`: 'V' | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 11 | 12 | **Default:** `0` | — |
| 01 | **`WS-SQLCODE-DISP`**<br/><small>`WS-SQLCODE-DISP`</small> | Numeric Display (9 digits) | `9(9)` | 23 | 9 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 32 | 8 | — | — |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 40 | 10 | — | — |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 40 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 40 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 42 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 43 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 45 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 46 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 50 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 50 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 52 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 53 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 55 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 56 | 4 | — | — |
| 01 | **`WS-PASSED-DATA`**<br/><small>`WS-PASSED-DATA`</small> | Group | *DISPLAY* | 60 | 13 | — | — |
| 02 | &nbsp;&nbsp;`WS-TEST-KEY`<br/><small>`WS-PASSED-DATA.WS-TEST-KEY`</small> | Alphanumeric (4 chars) | `X(4)` | 60 | 4 | — | — |
| 02 | &nbsp;&nbsp;`WS-SORT-CODE`<br/><small>`WS-PASSED-DATA.WS-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 64 | 6 | — | — |
| 02 | &nbsp;&nbsp;`WS-CUSTOMER-RANGE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE`</small> | Group | *DISPLAY* | 70 | 3 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-TOP`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-TOP`</small> | Alphanumeric (1 chars) | `X` | 70 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-MIDDLE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-MIDDLE`</small> | Alphanumeric (1 chars) | `X` | 71 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-BOTTOM`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-BOTTOM`</small> | Alphanumeric (1 chars) | `X` | 72 | 1 | — | — |
| 01 | **`WS-SORT-DIV`**<br/><small>`WS-SORT-DIV`</small> | Group | *DISPLAY* | 73 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV1`<br/><small>`WS-SORT-DIV.WS-SORT-DIV1`</small> | Alphanumeric (2 chars) | `XX` | 73 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV2`<br/><small>`WS-SORT-DIV.WS-SORT-DIV2`</small> | Alphanumeric (2 chars) | `XX` | 75 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV3`<br/><small>`WS-SORT-DIV.WS-SORT-DIV3`</small> | Alphanumeric (2 chars) | `XX` | 77 | 2 | — | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 79 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 79 | 6 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`CUSTOMER-KY.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 85 | 8 | **Default:** `0` | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 93 | 4 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 97 | 8 | — | — |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 105 | 4 | — | — |

