# Build the GUI version with compiled/protected code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Network Tester GUI" -ForegroundColor Cyan
Write-Host "Code Protected Version" -ForegroundColor Cyan
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

& $python build_gui_compiled.py

Read-Host "`nPress Enter to exit"
