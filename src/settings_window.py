"""
Settings Window - GUI for editing configuration
Follows Single Responsibility Principle (SRP)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
from typing import Dict, Callable


class SettingsWindow:
    """Settings window for editing application configuration."""
    
    def __init__(self, config: Dict, on_save_callback: Callable = None):
        """
        Initialize settings window.
        
        Args:
            config: Current configuration dictionary
            on_save_callback: Callback function to call when settings are saved
        """
        self.config = config.copy()
        self.on_save_callback = on_save_callback
        
        self.window = tk.Tk()
        self.window.title("Network Tester - Settings")
        self.window.geometry("650x650")
        self.window.resizable(True, True)
        self.window.minsize(600, 500)
        
        # Make window always on top initially
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))
        
        # Center window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 650) // 2
        y = (screen_height - 650) // 2
        self.window.geometry(f"+{x}+{y}")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all window widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg="#1976D2", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="⚙️ Settings",
            font=("Arial", 14, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=15)
        
        # Create main container
        container = tk.Frame(self.window)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(container, bg="white")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Content frame
        content_frame = tk.Frame(scrollable_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Monitoring Settings Section
        self._create_monitoring_section(content_frame)
        
        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Email Settings Section
        self._create_email_section(content_frame)
        
        # Add some spacing at bottom
        tk.Frame(content_frame, bg="white", height=20).pack()
        
        # Buttons frame (fixed at bottom)
        self._create_buttons()
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _create_monitoring_section(self, parent):
        """Create monitoring settings section."""
        section_frame = tk.Frame(parent, bg="white")
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Section title
        tk.Label(
            section_frame,
            text="🌐 Monitoring Settings",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Target Host
        self._create_field(
            section_frame,
            "Target Host (IP/Domain):",
            "target_host",
            self.config.get('monitoring', {}).get('target_host', '8.8.8.8'),
            "IP address or domain to monitor (e.g., 8.8.8.8, google.com)"
        )
        
        # Check Interval
        self._create_field(
            section_frame,
            "Check Interval (seconds):",
            "check_interval_seconds",
            str(self.config.get('monitoring', {}).get('check_interval_seconds', 30)),
            "How often to ping (recommended: 30)"
        )
        
        # Latency Threshold
        self._create_field(
            section_frame,
            "Latency Threshold (ms):",
            "latency_threshold_ms",
            str(self.config.get('monitoring', {}).get('latency_threshold_ms', 1000)),
            "Alert if latency exceeds this value"
        )
        
        # Failure Threshold
        self._create_field(
            section_frame,
            "Failure Threshold (count):",
            "failure_threshold",
            str(self.config.get('monitoring', {}).get('failure_threshold', 3)),
            "Alert after this many consecutive failures"
        )
    
    def _create_email_section(self, parent):
        """Create email settings section."""
        section_frame = tk.Frame(parent, bg="white")
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Section title
        tk.Label(
            section_frame,
            text="📧 Email Alert Settings",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 10))
        
        email_config = self.config.get('email', {})
        
        # SMTP Server
        self._create_field(
            section_frame,
            "SMTP Server:",
            "smtp_server",
            email_config.get('smtp_server', 'smtp.gmail.com'),
            "e.g., smtp.gmail.com"
        )
        
        # SMTP Port
        self._create_field(
            section_frame,
            "SMTP Port:",
            "smtp_port",
            str(email_config.get('smtp_port', 587)),
            "Usually 587 for TLS, 465 for SSL"
        )
        
        # Sender Email
        self._create_field(
            section_frame,
            "Sender Email:",
            "sender_email",
            email_config.get('sender_email', ''),
            "Your Gmail address"
        )
        
        # Sender Password (shown as password field)
        self._create_field(
            section_frame,
            "Sender Password (App Password):",
            "sender_password",
            email_config.get('sender_password', ''),
            "Gmail App Password (not your regular password)",
            show="*"
        )
        
        # Recipient Email
        self._create_field(
            section_frame,
            "Recipient Email:",
            "recipient_email",
            email_config.get('recipient_email', 'taranezy@gmail.com'),
            "Where to send alerts"
        )
    
    def _create_field(self, parent, label_text, field_name, default_value, tooltip="", show=None):
        """Create a labeled input field."""
        field_frame = tk.Frame(parent, bg="white")
        field_frame.pack(fill=tk.X, pady=5)
        
        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Arial", 9),
            bg="white",
            anchor="w",
            width=30
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Entry
        entry = tk.Entry(
            field_frame,
            font=("Arial", 9),
            show=show
        )
        entry.insert(0, default_value)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Store reference to entry widget
        setattr(self, f"entry_{field_name}", entry)
        
        # Tooltip
        if tooltip:
            help_label = tk.Label(
                parent,
                text=f"   ℹ️ {tooltip}",
                font=("Arial", 8),
                bg="white",
                fg="#666",
                anchor="w"
            )
            help_label.pack(fill=tk.X, pady=(0, 5))
    
    def _create_buttons(self):
        """Create action buttons."""
        # Button frame (fixed at bottom)
        button_frame = tk.Frame(self.window, bg="#f5f5f5", height=80)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)
        
        # Button container
        btn_container = tk.Frame(button_frame, bg="#f5f5f5")
        btn_container.pack(expand=True)
        
        # Save button (make it more prominent)
        save_btn = tk.Button(
            btn_container,
            text="💾 SAVE SETTINGS",
            command=self._save_settings,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=10,
            borderwidth=2,
            highlightbackground="#45a049",
            activebackground="#45a049"
        )
        save_btn.pack(side=tk.LEFT, padx=10)
        
        # Test Email button
        test_btn = tk.Button(
            btn_container,
            text="📨 Test Email",
            command=self._test_email,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        test_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            btn_container,
            text="❌ Cancel",
            command=self.close,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def _save_settings(self):
        """Save settings to config file."""
        try:
            # Update monitoring config
            if 'monitoring' not in self.config:
                self.config['monitoring'] = {}
            
            self.config['monitoring']['target_host'] = self.entry_target_host.get().strip()
            self.config['monitoring']['check_interval_seconds'] = int(self.entry_check_interval_seconds.get())
            self.config['monitoring']['latency_threshold_ms'] = float(self.entry_latency_threshold_ms.get())
            self.config['monitoring']['failure_threshold'] = int(self.entry_failure_threshold.get())
            
            # Update email config
            if 'email' not in self.config:
                self.config['email'] = {}
            
            self.config['email']['smtp_server'] = self.entry_smtp_server.get().strip()
            self.config['email']['smtp_port'] = int(self.entry_smtp_port.get())
            self.config['email']['sender_email'] = self.entry_sender_email.get().strip()
            self.config['email']['sender_password'] = self.entry_sender_password.get()
            self.config['email']['recipient_email'] = self.entry_recipient_email.get().strip()
            self.config['email']['use_tls'] = True
            
            # Validate
            if not self.config['monitoring']['target_host']:
                raise ValueError("Target host cannot be empty")
            
            if self.config['monitoring']['check_interval_seconds'] < 5:
                raise ValueError("Check interval must be at least 5 seconds")
            
            # Save to file
            config_path = Path('config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            
            messagebox.showinfo(
                "Settings Saved",
                "Settings have been saved and applied successfully!\n\n"
                "✅ Changes are now active:\n"
                f"• Target: {self.config['monitoring']['target_host']}\n"
                f"• Interval: {self.config['monitoring']['check_interval_seconds']}s\n"
                f"• Threshold: {self.config['monitoring']['latency_threshold_ms']}ms\n\n"
                "No restart required!"
            )
            
            # Call callback if provided
            if self.on_save_callback:
                self.on_save_callback(self.config)
            
            self.close()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your input:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")
    
    def _test_email(self):
        """Test email settings by sending a test email."""
        try:
            from services.email_service import EmailService
            
            smtp_server = self.entry_smtp_server.get().strip()
            smtp_port = int(self.entry_smtp_port.get())
            sender_email = self.entry_sender_email.get().strip()
            sender_password = self.entry_sender_password.get()
            recipient_email = self.entry_recipient_email.get().strip()
            
            if not all([smtp_server, smtp_port, sender_email, sender_password, recipient_email]):
                messagebox.showwarning(
                    "Incomplete Settings",
                    "Please fill in all email fields before testing."
                )
                return
            
            # Show testing message
            test_window = tk.Toplevel(self.window)
            test_window.title("Testing Email...")
            test_window.geometry("300x100")
            test_window.resizable(False, False)
            
            # Center it
            x = self.window.winfo_x() + (self.window.winfo_width() - 300) // 2
            y = self.window.winfo_y() + (self.window.winfo_height() - 100) // 2
            test_window.geometry(f"+{x}+{y}")
            
            tk.Label(
                test_window,
                text="Sending test email...\nPlease wait...",
                font=("Arial", 10)
            ).pack(expand=True)
            
            test_window.update()
            
            # Create email service and send test
            email_service = EmailService(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                use_tls=True
            )
            
            success = email_service.send_notification(
                recipient_email,
                "Network Tester - Test Email",
                "This is a test email from Network Tester.\n\n"
                "If you receive this, your email settings are configured correctly!\n\n"
                f"Sent from: {sender_email}"
            )
            
            test_window.destroy()
            
            if success:
                messagebox.showinfo(
                    "Email Test Successful",
                    f"Test email sent successfully to {recipient_email}!\n\n"
                    "Please check your inbox to confirm receipt."
                )
            else:
                messagebox.showerror(
                    "Email Test Failed",
                    "Failed to send test email.\n\n"
                    "Please check your SMTP settings and credentials.\n\n"
                    "For Gmail, make sure you're using an App Password,\n"
                    "not your regular password."
                )
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your input:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to test email:\n{e}")
    
    def show(self):
        """Show the settings window."""
        self.window.mainloop()
    
    def close(self):
        """Close the settings window."""
        try:
            self.window.destroy()
        except:
            pass
