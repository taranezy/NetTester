"""
Main entry point for Network Tester GUI (System Tray) application
"""
import sys
import json
from pathlib import Path
import pystray
from PIL import Image
import threading
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services.ping_service import PingService
from services.logger_service import LoggerService
from services.email_service import EmailService
from services.stats_tracker_service import StatsTrackerService
from services.icon_service import IconService
from services.single_instance_service import SingleInstanceService
from src.gui_network_monitor import GUINetworkMonitor
from src.gui_windows import QuickStatsWindow, FullStatsWindow
from src.settings_window import SettingsWindow


class NetworkTesterTrayApp:
    """System tray application for network monitoring."""
    
    def __init__(self):
        self.config = self.load_config()
        self.icon = None
        self.monitor = None
        self.stats_tracker = None
        self.icon_service = IconService()
        self.single_instance = SingleInstanceService("NetworkTester_GUI")
        
        # Initialize services
        self._init_services()
    
    def load_config(self, config_path: str = "config.json") -> dict:
        """Load configuration from JSON file."""
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
    
    def _init_services(self):
        """Initialize all services."""
        # Get monitoring settings
        monitoring_config = self.config.get('monitoring', {})
        target_host = monitoring_config.get('target_host', '8.8.8.8')
        check_interval = monitoring_config.get('check_interval_seconds', 30)
        latency_threshold = monitoring_config.get('latency_threshold_ms', 1000)
        failure_threshold = monitoring_config.get('failure_threshold', 3)
        log_file = monitoring_config.get('log_file', 'log.txt')
        
        # Initialize services
        ping_service = PingService(host=target_host)
        logger_service = LoggerService(log_file=log_file)
        self.stats_tracker = StatsTrackerService(max_history=1000)
        
        # Initialize email service if configured
        email_service = None
        recipient_email = None
        email_config = self.config.get('email', {})
        
        if email_config:
            smtp_server = email_config.get('smtp_server')
            smtp_port = email_config.get('smtp_port')
            sender_email = email_config.get('sender_email')
            sender_password = email_config.get('sender_password')
            use_tls = email_config.get('use_tls', True)
            recipient_email = email_config.get('recipient_email')
            
            if all([smtp_server, smtp_port, sender_email, sender_password, recipient_email]):
                if sender_email != "your-email@gmail.com" and sender_password != "your-app-password":
                    email_service = EmailService(
                        smtp_server=smtp_server,
                        smtp_port=smtp_port,
                        sender_email=sender_email,
                        sender_password=sender_password,
                        use_tls=use_tls
                    )
        
        # Create monitor
        self.monitor = GUINetworkMonitor(
            ping_service=ping_service,
            logger_service=logger_service,
            stats_tracker=self.stats_tracker,
            email_service=email_service,
            recipient_email=recipient_email,
            check_interval=check_interval,
            latency_threshold=latency_threshold,
            failure_threshold=failure_threshold,
            status_callback=self.update_icon
        )
    
    def update_icon(self, latency):
        """Update tray icon based on current status."""
        if self.icon:
            color = self.icon_service.get_status_color(latency)
            new_icon = self.icon_service.create_network_icon(size=64, color=color)
            self.icon.icon = new_icon
            self.icon.title = self.monitor.get_status_summary()
    
    def on_clicked(self, icon, item):
        """Handle single click - show quick stats."""
        # Run in separate thread to avoid blocking tray
        threading.Thread(target=self.show_quick_stats, daemon=True).start()
    
    def on_double_clicked(self, icon, item):
        """Handle double click - show full stats."""
        # Note: pystray doesn't have native double-click support
        # We'll use this as a menu item instead
        threading.Thread(target=self.show_full_stats, daemon=True).start()
    
    def on_settings(self, icon, item):
        """Handle settings menu - show settings window."""
        threading.Thread(target=self.show_settings, daemon=True).start()
    
    def show_quick_stats(self):
        """Show quick stats window (last 5 pings) with live updates."""
        try:
            window = QuickStatsWindow(self.stats_tracker)
            window.show()
        except Exception as e:
            print(f"Error showing quick stats: {e}")
    
    def show_full_stats(self):
        """Show full stats window (all history) with live updates."""
        try:
            window = FullStatsWindow(self.stats_tracker)
            window.show()
        except Exception as e:
            print(f"Error showing full stats: {e}")
    
    def reload_configuration(self):
        """Reload configuration and restart monitoring with new settings."""
        try:
            # Stop current monitor
            if self.monitor:
                self.monitor.stop()
            
            # Reload config from file
            self.config = self.load_config()
            
            # Reinitialize services with new config
            self._init_services()
            
            # Start monitoring with new settings
            self.monitor.start()
            
            return True
        except Exception as e:
            print(f"Error reloading configuration: {e}")
            return False
    
    def show_settings(self):
        """Show settings window."""
        def on_save(new_config):
            """Callback when settings are saved."""
            # Update config
            self.config = new_config
            # Reload configuration and restart monitoring
            if self.reload_configuration():
                print("Configuration reloaded successfully!")
                # Update icon title immediately
                if self.icon:
                    self.icon.title = self.monitor.get_status_summary()
            else:
                print("Failed to reload configuration!")
        
        window = SettingsWindow(self.config, on_save_callback=on_save)
        window.show()
    
    def on_quit(self, icon, item):
        """Handle quit action."""
        self.monitor.stop()
        self.single_instance.release_lock()
        icon.stop()
    
    def run(self):
        """Run the system tray application."""
        # Check if already running
        if not self.single_instance.acquire_lock():
            # Show error message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning(
                "Network Tester Already Running",
                "Network Tester is already running!\n\n"
                "Look for the network icon in your system tray.\n\n"
                "If you can't find it, check Task Manager and close any "
                "running pythonw.exe processes, then try again."
            )
            root.destroy()
            sys.exit(1)
        
        try:
            # Create initial icon
            initial_icon = self.icon_service.create_network_icon(size=64, color='gray')
            
            # Create menu
            menu = pystray.Menu(
                pystray.MenuItem("Quick Stats (Last 5)", self.on_clicked, default=True),
                pystray.MenuItem("Full Statistics", self.on_double_clicked),
                pystray.MenuItem("Settings", self.on_settings),
                pystray.MenuItem("---", None),
                pystray.MenuItem("Quit", self.on_quit)
            )
            
            # Create tray icon
            self.icon = pystray.Icon(
                "network_tester",
                initial_icon,
                "Network Monitor - Starting...",
                menu
            )
            
            # Start monitoring in background
            self.monitor.start()
            
            # Run tray icon (blocking)
            self.icon.run()
            
        finally:
            # Always release the lock when exiting
            self.single_instance.release_lock()


def main():
    """Main application entry point."""
    print("=" * 60)
    print("Network Tester - System Tray Mode")
    print("=" * 60)
    print()
    print("Starting system tray application...")
    print("Look for the network icon in your system tray!")
    print()
    print("Actions:")
    print("  - Left click: Show last 5 pings")
    print("  - Right click → Full Statistics: Show all history")
    print("  - Right click → Quit: Exit application")
    print()
    
    app = NetworkTesterTrayApp()
    app.run()


if __name__ == "__main__":
    main()
