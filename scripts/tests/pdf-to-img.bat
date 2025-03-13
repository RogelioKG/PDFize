@set "EXE_NAME=%1"
@set "TEST_DATA_DIR=%2"
@set "TEST_RESULTS_DIR=%3"
@set WAITING=%4


::====== PDF : image ======::

@echo 1 PDF : 1 image
%EXE_NAME% -s ASCII_SPEED pdf-to-img "%TEST_DATA_DIR%\pdfs\calendar112.pdf" -o "%TEST_RESULTS_DIR%\test_pdf_to_img" -n "test" -f "jpeg"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo 1 PDF : m images
%EXE_NAME% -s ASCII_SPEED pdf-to-img "%TEST_DATA_DIR%\pdfs\result.pdf" -o "%TEST_RESULTS_DIR%\test_pdf_to_img" -f "webp"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo m PDFs : m image
%EXE_NAME% -s ASCII_SPEED pdf-to-img "%TEST_DATA_DIR%\pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo m PDFs : m image (--subdir)
%EXE_NAME% -s ASCII_SPEED pdf-to-img "%TEST_DATA_DIR%\pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img" --subdir
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%

@echo m PDFs : m image (--name & pdf dir)
%EXE_NAME% -s ASCII_SPEED pdf-to-img "%TEST_DATA_DIR%\many_pdfs" -o "%TEST_RESULTS_DIR%\test_pdf_to_img" -n "Design Patterns"
@timeout %WAITING%
@call "scripts\tests\clear.bat" %TEST_RESULTS_DIR%