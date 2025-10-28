"""
Main entry point for Network Tester application
"""
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services.ping_service import PingService
from services.logger_service import LoggerService
from services.email_service import EmailService
from services.single_instance_service import SingleInstanceService
from src.network_monitor import NetworkMonitor


def load_config(config_path: str = "config.json") -> dict:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Warning: Config file '{config_path}' not found. Using defaults.")
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}


def main():
    """Main application entry point."""
    print("=" * 60)
    print("Network Tester - Latency Monitoring Application")
    print("=" * 60)
    print()
    
    # Check for single instance
    single_instance = SingleInstanceService("NetworkTester_Console")
    
    if not single_instance.acquire_lock():
        print("=" * 60)
        print("ERROR: Network Tester is already running!")
        print("=" * 60)
        print()
        print("Another instance of Network Tester is already active.")
        print("Please close the existing instance before starting a new one.")
        print()
        print("TIP: Check your system tray for the network icon,")
        print("     or look in Task Manager for python.exe processes.")
        print()
        input("Press Enter to exit...")
        sys.exit(1)
    
    try:
        # Load configuration
        config = load_config()
        
        # Get monitoring settings
        monitoring_config = config.get('monitoring', {})
        target_host = monitoring_config.get('target_host', '8.8.8.8')
        check_interval = monitoring_config.get('check_interval_seconds', 30)
        latency_threshold = monitoring_config.get('latency_threshold_ms', 1000)
        failure_threshold = monitoring_config.get('failure_threshold', 3)
        log_file = monitoring_config.get('log_file', 'log.txt')
        
        # Initialize services
        ping_service = PingService(host=target_host)
        logger_service = LoggerService(log_file=log_file)
        
        # Initialize email service if configured
        email_service = None
        recipient_email = None
        email_config = config.get('email', {})
        
        if email_config:
            smtp_server = email_config.get('smtp_server')
            smtp_port = email_config.get('smtp_port')
            sender_email = email_config.get('sender_email')
            sender_password = email_config.get('sender_password')
            use_tls = email_config.get('use_tls', True)
            recipient_email = email_config.get('recipient_email')
            
            # Check if all required email settings are provided
            if all([smtp_server, smtp_port, sender_email, sender_password, recipient_email]):
                # Check if using default placeholder values
                if sender_email != "your-email@gmail.com" and sender_password != "your-app-password":
                    email_service = EmailService(
                        smtp_server=smtp_server,
                        smtp_port=smtp_port,
                        sender_email=sender_email,
                        sender_password=sender_password,
                        use_tls=use_tls
                    )
                    print(f"✓ Email notifications enabled (recipient: {recipient_email})")
                else:
                    print("⚠ Email settings not configured in config.json")
                    print("  Please update sender_email and sender_password to enable alerts")
            else:
                print("⚠ Email settings incomplete in config.json")
        else:
            print("⚠ Email notifications disabled (no email config found)")
        
        print()
        
        # Create and start monitor
        monitor = NetworkMonitor(
            ping_service=ping_service,
            logger_service=logger_service,
            email_service=email_service,
            recipient_email=recipient_email,
            check_interval=check_interval,
            latency_threshold=latency_threshold,
            failure_threshold=failure_threshold
        )
        
        monitor.start()
        
    finally:
        # Always release lock when exiting
        single_instance.release_lock()


if __name__ == "__main__":
    main()
