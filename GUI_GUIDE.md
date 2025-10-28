# System Tray GUI Mode - User Guide

## 🎨 What is System Tray Mode?

The Network Tester now includes a **beautiful GUI interface** that runs in your Windows system tray (the area at the bottom-right of your screen, near the clock).

## ✨ Features

### 🔔 System Tray Icon
- Always visible in your system tray
- **Color-coded** to show network status at a glance:
  - 🟢 **Green**: Network is healthy (low latency)
  - 🟡 **Yellow**: Network is slow (high latency)
  - 🔴 **Red**: Network is down (no response)
  - ⚪ **Gray**: Starting up

### 👆 Single Click - Quick Stats Popup
Click once on the tray icon to see:
- Last 5 ping measurements
- Success rate percentage
- Average latency
- Number of consecutive failures
- Auto-closes after 10 seconds

### 🖱️ Right Click Menu
- **Quick Stats (Last 5)** - Shows quick popup (default action)
- **Full Statistics** - Opens complete history window
- **Quit** - Closes the application

### 📊 Full Statistics Window
Double-click or use the menu to see:
- Complete ping history (all measurements)
- Summary statistics:
  - Total pings
  - Successful/Failed counts
  - Success rate
  - Average, Min, Max latency
  - Consecutive failures
- Scrollable table with timestamps
- Color-coded status indicators

## 🚀 How to Use

### Starting the App

**Option 1: Quick Run**
```bash
.\run_gui.bat
```

**Option 2: Silent Mode (No Console Window)**
```bash
pythonw main_gui.py
```

**Option 3: Build Portable Version**
```bash
.\build_gui.bat
# Then run:
pythonw NetworkTester_GUI.pyz
```

### Using the Interface

1. **Launch the app** - Look for the network icon in your system tray
2. **Hover over icon** - See current status in tooltip
3. **Single click** - View last 5 pings in a popup
4. **Right-click → Full Statistics** - See complete history
5. **Right-click → Quit** - Exit the application

### Tips

- The app runs **silently in the background**
- No console window clutter
- Icon color changes based on network status
- All pings are still logged to `log.txt`
- Email alerts still work as configured

## 📸 Screenshots Description

### System Tray Icon
The icon appears in your system tray with a WiFi/network signal design. Color changes based on network status.

### Quick Stats Popup
A small window (400x280 pixels) that appears near the tray icon showing:
```
🌐 Network Monitor
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Success Rate: 98.5% | Avg: 35.2 ms | Failures: 0

Last 5 Pings:
● 14:32:15 - 28.34 ms
● 14:31:45 - 32.10 ms
● 14:31:15 - 27.85 ms
● 14:30:45 - 29.50 ms
● 14:30:15 - 31.20 ms

[Close]
```

### Full Statistics Window
A larger window (700x600 pixels) centered on screen showing:
- Summary section with 8 key statistics
- Complete scrollable history table
- Timestamps, latency values, status

## 🎨 Color Coding

### In Quick Stats Popup
- 🟢 Green dot: Latency < 100ms (Excellent)
- 🔵 Blue dot: Latency 100-500ms (Good)
- 🟠 Orange dot: Latency 500-1000ms (Fair)
- 🔴 Red dot: Latency > 1000ms (Poor)
- ⚫ Gray X: No response (Failed)

### In Full Stats Window
- **Excellent**: < 100ms
- **Good**: 100-500ms
- **Fair**: 500-1000ms
- **Poor**: > 1000ms
- **Failed**: No response

## 🔧 Configuration

The GUI mode uses the same `config.json` file:

```json
{
    "monitoring": {
        "target_host": "8.8.8.8",
        "check_interval_seconds": 30,
        "latency_threshold_ms": 1000,
        "failure_threshold": 3,
        "log_file": "log.txt"
    },
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

## 🆚 GUI Mode vs Console Mode

| Feature | GUI Mode | Console Mode |
|---------|----------|--------------|
| **Interface** | System tray + Windows | Console text |
| **Visual Status** | ✅ Color-coded icon | ❌ Text only |
| **Background Running** | ✅ Silent | ❌ Console window |
| **View Stats** | ✅ Click for popup | ❌ Scroll console |
| **History Access** | ✅ Scrollable window | ❌ Check log file |
| **Visibility** | ✅ Always in tray | ⚠️ Console visible |
| **User Friendly** | ✅ Very | ⚠️ Technical |

## 💡 Pro Tips

1. **Run on Windows Startup**
   - Press `Win + R`, type `shell:startup`
   - Create shortcut to `NetworkTester_GUI.pyz`
   - Set target to: `pythonw "C:\path\to\NetworkTester_GUI.pyz"`

2. **Hide Console Window**
   - Always use `pythonw` instead of `python`
   - Example: `pythonw NetworkTester_GUI.pyz`

3. **Quick Access**
   - Pin the script to your taskbar
   - Create desktop shortcut with custom icon

4. **Monitoring Multiple Servers**
   - Run multiple instances with different config files
   - Each will have its own tray icon

## 🐛 Troubleshooting

### Icon Not Appearing
- Check if app is running in Task Manager
- Try running with `python main_gui.py` to see errors
- Ensure pystray and Pillow are installed

### Windows Don't Show on Click
- Check if running as admin (might affect GUI)
- Look for errors in console if running with `python`
- Verify tkinter is installed (comes with Python)

### App Crashes on Start
- Run with `python main_gui.py` to see error message
- Check `log.txt` for errors
- Verify all dependencies installed: `pip install -r requirements.txt`

## 📦 Dependencies

GUI mode requires these additional packages:
- `pystray` - System tray icon support
- `Pillow` - Icon image generation
- `tkinter` - GUI windows (included with Python)

Install with:
```bash
pip install -r requirements.txt
```

## 🎯 Keyboard Shortcuts

While windows are open:
- `Esc` - Close current window (not implemented yet)
- `Alt + F4` - Close window

## 📝 Logging

Even in GUI mode:
- All pings are logged to `log.txt`
- Same format as console mode
- Errors are also logged

## ✉️ Email Alerts

Email alerts work the same in GUI mode:
- Sent when latency > threshold
- Sent after N consecutive failures
- Same configuration as console mode

---

**Enjoy your beautiful network monitoring experience!** 🎉
