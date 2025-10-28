# Network Tester - Silent GUI Launcher
# Runs in system tray with NO console window

param(
    [string]$Mode = "gui"  # gui or pyz
)

# Function to start without console window
function Start-Hidden {
    param($Command, $Arguments)
    
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Command
    $psi.Arguments = $Arguments
    $psi.CreateNoWindow = $true
    $psi.WindowStyle = 'Hidden'
    $psi.UseShellExecute = $false
    
    [System.Diagnostics.Process]::Start($psi) | Out-Null
}

# Determine which pythonw to use
$pythonw = $null
if (Test-Path ".venv\Scripts\pythonw.exe") {
    $pythonw = Resolve-Path ".venv\Scripts\pythonw.exe"
} elseif (Get-Command pythonw -ErrorAction SilentlyContinue) {
    $pythonw = "pythonw"
} else {
    Write-Host "Error: pythonw not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Run based on mode
if ($Mode -eq "pyz" -and (Test-Path "NetworkTester_GUI.pyz")) {
    Start-Hidden $pythonw "NetworkTester_GUI.pyz"
} else {
    Start-Hidden $pythonw "main_gui.py"
}

# Exit silently
exit 0
