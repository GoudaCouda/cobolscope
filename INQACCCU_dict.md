# Data Dictionary: `INQACCCU`

**Author:** James O'Grady  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 220 |
| **Level-88 Business Rules** | 7 |
| **Memory Overlays (REDEFINES)** | 8 |
| **Working-Storage Span** | 1,913 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 6 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 20 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 26 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
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
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 100 | 17 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 100 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 104 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP-DISPLAY`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP-DISPLAY`</small> | Numeric Display (9 digits) | `+9(8)` | 108 | 9 | — | — |
| 01 | **`EXIT-BROWSE-LOOP`**<br/><small>`EXIT-BROWSE-LOOP`</small> | Alphanumeric (1 chars) | `X` | 117 | 1 | **Default:** `N` | — |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 118 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 118 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 118 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 122 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 132 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 132 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 138 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 146 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 154 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 160 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 160 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 160 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 162 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 164 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 168 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 176 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 176 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 176 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 178 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 180 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 184 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 184 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 184 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 186 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 188 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 192 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 204 | 12 | — | — |
| 01 | **`RETURNED-DATA`**<br/><small>`RETURNED-DATA`</small> | Group | *DISPLAY* | 216 | 98 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-EYE-CATCHER`<br/><small>`RETURNED-DATA.RETURNED-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 216 | 4 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-CUST-NO`<br/><small>`RETURNED-DATA.RETURNED-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 220 | 10 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-KEY`<br/><small>`RETURNED-DATA.RETURNED-KEY`</small> | Group | *DISPLAY* | 230 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-SORT-CODE`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 230 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-NUMBER`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 236 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-TYPE`<br/><small>`RETURNED-DATA.RETURNED-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 244 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-INTEREST-RATE`<br/><small>`RETURNED-DATA.RETURNED-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 252 | 6 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OPENED`<br/><small>`RETURNED-DATA.RETURNED-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 258 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OVERDRAFT-LIMIT`<br/><small>`RETURNED-DATA.RETURNED-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 266 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-LAST-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 274 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-NEXT-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 282 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-AVAILABLE-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 290 | 12 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-ACTUAL-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 302 | 12 | — | — |
| 01 | **`DESIRED-KEY`**<br/><small>`DESIRED-KEY`</small> | Group | *DISPLAY* | 314 | 16 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-CUSTOMER`<br/><small>`DESIRED-KEY.DESIRED-KEY-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 314 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-SORTCODE`<br/><small>`DESIRED-KEY.DESIRED-KEY-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 324 | 6 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 330 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 330 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 334 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 335 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 337 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 338 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 01 | **`DATA-STORE-TYPE`**<br/><small>`DATA-STORE-TYPE`</small> | Alphanumeric (1 chars) | `X` | 340 | 1 | • `88 DATASTORE-TYPE-DB2`: '2'<br/>• `88 DATASTORE-TYPE-VSAM`: 'V' | — |
| 01 | **`DB2-EXIT-LOOP`**<br/><small>`DB2-EXIT-LOOP`</small> | Alphanumeric (1 chars) | `X` | 341 | 1 | — | — |
| 01 | **`FETCH-DATA-CNT`**<br/><small>`FETCH-DATA-CNT`</small> | Unsigned SmallInt (16-bit Binary) | `9(4)`<br/>*COMP* | 342 | 2 | — | — |
| 01 | **`WS-CUST-ALT-KEY-LEN`**<br/><small>`WS-CUST-ALT-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 344 | 2 | **Default:** `+10` | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 346 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 346 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`CUSTOMER-KY.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 352 | 8 | **Default:** `0` | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 360 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 368 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 372 | 1 | **Default:** `N` | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 373 | 20 | — | `CHECK-FOR-STORM-DRAIN-DB2`<br/><small>*CFSDD010*</small> |
| 01 | **`CUSTOMER-AREA`**<br/><small>`CUSTOMER-AREA`</small> | Group | *DISPLAY* | 393 | 397 | — | — |
| 03 | &nbsp;&nbsp;`CUSTOMER-RECORD`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD`</small> | Group | *DISPLAY* | 393 | 397 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-EYECATCHER`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 393 | 4 | • `88 CUSTOMER-EYECATCHER-VALUE`: 'CUST' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-KEY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-KEY`</small> | Group | *DISPLAY* | 397 | 16 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-SORTCODE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 397 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 403 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NAME`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-NAME`</small> | Group | *DISPLAY* | 413 | 110 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-TITLE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 413 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-FIRST-NAME`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 423 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-LAST-NAME`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 473 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-DOB`</small> | Group | *DISPLAY* | 523 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-DAY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 523 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-MONTH`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 525 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-YEAR`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 527 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-PHONE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 531 | 20 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDRESS`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS`</small> | Group | *DISPLAY* | 551 | 210 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE1`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 551 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE2`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 601 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CITY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 651 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-POSTCODE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 701 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-COUNTRY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 711 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-STATUS`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 761 | 10 | • `88 CUSTOMER-STATUS-ACTIVE`: 'ACTIVE'<br/>• `88 CUSTOMER-STATUS-INACTIVE`: 'INACTIVE'<br/>• `88 CUSTOMER-STATUS-SUSPENDED`: 'SUSPENDED' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DATE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE`</small> | Group | *DISPLAY* | 771 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DAY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 771 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-MONTH`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 773 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-YEAR`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 775 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREDIT-SCORE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 779 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DATE`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 782 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DAY`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 782 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-MONTH`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 784 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-YEAR`<br/><small>`CUSTOMER-AREA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 786 | 4 | — | — |
| 01 | **`INQCUST-COMMAREA`**<br/><small>`INQCUST-COMMAREA`</small> | Group | *DISPLAY* | 790 | 403 | — | `CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-EYE`<br/><small>`INQCUST-COMMAREA.INQCUST-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 790 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-SCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 794 | 6 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CUSTNO`<br/><small>`INQCUST-COMMAREA.INQCUST-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 800 | 10 | — | `CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME`</small> | Group | *DISPLAY* | 810 | 110 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-TITLE`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 810 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-FIRST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 820 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-LAST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 870 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-DOB`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB`</small> | Group | *DISPLAY* | 920 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 920 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 922 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 924 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PHONE`<br/><small>`INQCUST-COMMAREA.INQCUST-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 928 | 20 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-ADDR`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR`</small> | Group | *DISPLAY* | 948 | 210 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE1`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 948 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE2`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 998 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CITY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 1048 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-POSTCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 1098 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-COUNTRY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 1108 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-STATUS`<br/><small>`INQCUST-COMMAREA.INQCUST-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 1158 | 10 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREATED-DATE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE`</small> | Group | *DISPLAY* | 1168 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-DD`</small> | Numeric Display (2 digits) | `99` | 1168 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-MM`</small> | Numeric Display (2 digits) | `99` | 1170 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1172 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREDIT-SCORE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 1176 | 3 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CS-REVIEW-DT`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT`</small> | Group | *DISPLAY* | 1179 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-DD`</small> | Numeric Display (2 digits) | `99` | 1179 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-MM`</small> | Numeric Display (2 digits) | `99` | 1181 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1183 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-SUCCESS`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1187 | 1 | — | `CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-FAIL-CD`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 1188 | 1 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PCB-POINTER`<br/><small>`INQCUST-COMMAREA.INQCUST-PCB-POINTER`</small> | Alphanumeric (4 chars) | `X(4)` | 1189 | 4 | — | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 1193 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 1201 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 1201 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 1201 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1203 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 1204 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1206 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1207 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 1211 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 1211 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1213 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 1214 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1216 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 1217 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 1221 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 1221 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 1221 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 1221 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 1223 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 1225 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 1227 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 1235 | 678 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 1235 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 1235 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 1243 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 1247 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 1255 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 1259 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 1269 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 1277 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 1281 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1289 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1297 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 1305 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 1313 | 600 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 1981 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 03 | &nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`DFHCOMMAREA.NUMBER-OF-ACCOUNTS`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 0 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`CUSTOMER-CHECK`<br/><small>*CC010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`DFHCOMMAREA.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 4 | 10 | — | — |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 14 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`DFHCOMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 15 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-FOUND`<br/><small>`DFHCOMMAREA.CUSTOMER-FOUND`</small> | Alphanumeric (1 chars) | `X` | 16 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`COMM-PCB-POINTER`<br/><small>`DFHCOMMAREA.COMM-PCB-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 17 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DETAILS`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS`</small> | Group Array [20] | *DISPLAY* | 21 | 1960 | **OCCURS:** 1 TO 20 (DEPENDING ON NUMBER-OF-ACCOUNTS) | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-EYE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 21 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 25 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-SCODE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 35 | 6 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACCNO`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 41 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 49 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-INT-RATE`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 57 | 6 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 63 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 63 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 63 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 65 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 67 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OVERDRAFT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 71 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 79 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 79 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 79 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 81 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 83 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 87 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-GROUP`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 87 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DAY`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 87 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-MONTH`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 89 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-YEAR`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 91 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 95 | 12 | — | `FETCH-DATA`<br/><small>*FD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACTUAL-BAL`<br/><small>`DFHCOMMAREA.ACCOUNT-DETAILS.COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 107 | 12 | — | `FETCH-DATA`<br/><small>*FD010*</small> |

