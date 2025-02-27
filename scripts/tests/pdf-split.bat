@set "TEST_DATA_DIR=%1"
@set "TEST_RESULTS_DIR=%2"
@set WAITING=%3

::====== PDF split ======::

py pdfize.py split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 3 5 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

py pdfize.py split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 5 3 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

py pdfize.py split "%TEST_DATA_DIR%\pdfs\result.pdf" -r 3 -1 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

py pdfize.py split "%TEST_DATA_DIR%\pdfs\result.pdf" -r -2 3 -o "%TEST_RESULTS_DIR%\test_pdf_split\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%