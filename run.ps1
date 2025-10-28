# PowerShell script to run Network Tester
# No PyInstaller needed - runs directly with Python

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Network Tester - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Use virtual environment if it exists, otherwise use system Python
if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "Using virtual environment..." -ForegroundColor Green
    & .venv\Scripts\python.exe main.py
} else {
    Write-Host "Using system Python..." -ForegroundColor Green
    & python main.py
}

Read-Host "`nPress Enter to exit"
