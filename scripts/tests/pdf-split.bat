@set "EXE_NAME=%1"
@set "TEST_DATA_DIR=%2"
@set "TEST_RESULTS_DIR=%3"
@set WAITING=%4


::====== PDF split ======::

%EXE_NAME% split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 3 5 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 5 3 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 3 -1 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% split "%TEST_DATA_DIR%\pdfs\result.pdf" -r -2 3 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%