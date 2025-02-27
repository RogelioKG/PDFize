@set WAITING=15
@set "TEST_DATA_DIR=tests\test_data"
@set "TEST_RESULTS_DIR=tests\test_results"

@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%
@REM @call "scripts\tests\pdf-to-img.bat" %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\img-to-pdf.bat" %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-split.bat" %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-merge.bat" %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%
@REM @call "scripts\tests\pdf-to-img-mp.bat" %TEST_DATA_DIR% %TEST_RESULTS_DIR% %WAITING%