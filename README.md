# 🌐 Network Tester

A portable Windows system tray application for continuous network monitoring with email alerts and real-time statistics.

## ✨ Features

### 🔍 **Network Monitoring**
- **Continuous ping monitoring** of any target (IP address or domain)
- **Configurable intervals** (default: 30 seconds)
- **Latency threshold alerts** (default: >1000ms)
- **Failure detection** with consecutive failure counting
- **Automatic logging** to log.txt with timestamps

### 📧 **Email Alerts**
- **SMTP email notifications** for network issues
- **Gmail integration** with App Password support
- **Customizable thresholds** for when to send alerts
- **Test email functionality** to verify settings

### 🖥️ **System Tray Integration**
- **Silent background operation** - no console windows
- **WiFi-style status icons** with color-coded network status
- **Right-click context menu** with quick access to all features
- **Single instance protection** - prevents multiple copies running

### ⚡ **Real-Time Features**
- **Instant settings reload** - no restart required when changing configuration
- **Live statistics windows** with auto-refreshing data
- **Real-time icon updates** based on current network status
- **Dynamic configuration** - change ping targets instantly

### 🔒 **Security & Portability**
- **Bytecode compilation** - source code protection
- **Single file deployment** - just copy and run
- **No installation required** - fully portable
- **Protected configuration** - settings stored in JSON

## 🚀 Quick Start

### 1. **Download & Run**
```
1. Download the release files
2. Double-click: NetworkTester_GUI.vbs
3. Look for WiFi icon in system tray
4. Right-click → Settings to configure
```

### 2. **Configure Email (Optional)**
```
Right-click tray icon → Settings → Email Settings:
- SMTP Server: smtp.gmail.com
- Port: 587
- Email: your-email@gmail.com
- Password: your-app-password (not regular password!)
- Recipient: where-to-send-alerts@gmail.com
```

### 3. **Configure Monitoring**
```
Right-click tray icon → Settings → Monitoring:
- Target Host: 8.8.8.8 (or any IP/domain)
- Check Interval: 30 seconds
- Latency Threshold: 1000ms
- Failure Threshold: 3 consecutive failures
```

## 📁 Project Structure

```
NetTester/
├── 📁 services/               # Core monitoring services
│   ├── ping_service.py        # Network ping functionality
│   ├── email_service.py       # SMTP email notifications
│   ├── logger_service.py      # File logging system
│   ├── stats_tracker_service.py # Statistics collection
│   ├── icon_service.py        # System tray icons
│   └── single_instance_service.py # Prevent multiple instances
├── 📁 src/                    # GUI components
│   ├── gui_network_monitor.py # Main monitoring logic
│   ├── gui_windows.py         # Statistics display windows
│   └── settings_window.py     # Configuration GUI
├── 📁 .venv/                  # Python virtual environment
├── main_gui.py                # Application entry point
├── config.json                # Configuration file
├── build.py                   # Build script
├── NetworkTester_GUI.pyz      # Compiled application
├── NetworkTester_GUI.vbs      # Silent launcher
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Building from Source

### **Prerequisites**
- Python 3.11+ 
- Windows OS

### **Setup & Build**
```powershell
# 1. Clone repository
git clone <repository-url>
cd NetTester

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Build application
python build.py
```

### **Development Mode**
```powershell
# Run directly from source
.venv\Scripts\python.exe main_gui.py
```

## ⚙️ Configuration

### **config.json Structure**
```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your-email@gmail.com",
        "sender_password": "your-app-password",
        "use_tls": true,
        "recipient_email": "recipient@gmail.com"
    },
    "monitoring": {
        "target_host": "8.8.8.8",
        "check_interval_seconds": 30,
        "latency_threshold_ms": 1000.0,
        "failure_threshold": 3,
        "log_file": "log.txt"
    }
}
```

### **Gmail App Password Setup**
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account → Security → App passwords
3. Generate an app password for "Network Tester"
4. Use this 16-character password (not your regular Gmail password)

## 📊 System Tray Actions

### **Left Click**
- Shows **Quick Stats** window (last 5 pings)
- Auto-refreshes every 2 seconds
- Auto-closes after 30 seconds

### **Right Click Menu**
- **Quick Stats** - Last 5 ping results with live updates
- **Full Statistics** - Complete history with real-time data
- **Settings** - Configuration window with instant apply
- **Quit** - Stop monitoring and exit application

## 🎨 Status Icon Colors

| Color | Status | Description |
|-------|--------|-------------|
| 🟢 **Green** | Excellent | Latency < 100ms |
| 🔵 **Blue** | Good | Latency 100-500ms |
| 🟠 **Orange** | Fair | Latency 500-1000ms |
| 🔴 **Red** | Poor | Latency > 1000ms |
| ⚫ **Gray** | Failed | No response from target |

## 🔧 Technical Details

### **Architecture**
- **Service-oriented design** following SOLID principles
- **Single Responsibility Principle** - each service has one job
- **Event-driven monitoring** with callback system
- **Thread-safe statistics** collection and display

### **Dependencies**
- `pystray` - System tray functionality
- `Pillow` - Icon generation and image processing
- `tkinter` - GUI windows (built into Python)

### **Performance**
- **Low memory footprint** (~10-15MB RAM)
- **Minimal CPU usage** when idle
- **Efficient ping implementation** using subprocess
- **Background threading** for non-blocking operations

## 🐛 Troubleshooting

### **Application Won't Start**
```
- Check if Python 3.11+ is installed
- Ensure no other instance is running (check Task Manager)
- Try running: pythonw NetworkTester_GUI.pyz
```

### **Email Not Working**
```
- Verify Gmail App Password (not regular password)
- Check SMTP settings (smtp.gmail.com:587)
- Use "Test Email" button in Settings
- Ensure 2FA is enabled on Gmail account
```

### **No System Tray Icon**
```
- Check system tray area (might be hidden)
- Look in "Show hidden icons" section
- Try restarting the application
- Ensure Windows system tray is enabled
```

### **Settings Not Saving**
```
- Check config.json file permissions
- Ensure application has write access to directory
- Verify JSON syntax in config file
- Try running as administrator if needed
```

## 📝 Version History

### **v2.0.0** - Current
- ⚡ Real-time settings reload (no restart required)
- 📊 Live statistics windows with auto-refresh
- 🎨 Improved settings GUI with better layout
- 🔒 Enhanced bytecode protection
- 🧹 Simplified project structure
- 📚 Comprehensive documentation

### **v1.0.0** - Initial Release
- 🌐 Basic network monitoring
- 📧 Email alert system
- 🖥️ System tray integration
- 🔒 Source code protection
- 📱 Single instance protection

## 📄 License

This project is released under the MIT License. See the source code for full license details.

## 🤝 Support

For issues, questions, or feature requests, please check the troubleshooting section above or contact the developer.

---
**Network Tester** - Reliable network monitoring made simple! 🌐✨
