# Data Dictionary: `UPDCUST`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 153 |
| **Level-88 Business Rules** | 4 |
| **Memory Overlays (REDEFINES)** | 2 |
| **Working-Storage Span** | 409 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 77 | `SYSIDERR-RETRY`<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 9 | 0 | — | — |
| 01 | **`HOST-CUSTOMER-ROW`**<br/><small>`HOST-CUSTOMER-ROW`</small> | Group | *DISPLAY* | 9 | 384 | — | — |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-EYECATCHER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 9 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-SORTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 13 | 6 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-NUMBER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-NUMBER`</small> | Alphanumeric (10 chars) | `X(10)` | 19 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-TITLE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 29 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-FIRST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 39 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-LAST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 89 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-DOB`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-DOB`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 139 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-PHONE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 143 | 20 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE1`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 163 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE2`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 213 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CITY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 263 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-POSTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 313 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-COUNTRY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 323 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-STATUS`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 373 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREATE-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREATE-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 383 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREDIT-SCORE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREDIT-SCORE`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 387 | 2 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CS-REVIEW-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CS-REVIEW-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 389 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 393 | 0 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 393 | 8 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 401 | 8 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 401 | 4 | — | — |
| 03 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 405 | 4 | — | — |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 399 | — | — |
| 03 | &nbsp;&nbsp;`COMM-EYE`<br/><small>`DFHCOMMAREA.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SCODE`<br/><small>`DFHCOMMAREA.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 4 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME`</small> | Group | *DISPLAY* | 20 | 110 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-TITLE`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 20 | 10 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-FIRST-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 30 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 80 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-DOB`<br/><small>`DFHCOMMAREA.COMM-DOB`</small> | Group | *DISPLAY* | 130 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-DAY`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 130 | 2 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-MONTH`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 132 | 2 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-YEAR`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 134 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-PHONE`<br/><small>`DFHCOMMAREA.COMM-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 138 | 20 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ADDR`<br/><small>`DFHCOMMAREA.COMM-ADDR`</small> | Group | *DISPLAY* | 158 | 210 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ADDR-LINE1`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 158 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ADDR-LINE2`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 208 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CITY`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 258 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-POSTCODE`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 308 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-COUNTRY`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 318 | 50 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-STATUS`<br/><small>`DFHCOMMAREA.COMM-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 368 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CREATED-DATE`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE`</small> | Group | *DISPLAY* | 378 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-DAY`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 378 | 2 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-MONTH`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 380 | 2 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-YEAR`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 382 | 4 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CREDIT-SCORE`<br/><small>`DFHCOMMAREA.COMM-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `9(3)` | 386 | 3 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CS-REVIEW-DATE`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 389 | 8 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-DAY`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 389 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-MONTH`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 391 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-YEAR`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 393 | 4 | — | — |
| 03 | &nbsp;&nbsp;`COMM-UPD-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-UPD-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 397 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-UPD-FAIL-CD`<br/><small>`DFHCOMMAREA.COMM-UPD-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 398 | 1 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |

