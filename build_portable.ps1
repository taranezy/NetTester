# Build a portable self-contained Python application (PYZ format)
# This creates a single file that runs with Python - no PyInstaller needed!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Portable Network Tester" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/3] Preparing build directory..." -ForegroundColor Yellow
if (Test-Path "build_pyz") {
    Remove-Item -Recurse -Force build_pyz
}
New-Item -ItemType Directory -Path build_pyz | Out-Null

Write-Host "[2/3] Copying application files..." -ForegroundColor Yellow
Copy-Item -Recurse services build_pyz\services
Copy-Item -Recurse src build_pyz\src
Copy-Item main.py build_pyz\__main__.py
Copy-Item config.json build_pyz\config.json

Write-Host "[3/3] Creating portable application..." -ForegroundColor Yellow
& python -m zipapp build_pyz -o NetworkTester.pyz -p "/usr/bin/env python"

if (Test-Path "NetworkTester.pyz") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Created: NetworkTester.pyz" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run: " -NoNewline
    Write-Host "python NetworkTester.pyz" -ForegroundColor Yellow
    Write-Host "Or on Windows: " -NoNewline
    Write-Host "NetworkTester.pyz" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This is a single-file portable application!" -ForegroundColor Green
    Write-Host "No installation needed, just requires Python." -ForegroundColor Green
    
    # Cleanup
    Remove-Item -Recurse -Force build_pyz
    
    Write-Host ""
    Write-Host "File size: " -NoNewline
    $size = (Get-Item NetworkTester.pyz).Length / 1KB
    Write-Host ("{0:N2} KB" -f $size) -ForegroundColor Cyan
} else {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
