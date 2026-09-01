# NIST ANSI COBOL-85 Test Suite

## Overview

The **COBOL Compiler Validation System (CCVS85)** is a comprehensive test suite
developed by the National Institute of Standards and Technology (NIST) to validate COBOL
compiler conformance to the COBOL-85 standard (ANSI X3.23-1985, ISO 1989-1985).

It was later enhanced by rhe National Computing Centre, UK. It seems they made
a significant contribution in the nineties, adding tests for X/Open Cobol.

## Contents

This repository holds the COBOL source code for the NIST ANSI COBOL 85 test suite, release 4.2,
yet without the X/Open extensions.

### Test Suite Files

| File             | Size    | Description                                  |
|------------------|---------|----------------------------------------------|
| `newcob.val`     | 26.9 MB | Decompressed test suite master file          |
| `doc/`           | 21.4 MB | Documentation                                |
| `src/`           | 27.1 MB | 512 individual source and data files         |
| `z390/`          | 1.84 MB | 73 source and data files foruse with z390    |

### Documentation

| File                                                                           | Size    | Description                             |
|--------------------------------------------------------------------------------|---------|-----------------------------------------|
| [CCVS85 User Guide v4.2](doc/CCVS85_User_Guide_v4.2.pdf)                       |  6.9 MB | CCVS User Guide plus x/Open addendum    |
| [CCVS Documentation](doc/NISTIR_5731_CCVS_Documentation.pdf)                   |  6.1 MB | CCVS User Guide and reference           |
| [CCVS85 Concepts](NIST_SP_500-186_CCVS85_Concepts.pdf)                         |  3.9 MB | Issues in Transparent File Access       |
| [Intrinsic Functions Test](NIST_SP_500-203_COBOL_Intrinsic_Functions_Test.pdf) |  4.6 MB | Intrinsic function module tests         |
| `NIST_SP_500-162_Compiler_Validation.pdf`                                      | 21.1 MB | General compiler validation methodology |

**Note:** the document `NIST_SP_500-162_Compiler_Validation.pdf` is referenced, but not contained in this repository.

## Test Modules

The suite includes **14 test modules** covering all major COBOL-85 features:

| Prefix | Module              | Programs | Description                            |
|--------|---------------------|----------|----------------------------------------|
| NC     | Nucleus             |  97      | Core language features                 |
| SQ     | Sequential          |  86 +  1 | Sequential file operations             |
| IF     | Intrinsic Functions |  45      | Built-in functions (ANSI X3.23b-1993)  |
| IX     | Indexed I/O         |  42      | ISAM/VSAM indexed files                |
| IC     | Inter-program Comm  |  35 + 25 | CALL, CANCEL, nested programs          |
| RL     | Relative I/O        |  35      | Relative record file handling          |
| ST     | Sort/Merge          |  40      | SORT and MERGE statements              |
| DB     | Debug               |  15      | Debug module features                  |
| SG     | Segmentation        |  13      | Overlay segmentation                   |
| SM     | Source Manipulation |  17      | COPY and REPLACING                     |
| CM     | Communication       |   9      | Communication module                   |
| RW     | Report Writer       |   6      | Report generation                      |
| OB     | Obsolete            |   9      | Deprecated elements                    |
| EX     | Executive           |   1      | Test suite control program             |
| K      | Copy members        |  49      | Copy members (not programs)            |
| ALT    | Copy members        |   2      | Copy members for use by EXEC85 program |
|        | Data members        |   2      | For use with NC                        |

**Note:** the additional programs (1 for SQ and 25 for IC) are modified copies
that were created specifically for zCobol. These programs exist in the z390 subdirectory.

## Sources

This archive was assembled from multiple sources:

