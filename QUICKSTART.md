# 🚀 QUICK START GUIDE

## I just want to run it NOW!

### For GUI Mode (Recommended) 🎨

**Double-click this file:**
```
NetworkTester_GUI.vbs
```

That's it! Look for the network icon in your system tray (bottom-right, near the clock).

**NO console window will appear!** ✨

**Click the icon** to see your network stats!

---

### For Console Mode 📟

**Double-click this file:**
```
setup_and_run.bat
```

That's it! You'll see ping results in a console window.

---

## What You'll See

### GUI Mode
- A network icon appears in your system tray
- Icon color shows status:
  - 🟢 Green = Good connection
  - 🟡 Yellow = Slow connection  
  - 🔴 Red = Connection down
- **Click once**: See last 5 pings
- **Right-click → Full Statistics**: See all history

### Console Mode
- A black console window showing:
```
[14:32:15] Latency: 28.34 ms ✓
[14:32:45] Latency: 32.10 ms ✓
[14:33:15] Latency: NO RESPONSE ✗
```

---

## Configure Email Alerts (Optional)

1. Open `config.json` in Notepad
2. Change these lines:
   ```json
   "sender_email": "your-gmail@gmail.com",
   "sender_password": "your-app-password"
   ```
3. For Gmail, create an App Password here:
   https://myaccount.google.com/apppasswords

**That's all you need to know!**

For more details, see `README.md` or `GUI_GUIDE.md`
