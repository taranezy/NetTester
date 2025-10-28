@echo off
REM Build the GUI version with compiled/protected code

echo ========================================
echo Building Network Tester GUI
echo Code Protected Version
echo ========================================
echo.

REM Detect Python
if exist ".venv\Scripts\python.exe" (
    set PYTHON=.venv\Scripts\python.exe
) else (
    set PYTHON=python
)

%PYTHON% build_gui_compiled.py

pause