1. [**Wayback Machine**](https://web.archive.org/web/20060620073554/http://www.itl.nist.gov/div897/ctg/suites/newcob.val.Z) (Primary)
2. [**NIST Publications**](https://nvlpubs.nist.gov/)
3. [**GnuCOBOL SourceForge**](https://sourceforge.net/projects/open-cobol/files/nist/)
4. [**zCOBOL Project**](https://www.zcobol.org/)

After the initial download, 4 other sources were located and all collections were manually compared
to weed out any changes that had been applied to some of the collections.

## Usage

The test suite is used by COBOL compiler vendors and open-source projects
(GnuCOBOL, zCOBOL) to validate language conformance. The `EXEC85.cbl` program is
the executive that processes and prepares test programs.

## Extraction process

The first program in the `newcob.val` file `EXEC85` is intended to be extracted manually in order to use it
to extract all the source elements from the archive file. For details, please refer to the
(User Guide)[doc/CCVS85_User_Guide_v4.2.pdf] paragraphs 3.2 through 3.4 on pages 6 through 11.

### Running Tests

1. Extract the `EXEC85.CBL` from the archive (manually or otherwise)
2. Compile `EXEC85.CBL` (the executive program)
3. Use `EXEC85` to extract and configure individual test programs
4. Compile and run each test program
5. Compare output to expected results

## Description from internet archive

The COBOL85 test suite is a product of the National Computing Centre, UK.
It is used to determine, insofar as is practical, the degree to which a COBOL processor
conforms to the COBOL standard (ANSI X3.23-1985, ISO 1989-1985, ANSI X3.23a-1989 and ANSI X3.23b-1993.)

The COBOL85 test suite consists of programs containing features of Standard COBOL,
their related data and an executive program that prepares the test programs for compilation.
Each program includes tests and supporting procedures indicating the results of the tests.
The testing of a processor in a particular hardware/operating system environment is
accomplished by compiling and executing each program.

The COBOL Test Suite is a compressed file that must be extracted from a UNIX system.
Please rename the file as "filename" Z. To run the test suite, you need to extract and
set up the COBOL Executive routine program; execute the COBOL Executive to select and
prepare the test programs for compilation, and then prepare the necessary job scripts
to compile and execute the test programs.

## License and copyright

There are no specific licences specified in the source code.

There are copyright notices in some of the reports generated stating:

    FOR OFFICIAL USE ONLY
    ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.
    COPYRIGHT 1985

The National Computing Centre, UK. is also named as a source. It seems they made
a significant contribution in the nineties, adding tests for x/Open Cobol.
We have not been able to retrieve the details of this, nor have we found the
test programs that were added as part of that effort.

The code is already available in some other projects for validation of COBOL functionality.

See [sourceforge GnuCobol](https://sourceforge.net/projects/gnucobol/files/nist/)

The best case is this code could be treated as in the public domain.

## Historical Significance

- **First released**: 1986 (Version 2.0)
- **Final version**: 4.2 (October 1992)
- **Standards tested**: FIPS PUB 21-3, ANSI X3.23-1985, ISO 1989-1985
- **Used by**: IBM, Micro Focus, Fujitsu, GnuCOBOL, and virtually every COBOL compiler vendor

This test suite represents the gold standard for COBOL compiler validation
and remains relevant today for legacy system migration and modern COBOL implementations.

# Notes on adoption for the zCobol project

This repository holds the COBOL source code for the NIST ANSI COBOL 85 test suite.

    COBOL 85 VERSION 4.2, Apr  1993 SSVG

SSVG stands for Software Standards Validation Group which was a division of NIST
(National Institute of Standards and Technology).

The source was obtained from [archive.org](https://web.archive.org/web/20230917224831/https:/www.itl.nist.gov/div897/ctg/cobol_form.htm)
It is a single file `newcob.val` containing all the source elements needed to conduct the test.

The (`newcob.val`)[newcob.val] can be found in the root folder of this directory.
The extracted individual files are available in this repository in the (`src`)[src\] folder.

### python split_val.py

To circumvent dependence on the standard `EXEC85` program, we created
the Python script (`split_val.py`)[split_val.py] to decompose into individial files.
This script can be used as an alternative to the `EXEC85` program, although the python script is more limited in function.

The Python script `split_val.py` can be used split the `newcob.val` file into individial files and place it into the `src` folder
without making any substitutions or replacements as `EXEC85` might do.

The script assigns file extensions based on the file type provided in the header records.

* COBOL -> .COB
* CLBRY -> .CPY
* DATA -> .DAT

## zCobol use of the NIST test Suite

For z390 a separate subdirectoey has been created: z390

This directory contains z390-specific variations of NIST test programs and
copies of copy members - z390 requires extension .CPZ rather than .CPY

It also contains the RUNNIST.BAT script.
Start the RUNNIST.BAT without parameters to get an explanation of its parameters.

The RUNNIST.BAT procedure will compile, link, and execute all programs in the NIST suite
and also the additional z390 variations.
A complete log of all error messages can be found in (the full log)[z390/#full_log.txt].
Detailed documentation can be found in (zCobol compiler status by program)[z390/_status.md]

## Status in relation to z390 / zCobol compiler

The zCobol compiler still has a lot of limitations resulting in a large number of errors and failed compiles.
The z390 subdirectory holds source versions specific to z390/zCobol. Most importantly:
- The IC module uses nested programs which are not supported by zCobol. The programs have been stored as separate source files.
- The copy members used in the SM module have an extension of .CPY, but zCobol requires .CPZ instead. Required copy members are stored as .CPZ files.
- The RUNNIST.BAT script will compile the entire NIST suite and create #full_log.txt
- The #full_log.txt is intended to be used to monitor effects of code changes in z390/zCobol.
  Each code change to zCobol should lead to reduction of error messages in this file.
  No new additions should be allowed to appear.

