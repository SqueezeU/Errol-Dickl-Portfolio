@echo off
echo Installiere benoetigte Pakete...
pip install pymupdf pyinstaller -q
echo.
echo Erstelle PDF Tool User.exe ...
pyinstaller "PDF Tool User.spec"
echo.
echo Fertig! Die exe liegt im Ordner: dist\
pause