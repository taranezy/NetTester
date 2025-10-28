@echo off
REM Silent launcher for NetworkTester_GUI.pyz (No Console Window)

REM Use VBScript launcher to hide console completely
if exist "NetworkTester_GUI.vbs" (
    wscript "NetworkTester_GUI.vbs"
) else (
    REM Fallback: Use pythonw directly
    if exist ".venv\Scripts\pythonw.exe" (
        start "" ".venv\Scripts\pythonw.exe" NetworkTester_GUI.pyz
    ) else (
        start "" pythonw NetworkTester_GUI.pyz
    )
)

exit
