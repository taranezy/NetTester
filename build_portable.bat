@echo off
REM Build a portable self-contained Python application (PYZ format)
REM This creates a single file that runs with Python - no PyInstaller needed!

echo ========================================
echo Building Portable Network Tester
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo [1/3] Preparing build directory...
if exist "build_pyz" rmdir /s /q build_pyz
mkdir build_pyz

echo [2/3] Copying application files...
xcopy /E /I /Y services build_pyz\services >nul
xcopy /E /I /Y src build_pyz\src >nul
copy main.py build_pyz\__main__.py >nul
copy config.json build_pyz\config.json >nul

echo [3/3] Creating portable application...
python -m zipapp build_pyz -o NetworkTester.pyz -p "/usr/bin/env python"

if exist "NetworkTester.pyz" (
    echo.
    echo ========================================
    echo Build Successful!
    echo ========================================
    echo.
    echo Created: NetworkTester.pyz
    echo.
    echo To run: python NetworkTester.pyz
    echo Or on Windows: NetworkTester.pyz
    echo.
    echo This is a single-file portable application!
    echo No installation needed, just requires Python.
    
    REM Cleanup
    rmdir /s /q build_pyz
) else (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

pause
