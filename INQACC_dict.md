# Data Dictionary: `INQACC`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 158 |
| **Level-88 Business Rules** | 3 |
| **Memory Overlays (REDEFINES)** | 10 |
| **Working-Storage Span** | 1,172 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>*( +2 more)* |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 6 | 0 | — | — |
| 01 | **`HOST-ACCOUNT-ROW`**<br/><small>`HOST-ACCOUNT-ROW`</small> | Group | *DISPLAY* | 6 | 88 | — | — |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-EYECATCHER`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-CUST-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-CUST-NO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-SORTCODE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 20 | 6 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-NO`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-NO`</small> | Alphanumeric (8 chars) | `X(8)` | 26 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACC-TYPE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 34 | 8 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-INT-RATE`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-INT-RATE`</small> | Signed Decimal(6, 2) Packed | `S9(4)V99`<br/>*COMP_3* | 42 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OPENED`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OPENED`</small> | Alphanumeric (10 chars) | `X(10)` | 46 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-OVERDRAFT-LIM`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-OVERDRAFT-LIM`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 56 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-LAST-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-LAST-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 60 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-NEXT-STMT`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-NEXT-STMT`</small> | Alphanumeric (10 chars) | `X(10)` | 70 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-AVAIL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-AVAIL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 80 | 7 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`HV-ACCOUNT-ACTUAL-BAL`<br/><small>`HOST-ACCOUNT-ROW.HV-ACCOUNT-ACTUAL-BAL`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 87 | 7 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 94 | 0 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 94 | 0 | — | — |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 94 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 94 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 98 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`EXIT-BROWSE-LOOP`**<br/><small>`EXIT-BROWSE-LOOP`</small> | Alphanumeric (1 chars) | `X` | 102 | 1 | **Default:** `N` | — |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 103 | 98 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 103 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 103 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 107 | 10 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 117 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 117 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 123 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 131 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 139 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 145 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 145 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 145 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 147 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 149 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 153 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 161 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 161 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 161 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 163 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 165 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 169 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 169 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 169 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 171 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 173 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 177 | 12 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 189 | 12 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 01 | **`RETURNED-DATA`**<br/><small>`RETURNED-DATA`</small> | Group | *DISPLAY* | 201 | 98 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-EYE-CATCHER`<br/><small>`RETURNED-DATA.RETURNED-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 201 | 4 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-CUST-NO`<br/><small>`RETURNED-DATA.RETURNED-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 205 | 10 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-KEY`<br/><small>`RETURNED-DATA.RETURNED-KEY`</small> | Group | *DISPLAY* | 215 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-SORT-CODE`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 215 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-NUMBER`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 221 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-TYPE`<br/><small>`RETURNED-DATA.RETURNED-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 229 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-INTEREST-RATE`<br/><small>`RETURNED-DATA.RETURNED-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 237 | 6 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OPENED`<br/><small>`RETURNED-DATA.RETURNED-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 243 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OVERDRAFT-LIMIT`<br/><small>`RETURNED-DATA.RETURNED-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 251 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-LAST-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 259 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-NEXT-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 267 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-AVAILABLE-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 275 | 12 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-ACTUAL-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 287 | 12 | — | — |
| 01 | **`DESIRED-KEY`**<br/><small>`DESIRED-KEY`</small> | Unsigned BigInt (64-bit Binary) | `9(10)`<br/>*BINARY* | 299 | 8 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 307 | 10 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 307 | 4 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 311 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 312 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 314 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 315 | 2 | — | `FETCH-DATA`<br/><small>*FD010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 01 | **`DATA-STORE-TYPE`**<br/><small>`DATA-STORE-TYPE`</small> | Alphanumeric (1 chars) | `X` | 317 | 1 | • `88 DATASTORE-TYPE-DB2`: '2'<br/>• `88 DATASTORE-TYPE-VSAM`: 'V' | — |
| 01 | **`DB2-EXIT-LOOP`**<br/><small>`DB2-EXIT-LOOP`</small> | Alphanumeric (1 chars) | `X` | 318 | 1 | — | — |
| 01 | **`FETCH-DATA-CNT`**<br/><small>`FETCH-DATA-CNT`</small> | Unsigned SmallInt (16-bit Binary) | `9(4)`<br/>*COMP* | 319 | 2 | — | — |
| 01 | **`WS-CUST-ALT-KEY-LEN`**<br/><small>`WS-CUST-ALT-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 321 | 2 | **Default:** `+10` | — |
| 01 | **`ACCOUNT-KY`**<br/><small>`ACCOUNT-KY`</small> | Group | *DISPLAY* | 323 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`ACCOUNT-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 323 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`ACCOUNT-KY.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 329 | 8 | **Default:** `0` | — |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 337 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 341 | 1 | **Default:** `N` | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 342 | 20 | — | `CHECK-FOR-STORM-DRAIN-DB2`<br/><small>*CFSDCD010*</small> |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 362 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +3 more)* |
| 01 | **`NCS-ACC-NO-STUFF`**<br/><small>`NCS-ACC-NO-STUFF`</small> | Group | *DISPLAY* | 370 | 34 | — | — |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-NAME`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME`</small> | Group | *DISPLAY* | 370 | 16 | — | `GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-ACT-NAME`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-ACT-NAME`</small> | Alphanumeric (8 chars) | `X(8)` | 370 | 8 | **Default:** `HBNKACCT` | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-TEST-SORT`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-TEST-SORT`</small> | Alphanumeric (6 chars) | `X(6)` | 378 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-ACC-NO-FILL`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-NAME.NCS-ACC-NO-FILL`</small> | Alphanumeric (2 chars) | `XX` | 384 | 2 | — | — |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-INC`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-INC`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 386 | 8 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-VALUE`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-VALUE`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 394 | 8 | **Default:** `0` | `READ-ACCOUNT-LAST`<br/><small>*RAN010*</small> |
| 03 | &nbsp;&nbsp;`NCS-ACC-NO-RESP`<br/><small>`NCS-ACC-NO-STUFF.NCS-ACC-NO-RESP`</small> | Alphanumeric (2 chars) | `XX` | 402 | 2 | **Default:** `00` | — |
| 01 | **`WS-DISP-ACC-NO-VAL`**<br/><small>`WS-DISP-ACC-NO-VAL`</small> | Signed Numeric Display (18 digits) | `S9(18)` | 404 | 18 | — | — |
| 01 | **`ACCOUNT-KY2`**<br/><small>`ACCOUNT-KY2`</small> | Group | *DISPLAY* | 422 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE2`<br/><small>`ACCOUNT-KY2.REQUIRED-SORT-CODE2`</small> | Numeric Display (6 digits) | `9(6)` | 422 | 6 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUMBER2`<br/><small>`ACCOUNT-KY2.REQUIRED-ACC-NUMBER2`</small> | Numeric Display (8 digits) | `9(8)` | 428 | 8 | **Default:** `0` | `READ-ACCOUNT-LAST`<br/><small>*RAN010*</small><br/>&nbsp;<br/>`GET-LAST-ACCOUNT-DB2`<br/><small>*GLAD010*</small> |
| 01 | **`WS-POINTER`**<br/><small>`WS-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 436 | 4 | — | — |
| 01 | **`WS-POINTER-BYTES`**<br/><small>`WS-POINTER-BYTES`</small> | Alphanumeric (8 chars) | `X(8)` | 436 | 8 | <mark>REDEFINES WS-POINTER</mark> | — |
| 01 | **`WS-POINTER-NUMBER`**<br/><small>`WS-POINTER-NUMBER`</small> | Unsigned Integer (32-bit Binary) | `9(8)`<br/>*BINARY* | 436 | 4 | <mark>REDEFINES WS-POINTER</mark> | — |
| 01 | **`WS-POINTER-NUMBER-DISPLAY`**<br/><small>`WS-POINTER-NUMBER-DISPLAY`</small> | Numeric Display (8 digits) | `9(8)` | 444 | 8 | — | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 452 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 460 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 460 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 460 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 462 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 463 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 465 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 466 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 470 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 470 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 472 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 473 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 475 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 476 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 480 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 480 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 480 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 480 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 482 | 2 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 484 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 486 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 494 | 678 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 494 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 494 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 502 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 506 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 514 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 518 | 10 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 528 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 536 | 4 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 540 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 548 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 556 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 564 | 8 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 572 | 600 | — | `READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small><br/>*( +2 more)* |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 103 | — | — |
| 03 | &nbsp;&nbsp;`INQACC-EYE`<br/><small>`DFHCOMMAREA.INQACC-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-CUSTNO`<br/><small>`DFHCOMMAREA.INQACC-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 4 | 10 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-SCODE`<br/><small>`DFHCOMMAREA.INQACC-SCODE`</small> | Numeric Display (6 digits) | `9(6)` | 14 | 6 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-ACCNO`<br/><small>`DFHCOMMAREA.INQACC-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 20 | 8 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`READ-ACCOUNT-DB2`<br/><small>*RAD010*</small><br/>&nbsp;<br/>`FETCH-DATA`<br/><small>*FD010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-ACC-TYPE`<br/><small>`DFHCOMMAREA.INQACC-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 28 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-INT-RATE`<br/><small>`DFHCOMMAREA.INQACC-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 36 | 6 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-OPENED`<br/><small>`DFHCOMMAREA.INQACC-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 42 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-OPENED-GROUP`<br/><small>`DFHCOMMAREA.INQACC-OPENED-GROUP`</small> | Group | *DISPLAY* | 42 | 8 | <mark>REDEFINES INQACC-OPENED</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-OPENED-DAY`<br/><small>`DFHCOMMAREA.INQACC-OPENED-GROUP.INQACC-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 42 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-OPENED-MONTH`<br/><small>`DFHCOMMAREA.INQACC-OPENED-GROUP.INQACC-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 44 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-OPENED-YEAR`<br/><small>`DFHCOMMAREA.INQACC-OPENED-GROUP.INQACC-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 46 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQACC-OVERDRAFT`<br/><small>`DFHCOMMAREA.INQACC-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 50 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-LAST-STMT-DT`<br/><small>`DFHCOMMAREA.INQACC-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 58 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-LAST-STMT-GROUP`<br/><small>`DFHCOMMAREA.INQACC-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 58 | 8 | <mark>REDEFINES INQACC-LAST-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-LAST-STMT-DAY`<br/><small>`DFHCOMMAREA.INQACC-LAST-STMT-GROUP.INQACC-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 58 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-LAST-STMT-MONTH`<br/><small>`DFHCOMMAREA.INQACC-LAST-STMT-GROUP.INQACC-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 60 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-LAST-STMT-YEAR`<br/><small>`DFHCOMMAREA.INQACC-LAST-STMT-GROUP.INQACC-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 62 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQACC-NEXT-STMT-DT`<br/><small>`DFHCOMMAREA.INQACC-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 66 | 8 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-NEXT-STMT-GROUP`<br/><small>`DFHCOMMAREA.INQACC-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 66 | 8 | <mark>REDEFINES INQACC-NEXT-STMT-DT</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-NEXT-STMT-DAY`<br/><small>`DFHCOMMAREA.INQACC-NEXT-STMT-GROUP.INQACC-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 66 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-NEXT-STMT-MONTH`<br/><small>`DFHCOMMAREA.INQACC-NEXT-STMT-GROUP.INQACC-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 68 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQACC-NEXT-STMT-YEAR`<br/><small>`DFHCOMMAREA.INQACC-NEXT-STMT-GROUP.INQACC-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 70 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQACC-AVAIL-BAL`<br/><small>`DFHCOMMAREA.INQACC-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 74 | 12 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-ACTUAL-BAL`<br/><small>`DFHCOMMAREA.INQACC-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 86 | 12 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-SUCCESS`<br/><small>`DFHCOMMAREA.INQACC-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 98 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`INQACC-PCB1-POINTER`<br/><small>`DFHCOMMAREA.INQACC-PCB1-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 99 | 4 | — | — |

