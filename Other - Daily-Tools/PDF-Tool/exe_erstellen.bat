@echo off
echo Installiere benoetigte Pakete...
pip install pymupdf pyinstaller -q
echo.
echo Erstelle pdf_tool.exe ...
pyinstaller --onefile --windowed --name "PDF Tool" pdf_tool_devs.py
echo.
echo Fertig! Die exe liegt im Ordner: dist\PDF Tool.exe
pause
