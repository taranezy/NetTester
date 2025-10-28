@echo off
REM ================================================================
REM           NETWORK MONITOR - DOUBLE-CLICK TO START
REM ================================================================
REM 
REM This will start Network Monitor in your system tray.
REM 
REM Look for the network icon in the bottom-right of your screen!
REM 
REM NO CONSOLE WINDOW WILL APPEAR - App runs silently.
REM 
REM ================================================================

REM Launch silently using VBScript
if exist "NetworkTester_GUI_Source.vbs" (
    wscript "NetworkTester_GUI_Source.vbs"
) else (
    REM Fallback to pythonw
    if exist ".venv\Scripts\pythonw.exe" (
        start "" /B ".venv\Scripts\pythonw.exe" main_gui.py
    ) else (
        start "" /B pythonw main_gui.py
    )
)

REM Exit immediately (no pause, no window)
exit /B 0
