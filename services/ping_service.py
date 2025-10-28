"""
Ping Service - Responsible for measuring network latency
Follows Single Responsibility Principle (SRP)
"""
import subprocess
import platform
import re
import sys
from typing import Optional


class PingService:
    """Service to perform ping operations and measure latency."""
    
    def __init__(self, host: str = "8.8.8.8"):
        """
        Initialize the ping service.
        
        Args:
            host: The host to ping (default: Google DNS 8.8.8.8)
        """
        self.host = host
        self._is_windows = platform.system().lower() == "windows"
        
        # Windows-specific: Create startup info to hide console window
        if self._is_windows:
            self._startupinfo = subprocess.STARTUPINFO()
            self._startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._startupinfo.wShowWindow = subprocess.SW_HIDE
            # Also set creation flags to prevent console window
            # CREATE_NO_WINDOW is available in Python 3.7+
            if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                self._creationflags = subprocess.CREATE_NO_WINDOW
            else:
                self._creationflags = 0x08000000  # CREATE_NO_WINDOW value
        else:
            self._startupinfo = None
            self._creationflags = 0
    
    def ping(self) -> Optional[float]:
        """
        Perform a ping operation and return latency in milliseconds.
        
        Returns:
            float: Latency in milliseconds, or None if ping failed
        """
        try:
            # Prepare ping command based on OS
            param = "-n" if self._is_windows else "-c"
            timeout_param = "-w" if self._is_windows else "-W"
            
            # Execute ping command with 1 packet and 5 second timeout
            command = ["ping", param, "1", timeout_param, "5000" if self._is_windows else "5", self.host]
            
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
                startupinfo=self._startupinfo if self._is_windows else None,
                creationflags=self._creationflags if self._is_windows else 0
            )
            
            if result.returncode != 0:
                return None
            
            # Parse latency from output
            return self._parse_latency(result.stdout)
            
        except (subprocess.TimeoutExpired, Exception):
            return None
    
    def _parse_latency(self, output: str) -> Optional[float]:
        """
        Parse latency from ping command output.
        
        Args:
            output: Raw output from ping command
            
        Returns:
            float: Latency in milliseconds, or None if parsing failed
        """
        try:
            if self._is_windows:
                # Windows format: "time=XXms" or "time<1ms"
                match = re.search(r"time[=<](\d+)ms", output.lower())
                if match:
                    return float(match.group(1))
            else:
                # Linux/Mac format: "time=XX.X ms"
                match = re.search(r"time=(\d+\.?\d*)\s*ms", output.lower())
                if match:
                    return float(match.group(1))
            
            return None
            
        except (ValueError, AttributeError):
            return None
