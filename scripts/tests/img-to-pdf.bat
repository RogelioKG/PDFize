@set "EXE_NAME=%1"
@set "TEST_DATA_DIR=%2"
@set "TEST_RESULTS_DIR=%3"
@set WAITING=%4


::====== image : PDF =====::

@echo 1 image : 1 PDF
%EXE_NAME% img-to-pdf "%TEST_DATA_DIR%\images\no_man_sky.jpg" -o "%TEST_RESULTS_DIR%\test_img_to_pdf\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo m images : 1 PDF
%EXE_NAME% img-to-pdf "%TEST_DATA_DIR%\images" -o "%TEST_RESULTS_DIR%\test_img_to_pdf\test.pdf"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%