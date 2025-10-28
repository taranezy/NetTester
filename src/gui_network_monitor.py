"""
GUI Network Monitor - System tray version with GUI
Extends NetworkMonitor for GUI mode
"""
import time
import threading
from datetime import datetime
from typing import Optional

from services.ping_service import PingService
from services.logger_service import LoggerService
from services.email_service import EmailService
from services.stats_tracker_service import StatsTrackerService
from services.icon_service import IconService


class GUINetworkMonitor:
    """
    Network monitor for GUI/System Tray mode.
    Runs in background thread and updates GUI components.
    """
    
    def __init__(self, ping_service: PingService, logger_service: LoggerService, 
                 stats_tracker: StatsTrackerService,
                 email_service: Optional[EmailService] = None, 
                 recipient_email: Optional[str] = None,
                 check_interval: int = 30,
                 latency_threshold: float = 1000.0,
                 failure_threshold: int = 3,
                 status_callback=None):
        """
        Initialize the GUI network monitor.
        
        Args:
            ping_service: Service to perform ping operations
            logger_service: Service to log measurements
            stats_tracker: Service to track statistics
            email_service: Service to send email notifications (optional)
            recipient_email: Email address to send notifications to
            check_interval: Seconds between ping checks (default: 30)
            latency_threshold: Latency threshold in ms to consider as issue (default: 1000)
            failure_threshold: Number of consecutive failures before alerting (default: 3)
            status_callback: Callback function to update status (e.g., tray icon)
        """
        self.ping_service = ping_service
        self.logger_service = logger_service
        self.stats_tracker = stats_tracker
        self.email_service = email_service
        self.recipient_email = recipient_email
        self.check_interval = check_interval
        self.latency_threshold = latency_threshold
        self.failure_threshold = failure_threshold
        self.status_callback = status_callback
        
        self._alert_sent = False
        self._running = False
        self._thread = None
        
        # Current status
        self.current_latency = None
        self.current_status = "Starting..."
    
    def start(self) -> None:
        """Start the network monitoring in a background thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop the network monitoring loop."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop (runs in background thread)."""
        try:
            while self._running:
                self._check_network()
                time.sleep(self.check_interval)
        except Exception as e:
            self.logger_service.log_error(f"Monitor loop error: {e}")
    
    def _check_network(self) -> None:
        """Perform a single network check."""
        latency = self.ping_service.ping()
        
        # Store in stats tracker
        self.stats_tracker.add_measurement(latency)
        
        # Log to file
        self.logger_service.log_latency(latency)
        
        # Update current status
        self.current_latency = latency
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if latency is not None:
            self.current_status = f"[{timestamp}] {latency:.2f} ms"
            if latency > self.latency_threshold:
                self._handle_network_issue(latency)
            else:
                self._reset_failure_count()
        else:
            self.current_status = f"[{timestamp}] NO RESPONSE"
            self._handle_network_issue(None)
        
        # Update GUI (icon, tooltip, etc.)
        if self.status_callback:
            self.status_callback(latency)
    
    def _handle_network_issue(self, latency: Optional[float]) -> None:
        """Handle network issue (high latency or no response)."""
        consecutive_failures = self.stats_tracker.get_consecutive_failures()
        
        if consecutive_failures >= self.failure_threshold and not self._alert_sent:
            self._send_alert(latency)
            self._alert_sent = True
    
    def _reset_failure_count(self) -> None:
        """Reset alert flag when network is healthy."""
        if self._alert_sent:
            self._alert_sent = False
            self.logger_service.log_error("Network recovered")
    
    def _send_alert(self, latency: Optional[float]) -> None:
        """Send email alert about network issue."""
        consecutive_failures = self.stats_tracker.get_consecutive_failures()
        
        subject = "Internet is down"
        
        if latency is None:
            message = (
                f"Network alert: No response from {self.ping_service.host}\n"
                f"Consecutive failures: {consecutive_failures}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            message = (
                f"Network alert: High latency to {self.ping_service.host}\n"
                f"Current latency: {latency:.2f} ms\n"
                f"Threshold: {self.latency_threshold} ms\n"
                f"Consecutive failures: {consecutive_failures}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        
        self.logger_service.log_error(f"Network issue detected - {consecutive_failures} consecutive failures")
        
        if self.email_service and self.recipient_email:
            success = self.email_service.send_notification(
                self.recipient_email,
                subject,
                message
            )
            if success:
                self.logger_service.log_error("Alert email sent successfully")
            else:
                self.logger_service.log_error("Failed to send alert email")
        else:
            self.logger_service.log_error("Email service not configured")
    
    def get_status_summary(self) -> str:
        """Get current status as a string for tooltip."""
        summary = self.stats_tracker.get_summary()
        return (
            f"Network Monitor\n"
            f"{self.current_status}\n"
            f"Success Rate: {summary['success_rate']:.1f}%\n"
            f"Avg: {summary['avg_latency']:.1f} ms"
        )
