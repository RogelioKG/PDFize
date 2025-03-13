@set WAITING=15
@set "EXE_NAME=pdfize"
@set "TEST_DATA_DIR=tests\test_data"
@set "TEST_RESULTS_DIR=tests\test_results"

@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%
@REM @call "scripts\tests\pdf-to-img.bat" %EXE_NAME% %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\img-to-pdf.bat" %EXE_NAME% %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-split.bat" %EXE_NAME% %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-merge.bat" %EXE_NAME% %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-to-img-mp.bat" %EXE_NAME% %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%