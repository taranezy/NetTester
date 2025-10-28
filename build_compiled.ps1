# Build a compiled version where source code is protected
# Users will only see bytecode (.pyc files), not your source code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building COMPILED Network Tester" -ForegroundColor Cyan
Write-Host "Source code will be protected!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Detect Python
if (Test-Path ".venv\Scripts\python.exe") {
    $python = ".venv\Scripts\python.exe"
    Write-Host "Using virtual environment Python" -ForegroundColor Green
} else {
    $python = "python"
    Write-Host "Using system Python" -ForegroundColor Green
}

# Run the build script
& $python build_compiled.py

Read-Host "`nPress Enter to exit"
