# Data Dictionary: `GETSCODE`

**Author:** James O'Grady  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 4 |
| **Level-88 Business Rules** | 0 |
| **Memory Overlays (REDEFINES)** | 0 |
| **Working-Storage Span** | 6 bytes |

## WORKING-STORAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 77 | `LITERAL-SORTCODE`<br/><small>`LITERAL-SORTCODE`</small> | Numeric Display (6 digits) | `9(6)` | 0 | 6 | **Default:** `987654` | `PREMIERE`<br/><small>*A010*</small> |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 6 | — | — |
| 03 | &nbsp;&nbsp;`GETSORTCODEOperation`<br/><small>`DFHCOMMAREA.GETSORTCODEOperation`</small> | Group | *DISPLAY* | 0 | 6 | — | — |
| 06 | &nbsp;&nbsp;&nbsp;&nbsp;`SORTCODE`<br/><small>`DFHCOMMAREA.GETSORTCODEOperation.SORTCODE`</small> | Alphanumeric (6 chars) | `xXXXXX` | 0 | 6 | — | `PREMIERE`<br/><small>*A010*</small> |

