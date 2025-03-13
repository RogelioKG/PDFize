@set "EXE_NAME=%1"
@set "TEST_DATA_DIR=%2"
@set "TEST_RESULTS_DIR=%3"
@set WAITING=%4


::====== PDF merge ======::

%EXE_NAME% merge "%TEST_DATA_DIR%\pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_merge\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%