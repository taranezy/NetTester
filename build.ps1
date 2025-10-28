# Build script for creating standalone executable
# Run this script to build NetworkTester.exe

Write-Host "Building Network Tester executable..." -ForegroundColor Cyan
Write-Host ""

# Detect Python executable (check virtual environment first)
$pythonExe = $null
if (Test-Path ".venv\Scripts\python.exe") {
    $pythonExe = ".venv\Scripts\python.exe"
    Write-Host "Using virtual environment Python" -ForegroundColor Green
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = "python"
    Write-Host "Using system Python" -ForegroundColor Green
} else {
    Write-Host "Python not found! Please install Python." -ForegroundColor Red
    exit 1
}

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Cyan
$pyinstallerCheck = & $pythonExe -m pip show pyinstaller 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    & $pythonExe -m pip install pyinstaller
}

# Build the executable
Write-Host "Building executable with PyInstaller..." -ForegroundColor Green
& $pythonExe -m PyInstaller NetworkTester.spec --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Executable location: dist\NetworkTester.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Don't forget to:" -ForegroundColor Yellow
    Write-Host "1. Copy config.json to the dist folder" -ForegroundColor Yellow
    Write-Host "2. Update config.json with your email settings" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
}
