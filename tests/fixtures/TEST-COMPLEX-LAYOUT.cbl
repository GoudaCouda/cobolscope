       IDENTIFICATION DIVISION.
       PROGRAM-ID. TSTCMPLX.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       77  WS-STANDALONE-COUNT        PIC S9(4) COMP VALUE 0.

       01  WS-CUSTOMER-RECORD.
           05  WS-RECORD-HEADER.
               10  WS-RECORD-TYPE     PIC X.
               10  FILLER             PIC X(2).
               10  WS-RECORD-LENGTH   PIC 9(5) COMP-3.
           05  WS-CUSTOMER-DETAIL.
               10  WS-CUSTOMER-KEY.
                   15  WS-BRANCH-CODE  PIC 9(6).
                   15  WS-ACCOUNT-NO   PIC 9(10).
               10  WS-CUSTOMER-NAME.
                   15  WS-TITLE        PIC X(8).
                   15  WS-FIRST-NAME   PIC X(20).
                   15  WS-LAST-NAME    PIC X(30).
               10  WS-CONTACT-GROUP.
                   15  WS-PHONE OCCURS 3 TIMES.
                       20  WS-PHONE-TYPE PIC X.
                       20  WS-PHONE-NUMBER PIC X(15).
           05  WS-ACCOUNT-TABLE OCCURS 2 TIMES.
               10  WS-ACCOUNT-DETAIL.
                   15  WS-ACCOUNT-TYPE PIC X(3).
                   15  FILLER          PIC X.
                   15  WS-BALANCE      PIC S9(9)V99 COMP-3.
                   15  WS-LIMIT        PIC S9(9) COMP.
               10  WS-MONTH-TABLE OCCURS 12 TIMES.
                   15  WS-MONTH-AMOUNT PIC S9(7)V99 COMP-3.

       01  WS-STATUS                  PIC X VALUE 'N'.
           88  WS-STATUS-VALID        VALUE 'Y'.
           88  WS-STATUS-INVALID      VALUE 'N'.

       01  WS-DATE-STORAGE.
           05  WS-DATE-RAW            PIC X(8).
           05  WS-DATE-PARTS REDEFINES WS-DATE-RAW.
               10  WS-DATE-YEAR       PIC 9(4).
               10  WS-DATE-MONTH      PIC 99.
               10  WS-DATE-DAY        PIC 99.
           05  WS-DATE-TRAILER        PIC X(2).

       01  WS-ALIGNMENT-RECORD.
           05  WS-ALIGN-PREFIX        PIC X.
           05  FILLER                 PIC X.
           05  WS-ALIGNED-SHORT       PIC S9(4) COMP.
           05  FILLER                 PIC X(3).
           05  FILLER                 PIC X(3).
           05  WS-ALIGNED-LONG        PIC S9(9) COMP.
           05  WS-ALIGN-SUFFIX        PIC X(2).

       LINKAGE SECTION.
       01  LK-REQUEST.
           05  LK-REQUEST-ID          PIC X(12).
           05  LK-REQUEST-DATA.
               10  LK-REQUEST-CODE    PIC 9(4) COMP.
               10  LK-REQUEST-AMOUNT  PIC S9(7)V99 COMP-3.
               10  FILLER             PIC X(5).

       PROCEDURE DIVISION USING LK-REQUEST.
       0000-MAIN.
           GOBACK.
