@echo off
REM Run Network Tester in GUI/System Tray mode (No Console Window)

REM Detect Python (use pythonw to hide console)
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main_gui.py
) else (
    start "" pythonw main_gui.py
)

REM Exit immediately (no pause, no console window stays open)
exit
