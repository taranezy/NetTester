"""
Single Instance Service - Ensures only one instance runs at a time
Follows Single Responsibility Principle (SRP)
"""
import sys
import os
from pathlib import Path


class SingleInstanceService:
    """Service to ensure only one instance of the application runs."""
    
    def __init__(self, app_name: str = "NetworkTester"):
        """
        Initialize single instance checker.
        
        Args:
            app_name: Unique identifier for the application
        """
        self.app_name = app_name
        self.lock_file = None
        self._platform = sys.platform
        
        if self._platform == "win32":
            # Windows: Use mutex-style lock file in temp
            import tempfile
            self.lock_path = Path(tempfile.gettempdir()) / f"{app_name}.lock"
        else:
            # Linux/Mac: Use lock file in /tmp
            self.lock_path = Path(f"/tmp/{app_name}.lock")
    
    def is_already_running(self) -> bool:
        """
        Check if another instance is already running.
        
        Returns:
            bool: True if already running, False otherwise
        """
        try:
            if self.lock_path.exists():
                # Check if the PID in the lock file is still running
                try:
                    with open(self.lock_path, 'r') as f:
                        old_pid = int(f.read().strip())
                    
                    # Check if process is still running
                    if self._is_process_running(old_pid):
                        return True
                    else:
                        # Stale lock file, remove it
                        self.lock_path.unlink()
                except (ValueError, IOError):
                    # Invalid lock file, remove it
                    try:
                        self.lock_path.unlink()
                    except:
                        pass
            
            return False
            
        except Exception:
            # If we can't determine, assume not running
            return False
    
    def acquire_lock(self) -> bool:
        """
        Acquire the lock (mark this instance as running).
        
        Returns:
            bool: True if lock acquired, False if already locked
        """
        if self.is_already_running():
            return False
        
        try:
            # Write our PID to the lock file
            with open(self.lock_path, 'w') as f:
                f.write(str(os.getpid()))
            
            self.lock_file = self.lock_path
            return True
            
        except Exception:
            return False
    
    def release_lock(self) -> None:
        """Release the lock (allow new instances)."""
        try:
            if self.lock_file and self.lock_file.exists():
                self.lock_file.unlink()
        except Exception:
            pass
    
    def _is_process_running(self, pid: int) -> bool:
        """
        Check if a process with given PID is running.
        
        Args:
            pid: Process ID to check
            
        Returns:
            bool: True if running, False otherwise
        """
        try:
            if self._platform == "win32":
                # Windows: Use tasklist
                import subprocess
                result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                return str(pid) in result.stdout
            else:
                # Linux/Mac: Send signal 0
                os.kill(pid, 0)
                return True
        except (OSError, subprocess.TimeoutExpired):
            return False
        except Exception:
            return False
    
    def __enter__(self):
        """Context manager entry."""
        if not self.acquire_lock():
            raise RuntimeError(f"{self.app_name} is already running!")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release_lock()
