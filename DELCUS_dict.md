# Data Dictionary: `DELCUS`

**Author:** Jon Collett  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 376 |
| **Level-88 Business Rules** | 32 |
| **Memory Overlays (REDEFINES)** | 17 |
| **Working-Storage Span** | 4,857 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `SORTCODE`<br/><small>`SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`SYSIDERR-RETRY`**<br/><small>`SYSIDERR-RETRY`</small> | Numeric Display (3 digits) | `999` | 6 | 3 | — | — |
| 01 | **`FILE-RETRY`**<br/><small>`FILE-RETRY`</small> | Numeric Display (3 digits) | `999` | 9 | 3 | — | — |
| 01 | **`WS-EXIT-RETRY-LOOP`**<br/><small>`WS-EXIT-RETRY-LOOP`</small> | Alphanumeric (1 chars) | `X` | 12 | 1 | — | — |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 13 | 0 | — | — |
| 01 | **`HOST-CUSTOMER-ROW`**<br/><small>`HOST-CUSTOMER-ROW`</small> | Group | *DISPLAY* | 13 | 384 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-EYECATCHER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 13 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-SORTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-SORTCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 17 | 6 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-NUMBER`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-NUMBER`</small> | Alphanumeric (10 chars) | `X(10)` | 23 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-TITLE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 33 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-FIRST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 43 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-LAST-NAME`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 93 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-DOB`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-DOB`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 143 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-PHONE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 147 | 20 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE1`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 167 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-ADDR-LINE2`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 217 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CITY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 267 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-POSTCODE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 317 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-COUNTRY`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 327 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-STATUS`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 377 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREATE-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREATE-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 387 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CREDIT-SCORE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CREDIT-SCORE`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 391 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-CUSTOMER-CS-REVIEW-DATE`<br/><small>`HOST-CUSTOMER-ROW.HV-CUSTOMER-CS-REVIEW-DATE`</small> | Signed Integer (32-bit Binary) | `S9(9)`<br/>*COMP* | 393 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 397 | 0 | — | — |
| 01 | **`HOST-PROCTRAN-ROW`**<br/><small>`HOST-PROCTRAN-ROW`</small> | Group | *DISPLAY* | 397 | 96 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-EYECATCHER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 397 | 4 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-SORT-CODE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-SORT-CODE`</small> | Alphanumeric (6 chars) | `X(6)` | 401 | 6 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-ACC-NUMBER`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-ACC-NUMBER`</small> | Alphanumeric (8 chars) | `X(8)` | 407 | 8 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DATE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 415 | 10 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TIME`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TIME`</small> | Alphanumeric (6 chars) | `X(6)` | 425 | 6 | — | — |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-REF`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-REF`</small> | Alphanumeric (12 chars) | `X(12)` | 431 | 12 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-TYPE`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 443 | 3 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-DESC`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 446 | 40 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`HV-PROCTRAN-AMOUNT`<br/><small>`HOST-PROCTRAN-ROW.HV-PROCTRAN-AMOUNT`</small> | Signed Decimal(12, 2) Packed | `S9(10)V99`<br/>*COMP_3* | 486 | 7 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 01 | **`FILLER`**<br/><small>`FILLER`</small> | Elementary | *DISPLAY* | 493 | 0 | — | — |
| 01 | **`SQLCODE-DISPLAY`**<br/><small>`SQLCODE-DISPLAY`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 493 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 01 | **`WS-CICS-WORK-AREA`**<br/><small>`WS-CICS-WORK-AREA`</small> | Group | *DISPLAY* | 501 | 8 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 501 | 4 | — | — |
| 05 | &nbsp;&nbsp;`WS-CICS-RESP2`<br/><small>`WS-CICS-WORK-AREA.WS-CICS-RESP2`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 505 | 4 | — | — |
| 01 | **`EXIT-BROWSE-LOOP`**<br/><small>`EXIT-BROWSE-LOOP`</small> | Alphanumeric (1 chars) | `X` | 509 | 1 | **Default:** `N` | — |
| 01 | **`OUTPUT-DATA`**<br/><small>`OUTPUT-DATA`</small> | Group | *DISPLAY* | 510 | 98 | — | — |
| 03 | &nbsp;&nbsp;`ACCOUNT-DATA`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA`</small> | Group | *DISPLAY* | 510 | 98 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-EYE-CATCHER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 510 | 4 | • `88 ACCOUNT-EYECATCHER-VALUE`: 'ACCT' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-CUST-NO`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 514 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-KEY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY`</small> | Group | *DISPLAY* | 524 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-SORT-CODE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 524 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NUMBER`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-KEY.ACCOUNT-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 530 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-TYPE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 538 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-INTEREST-RATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 546 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 552 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP`</small> | Group | *DISPLAY* | 552 | 8 | <mark>REDEFINES ACCOUNT-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 552 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 554 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OPENED-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OPENED-GROUP.ACCOUNT-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 556 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-OVERDRAFT-LIMIT`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 560 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 568 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 568 | 8 | <mark>REDEFINES ACCOUNT-LAST-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 568 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 570 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-LAST-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-LAST-STMT-GROUP.ACCOUNT-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 572 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DATE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 576 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-GROUP`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 576 | 8 | <mark>REDEFINES ACCOUNT-NEXT-STMT-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-DAY`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 576 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-MONTH`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 578 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-NEXT-STMT-YEAR`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-NEXT-STMT-GROUP.ACCOUNT-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 580 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-AVAILABLE-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 584 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ACCOUNT-ACTUAL-BALANCE`<br/><small>`OUTPUT-DATA.ACCOUNT-DATA.ACCOUNT-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 596 | 12 | — | — |
| 01 | **`OUTPUT-CUST-DATA`**<br/><small>`OUTPUT-CUST-DATA`</small> | Group | *DISPLAY* | 608 | 397 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-RECORD`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD`</small> | Group | *DISPLAY* | 608 | 397 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-EYECATCHER`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 608 | 4 | • `88 CUSTOMER-EYECATCHER-VALUE`: 'CUST' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-KEY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY`</small> | Group | *DISPLAY* | 612 | 16 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-SORTCODE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 612 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-KEY.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 618 | 10 | — | `GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-NAME`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME`</small> | Group | *DISPLAY* | 628 | 110 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-TITLE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 628 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-FIRST-NAME`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 638 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-LAST-NAME`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-NAME.CUSTOMER-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 688 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB`</small> | Group | *DISPLAY* | 738 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-DAY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 738 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-MONTH`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 740 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-DOB-YEAR`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-DOB.CUSTOMER-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 742 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-PHONE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 746 | 20 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDRESS`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS`</small> | Group | *DISPLAY* | 766 | 210 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE1`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 766 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-ADDR-LINE2`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 816 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CITY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 866 | 50 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-POSTCODE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 916 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-COUNTRY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-ADDRESS.CUSTOMER-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 926 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-STATUS`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 976 | 10 | • `88 CUSTOMER-STATUS-ACTIVE`: 'ACTIVE'<br/>• `88 CUSTOMER-STATUS-INACTIVE`: 'INACTIVE'<br/>• `88 CUSTOMER-STATUS-SUSPENDED`: 'SUSPENDED' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DATE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE`</small> | Group | *DISPLAY* | 986 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-DAY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 986 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-MONTH`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 988 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREATED-YEAR`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREATED-DATE.CUSTOMER-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 990 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CREDIT-SCORE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 994 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DATE`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 997 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-DAY`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 997 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-MONTH`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 999 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`CUSTOMER-CS-REVIEW-YEAR`<br/><small>`OUTPUT-CUST-DATA.CUSTOMER-RECORD.CUSTOMER-CS-REVIEW-DATE.CUSTOMER-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1001 | 4 | — | — |
| 01 | **`PROCTRAN-AREA`**<br/><small>`PROCTRAN-AREA`</small> | Group | *DISPLAY* | 1005 | 99 | — | — |
| 03 | &nbsp;&nbsp;`PROC-TRAN-DATA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA`</small> | Group | *DISPLAY* | 1005 | 99 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-EYE-CATCHER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 1005 | 4 | • `88 PROC-TRAN-VALID`: 'PRTR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-AREA`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA`</small> | Group | *DISPLAY* | 1005 | 4 | <mark>REDEFINES PROC-TRAN-EYE-CATCHER</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-LOGICAL-DELETE-FLAG`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.PROC-TRAN-LOGICAL-DELETE-FLAG`</small> | Alphanumeric (1 chars) | `X` | 1005 | 1 | • `88 PROC-TRAN-LOGICALLY-DELETED`: 'X'FF'' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-LOGICAL-DELETE-AREA.FILLER`</small> | Alphanumeric (3 chars) | `X(3)` | 1006 | 3 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-ID`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID`</small> | Group | *DISPLAY* | 1009 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-SORT-CODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 1009 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-NUMBER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-ID.PROC-TRAN-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 1015 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 1023 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP`</small> | Group | *DISPLAY* | 1023 | 8 | <mark>REDEFINES PROC-TRAN-DATE</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1023 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 1027 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DATE-GRP-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DATE-GRP.PROC-TRAN-DATE-GRP-DD`</small> | Numeric Display (2 digits) | `99` | 1029 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME`</small> | Numeric Display (6 digits) | `9(6)` | 1031 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP`</small> | Group | *DISPLAY* | 1031 | 6 | <mark>REDEFINES PROC-TRAN-TIME</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-HH`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 1031 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 1033 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TIME-GRP-SS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TIME-GRP.PROC-TRAN-TIME-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 1035 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-REF`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-REF`</small> | Numeric Display (12 digits) | `9(12)` | 1037 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-TYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-TYPE`</small> | Alphanumeric (3 chars) | `X(3)` | 1049 | 3 | • `88 PROC-TY-CHEQUE-ACKNOWLEDGED`: 'CHA'<br/>• `88 PROC-TY-CHEQUE-FAILURE`: 'CHF'<br/>• `88 PROC-TY-CHEQUE-PAID-IN`: 'CHI'<br/>• `88 PROC-TY-CHEQUE-PAID-OUT`: 'CHO'<br/>• `88 PROC-TY-CREDIT`: 'CRE'<br/>• `88 PROC-TY-DEBIT`: 'DEB'<br/>• `88 PROC-TY-WEB-CREATE-ACCOUNT`: 'ICA'<br/>• `88 PROC-TY-WEB-CREATE-CUSTOMER`: 'ICC'<br/>• `88 PROC-TY-WEB-DELETE-ACCOUNT`: 'IDA'<br/>• `88 PROC-TY-WEB-DELETE-CUSTOMER`: 'IDC'<br/>• `88 PROC-TY-BRANCH-CREATE-ACCOUNT`: 'OCA'<br/>• `88 PROC-TY-BRANCH-CREATE-CUSTOMER`: 'OCC'<br/>• `88 PROC-TY-BRANCH-DELETE-ACCOUNT`: 'ODA'<br/>• `88 PROC-TY-BRANCH-DELETE-CUSTOMER`: 'ODC'<br/>• `88 PROC-TY-CREATE-SODD`: 'OCS'<br/>• `88 PROC-TY-PAYMENT-CREDIT`: 'PCR'<br/>• `88 PROC-TY-PAYMENT-DEBIT`: 'PDR'<br/>• `88 PROC-TY-TRANSFER`: 'TFR' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC`</small> | Alphanumeric (40 chars) | `X(40)` | 1052 | 40 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR`</small> | Group | *DISPLAY* | 1052 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-HEADER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-HEADER`</small> | Alphanumeric (26 chars) | `X(26)` | 1052 | 26 | • `88 PROC-TRAN-DESC-XFR-FLAG`: 'TRANSFER' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1078 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-XFR-ACCOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-XFR.PROC-TRAN-DESC-XFR-ACCOUNT`</small> | Numeric Display (8 digits) | `9(8)` | 1084 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC`</small> | Group | *DISPLAY* | 1052 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 1052 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1062 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 1070 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 1072 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1074 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 1078 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 1080 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1082 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELACC.PROC-DESC-DELACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 1086 | 6 | • `88 PROC-DESC-DELACC-FLAG`: 'DELETE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CREACC`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC`</small> | Group | *DISPLAY* | 1052 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 1052 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-ACCTYPE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-ACCTYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1062 | 8 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-DD`</small> | Numeric Display (2 digits) | `99` | 1070 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-MM`</small> | Numeric Display (2 digits) | `99` | 1072 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-LAST-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-LAST-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1074 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-DD`</small> | Numeric Display (2 digits) | `99` | 1078 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-MM`</small> | Numeric Display (2 digits) | `99` | 1080 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-NEXT-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-NEXT-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1082 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CREACC-FOOTER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CREACC.PROC-DESC-CREACC-FOOTER`</small> | Alphanumeric (6 chars) | `X(6)` | 1086 | 6 | • `88 PROC-DESC-CREACC-FLAG`: 'CREATE' | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-DELCUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS`</small> | Group | *DISPLAY* | 1052 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1052 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 1058 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 1068 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1082 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 1086 | 1 | • `88 PROC-DESC-DELCUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 1087 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 1089 | 1 | • `88 PROC-DESC-DELCUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-DELCUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-DELCUS.PROC-DESC-DELCUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 1090 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-DESC-CRECUS`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS`</small> | Group | *DISPLAY* | 1052 | 40 | <mark>REDEFINES PROC-TRAN-DESC</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-SORTCODE`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1052 | 6 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-CUSTOMER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 1058 | 10 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-NAME`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-NAME`</small> | Alphanumeric (14 chars) | `X(14)` | 1068 | 14 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-YYYY`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1082 | 4 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER`</small> | Alphanumeric (1 chars) | `X` | 1086 | 1 | • `88 PROC-DESC-CRECUS-FILLER-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-MM`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 1087 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-FILLER2`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-FILLER2`</small> | Alphanumeric (1 chars) | `X` | 1089 | 1 | • `88 PROC-DESC-CRECUS-FILLER2-SET`: '-' | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`PROC-DESC-CRECUS-DOB-DD`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-DESC-CRECUS.PROC-DESC-CRECUS-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 1090 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`PROC-TRAN-AMOUNT`<br/><small>`PROCTRAN-AREA.PROC-TRAN-DATA.PROC-TRAN-AMOUNT`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1092 | 12 | — | — |
| 01 | **`PROCTRAN-RIDFLD`**<br/><small>`PROCTRAN-RIDFLD`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*COMP* | 1104 | 4 | — | — |
| 77 | `PROCTRAN-RETRY`<br/><small>`PROCTRAN-RETRY`</small> | Numeric Display (3 digits) | `999` | 1108 | 3 | — | — |
| 01 | **`ACCOUNT-ACT-BAL-STORE`**<br/><small>`ACCOUNT-ACT-BAL-STORE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1111 | 12 | **Default:** `0` | — |
| 01 | **`RETURNED-DATA`**<br/><small>`RETURNED-DATA`</small> | Group | *DISPLAY* | 1123 | 98 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-EYE-CATCHER`<br/><small>`RETURNED-DATA.RETURNED-EYE-CATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 1123 | 4 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-CUST-NO`<br/><small>`RETURNED-DATA.RETURNED-CUST-NO`</small> | Numeric Display (10 digits) | `9(10)` | 1127 | 10 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-KEY`<br/><small>`RETURNED-DATA.RETURNED-KEY`</small> | Group | *DISPLAY* | 1137 | 14 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-SORT-CODE`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 1137 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`RETURNED-NUMBER`<br/><small>`RETURNED-DATA.RETURNED-KEY.RETURNED-NUMBER`</small> | Numeric Display (8 digits) | `9(8)` | 1143 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-TYPE`<br/><small>`RETURNED-DATA.RETURNED-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1151 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-INTEREST-RATE`<br/><small>`RETURNED-DATA.RETURNED-INTEREST-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 1159 | 6 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OPENED`<br/><small>`RETURNED-DATA.RETURNED-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 1165 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-OVERDRAFT-LIMIT`<br/><small>`RETURNED-DATA.RETURNED-OVERDRAFT-LIMIT`</small> | Numeric Display (8 digits) | `9(8)` | 1173 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-LAST-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-LAST-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 1181 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-NEXT-STMT-DATE`<br/><small>`RETURNED-DATA.RETURNED-NEXT-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 1189 | 8 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-AVAILABLE-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-AVAILABLE-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1197 | 12 | — | — |
| 03 | &nbsp;&nbsp;`RETURNED-ACTUAL-BALANCE`<br/><small>`RETURNED-DATA.RETURNED-ACTUAL-BALANCE`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1209 | 12 | — | — |
| 01 | **`ACCTCUST-DESIRED-KEY`**<br/><small>`ACCTCUST-DESIRED-KEY`</small> | Unsigned BigInt (64-bit Binary) | `9(10)`<br/>*BINARY* | 1221 | 8 | — | — |
| 01 | **`DB2-DATE-REFORMAT`**<br/><small>`DB2-DATE-REFORMAT`</small> | Group | *DISPLAY* | 1229 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-YR`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-YR`</small> | Numeric Display (4 digits) | `9(4)` | 1229 | 4 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1233 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-MNTH`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-MNTH`</small> | Numeric Display (2 digits) | `99` | 1234 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`DB2-DATE-REFORMAT.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1236 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DB2-DATE-REF-DAY`<br/><small>`DB2-DATE-REFORMAT.DB2-DATE-REF-DAY`</small> | Numeric Display (2 digits) | `99` | 1237 | 2 | — | — |
| 01 | **`DB2-EXIT-LOOP`**<br/><small>`DB2-EXIT-LOOP`</small> | Alphanumeric (1 chars) | `X` | 1239 | 1 | — | — |
| 01 | **`FETCH-DATA-CNT`**<br/><small>`FETCH-DATA-CNT`</small> | Unsigned SmallInt (16-bit Binary) | `9(4)`<br/>*COMP* | 1240 | 2 | — | — |
| 01 | **`WS-CUST-ALT-KEY-LEN`**<br/><small>`WS-CUST-ALT-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1242 | 2 | **Default:** `+10` | — |
| 01 | **`WS-EIBTASKN12`**<br/><small>`WS-EIBTASKN12`</small> | Numeric Display (12 digits) | `9(12)` | 1244 | 12 | **Default:** `0` | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 01 | **`WS-CNT`**<br/><small>`WS-CNT`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1256 | 2 | **Default:** `0` | — |
| 01 | **`CUSTOMER-KY`**<br/><small>`CUSTOMER-KY`</small> | Group | *DISPLAY* | 1258 | 6 | — | — |
| 03 | &nbsp;&nbsp;`REQUIRED-SORT-CODE`<br/><small>`CUSTOMER-KY.REQUIRED-SORT-CODE`</small> | Numeric Display (6 digits) | `9(6)` | 1258 | 6 | **Default:** `0` | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-ACC-KEY-LEN`**<br/><small>`WS-ACC-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1264 | 2 | **Default:** `+14` | — |
| 01 | **`WS-ACC-NUM`**<br/><small>`WS-ACC-NUM`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1266 | 2 | **Default:** `0` | — |
| 01 | **`WS-CUST-KEY-LEN`**<br/><small>`WS-CUST-KEY-LEN`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1268 | 2 | **Default:** `+16` | — |
| 01 | **`WS-CUST-NUM`**<br/><small>`WS-CUST-NUM`</small> | Signed SmallInt (16-bit Binary) | `S9(4)`<br/>*COMP* | 1270 | 2 | **Default:** `0` | — |
| 01 | **`DESIRED-KEY-ACCTCUST`**<br/><small>`DESIRED-KEY-ACCTCUST`</small> | Group | *DISPLAY* | 1272 | 16 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-CUSTOMER-ACCTCUST`<br/><small>`DESIRED-KEY-ACCTCUST.DESIRED-KEY-CUSTOMER-ACCTCUST`</small> | Numeric Display (10 digits) | `9(10)` | 1272 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-SORTCODE-ACCTCUST`<br/><small>`DESIRED-KEY-ACCTCUST.DESIRED-KEY-SORTCODE-ACCTCUST`</small> | Numeric Display (6 digits) | `9(6)` | 1282 | 6 | — | — |
| 01 | **`DESIRED-KEY`**<br/><small>`DESIRED-KEY`</small> | Group | *DISPLAY* | 1288 | 16 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-SORTCODE`<br/><small>`DESIRED-KEY.DESIRED-KEY-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1288 | 6 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`DESIRED-KEY-CUSTOMER`<br/><small>`DESIRED-KEY.DESIRED-KEY-CUSTOMER`</small> | Numeric Display (10 digits) | `9(10)` | 1294 | 10 | — | `PREMIERE`<br/><small>*A010*</small> |
| 01 | **`WS-U-TIME`**<br/><small>`WS-U-TIME`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 1304 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 01 | **`WS-ORIG-DATE`**<br/><small>`WS-ORIG-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 1312 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 01 | **`WS-ORIG-DATE-GRP`**<br/><small>`WS-ORIG-DATE-GRP`</small> | Group | *DISPLAY* | 1312 | 10 | <mark>REDEFINES WS-ORIG-DATE</mark> | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-DD`</small> | Numeric Display (2 digits) | `99` | 1312 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1314 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-MM`</small> | Numeric Display (2 digits) | `99` | 1315 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1317 | 1 | — | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY`<br/><small>`WS-ORIG-DATE-GRP.WS-ORIG-DATE-YYYY`</small> | Numeric Display (4 digits) | `9999` | 1318 | 4 | — | — |
| 01 | **`WS-ORIG-DATE-GRP-X`**<br/><small>`WS-ORIG-DATE-GRP-X`</small> | Group | *DISPLAY* | 1322 | 10 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-DD-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-DD-X`</small> | Alphanumeric (2 chars) | `XX` | 1322 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1324 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-MM-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-MM-X`</small> | Alphanumeric (2 chars) | `XX` | 1325 | 2 | — | — |
| 03 | &nbsp;&nbsp;`FILLER`<br/><small>`WS-ORIG-DATE-GRP-X.FILLER`</small> | Alphanumeric (1 chars) | `X` | 1327 | 1 | **Default:** `.` | — |
| 03 | &nbsp;&nbsp;`WS-ORIG-DATE-YYYY-X`<br/><small>`WS-ORIG-DATE-GRP-X.WS-ORIG-DATE-YYYY-X`</small> | Alphanumeric (4 chars) | `X(4)` | 1328 | 4 | — | — |
| 01 | **`REMIX-STMT-DATE`**<br/><small>`REMIX-STMT-DATE`</small> | Numeric Display (8 digits) | `9(8)` | 1332 | 8 | — | — |
| 01 | **`WS-APPLID`**<br/><small>`WS-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 1340 | 8 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 01 | **`VAR-REMIX`**<br/><small>`VAR-REMIX`</small> | Group | *DISPLAY* | 1348 | 6 | — | — |
| 03 | &nbsp;&nbsp;`REMIX-SCODE`<br/><small>`VAR-REMIX.REMIX-SCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1348 | 6 | — | — |
| 03 | &nbsp;&nbsp;`REMIX-CHAR`<br/><small>`VAR-REMIX.REMIX-CHAR`</small> | Group | *DISPLAY* | 1348 | 6 | <mark>REDEFINES REMIX-SCODE</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`REMIX-SCODE-CHAR`<br/><small>`VAR-REMIX.REMIX-CHAR.REMIX-SCODE-CHAR`</small> | Alphanumeric (6 chars) | `X(6)` | 1348 | 6 | — | — |
| 01 | **`WS-STOREDC-CUSTOMER`**<br/><small>`WS-STOREDC-CUSTOMER`</small> | Group | *DISPLAY* | 1354 | 263 | — | — |
| 03 | &nbsp;&nbsp;`WS-STOREDC-EYECATCHER`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-EYECATCHER`</small> | Alphanumeric (4 chars) | `X(4)` | 1354 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-SORTCODE`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 1358 | 6 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-NUMBER`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 1364 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-NAME`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-NAME`</small> | Alphanumeric (60 chars) | `X(60)` | 1374 | 60 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-ADDRESS`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-ADDRESS`</small> | Alphanumeric (160 chars) | `X(160)` | 1434 | 160 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-DATE-OF-BIRTH`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-DATE-OF-BIRTH`</small> | Alphanumeric (10 chars) | `X(10)` | 1594 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-CREDIT-SCORE`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `9(3)` | 1604 | 3 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`WS-STOREDC-CS-REVIEW-DATE`<br/><small>`WS-STOREDC-CUSTOMER.WS-STOREDC-CS-REVIEW-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 1607 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 01 | **`WS-NONE-LEFT`**<br/><small>`WS-NONE-LEFT`</small> | Alphanumeric (1 chars) | `X` | 1617 | 1 | **Default:** `N` | — |
| 01 | **`WS-EXIT-FETCH`**<br/><small>`WS-EXIT-FETCH`</small> | Alphanumeric (1 chars) | `X` | 1618 | 1 | **Default:** `N` | — |
| 01 | **`DELACC-COMMAREA`**<br/><small>`DELACC-COMMAREA`</small> | Group | *DISPLAY* | 1619 | 118 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-COMM-EYE`<br/><small>`DELACC-COMMAREA.DELACC-COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 1619 | 4 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-CUSTNO`<br/><small>`DELACC-COMMAREA.DELACC-COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 1623 | 10 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-SCODE`<br/><small>`DELACC-COMMAREA.DELACC-COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 1633 | 6 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-ACCNO`<br/><small>`DELACC-COMMAREA.DELACC-COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 1639 | 8 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-COMM-ACC-TYPE`<br/><small>`DELACC-COMMAREA.DELACC-COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1647 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-INT-RATE`<br/><small>`DELACC-COMMAREA.DELACC-COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 1655 | 6 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-OPENED`<br/><small>`DELACC-COMMAREA.DELACC-COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 1661 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-OVERDRAFT`<br/><small>`DELACC-COMMAREA.DELACC-COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 1669 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-LAST-STMT-DT`<br/><small>`DELACC-COMMAREA.DELACC-COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1677 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-NEXT-STMT-DT`<br/><small>`DELACC-COMMAREA.DELACC-COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1685 | 8 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-AVAIL-BAL`<br/><small>`DELACC-COMMAREA.DELACC-COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1693 | 12 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-ACTUAL-BAL`<br/><small>`DELACC-COMMAREA.DELACC-COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1705 | 12 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-SUCCESS`<br/><small>`DELACC-COMMAREA.DELACC-COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1717 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-FAIL-CD`<br/><small>`DELACC-COMMAREA.DELACC-COMM-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 1718 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-DEL-SUCCESS`<br/><small>`DELACC-COMMAREA.DELACC-COMM-DEL-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1719 | 1 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-COMM-DEL-FAIL-CD`<br/><small>`DELACC-COMMAREA.DELACC-COMM-DEL-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 1720 | 1 | — | — |
| 03 | &nbsp;&nbsp;`DELACC-COMM-APPLID`<br/><small>`DELACC-COMMAREA.DELACC-COMM-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 1721 | 8 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-COMM-PCB1`<br/><small>`DELACC-COMMAREA.DELACC-COMM-PCB1`</small> | Memory Pointer (4 bytes) | *POINTER* | 1729 | 4 | — | `GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 03 | &nbsp;&nbsp;`DELACC-COMM-PCB2`<br/><small>`DELACC-COMMAREA.DELACC-COMM-PCB2`</small> | Memory Pointer (4 bytes) | *POINTER* | 1733 | 4 | — | — |
| 01 | **`WS-TOKEN`**<br/><small>`WS-TOKEN`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 1737 | 4 | — | — |
| 01 | **`WS-INDEX`**<br/><small>`WS-INDEX`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 1741 | 4 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 01 | **`INQACCCU-PROGRAM`**<br/><small>`INQACCCU-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 1745 | 8 | **Default:** `INQACCCU` | — |
| 01 | **`INQACCCU-COMMAREA`**<br/><small>`INQACCCU-COMMAREA`</small> | Group | *DISPLAY* | 1753 | 1981 | — | `GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 03 | &nbsp;&nbsp;`NUMBER-OF-ACCOUNTS`<br/><small>`INQACCCU-COMMAREA.NUMBER-OF-ACCOUNTS`</small> | Signed Integer (32-bit Binary) | `S9(8)`<br/>*BINARY* | 1753 | 4 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`DELETE-ACCOUNTS`<br/><small>*DA010*</small><br/>&nbsp;<br/>`GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 03 | &nbsp;&nbsp;`CUSTOMER-NUMBER`<br/><small>`INQACCCU-COMMAREA.CUSTOMER-NUMBER`</small> | Numeric Display (10 digits) | `9(10)` | 1757 | 10 | — | `GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SUCCESS`<br/><small>`INQACCCU-COMMAREA.COMM-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 1767 | 1 | — | — |
| 03 | &nbsp;&nbsp;`COMM-FAIL-CODE`<br/><small>`INQACCCU-COMMAREA.COMM-FAIL-CODE`</small> | Alphanumeric (1 chars) | `X` | 1768 | 1 | — | — |
| 03 | &nbsp;&nbsp;`CUSTOMER-FOUND`<br/><small>`INQACCCU-COMMAREA.CUSTOMER-FOUND`</small> | Alphanumeric (1 chars) | `X` | 1769 | 1 | — | — |
| 03 | &nbsp;&nbsp;`COMM-PCB-POINTER`<br/><small>`INQACCCU-COMMAREA.COMM-PCB-POINTER`</small> | Memory Pointer (4 bytes) | *POINTER* | 1770 | 4 | — | `GET-ACCOUNTS`<br/><small>*GAC010*</small> |
| 03 | &nbsp;&nbsp;`ACCOUNT-DETAILS`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS`</small> | Group Array [20] | *DISPLAY* | 1774 | 1960 | **OCCURS:** 1 TO 20 (DEPENDING ON NUMBER-OF-ACCOUNTS) | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-EYE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 1774 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 1778 | 10 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-ACCOUNTS`<br/><small>*GAC010*</small><br/>&nbsp;<br/>`DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-SCODE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 1788 | 6 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACCNO`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACCNO`</small> | Numeric Display (8 digits) | `9(8)` | 1794 | 8 | — | `DELETE-ACCOUNTS`<br/><small>*DA010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACC-TYPE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACC-TYPE`</small> | Alphanumeric (8 chars) | `X(8)` | 1802 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-INT-RATE`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-INT-RATE`</small> | Decimal Display (6, 2) | `9(4)V99` | 1810 | 6 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED`</small> | Numeric Display (8 digits) | `9(8)` | 1816 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP`</small> | Group | *DISPLAY* | 1816 | 8 | <mark>REDEFINES COMM-OPENED</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-DAY`</small> | Numeric Display (2 digits) | `99` | 1816 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-MONTH`</small> | Numeric Display (2 digits) | `99` | 1818 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-OPENED-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OPENED-GROUP.COMM-OPENED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1820 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-OVERDRAFT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-OVERDRAFT`</small> | Numeric Display (8 digits) | `9(8)` | 1824 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1832 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP`</small> | Group | *DISPLAY* | 1832 | 8 | <mark>REDEFINES COMM-LAST-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 1832 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 1834 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-STMT-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-LAST-STMT-GROUP.COMM-LAST-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1836 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DT`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-DT`</small> | Numeric Display (8 digits) | `9(8)` | 1840 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-GROUP`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP`</small> | Group | *DISPLAY* | 1840 | 8 | <mark>REDEFINES COMM-NEXT-STMT-DT</mark> | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-DAY`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-DAY`</small> | Numeric Display (2 digits) | `99` | 1840 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-MONTH`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-MONTH`</small> | Numeric Display (2 digits) | `99` | 1842 | 2 | — | — |
| 07 | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`COMM-NEXT-STMT-YEAR`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-NEXT-STMT-GROUP.COMM-NEXT-STMT-YEAR`</small> | Numeric Display (4 digits) | `9999` | 1844 | 4 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-AVAIL-BAL`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-AVAIL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1848 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ACTUAL-BAL`<br/><small>`INQACCCU-COMMAREA.ACCOUNT-DETAILS.COMM-ACTUAL-BAL`</small> | Signed Decimal Display (12, 2) | `S9(10)V99` | 1860 | 12 | — | — |
| 01 | **`STORM-DRAIN-CONDITION`**<br/><small>`STORM-DRAIN-CONDITION`</small> | Alphanumeric (20 chars) | `X(20)` | 3734 | 20 | — | — |
| 01 | **`INQCUST-PROGRAM`**<br/><small>`INQCUST-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 3754 | 8 | **Default:** `INQCUST` | — |
| 01 | **`INQCUST-COMMAREA`**<br/><small>`INQCUST-COMMAREA`</small> | Group | *DISPLAY* | 3762 | 403 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-EYE`<br/><small>`INQCUST-COMMAREA.INQCUST-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 3762 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-SCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 3766 | 6 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CUSTNO`<br/><small>`INQCUST-COMMAREA.INQCUST-CUSTNO`</small> | Numeric Display (10 digits) | `9(10)` | 3772 | 10 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME`</small> | Group | *DISPLAY* | 3782 | 110 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-TITLE`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 3782 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-FIRST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 3792 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-LAST-NAME`<br/><small>`INQCUST-COMMAREA.INQCUST-NAME.INQCUST-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 3842 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-DOB`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB`</small> | Group | *DISPLAY* | 3892 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-DD`</small> | Numeric Display (2 digits) | `99` | 3892 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-MM`</small> | Numeric Display (2 digits) | `99` | 3894 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-DOB-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-DOB.INQCUST-DOB-YYYY`</small> | Numeric Display (4 digits) | `9999` | 3896 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-PHONE`<br/><small>`INQCUST-COMMAREA.INQCUST-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 3900 | 20 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-ADDR`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR`</small> | Group | *DISPLAY* | 3920 | 210 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE1`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 3920 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-ADDR-LINE2`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 3970 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CITY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 4020 | 50 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-POSTCODE`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 4070 | 10 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-COUNTRY`<br/><small>`INQCUST-COMMAREA.INQCUST-ADDR.INQCUST-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 4080 | 50 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-STATUS`<br/><small>`INQCUST-COMMAREA.INQCUST-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 4130 | 10 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREATED-DATE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE`</small> | Group | *DISPLAY* | 4140 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-DD`</small> | Numeric Display (2 digits) | `99` | 4140 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-MM`</small> | Numeric Display (2 digits) | `99` | 4142 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CREATED-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CREATED-DATE.INQCUST-CREATED-YYYY`</small> | Numeric Display (4 digits) | `9999` | 4144 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CREDIT-SCORE`<br/><small>`INQCUST-COMMAREA.INQCUST-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `999` | 4148 | 3 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-CS-REVIEW-DT`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT`</small> | Group | *DISPLAY* | 4151 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-DD`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-DD`</small> | Numeric Display (2 digits) | `99` | 4151 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-MM`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-MM`</small> | Numeric Display (2 digits) | `99` | 4153 | 2 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`INQCUST-CS-REVIEW-YYYY`<br/><small>`INQCUST-COMMAREA.INQCUST-CS-REVIEW-DT.INQCUST-CS-REVIEW-YYYY`</small> | Numeric Display (4 digits) | `9999` | 4155 | 4 | — | — |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-SUCCESS`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 4159 | 1 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-INQ-FAIL-CD`<br/><small>`INQCUST-COMMAREA.INQCUST-INQ-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 4160 | 1 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`INQCUST-PCB-POINTER`<br/><small>`INQCUST-COMMAREA.INQCUST-PCB-POINTER`</small> | Alphanumeric (4 chars) | `X(4)` | 4161 | 4 | — | — |
| 01 | **`WS-TIME-DATA`**<br/><small>`WS-TIME-DATA`</small> | Group | *DISPLAY* | 4165 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW`<br/><small>`WS-TIME-DATA.WS-TIME-NOW`</small> | Numeric Display (6 digits) | `9(6)` | 4165 | 6 | — | — |
| 03 | &nbsp;&nbsp;`WS-TIME-NOW-GRP`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP`</small> | Group | *DISPLAY* | 4165 | 6 | <mark>REDEFINES WS-TIME-NOW</mark> | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-HH`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-HH`</small> | Numeric Display (2 digits) | `99` | 4165 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-MM`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-MM`</small> | Numeric Display (2 digits) | `99` | 4167 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`WS-TIME-NOW-GRP-SS`<br/><small>`WS-TIME-DATA.WS-TIME-NOW-GRP.WS-TIME-NOW-GRP-SS`</small> | Numeric Display (2 digits) | `99` | 4169 | 2 | — | — |
| 01 | **`WS-ABEND-PGM`**<br/><small>`WS-ABEND-PGM`</small> | Alphanumeric (8 chars) | `X(8)` | 4171 | 8 | **Default:** `ABNDPROC` | — |
| 01 | **`ABNDINFO-REC`**<br/><small>`ABNDINFO-REC`</small> | Group | *DISPLAY* | 4179 | 678 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-VSAM-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY`</small> | Group | *DISPLAY* | 4179 | 12 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-UTIME-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-UTIME-KEY`</small> | Signed Integer(15) Packed | `S9(15)`<br/>*COMP_3* | 4179 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`ABND-TASKNO-KEY`<br/><small>`ABNDINFO-REC.ABND-VSAM-KEY.ABND-TASKNO-KEY`</small> | Numeric Display (4 digits) | `9(4)` | 4187 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-APPLID`<br/><small>`ABNDINFO-REC.ABND-APPLID`</small> | Alphanumeric (8 chars) | `X(8)` | 4191 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-TRANID`<br/><small>`ABNDINFO-REC.ABND-TRANID`</small> | Alphanumeric (4 chars) | `X(4)` | 4199 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-DATE`<br/><small>`ABNDINFO-REC.ABND-DATE`</small> | Alphanumeric (10 chars) | `X(10)` | 4203 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-TIME`<br/><small>`ABNDINFO-REC.ABND-TIME`</small> | Alphanumeric (8 chars) | `X(8)` | 4213 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-CODE`<br/><small>`ABNDINFO-REC.ABND-CODE`</small> | Alphanumeric (4 chars) | `X(4)` | 4221 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-PROGRAM`<br/><small>`ABNDINFO-REC.ABND-PROGRAM`</small> | Alphanumeric (8 chars) | `X(8)` | 4225 | 8 | — | — |
| 03 | &nbsp;&nbsp;`ABND-RESPCODE`<br/><small>`ABNDINFO-REC.ABND-RESPCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 4233 | 8 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-RESP2CODE`<br/><small>`ABNDINFO-REC.ABND-RESP2CODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 4241 | 8 | — | `WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-SQLCODE`<br/><small>`ABNDINFO-REC.ABND-SQLCODE`</small> | Signed Numeric Display (8 digits) | `S9(8)` | 4249 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |
| 03 | &nbsp;&nbsp;`ABND-FREEFORM`<br/><small>`ABNDINFO-REC.ABND-FREEFORM`</small> | Alphanumeric (600 chars) | `X(600)` | 4257 | 600 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small><br/>&nbsp;<br/>`WRITE-PROCTRAN-CUST-DB2`<br/><small>*WPCD010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 399 | — | `PREMIERE`<br/><small>*A010*</small><br/>&nbsp;<br/>`GET-ACCOUNTS`<br/><small>*GAC010*</small><br/>&nbsp;<br/>`DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-EYE`<br/><small>`DFHCOMMAREA.COMM-EYE`</small> | Alphanumeric (4 chars) | `X(4)` | 0 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-SCODE`<br/><small>`DFHCOMMAREA.COMM-SCODE`</small> | Alphanumeric (6 chars) | `X(6)` | 4 | 6 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CUSTNO`<br/><small>`DFHCOMMAREA.COMM-CUSTNO`</small> | Alphanumeric (10 chars) | `X(10)` | 10 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME`</small> | Group | *DISPLAY* | 20 | 110 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-TITLE`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-TITLE`</small> | Alphanumeric (10 chars) | `X(10)` | 20 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-FIRST-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-FIRST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 30 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-LAST-NAME`<br/><small>`DFHCOMMAREA.COMM-NAME.COMM-LAST-NAME`</small> | Alphanumeric (50 chars) | `X(50)` | 80 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-DOB`<br/><small>`DFHCOMMAREA.COMM-DOB`</small> | Group | *DISPLAY* | 130 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-DAY`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-DAY`</small> | Numeric Display (2 digits) | `99` | 130 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-MONTH`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-MONTH`</small> | Numeric Display (2 digits) | `99` | 132 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-DOB-YEAR`<br/><small>`DFHCOMMAREA.COMM-DOB.COMM-DOB-YEAR`</small> | Numeric Display (4 digits) | `9999` | 134 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-PHONE`<br/><small>`DFHCOMMAREA.COMM-PHONE`</small> | Alphanumeric (20 chars) | `X(20)` | 138 | 20 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-ADDR`<br/><small>`DFHCOMMAREA.COMM-ADDR`</small> | Group | *DISPLAY* | 158 | 210 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ADDR-LINE1`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-ADDR-LINE1`</small> | Alphanumeric (50 chars) | `X(50)` | 158 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-ADDR-LINE2`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-ADDR-LINE2`</small> | Alphanumeric (50 chars) | `X(50)` | 208 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CITY`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-CITY`</small> | Alphanumeric (50 chars) | `X(50)` | 258 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-POSTCODE`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-POSTCODE`</small> | Alphanumeric (10 chars) | `X(10)` | 308 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-COUNTRY`<br/><small>`DFHCOMMAREA.COMM-ADDR.COMM-COUNTRY`</small> | Alphanumeric (50 chars) | `X(50)` | 318 | 50 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-STATUS`<br/><small>`DFHCOMMAREA.COMM-STATUS`</small> | Alphanumeric (10 chars) | `X(10)` | 368 | 10 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CREATED-DATE`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE`</small> | Group | *DISPLAY* | 378 | 8 | — | — |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-DAY`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-DAY`</small> | Numeric Display (2 digits) | `99` | 378 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-MONTH`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-MONTH`</small> | Numeric Display (2 digits) | `99` | 380 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CREATED-YEAR`<br/><small>`DFHCOMMAREA.COMM-CREATED-DATE.COMM-CREATED-YEAR`</small> | Numeric Display (4 digits) | `9999` | 382 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CREDIT-SCORE`<br/><small>`DFHCOMMAREA.COMM-CREDIT-SCORE`</small> | Numeric Display (3 digits) | `9(3)` | 386 | 3 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-CS-REVIEW-DATE`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE`</small> | Group | *DISPLAY* | 389 | 8 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-DAY`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-DAY`</small> | Numeric Display (2 digits) | `99` | 389 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-MONTH`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-MONTH`</small> | Numeric Display (2 digits) | `99` | 391 | 2 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 05 | &nbsp;&nbsp;&nbsp;&nbsp;`COMM-CS-REVIEW-YEAR`<br/><small>`DFHCOMMAREA.COMM-CS-REVIEW-DATE.COMM-CS-REVIEW-YEAR`</small> | Numeric Display (4 digits) | `9999` | 393 | 4 | — | `DEL-CUST-DB2`<br/><small>*DCD010*</small> |
| 03 | &nbsp;&nbsp;`COMM-DEL-SUCCESS`<br/><small>`DFHCOMMAREA.COMM-DEL-SUCCESS`</small> | Alphanumeric (1 chars) | `X` | 397 | 1 | — | `PREMIERE`<br/><small>*A010*</small> |
| 03 | &nbsp;&nbsp;`COMM-DEL-FAIL-CD`<br/><small>`DFHCOMMAREA.COMM-DEL-FAIL-CD`</small> | Alphanumeric (1 chars) | `X` | 398 | 1 | — | `PREMIERE`<br/><small>*A010*</small> |

