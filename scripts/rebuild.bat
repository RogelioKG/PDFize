@call "scripts\venv.bat"
pyinstaller -F pdfize.py
copy "dist\pdfize.exe" "%HomeDrive%%HomePath%\Desktop\pdfize.exe"