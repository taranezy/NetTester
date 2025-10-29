"""
Stats Tracker Service - Maintains ping statistics history
Follows Single Responsibility Principle (SRP)
"""
from datetime import datetime
from collections import deque
from typing import Optional, List, Dict
from pathlib import Path


class StatsEntry:
    """Represents a single ping measurement."""
    
    def __init__(self, timestamp: datetime, latency: Optional[float]):
        self.timestamp = timestamp
        self.latency = latency
    
    def __str__(self):
        time_str = self.timestamp.strftime("%H:%M:%S")
        if self.latency is not None:
            return f"[{time_str}] {self.latency:.2f} ms"
        else:
            return f"[{time_str}] NO RESPONSE"
    
    def to_dict(self):
        """Convert to dictionary for easy access."""
        return {
            'timestamp': self.timestamp,
            'latency': self.latency,
            'formatted': str(self)
        }


class StatsTrackerService:
    """Service to track and manage ping statistics."""
    
    def __init__(self, max_history: int = 1000, log_file: Optional[str] = None):
        """
        Initialize stats tracker.
        
        Args:
            max_history: Maximum number of entries to keep in history
            log_file: Optional path to log file to restore ping count from
        """
        self.max_history = max_history
        self._history = deque(maxlen=max_history)
        self._consecutive_failures = 0
        self._total_pings = 0
        self._failed_pings = 0
        self._total_latency = 0.0
        
        # Restore ping count from existing log file if provided
        if log_file:
            self._restore_from_log(log_file)
    
    def _restore_from_log(self, log_file: str) -> None:
        """
        Restore ping count and historical entries from existing log file.
        
        Args:
            log_file: Path to the log file to restore from
        """
        try:
            log_path = Path(log_file)
            if not log_path.exists():
                return
            
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse lines that contain latency measurements (not errors)
                    if "Latency:" in line and "ERROR:" not in line:
                        try:
                            # Parse: [YYYY-MM-DD HH:MM:SS] Latency: X.XX ms
                            parts = line.split("] ")
                            if len(parts) < 2:
                                continue
                            
                            timestamp_str = parts[0].lstrip("[")
                            rest = parts[1]
                            
                            # Parse timestamp
                            try:
                                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                continue
                            
                            # Parse latency
                            if "NO RESPONSE" in rest:
                                latency = None
                                entry = StatsEntry(timestamp, latency)
                                self._history.append(entry)
                                self._total_pings += 1
                                self._failed_pings += 1
                                self._consecutive_failures += 1
                            else:
                                # Extract latency value: "Latency: X.XX ms"
                                latency_str = rest.split("Latency: ")[1].split(" ms")[0]
                                latency = float(latency_str)
                                entry = StatsEntry(timestamp, latency)
                                self._history.append(entry)
                                self._total_pings += 1
                                self._total_latency += latency
                                self._consecutive_failures = 0
                        except (IndexError, ValueError) as e:
                            # Skip lines that don't parse correctly
                            continue
            
            print(f"📊 Restored stats: {self._total_pings} total pings, {len(self._history)} entries loaded from log file")
        except Exception as e:
            print(f"⚠️ Could not restore stats from log: {e}")
    
    def add_measurement(self, latency: Optional[float]) -> None:
        """
        Add a new measurement to the history.
        
        Args:
            latency: Latency in milliseconds, or None if ping failed
        """
        entry = StatsEntry(datetime.now(), latency)
        self._history.append(entry)
        
        self._total_pings += 1
        
        if latency is None:
            self._failed_pings += 1
            self._consecutive_failures += 1
        else:
            self._consecutive_failures = 0
            self._total_latency += latency
    
    def get_last_n(self, n: int = 5) -> List[StatsEntry]:
        """
        Get the last N measurements.
        
        Args:
            n: Number of measurements to retrieve
            
        Returns:
            List of StatsEntry objects
        """
        return list(self._history)[-n:] if len(self._history) >= n else list(self._history)
    
    def get_all(self) -> List[StatsEntry]:
        """Get all measurements in history."""
        return list(self._history)
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with summary stats
        """
        success_count = self._total_pings - self._failed_pings
        avg_latency = self._total_latency / success_count if success_count > 0 else 0
        success_rate = (success_count / self._total_pings * 100) if self._total_pings > 0 else 0
        
        # Get min/max from successful pings
        successful_latencies = [e.latency for e in self._history if e.latency is not None]
        min_latency = min(successful_latencies) if successful_latencies else 0
        max_latency = max(successful_latencies) if successful_latencies else 0
        
        return {
            'total_pings': self._total_pings,
            'successful': success_count,
            'failed': self._failed_pings,
            'success_rate': success_rate,
            'avg_latency': avg_latency,
            'min_latency': min_latency,
            'max_latency': max_latency,
            'consecutive_failures': self._consecutive_failures
        }
    
    def get_consecutive_failures(self) -> int:
        """Get number of consecutive failures."""
        return self._consecutive_failures
    
    def clear(self) -> None:
        """Clear all statistics."""
        self._history.clear()
        self._consecutive_failures = 0
        self._total_pings = 0
        self._failed_pings = 0
        self._total_latency = 0.0
    
    def add_measurement(self, latency: Optional[float]) -> None:
        """
        Add a new measurement to the history.
        
        Args:
            latency: Latency in milliseconds, or None if ping failed
        """
        entry = StatsEntry(datetime.now(), latency)
        self._history.append(entry)
        
        self._total_pings += 1
        
        if latency is None:
            self._failed_pings += 1
            self._consecutive_failures += 1
        else:
            self._consecutive_failures = 0
            self._total_latency += latency
    
    def get_last_n(self, n: int = 5) -> List[StatsEntry]:
        """
        Get the last N measurements.
        
        Args:
            n: Number of measurements to retrieve
            
        Returns:
            List of StatsEntry objects
        """
        return list(self._history)[-n:] if len(self._history) >= n else list(self._history)
    
    def get_all(self) -> List[StatsEntry]:
        """Get all measurements in history."""
        return list(self._history)
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with summary stats
        """
        success_count = self._total_pings - self._failed_pings
        avg_latency = self._total_latency / success_count if success_count > 0 else 0
        success_rate = (success_count / self._total_pings * 100) if self._total_pings > 0 else 0
        
        # Get min/max from successful pings
        successful_latencies = [e.latency for e in self._history if e.latency is not None]
        min_latency = min(successful_latencies) if successful_latencies else 0
        max_latency = max(successful_latencies) if successful_latencies else 0
        
        return {
            'total_pings': self._total_pings,
            'successful': success_count,
            'failed': self._failed_pings,
            'success_rate': success_rate,
            'avg_latency': avg_latency,
            'min_latency': min_latency,
            'max_latency': max_latency,
            'consecutive_failures': self._consecutive_failures
        }
    
    def get_consecutive_failures(self) -> int:
        """Get number of consecutive failures."""
        return self._consecutive_failures
    
    def clear(self) -> None:
        """Clear all statistics."""
        self._history.clear()
        self._consecutive_failures = 0
        self._total_pings = 0
        self._failed_pings = 0
        self._total_latency = 0.0
