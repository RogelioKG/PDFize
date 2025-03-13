@set "EXE_NAME=%1"
@set "TEST_DATA_DIR=%2"
@set "TEST_RESULTS_DIR=%3"
@set WAITING=%4


::====== PDF : image (mp) ======::

%EXE_NAME% pdf-to-img "%TEST_DATA_DIR%\many_pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp" --parallel -w 4
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% pdf-to-img "%TEST_DATA_DIR%\many_pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp" --parallel
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% pdf-to-img "%TEST_DATA_DIR%\many_pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp" --parallel --subdir
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% pdf-to-img "%TEST_DATA_DIR%\large_pdf" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp_single" --parallel
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

%EXE_NAME% pdf-to-img "%TEST_DATA_DIR%\large_pdf\Design Patterns.pdf" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp_single" --parallel
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

::====== Profiler ======::

@REM viztracer -o "%TEST_RESULTS_DIR%\result.html" -- "%EXE_NAME%" pdf-to-img "%TEST_DATA_DIR%\large_pdf\Design Patterns.pdf" -o "%TEST_RESULTS_DIR%\test_pdf_to_img_mp_single" --parallel
@REM @timeout %WAITING%
@REM @call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%
@REM vizviewer "%TEST_RESULTS_DIR%\result.html"