# Run Network Tester in GUI/System Tray mode (No Console Window)

# Detect Python (use pythonw to hide console)
if (Test-Path ".venv\Scripts\pythonw.exe") {
    Start-Process -FilePath ".venv\Scripts\pythonw.exe" -ArgumentList "main_gui.py" -WindowStyle Hidden
} else {
    Start-Process -FilePath "pythonw" -ArgumentList "main_gui.py" -WindowStyle Hidden
}
