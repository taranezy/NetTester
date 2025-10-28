@echo off
REM =============================================================
REM Network Tester - Silent GUI Launcher (NO CONSOLE WINDOW)
REM =============================================================
REM This launcher starts the app in system tray mode with
REM absolutely NO console window visible.
REM =============================================================

REM Use VBScript to launch completely hidden
if exist "NetworkTester_GUI.vbs" (
    REM Launch GUI from source
    if exist "main_gui.py" (
        wscript NetworkTester_GUI_Source.vbs
    ) else (
        REM Launch from .pyz file
        wscript NetworkTester_GUI.vbs
    )
) else (
    REM Fallback: Direct pythonw launch
    if exist ".venv\Scripts\pythonw.exe" (
        start "" /B ".venv\Scripts\pythonw.exe" main_gui.py
    ) else (
        start "" /B pythonw main_gui.py
    )
)

REM Exit immediately
exit /B 0
