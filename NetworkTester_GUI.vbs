' VBScript to run NetworkTester_GUI.pyz without console window
' This is a silent launcher - no console, just the system tray icon

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check for virtual environment pythonw first, then system pythonw
pythonw = scriptDir & "\.venv\Scripts\pythonw.exe"
pyzFile = scriptDir & "\NetworkTester_GUI.pyz"

If Not fso.FileExists(pythonw) Then
    pythonw = "pythonw"
End If

' Run pythonw with the .pyz file, hidden (0 = hidden window)
WshShell.Run """" & pythonw & """ """ & pyzFile & """", 0, False

Set WshShell = Nothing
Set fso = Nothing
