       IDENTIFICATION DIVISION.
       PROGRAM-ID. TSTDIC01.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      * 1. Mixed PIC and USAGE types
       01  WS-TYPES-RECORD.
           05  WS-STR-ALPHANUM       PIC X(10).
           05  WS-NUM-DISPLAY        PIC 9(5)V99.
           05  WS-COMP-1-FLOAT       COMP-1.
           05  WS-COMP-2-FLOAT       COMP-2.
           05  WS-COMP-HALFWORD      PIC S9(4) COMP.
           05  WS-COMP-FULLWORD      PIC S9(8) COMP.
           05  WS-COMP-DOUBLEWORD    PIC S9(16) COMP.
           05  WS-COMP3-PACKED-EVEN  PIC S9(6) COMP-3.
           05  WS-COMP3-PACKED-ODD   PIC S9(7) COMP-3.
           05  WS-PTR-ADDR           USAGE POINTER.

      * 2. Overlays & REDEFINES Trees
       01  WS-BASE-RECORD.
           05  WS-RAW-DATE           PIC X(8).
           05  WS-DATE-PARTS REDEFINES WS-RAW-DATE.
               10  WS-YEAR           PIC 9(4).
               10  WS-MONTH          PIC 9(2).
               10  WS-DAY            PIC 9(2).
           05  WS-NEXT-FIELD         PIC X(4).

      * 3. Multidimensional Arrays (OCCURS)
       01  WS-MATRIX-RECORD.
           05  WS-MONTHS OCCURS 12 TIMES.
               10  WS-MONTH-NAME     PIC X(3).
               10  WS-DAYS OCCURS 31 TIMES PIC X(1).
               10  WS-TOTAL-AMT      PIC S9(5)V99 COMP-3.

      * 4. Level-88 Flags
       01  WS-STATUS-FLAG            PIC X(1).
           88  IS-VALID              VALUE 'Y', 'y'.
           88  IS-INVALID            VALUE 'N', 'n'.
           88  IS-UNKNOWN            VALUE SPACE.

       PROCEDURE DIVISION.
       0000-MAIN.
           DISPLAY 'TEST-DATA-DICT EXECUTED'
           STOP RUN.
