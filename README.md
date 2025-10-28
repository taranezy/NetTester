# Network Tester

A minimalistic network monitoring application that measures latency to Google DNS (8.8.8.8) and sends email alerts when the network is down.

## Features

- 🔄 Pings Google DNS (8.8.8.8) every 30 seconds
- 📊 Logs all latency measurements to `log.txt`
- 📧 Sends email alerts when:
  - Latency exceeds 1000ms
  - No response for 3 consecutive attempts
- 🎯 Built with SOLID principles
- 🔧 Configurable via `config.json`
- 📦 Can be built as standalone executable
- 🖥️ **NEW: System Tray GUI Mode**
  - Runs in Windows system tray
  - Single click: View last 5 pings
  - Double click menu: View full statistics
  - Color-coded network status icon (green/yellow/red)
  - No console window clutter

## Architecture

The application follows SOLID principles:

- **Single Responsibility Principle (SRP)**: Each service has one responsibility
  - `PingService`: Handles ping operations
  - `LoggerService`: Handles logging
  - `EmailService`: Handles email notifications
  - `NetworkMonitor`: Orchestrates the monitoring process

- **Open/Closed Principle**: Easy to extend with new features
- **Dependency Inversion**: High-level modules depend on abstractions

## Project Structure

```
NetTester/
├── services/
│   ├── __init__.py
│   ├── ping_service.py      # Ping functionality
│   ├── logger_service.py    # Logging functionality
│   └── email_service.py     # Email notifications
├── src/
│   └── network_monitor.py   # Main monitoring orchestrator
├── main.py                  # Entry point
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── NetworkTester.spec       # PyInstaller spec file
└── README.md               # This file
```

## Setup

### 1. Install Python
Make sure Python 3.7+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Email Settings

Edit `config.json` and update the email settings:

```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "use_tls": true,
        "recipient_email": "taranezy@gmail.com"
    }
}
```

**For Gmail users:**
1. Enable 2-factor authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password in `sender_password` field

## Running the Application

### 🎨 Option 1: System Tray GUI Mode (RECOMMENDED) ⭐
Run with a nice system tray interface - **NO console window!**

**Easiest - Just double-click:**
```
NetworkTester_GUI.vbs (for .pyz file)
NetworkTester_GUI_Source.vbs (for source code)
START_GUI.bat (auto-detects)
```

**Or run from command line:**
```bash
pythonw main_gui.py
# Or for compiled version:
pythonw NetworkTester_GUI.pyz
```

**Features:**
- 🎯 Runs in Windows system tray (bottom-right of screen)
- 🟢 Color-coded icon (green=good, yellow=slow, red=down)
- 👆 **Single click**: Show popup with last 5 pings
- 🖱️ **Right click → Full Statistics**: Show all ping history
- 📊 Beautiful GUI windows with statistics
- 🔕 **NO console window** (completely silent)

> **Important:** Always use `pythonw` (not `python`) to hide console window!  
> **Best:** Just double-click the `.vbs` file for completely silent launch!

### 📟 Option 2: Console Mode (Classic)
Quick start with console output:
- **`setup_and_run.bat`** - Auto-installs everything and runs (Windows)
- **`run.bat`** - Quick run if already set up (Windows)
- **`run.ps1`** - PowerShell version

### Option 3: Build Portable GUI Version - CODE PROTECTED 🔒
Build a system tray version with **source code protection**:

```bash
# Windows:
.\build_gui.bat

# Or PowerShell:
.\build_gui.ps1

# Then run:
python NetworkTester_GUI.pyz
# Or without console:
pythonw NetworkTester_GUI.pyz
```

**Advantages:**
- ✅ **System tray interface** with GUI windows
- ✅ **Source code is hidden** (compiled to .pyc bytecode)
- ✅ Single file (~28 KB)
- ✅ No installation needed
- ✅ Color-coded network status icon

### Option 4: Build Console Version - CODE PROTECTED 🔒
Build a console version where **source code is compiled to bytecode**:

```bash
# Windows:
.\build_compiled.bat

# Or PowerShell:
.\build_compiled.ps1

# Then run:
python NetworkTester_Compiled.pyz
```

**Advantages:**
- ✅ **Source code is hidden** (compiled to .pyc bytecode)
- ✅ **Users cannot see your code** when opening in editor
- ✅ Single file (~13 KB)
- ✅ No installation needed
- ✅ Works on Windows, Linux, Mac
- ✅ No PyInstaller required
- ✅ Optimized and faster

### Option 5: Portable Single-File Application (Source Visible)
Build a single `.pyz` file (source code is visible if extracted):

```bash
# Windows:
.\build_portable.bat

# Or PowerShell:
.\build_portable.ps1

# Then run:
python NetworkTester.pyz
```

**Advantages:**
- ✅ Single file (NetworkTester.pyz)
- ✅ No installation needed
- ✅ Works on Windows, Linux, Mac
- ✅ No PyInstaller required
- ✅ Small file size (~39 KB)

### Option 6: Run Directly with Python
```bash
python main.py
```

### Option 7: Build as EXE (Advanced - Requires PyInstaller)
```bash
# This requires PyInstaller to be installed
.\build.ps1

# The executable will be in: dist/NetworkTester.exe
```

After building, `config.json` is already copied to the dist directory.

## Configuration Options

Edit `config.json` to customize:

```json
{
    "monitoring": {
        "target_host": "8.8.8.8",           // Host to ping
        "check_interval_seconds": 30,       // Seconds between checks
        "latency_threshold_ms": 1000,       // Alert if latency > this
        "failure_threshold": 3,             // Alert after N failures
        "log_file": "log.txt"              // Log file path
    }
}
```

## Log File Format

The `log.txt` file contains entries like:

```
[2025-10-28 14:30:00] Latency: 25.50 ms
[2025-10-28 14:30:30] Latency: 28.30 ms
[2025-10-28 14:31:00] Latency: NO RESPONSE
[2025-10-28 14:31:30] ERROR: Network issue detected - 3 consecutive failures
```

## Email Alert

When network issues are detected, an email is sent with:
- **Subject**: "Internet is down"
- **Body**: Details about the failure (timestamp, consecutive failures, latency)

## Stopping the Application

Press `Ctrl+C` to gracefully stop the monitoring.

## Troubleshooting

### Email not sending?
- Check your SMTP settings in `config.json`
- For Gmail, ensure you're using an App Password, not your regular password
- Check firewall settings allowing outbound SMTP connections

### Ping not working?
- The application requires ICMP (ping) to be allowed
- On Windows, ensure you have proper permissions
- Some networks may block ICMP packets

## License

This project is provided as-is for network monitoring purposes.
