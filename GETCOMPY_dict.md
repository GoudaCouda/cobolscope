# Data Dictionary: `GETCOMPY`

**Author:** James O'Grady  
## Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Data Items** | 3 |
| **Level-88 Business Rules** | 0 |
| **Memory Overlays (REDEFINES)** | 0 |
| **Working-Storage Span** | 0 bytes |

## LINKAGE

| Level | Field Name / Path | Business Type | PIC / Usage | Offset | Bytes | Allowed Values / Attributes | References |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| 01 | **`DFHCOMMAREA`**<br/><small>`DFHCOMMAREA`</small> | Group | *DISPLAY* | 0 | 40 | — | — |
| 03 | &nbsp;&nbsp;`GETCompanyOperation`<br/><small>`DFHCOMMAREA.GETCompanyOperation`</small> | Group | *DISPLAY* | 0 | 40 | — | — |
| 06 | &nbsp;&nbsp;&nbsp;&nbsp;`company-name`<br/><small>`DFHCOMMAREA.GETCompanyOperation.company-name`</small> | Alphanumeric (40 chars) | `x(40)` | 0 | 40 | — | `PREMIERE`<br/><small>*A010*</small> |

