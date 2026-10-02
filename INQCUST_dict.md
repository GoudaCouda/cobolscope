# Data Dictionary: `INQCUST`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 175 |
| **Level-88 Business Rules** | 4 |
| **Memory Overlays (REDEFINES)** | 6 |
| **Working-Storage Span** | 407 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SYSIDERR-RETRY`<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 0 | 3 | — | — |
| 77 | `INQCUST-RETRY`<br/><small>`INQCUST-RETRY`</small> | Numeric Display (4 digits) | `9999` | 3 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`GENERATE-RANDOM-CUSTOMER`<br/><small>*GRC010*</small><br/>&nbsp;<br/>`GENERATE-RANDOM-CUSTOMER-AGAIN`<br/><small>*GRCA10*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 7 | 0 | — | — |
| 01 | **`HOST-CUSTOMER-ROW`**<br/><small>`HOST-CUSTOMER-ROW`</small> | Group | *DISPLAY* | 7 | 384 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-EYECATCHER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 7 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-SORTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 11 | 6 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-NUMBER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-NUMBER`</small> | Alphanumeric (10 chars) | `X(10)` | 17 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-TITLE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 27 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-FIRST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 37 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-LAST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 87 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-DOB`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-DOB`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 137 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-PHONE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 141 | 20 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE1`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 161 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE2`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 211 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CITY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 261 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-POSTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 311 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-COUNTRY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 321 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-STATUS`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 371 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREATE-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREATE-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 381 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREDIT-SCORE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREDIT-SCORE`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 385 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CS-REVIEW-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CS-REVIEW-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 387 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 391 | 0 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 391 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 399 | 8 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 399 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 403 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 403 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-EYE`<br/><small>`DFHCOMMAREA.INQCUST-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-SCODE`<br/><small>`DFHCOMMAREA.INQCUST-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 4 | 6 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-CUSTNO`<br/><small>`DFHCOMMAREA.INQCUST-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 10 | 10 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-NAME`<br/><small>`DFHCOMMAREA.INQCUST-NAME`</small> | Group | *DISPLAY* | 20 | 110 | — | `PREMIERE`<br/><small>*P010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-TITLE`<br/><small>`DFHCOMMAREA.INQCUST-NAME.INQCUST-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 20 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-FIRST-NAME`<br/><small>`DFHCOMMAREA.INQCUST-NAME.INQCUST-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 30 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-LAST-NAME`<br/><small>`DFHCOMMAREA.INQCUST-NAME.INQCUST-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 80 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-DOB`<br/><small>`DFHCOMMAREA.INQCUST-DOB`</small> | Group | *DISPLAY* | 130 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-DD`<br/><small>`DFHCOMMAREA.INQCUST-DOB.INQCUST-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 130 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-MM`<br/><small>`DFHCOMMAREA.INQCUST-DOB.INQCUST-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 132 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-YYYY`<br/><small>`DFHCOMMAREA.INQCUST-DOB.INQCUST-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 134 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PHONE`<br/><small>`DFHCOMMAREA.INQCUST-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 138 | 20 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-ADDR`<br/><small>`DFHCOMMAREA.INQCUST-ADDR`</small> | Group | *DISPLAY* | 158 | 210 | — | `PREMIERE`<br/><small>*P010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE1`<br/><small>`DFHCOMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 158 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE2`<br/><small>`DFHCOMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 208 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CITY`<br/><small>`DFHCOMMAREA.INQCUST-ADDR.INQCUST-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 258 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-POSTCODE`<br/><small>`DFHCOMMAREA.INQCUST-ADDR.INQCUST-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 308 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-COUNTRY`<br/><small>`DFHCOMMAREA.INQCUST-ADDR.INQCUST-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 318 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-STATUS`<br/><small>`DFHCOMMAREA.INQCUST-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 368 | 10 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-CREATED-DATE`<br/><small>`DFHCOMMAREA.INQCUST-CREATED-DATE`</small> | Group | *DISPLAY* | 378 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-DD`<br/><small>`DFHCOMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-DD`</small> | Numeric Display (2 digits) | `99` | 378 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-MM`<br/><small>`DFHCOMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-MM`</small> | Numeric Display (2 digits) | `99` | 380 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-YYYY`<br/><small>`DFHCOMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-YYYY`</small> | Numeric Display (4 digits) | `9999` | 382 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREDIT-SCORE`<br/><small>`DFHCOMMAREA.INQCUST-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 386 | 3 | — | `PREMIERE`<br/><small>*P010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-CS-REVIEW-DT`<br/><small>`DFHCOMMAREA.INQCUST-CS-REVIEW-DT`</small> | Group | *DISPLAY* | 389 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-DD`<br/><small>`DFHCOMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-DD`</small> | Numeric Display (2 digits) | `99` | 389 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-MM`<br/><small>`DFHCOMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-MM`</small> | Numeric Display (2 digits) | `99` | 391 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-YYYY`<br/><small>`DFHCOMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-YYYY`</small> | Numeric Display (4 digits) | `9999` | 393 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-SUCCESS`<br/><small>`DFHCOMMAREA.INQCUST-INQ-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 397 | 1 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-NCS`<br/><small>*RCN010*</small><br/>*( +4 more)* |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-FAIL-CD`<br/><small>`DFHCOMMAREA.INQCUST-INQ-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 398 | 1 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>*( +2 more)* |
| 03 | &nbsp;&nbsp;`INQCUST-PCB-POINTER`<br/><small>`DFHCOMMAREA.INQCUST-PCB-POINTER`</small> | Alphanumeric (4 chars) | `X(4)` | 399 | 4 | — | — |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*P010*</small> |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 6 | 397 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-RECORD`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD`</small> | Group | *DISPLAY* | 6 | 397 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-EYECATCHER`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 6 | 4 | • `88 CUSTOMER-EYECATCHER-VALUE`: 'CUST' | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-KEY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-KEY`</small> | Group | *DISPLAY* | 10 | 16 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-SORTCODE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 10 | 6 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 16 | 10 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NAME`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-NAME`</small> | Group | *DISPLAY* | 26 | 110 | — | `PREMIERE`<br/><small>*P010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-TITLE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 26 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-FIRST-NAME`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 36 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-LAST-NAME`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 86 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-DOB`</small> | Group | *DISPLAY* | 136 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-DAY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 136 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-MONTH`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 138 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-YEAR`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 140 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-PHONE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 144 | 20 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDRESS`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS`</small> | Group | *DISPLAY* | 164 | 210 | — | `PREMIERE`<br/><small>*P010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE1`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 164 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE2`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 214 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CITY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 264 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-POSTCODE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 314 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-COUNTRY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 324 | 50 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-STATUS`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 374 | 10 | • `88 CUSTOMER-STATUS-ACTIVE`: 'ACTIVE'<br/>• `88 CUSTOMER-STATUS-INACTIVE`: 'INACTIVE'<br/>• `88 CUSTOMER-STATUS-SUSPENDED`: 'SUSPENDED' | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DATE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE`</small> | Group | *DISPLAY* | 384 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DAY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 384 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-MONTH`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 386 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-YEAR`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 388 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREDIT-SCORE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 392 | 3 | — | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DATE`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 395 | 8 | — | `PREMIERE`<br/><small>*P010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DAY`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 395 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-MONTH`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 397 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-YEAR`<br/><small>`OUTPUT-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 399 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 403 | 16 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 403 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-CUST-NUMBER`<br/><small>`CUSTOMER-KY.REQUIRED-CUST-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 409 | 10 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`CUSTOMER-KY2`**<br/><small>`CUSTOMER-KY2`</small> | Group | *DISPLAY* | 419 | 16 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE2`<br/><small>`CUSTOMER-KY2.REQUIRED-SORT-CODE2`</small> | Numeric Display (6 digits) | `9(6)` | 419 | 6 | **Default:** `0` | `GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 03 | &nbsp;&nbsp;`REQUIRED-CUST-NUMBER2`<br/><small>`CUSTOMER-KY2.REQUIRED-CUST-NUMBER2`</small> | Numeric Display (10 digits) | `9(10)` | 425 | 10 | **Default:** `0` | `READ-CUSTOMER-NCS`<br/><small>*RCN010*</small><br/>&nbsp;<br/>`GET-LAST-CUSTOMER-DB2`<br/><small>*GLCD010*</small> |
| 01 | **`RANDOM-CUSTOMER`**<br/><small>`RANDOM-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 435 | 10 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>*( +2 more)* |
| 01 | **`HIGHEST-CUST-NUMBER`**<br/><small>`HIGHEST-CUST-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 445 | 10 | **Default:** `0` | — |
| 01 | **`EXIT-VSAM-READ`**<br/><small>`EXIT-VSAM-READ`</small> | Alphanumeric (1 chars) | `X` | 455 | 1 | **Default:** `N` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`EXIT-DB2-READ`**<br/><small>`EXIT-DB2-READ`</small> | Alphanumeric (1 chars) | `X` | 456 | 1 | **Default:** `N` | `PREMIERE`<br/><small>*P010*</small> |
| 01 | **`EXIT-IMS-READ`**<br/><small>`EXIT-IMS-READ`</small> | Alphanumeric (1 chars) | `X` | 457 | 1 | **Default:** `N` | — |
| 01 | **`WS-V-RETRIED`**<br/><small>`WS-V-RETRIED`</small> | Alphanumeric (1 chars) | `X` | 458 | 1 | **Default:** `N` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-DB2`<br/><small>*RCD010*</small> |
| 01 | **`WS-D-RETRIED`**<br/><small>`WS-D-RETRIED`</small> | Alphanumeric (1 chars) | `X` | 459 | 1 | **Default:** `N` | `PREMIERE`<br/><small>*P010*</small> |
| 01 | **`WS-PROGRAM`**<br/><small>`WS-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 460 | 8 | **Default:** `SPACES` | — |
| 01 | **`NCS-CUST-NO-STUFF`**<br/><small>`NCS-CUST-NO-STUFF`</small> | Group | *DISPLAY* | 468 | 34 | — | — |
| 03 | &nbsp;&nbsp;`NCS-CUST-NO-NAME`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-NAME`</small> | Group | *DISPLAY* | 468 | 16 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-CUST-NO-ACT-NAME`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-NAME.NCS-CUST-NO-ACT-NAME`</small> | Alphanumeric (8 chars) | `X(8)` | 468 | 8 | **Default:** `HBNKCUST` | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-CUST-NO-TEST-SORT`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-NAME.NCS-CUST-NO-TEST-SORT`</small> | Alphanumeric (6 chars) | `X(6)` | 476 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`NCS-CUST-NO-FILL`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-NAME.NCS-CUST-NO-FILL`</small> | Alphanumeric (2 chars) | `XX` | 482 | 2 | — | — |
| 03 | &nbsp;&nbsp;`NCS-CUST-NO-INC`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-INC`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 484 | 8 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`NCS-CUST-NO-VALUE`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-VALUE`</small> | Unsigned BigInt (64-bit Binary) | `9(16)`<br/>*COMP* | 492 | 8 | **Default:** `0` | `PREMIERE`<br/><small>*P010*</small><br/>&nbsp;<br/>`READ-CUSTOMER-NCS`<br/><small>*RCN010*</small><br/>*( +3 more)* |
| 03 | &nbsp;&nbsp;`NCS-CUST-NO-RESP`<br/><small>`NCS-CUST-NO-STUFF.NCS-CUST-NO-RESP`</small> | Alphanumeric (2 chars) | `XX` | 500 | 2 | **Default:** `00` | — |
| 01 | **`WS-PASSED-DATA`**<br/><small>`WS-PASSED-DATA`</small> | Group | *DISPLAY* | 502 | 13 | — | — |
| 02 | &nbsp;&nbsp;`WS-TEST-KEY`<br/><small>`WS-PASSED-DATA.WS-TEST-KEY`</small> | Alphanumeric (4 chars) | `X(4)` | 502 | 4 | — | — |
| 02 | &nbsp;&nbsp;`WS-SORT-CODE`<br/><small>`WS-PASSED-DATA.WS-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 506 | 6 | — | — |
| 02 | &nbsp;&nbsp;`WS-CUSTOMER-RANGE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE`</small> | Group | *DISPLAY* | 512 | 3 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-TOP`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-TOP`</small> | Alphanumeric (1 chars) | `X` | 512 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-MIDDLE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-MIDDLE`</small> | Alphanumeric (1 chars) | `X` | 513 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-BOTTOM`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-BOTTOM`</small> | Alphanumeric (1 chars) | `X` | 514 | 1 | — | — |
| 01 | **`WS-SORT-DIV`**<br/><small>`WS-SORT-DIV`</small> | Group | *DISPLAY* | 515 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV1`<br/><small>`WS-SORT-DIV.WS-SORT-DIV1`</small> | Alphanumeric (2 chars) | `XX` | 515 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV2`<br/><small>`WS-SORT-DIV.WS-SORT-DIV2`</small> | Alphanumeric (2 chars) | `XX` | 517 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV3`<br/><small>`WS-SORT-DIV.WS-SORT-DIV3`</small> | Alphanumeric (2 chars) | `XX` | 519 | 2 | — | — |
| 01 | **`WS-DISP-CUST-NO-VAL`**<br/><small>`WS-DISP-CUST-NO-VAL`</small> | Signed Numeric Display (18 digits) | `S9(18)` | 521 | 18 | — | — |
| 01 | **`VAR-REMIX`**<br/><small>`VAR-REMIX`</small> | Group | *DISPLAY* | 539 | 6 | — | — |
| 03 | &nbsp;&nbsp;`REMIX-SCODE`<br/><small>`VAR-REMIX.REMIX-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 539 | 6 | — | — |
| 03 | &nbsp;&nbsp;`REMIX-NUM`<br/><small>`VAR-REMIX.REMIX-NUM`</small> | Group | *DISPLAY* | 539 | 6 | <mark>REDEFINES REMIX-SCODE</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`REMIX-SCODE-NUM`<br/><small>`VAR-REMIX.REMIX-NUM.REMIX-SCODE-NUM`</small> | Numeric Display (6 digits) | `9(6)` | 539 | 6 | — | — |
| 01 | **`VAR-REMIX2`**<br/><small>`VAR-REMIX2`</small> | Group | *DISPLAY* | 545 | 3 | — | — |
| 03 | &nbsp;&nbsp;`REMIX2-CREDIT-SCR`<br/><small>`VAR-REMIX2.REMIX2-CREDIT-SCR`</small> | Alphanumeric (3 chars) | `X(3)` | 545 | 3 | — | — |
| 03 | &nbsp;&nbsp;`REMIX2-NUM`<br/><small>`VAR-REMIX2.REMIX2-NUM`</small> | Group | *DISPLAY* | 545 | 3 | <mark>REDEFINES REMIX2-CREDIT-SCR</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`REMIX2-CREDIT-SCR-NUM`<br/><small>`VAR-REMIX2.REMIX2-NUM.REMIX2-CREDIT-SCR-NUM`</small> | Numeric Display (3 digits) | `9(3)` | 545 | 3 | — | — |
| 01 | **`MY-ABEND-CODE`**<br/><small>`MY-ABEND-CODE`</small> | Alphanumeric (4 chars) | `XXXX` | 548 | 4 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-STORM-DRAIN`**<br/><small>`WS-STORM-DRAIN`</small> | Alphanumeric (1 chars) | `X` | 552 | 1 | **Default:** `N` | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 553 | 20 | — | — |
| 01 | **`WS-INVOKING-PROGRAM`**<br/><small>`WS-INVOKING-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 573 | 8 | — | — |
| 01 | **`WS-POINTER`**<br/><small>`WS-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 581 | 4 | — | — |
| 01 | **`WS-POINTER-BYTES`**<br/><small>`WS-POINTER-BYTES`</small> | Alphanumeric (8 chars) | `X(8)` | 581 | 8 | <mark>REDEFINES WS-POINTER</mark> | — |
| 01 | **`WS-POINTER-NUMBER`**<br/><small>`WS-POINTER-NUMBER`</small> | Unsigned Integer (32-bit Binary) | `9(8)`<br/>*BINARY* | 581 | 4 | <mark>REDEFINES WS-POINTER</mark> | — |
| 01 | **`WS-POINTER-NUMBER-DISPLAY`**<br/><small>`WS-POINTER-NUMBER-DISPLAY`</small> | Numeric Display (8 digits) | `9(8)` | 589 | 8 | — | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 597 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 605 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 605 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 605 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 607 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 608 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 610 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 611 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 615 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 615 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 617 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 618 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 620 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 621 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 625 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 625 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 625 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 625 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 627 | 2 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 629 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 631 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 639 | 678 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 639 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 639 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 647 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 651 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 659 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 663 | 10 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 673 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 681 | 4 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 685 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 693 | 8 | — | `ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 701 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 709 | 8 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 717 | 600 | — | `READ-CUSTOMER-DB2`<br/><small>*RCD010*</small><br/>&nbsp;<br/>`ABEND-HANDLING`<br/><small>*AH010*</small> |

