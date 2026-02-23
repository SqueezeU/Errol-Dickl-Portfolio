@echo off
echo Suche Anaconda Python...

:: Typische Anaconda-Pfade durchsuchen
set CONDA_PYTHON=
if exist "%USERPROFILE%\anaconda3\python.exe" set CONDA_PYTHON=%USERPROFILE%\anaconda3\
if exist "%USERPROFILE%\Anaconda3\python.exe" set CONDA_PYTHON=%USERPROFILE%\Anaconda3\
if exist "C:\ProgramData\anaconda3\python.exe" set CONDA_PYTHON=C:\ProgramData\anaconda3\
if exist "C:\anaconda3\python.exe" set CONDA_PYTHON=C:\anaconda3\

if "%CONDA_PYTHON%"=="" (
    echo FEHLER: Anaconda nicht gefunden!
    echo Bitte Anaconda Prompt oeffnen und von dort starten.
    pause
    exit
)

echo Gefunden: %CONDA_PYTHON%
echo.
echo Installiere benoetigte Pakete...
"%CONDA_PYTHON%python.exe" -m pip install pymupdf pyinstaller -q
echo.
echo Erstelle PDF Tool User.exe ...
"%CONDA_PYTHON%Scripts\pyinstaller.exe" "PDF Tool User.spec"
echo.
echo Fertig! Die exe liegt im Ordner: dist\
pause
