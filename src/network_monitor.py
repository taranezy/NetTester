"""
Network Monitor - Orchestrates ping monitoring and notifications
Follows Open/Closed Principle and Dependency Inversion Principle
"""
import time
from datetime import datetime
from typing import Optional

from services.ping_service import PingService
from services.logger_service import LoggerService
from services.email_service import EmailService


class NetworkMonitor:
    """
    Main orchestrator for network monitoring.
    Depends on abstractions (service classes) rather than concrete implementations.
    """
    
    def __init__(self, ping_service: PingService, logger_service: LoggerService, 
                 email_service: Optional[EmailService] = None, 
                 recipient_email: Optional[str] = None,
                 check_interval: int = 30,
                 latency_threshold: float = 1000.0,
                 failure_threshold: int = 3):
        """
        Initialize the network monitor.
        
        Args:
            ping_service: Service to perform ping operations
            logger_service: Service to log measurements
            email_service: Service to send email notifications (optional)
            recipient_email: Email address to send notifications to
            check_interval: Seconds between ping checks (default: 30)
            latency_threshold: Latency threshold in ms to consider as issue (default: 1000)
            failure_threshold: Number of consecutive failures before alerting (default: 3)
        """
        self.ping_service = ping_service
        self.logger_service = logger_service
        self.email_service = email_service
        self.recipient_email = recipient_email
        self.check_interval = check_interval
        self.latency_threshold = latency_threshold
        self.failure_threshold = failure_threshold
        
        self._consecutive_failures = 0
        self._alert_sent = False
        self._running = False
    
    def start(self) -> None:
        """Start the network monitoring loop."""
        self._running = True
        print("Network Monitor started...")
        print(f"Monitoring {self.ping_service.host} every {self.check_interval} seconds")
        print(f"Alert threshold: {self.latency_threshold} ms or {self.failure_threshold} consecutive failures")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self._running:
                self._check_network()
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\nNetwork Monitor stopped by user")
            self.logger_service.log_error("Monitor stopped by user")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            self.logger_service.log_error(f"Unexpected error: {e}")
        finally:
            self._running = False
    
    def stop(self) -> None:
        """Stop the network monitoring loop."""
        self._running = False
    
    def _check_network(self) -> None:
        """Perform a single network check."""
        latency = self.ping_service.ping()
        self.logger_service.log_latency(latency)
        
        # Display result to console
        timestamp = datetime.now().strftime("%H:%M:%S")
        if latency is not None:
            print(f"[{timestamp}] Latency: {latency:.2f} ms", end="")
            if latency > self.latency_threshold:
                print(" ⚠ HIGH LATENCY")
                self._handle_network_issue(latency)
            else:
                print(" ✓")
                self._reset_failure_count()
        else:
            print(f"[{timestamp}] Latency: NO RESPONSE ✗")
            self._handle_network_issue(None)
    
    def _handle_network_issue(self, latency: Optional[float]) -> None:
        """
        Handle network issue (high latency or no response).
        
        Args:
            latency: Current latency in ms, or None if no response
        """
        self._consecutive_failures += 1
        
        if self._consecutive_failures >= self.failure_threshold and not self._alert_sent:
            self._send_alert(latency)
            self._alert_sent = True
    
    def _reset_failure_count(self) -> None:
        """Reset failure counter when network is healthy."""
        if self._consecutive_failures > 0 or self._alert_sent:
            self._consecutive_failures = 0
            self._alert_sent = False
            print("  Network recovered ✓")
            self.logger_service.log_error("Network recovered")
    
    def _send_alert(self, latency: Optional[float]) -> None:
        """
        Send email alert about network issue.
        
        Args:
            latency: Current latency in ms, or None if no response
        """
        subject = "Internet is down"
        
        if latency is None:
            message = (
                f"Network alert: No response from {self.ping_service.host}\n"
                f"Consecutive failures: {self._consecutive_failures}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            message = (
                f"Network alert: High latency to {self.ping_service.host}\n"
                f"Current latency: {latency:.2f} ms\n"
                f"Threshold: {self.latency_threshold} ms\n"
                f"Consecutive failures: {self._consecutive_failures}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        
        print(f"\n🚨 ALERT: Sending notification email...")
        self.logger_service.log_error(f"Network issue detected - {self._consecutive_failures} consecutive failures")
        
        if self.email_service and self.recipient_email:
            success = self.email_service.send_notification(
                self.recipient_email,
                subject,
                message
            )
            if success:
                print("✓ Alert email sent successfully")
                self.logger_service.log_error("Alert email sent successfully")
            else:
                print("✗ Failed to send alert email")
                self.logger_service.log_error("Failed to send alert email")
        else:
            print("⚠ Email service not configured - alert not sent")
            self.logger_service.log_error("Email service not configured")
