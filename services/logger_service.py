"""
Logger Service - Responsible for logging latency measurements
Follows Single Responsibility Principle (SRP)
"""
from datetime import datetime
from pathlib import Path
from typing import Optional


class LoggerService:
    """Service to log network latency measurements to file."""
    
    def __init__(self, log_file: str = "log.txt"):
        """
        Initialize the logger service.
        
        Args:
            log_file: Path to the log file
        """
        self.log_file = Path(log_file)
        self._ensure_log_file_exists()
    
    def _ensure_log_file_exists(self) -> None:
        """Create log file if it doesn't exist."""
        if not self.log_file.exists():
            self.log_file.touch()
    
    def log_latency(self, latency: Optional[float]) -> None:
        """
        Log a latency measurement to the log file.
        
        Args:
            latency: Latency in milliseconds, or None if ping failed
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if latency is not None:
            message = f"[{timestamp}] Latency: {latency:.2f} ms\n"
        else:
            message = f"[{timestamp}] Latency: NO RESPONSE\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def log_error(self, error_message: str) -> None:
        """
        Log an error message to the log file.
        
        Args:
            error_message: The error message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] ERROR: {error_message}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception as e:
            print(f"Error writing to log file: {e}")
