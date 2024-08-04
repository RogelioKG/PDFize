@call "scripts\venv.bat"
pyinstaller -F pdfize.py --icon="icon\pdfize.ico"
copy "dist\pdfize.exe" "%HomeDrive%%HomePath%\Desktop\pdfize.exe"