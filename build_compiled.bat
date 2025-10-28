@echo off
REM Build a compiled version where source code is protected
REM Users will only see bytecode (.pyc files), not your source code

echo ========================================
echo Building COMPILED Network Tester
echo Source code will be protected!
echo ========================================
echo.

REM Detect Python
if exist ".venv\Scripts\python.exe" (
    set PYTHON=.venv\Scripts\python.exe
) else (
    set PYTHON=python
)

REM Run the build script
%PYTHON% build_compiled.py

pause
