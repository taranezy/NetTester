@echo off
REM Complete setup and run script - No manual installation needed
REM This script sets up everything and runs the application

echo ========================================
echo Network Tester - Auto Setup and Run
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/3] Python found!
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [2/3] Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo [2/3] Virtual environment already exists
)
echo.

REM Install dependencies (if needed)
echo [3/3] Checking dependencies...
.venv\Scripts\python.exe -m pip install --quiet --upgrade pip
echo Dependencies ready!
echo.

echo ========================================
echo Starting Network Monitor...
echo ========================================
echo.

REM Run the application
.venv\Scripts\python.exe main.py

pause
