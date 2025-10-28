# ✅ Single Instance Protection Added!

## What Changed

The app now prevents multiple instances from running simultaneously.

## How It Works

### Lock File System
- When app starts, it creates a lock file in the temp directory
- Lock file contains the Process ID (PID) of the running instance
- Before starting, checks if lock file exists and if that process is still running
- If already running, shows an error and exits

### Lock File Locations
- **Windows**: `%TEMP%\NetworkTester_GUI.lock` or `NetworkTester_Console.lock`
- **Linux/Mac**: `/tmp/NetworkTester_GUI.lock` or `/tmp/NetworkTester_Console.lock`

### Separate Locks
- **GUI version** uses: `NetworkTester_GUI.lock`
- **Console version** uses: `NetworkTester_Console.lock`
- You can run GUI and Console versions simultaneously (different locks)
- But you cannot run two GUI instances or two Console instances

## What Happens

### GUI Version
When you try to start a second instance:
1. A popup window appears:
   ```
   ⚠ Network Tester Already Running
   
   Network Tester is already running!
   
   Look for the network icon in your system tray.
   
   If you can't find it, check Task Manager and close any
   running pythonw.exe processes, then try again.
   ```
2. Second instance exits immediately

### Console Version
When you try to start a second instance:
1. Console shows:
   ```
   ============================================================
   ERROR: Network Tester is already running!
   ============================================================
   
   Another instance of Network Tester is already active.
   Please close the existing instance before starting a new one.
   
   TIP: Check your system tray for the network icon,
        or look in Task Manager for python.exe processes.
   
   Press Enter to exit...
   ```
2. Second instance exits after you press Enter

## Features

### Intelligent Lock Detection
- ✅ Detects if lock file is from a crashed process (stale lock)
- ✅ Removes stale locks automatically
- ✅ Checks if process is actually still running (not just file existence)
- ✅ Works on Windows, Linux, and Mac

### Automatic Cleanup
- ✅ Lock is released when app exits normally
- ✅ Lock is released when app is interrupted (Ctrl+C)
- ✅ Lock is released when user quits from tray menu
- ✅ Uses try-finally to ensure cleanup

### Cross-Platform
- ✅ Windows: Uses `tasklist` to check running processes
- ✅ Linux/Mac: Uses `os.kill(pid, 0)` signal to check processes
- ✅ Falls back gracefully if checking fails

## Files Modified

| File | Change |
|------|--------|
| `services/single_instance_service.py` | **NEW** - Single instance logic |
| `main_gui.py` | Added instance check with GUI popup |
| `main.py` | Added instance check with console message |
| `NetworkTester_GUI.pyz` | Rebuilt (32.71 KB, was 29.58 KB) |

## Testing

### Test 1: Start GUI Twice
1. Double-click `NetworkTester_GUI.vbs`
2. Icon appears in system tray ✓
3. Double-click `NetworkTester_GUI.vbs` again
4. **Popup appears**: "Network Tester Already Running" ✓
5. Second instance exits ✓

### Test 2: Start Console Twice
1. Run `python main.py`
2. Console starts monitoring ✓
3. Open new terminal, run `python main.py` again
4. **Error message appears** ✓
5. Second instance exits ✓

### Test 3: Crash Recovery
1. Start app
2. Kill process forcefully (Task Manager)
3. Start app again
4. **Works fine** - detects stale lock and removes it ✓

### Test 4: Normal Exit
1. Start app
2. Exit normally (Quit from menu or Ctrl+C)
3. Start app again
4. **Works fine** - lock was properly released ✓

## Benefits

✅ **Prevents conflicts** - No duplicate monitoring  
✅ **Prevents resource waste** - No multiple instances pinging  
✅ **Prevents duplicate alerts** - Only one email sender  
✅ **User-friendly** - Clear error messages  
✅ **Automatic cleanup** - Handles crashes gracefully  
✅ **Cross-platform** - Works everywhere  

## Edge Cases Handled

| Scenario | Behavior |
|----------|----------|
| App crashes | Stale lock detected and removed on next start |
| User kills process | Stale lock detected and removed on next start |
| Multiple quick starts | Second instance waits briefly, shows error |
| Lock file deleted manually | New lock created normally |
| No write permissions | Falls back gracefully, allows start |
| GUI + Console both run | ✓ Allowed (different lock files) |

## Known Limitations

- Lock files in temp directory may be cleaned by system
- If temp directory is not accessible, single instance check is skipped
- On some systems, checking if PID is running may fail (allows duplicate)

## Manual Override

If you need to force start a second instance (not recommended):

1. **Delete the lock file:**
   - Windows: `del %TEMP%\NetworkTester_GUI.lock`
   - Linux: `rm /tmp/NetworkTester_GUI.lock`

2. **Or kill the running process:**
   - Task Manager → End `pythonw.exe`
   - Or: `taskkill /F /IM pythonw.exe`

---

**The app now safely prevents multiple instances!** 🎉
