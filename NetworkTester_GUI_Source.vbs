' VBScript to run main_gui.py without console window
' This launches from source code (for development/testing)

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check for virtual environment pythonw first, then system pythonw
pythonw = scriptDir & "\.venv\Scripts\pythonw.exe"
mainFile = scriptDir & "\main_gui.py"

If Not fso.FileExists(pythonw) Then
    pythonw = "pythonw"
End If

' Run pythonw with main_gui.py, hidden (0 = hidden window)
WshShell.Run """" & pythonw & """ """ & mainFile & """", 0, False

Set WshShell = Nothing
Set fso = Nothing
