@set "TEST_DATA_DIR=%1"
@set "TEST_RESULTS_DIR=%2"
@set WAITING=%3

::====== image : PDF =====::

@echo 1 image : 1 PDF
py pdfize.py img-to-pdf "%TEST_DATA_DIR%\images\no_man_sky.jpg" -o "%TEST_RESULTS_DIR%\test_img_to_pdf\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo m images : 1 PDF
py pdfize.py img-to-pdf "%TEST_DATA_DIR%\images" -o "%TEST_RESULTS_DIR%\test_img_to_pdf\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%