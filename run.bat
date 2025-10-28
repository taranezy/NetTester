@echo off
REM Simple batch file to run Network Tester without needing PyInstaller
REM This creates a truly portable application

echo ========================================
echo Network Tester - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    .venv\Scripts\python.exe main.py
) else (
    echo Using system Python...
    python main.py
)

pause
