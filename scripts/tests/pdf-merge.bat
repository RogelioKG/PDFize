@set "TEST_DATA_DIR=%1"
@set "TEST_RESULTS_DIR=%2"
@set WAITING=%3

::====== PDF merge ======::

py pdfize.py merge "%TEST_DATA_DIR%\pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_merge\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%