## LOCAL-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 0 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 0 | 4 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 4 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 5 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 7 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 8 | 2 | — | — |
| 01 | **`WS-CUST-DATA`**<br/><small>`WS-CUST-DATA`</small> | Group | *DISPLAY* | 10 | 397 | — | — |
| 03 | &nbsp;&nbsp;`CUSTOMER-RECORD`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD`</small> | Group | *DISPLAY* | 10 | 397 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-EYECATCHER`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 10 | 4 | • `88 CUSTOMER-EYECATCHER-VALUE`: 'CUST' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-KEY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY`</small> | Group | *DISPLAY* | 14 | 16 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-SORTCODE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 14 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 20 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NAME`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME`</small> | Group | *DISPLAY* | 30 | 110 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-TITLE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 30 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-FIRST-NAME`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 40 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-LAST-NAME`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 90 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB`</small> | Group | *DISPLAY* | 140 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-DAY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 140 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-MONTH`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 142 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-YEAR`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 144 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-PHONE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 148 | 20 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDRESS`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS`</small> | Group | *DISPLAY* | 168 | 210 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE1`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 168 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE2`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 218 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CITY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 268 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-POSTCODE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 318 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-COUNTRY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 328 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-STATUS`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 378 | 10 | • `88 CUSTOMER-STATUS-ACTIVE`: 'ACTIVE'<br/>• `88 CUSTOMER-STATUS-INACTIVE`: 'INACTIVE'<br/>• `88 CUSTOMER-STATUS-SUSPENDED`: 'SUSPENDED' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DATE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE`</small> | Group | *DISPLAY* | 388 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DAY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 388 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-MONTH`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 390 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-YEAR`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 392 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREDIT-SCORE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 396 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DATE`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 399 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DAY`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 399 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-MONTH`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 401 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-YEAR`<br/><small>`WS-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 403 | 4 | — | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 407 | 12 | **Default:** `0` | — |
| 01 | **`WS-SQLCODE-DISP`**<br/><small>`WS-SQLCODE-DISP`</small> | Numeric Display (9 digits) | `9(9)` | 419 | 9 | **Default:** `0` | — |
| 01 | **`DESIRED-CUST-KEY`**<br/><small>`DESIRED-CUST-KEY`</small> | Group | *DISPLAY* | 428 | 16 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-SORT-CODE`<br/><small>`DESIRED-CUST-KEY.DESIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 428 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 03 | &nbsp;&nbsp;`DESIRED-CUSTNO`<br/><small>`DESIRED-CUST-KEY.DESIRED-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 434 | 10 | — | `UPDATE-CUSTOMER-DB2`<br/><small>*UCD010*</small> |
| 01 | **`WS-CUST-REC-LEN`**<br/><small>`WS-CUST-REC-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 444 | 2 | **Default:** `0` | — |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 446 | 8 | — | — |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 454 | 10 | — | — |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 454 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 454 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 456 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 457 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 459 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 460 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 464 | 10 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 464 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 466 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 467 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 469 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 470 | 4 | — | — |
| 01 | **`REJ-REASON`**<br/><small>`REJ-REASON`</small> | Alphanumeric (2 chars) | `XX` | 474 | 2 | **Default:** `SPACES` | — |
| 01 | **`WS-PASSED-DATA`**<br/><small>`WS-PASSED-DATA`</small> | Group | *DISPLAY* | 476 | 13 | — | — |
| 02 | &nbsp;&nbsp;`WS-TEST-KEY`<br/><small>`WS-PASSED-DATA.WS-TEST-KEY`</small> | Alphanumeric (4 chars) | `X(4)` | 476 | 4 | — | — |
| 02 | &nbsp;&nbsp;`WS-SORT-CODE`<br/><small>`WS-PASSED-DATA.WS-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 480 | 6 | — | — |
| 02 | &nbsp;&nbsp;`WS-CUSTOMER-RANGE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE`</small> | Group | *DISPLAY* | 486 | 3 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-TOP`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-TOP`</small> | Alphanumeric (1 chars) | `X` | 486 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-MIDDLE`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-MIDDLE`</small> | Alphanumeric (1 chars) | `X` | 487 | 1 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-CUSTOMER-RANGE-BOTTOM`<br/><small>`WS-PASSED-DATA.WS-CUSTOMER-RANGE.WS-CUSTOMER-RANGE-BOTTOM`</small> | Alphanumeric (1 chars) | `X` | 488 | 1 | — | — |
| 01 | **`WS-SORT-DIV`**<br/><small>`WS-SORT-DIV`</small> | Group | *DISPLAY* | 489 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV1`<br/><small>`WS-SORT-DIV.WS-SORT-DIV1`</small> | Alphanumeric (2 chars) | `XX` | 489 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV2`<br/><small>`WS-SORT-DIV.WS-SORT-DIV2`</small> | Alphanumeric (2 chars) | `XX` | 491 | 2 | — | — |
| 03 | &nbsp;&nbsp;`WS-SORT-DIV3`<br/><small>`WS-SORT-DIV.WS-SORT-DIV3`</small> | Alphanumeric (2 chars) | `XX` | 493 | 2 | — | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 495 | 14 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 495 | 6 | **Default:** `0` | — |
| 03 | &nbsp;&nbsp;`REQUIRED-ACC-NUM`<br/><small>`CUSTOMER-KY.REQUIRED-ACC-NUM`</small> | Numeric Display (8 digits) | `9(8)` | 501 | 8 | **Default:** `0` | — |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 509 | 20 | — | — |
| 01 | **`WS-UNSTR-TITLE`**<br/><small>`WS-UNSTR-TITLE`</small> | Alphanumeric (9 chars) | `X(9)` | 529 | 9 | — | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-TITLE-VALID`**<br/><small>`WS-TITLE-VALID`</small> | Alphanumeric (1 chars) | `X` | 538 | 1 | — | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 539 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 539 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 539 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 539 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 541 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 543 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 545 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 553 | 678 | — | — |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 553 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 553 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 561 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 565 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 573 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 577 | 10 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 587 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 595 | 4 | — | — |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 599 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 607 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 615 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 623 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 631 | 600 | — | — |

