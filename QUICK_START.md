## 🚀 QUICK START GUIDE

### **FASTEST WAY TO RUN (RECOMMENDED)**
```
1. Open File Explorer
2. Navigate to: D:\Development\NetTester
3. Double-click: NetworkTester_GUI.vbs
4. Look for WiFi icon in system tray (bottom-right)
5. Right-click for menu options
```

---

## 📋 HOW TO BUILD & RUN

### **Option 1: Quick Run (Already Built) ⭐ BEST**
The application is already compiled and ready to use!

**Windows GUI:**
- File Explorer → Double-click `NetworkTester_GUI.vbs`

**Command Line:**
```powershell
cd D:\Development\NetTester
pythonw NetworkTester_GUI.pyz
```

---

### **Option 2: Build from Source (If code changed)**
```powershell
cd D:\Development\NetTester
.venv\Scripts\activate
python build.py
pythonw NetworkTester_GUI.pyz
```

---

### **Option 3: Development Mode (For testing)**
```powershell
cd D:\Development\NetTester
.venv\Scripts\activate
.venv\Scripts\python.exe main_gui.py
```
This runs with source code (easier to debug/modify).

---

### **Option 4: First-Time Setup**
```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build application
python build.py

# Run
pythonw NetworkTester_GUI.pyz
```

---

## 🎯 WHAT HAPPENS WHEN YOU RUN

✅ Application starts silently (no console window)
✅ WiFi-style icon appears in system tray
✅ Begins monitoring network immediately
✅ Shows status via icon color

**System Tray Menu:**
- **Left Click** → Quick Stats (last 5 pings)
- **Right Click** → Full menu:
  - Quick Stats
  - Full Statistics
  - Settings (edit config.json)
  - Quit

---

## ⚙️ CONFIGURATION

Edit `config.json` to customize:
- **Target Host** (default: 8.8.8.8)
- **Check Interval** (default: 30 seconds)
- **Email Settings** (SMTP, credentials)
- **Latency Threshold** (default: 1000ms)
- **Failure Threshold** (default: 3)

**Note:** Changes in Settings window apply IMMEDIATELY - no restart needed!

---

## 🔒 PROJECT STRUCTURE

```
NetTester/
├── build.py                  # Build script
├── main_gui.py               # Entry point
├── config.json               # Configuration
├── NetworkTester_GUI.pyz     # Compiled app (45KB)
├── NetworkTester_GUI.vbs     # Silent launcher
├── services/                 # Core logic
├── src/                      # GUI components
└── .venv/                    # Python environment
```

---

## ❓ QUICK TROUBLESHOOTING

**Won't start?**
- Check Python: `python --version`
- Kill existing: `taskkill /f /im pythonw.exe`
- Check Task Manager for multiple instances

**No system tray icon?**
- Look in "Show hidden icons" area
- Restart the application
- Check if Windows system tray is enabled

**Email not working?**
- Use Gmail App Password (not regular password)
- Check SMTP settings: smtp.gmail.com:587
- Use "Test Email" button in Settings

---

## 📚 For more details, see: README.md
