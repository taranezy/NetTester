"""
GUI Windows - Tkinter windows for displaying stats
Follows Single Responsibility Principle (SRP)
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Dict
from services.stats_tracker_service import StatsEntry


class QuickStatsWindow:
    """Small popup window showing last 5 ping results with auto-refresh."""
    
    def __init__(self, stats_tracker, initial_stats: List[StatsEntry] = None, initial_summary: Dict = None):
        """
        Initialize quick stats window.
        
        Args:
            stats_tracker: StatsTrackerService instance for live data
            initial_stats: Initial stats to display (optional)
            initial_summary: Initial summary to display (optional)
        """
        self.stats_tracker = stats_tracker
        self.window = tk.Tk()
        self.window.title("Network Monitor - Quick Stats (Live)")
        self.window.geometry("420x300")
        self.window.resizable(False, False)
        
        # Make window appear near system tray (bottom right)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = screen_width - 440
        y = screen_height - 370
        self.window.geometry(f"+{x}+{y}")
        
        # Store widgets for updating
        self.summary_label = None
        self.stats_container = None
        
        # Create initial widgets
        stats = initial_stats or self.stats_tracker.get_last_n(5)
        summary = initial_summary or self.stats_tracker.get_summary()
        self._create_widgets(stats, summary)
        
        # Start auto-refresh (every 2 seconds)
        self._schedule_refresh()
        
        # Auto-close after 30 seconds
        self.window.after(30000, self.close)
    
    def _create_widgets(self, stats: List[StatsEntry], summary: Dict):
        """Create window widgets."""
        # Title
        title_frame = tk.Frame(self.window, bg="#2196F3", height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🌐 Network Monitor",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title_label.pack(pady=8)
        
        # Summary section
        summary_frame = tk.Frame(self.window, bg="white")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        summary_text = f"Success Rate: {summary['success_rate']:.1f}% | Avg: {summary['avg_latency']:.1f} ms | Failures: {summary['consecutive_failures']}"
        self.summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=("Arial", 9),
            bg="white",
            fg="#555"
        )
        self.summary_label.pack(pady=5)
        
        # Stats list
        self.stats_container = tk.Frame(self.window, bg="white")
        self.stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            self.stats_container,
            text="Last 5 Pings (Live):",
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Stats frame for entries
        self.stats_frame = tk.Frame(self.stats_container, bg="white")
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display initial stats
        self._update_stats_display(stats)
        
        # Close button
        close_btn = tk.Button(
            self.window,
            text="Close",
            command=self.close,
            bg="#f0f0f0",
            relief=tk.FLAT,
            cursor="hand2"
        )
        close_btn.pack(pady=10)
    
    def _create_stat_entry(self, parent, entry: StatsEntry):
        """Create a single stat entry widget."""
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.X, pady=2)
        
        time_str = entry.timestamp.strftime("%H:%M:%S")
        
        if entry.latency is not None:
            # Determine color based on latency
            if entry.latency < 100:
                color = "#4CAF50"  # Green
                status = "●"
            elif entry.latency < 500:
                color = "#2196F3"  # Blue
                status = "●"
            elif entry.latency < 1000:
                color = "#FF9800"  # Orange
                status = "●"
            else:
                color = "#F44336"  # Red
                status = "●"
            
            text = f"{status} {time_str} - {entry.latency:.2f} ms"
        else:
            color = "#9E9E9E"  # Gray
            text = f"✗ {time_str} - NO RESPONSE"
        
        label = tk.Label(
            frame,
            text=text,
            font=("Consolas", 9),
            bg="white",
            fg=color,
            anchor="w"
        )
        label.pack(fill=tk.X, padx=5)
    
    def _update_stats_display(self, stats: List[StatsEntry]):
        """Update the stats display with new data."""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Display new stats (newest first)
        for entry in reversed(stats):
            self._create_stat_entry(self.stats_frame, entry)
    
    def _refresh_data(self):
        """Refresh the window with latest data."""
        try:
            # Get latest data
            stats = self.stats_tracker.get_last_n(5)
            summary = self.stats_tracker.get_summary()
            
            # Update summary
            summary_text = f"Success Rate: {summary['success_rate']:.1f}% | Avg: {summary['avg_latency']:.1f} ms | Failures: {summary['consecutive_failures']}"
            self.summary_label.config(text=summary_text)
            
            # Update stats display
            self._update_stats_display(stats)
            
        except Exception as e:
            print(f"Error refreshing quick stats: {e}")
    
    def _schedule_refresh(self):
        """Schedule the next refresh."""
        try:
            if self.window.winfo_exists():
                self._refresh_data()
                # Schedule next refresh in 2 seconds
                self.window.after(2000, self._schedule_refresh)
        except:
            # Window was closed
            pass
    
    def show(self):
        """Show the window."""
        self.window.mainloop()
    
    def close(self):
        """Close the window."""
        try:
            self.window.destroy()
        except:
            pass


class FullStatsWindow:
    """Full statistics window with complete history and auto-refresh."""
    
    def __init__(self, stats_tracker, initial_stats: List[StatsEntry] = None, initial_summary: Dict = None):
        """
        Initialize full stats window.
        
        Args:
            stats_tracker: StatsTrackerService instance for live data
            initial_stats: Initial stats to display (optional)
            initial_summary: Initial summary to display (optional)
        """
        self.stats_tracker = stats_tracker
        self.window = tk.Tk()
        self.window.title("Network Monitor - Full Statistics (Live)")
        self.window.geometry("700x600")
        
        # Center window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 600) // 2
        self.window.geometry(f"+{x}+{y}")
        
        # Store widgets for updating
        self.summary_widgets = {}
        self.stats_tree = None
        
        # Create initial widgets
        stats = initial_stats or self.stats_tracker.get_all()
        summary = initial_summary or self.stats_tracker.get_summary()
        self._create_widgets(stats, summary)
        
        # Start auto-refresh (every 3 seconds)
        self._schedule_refresh()
    
    def _create_widgets(self, stats: List[StatsEntry], summary: Dict):
        """Create window widgets."""
        # Header
        header_frame = tk.Frame(self.window, bg="#1976D2", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📊 Network Monitor - Full Statistics",
            font=("Arial", 14, "bold"),
            bg="#1976D2",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Summary section
        self._create_summary_section(summary)
        
        # Stats table
        self._create_stats_table(stats)
        
        # Footer buttons
        self._create_footer()
    
    def _create_summary_section(self, summary: Dict):
        """Create summary statistics section."""
        summary_frame = tk.Frame(self.window, bg="#f5f5f5", height=120)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        summary_frame.pack_propagate(False)
        
        tk.Label(
            summary_frame,
            text="Summary Statistics",
            font=("Arial", 11, "bold"),
            bg="#f5f5f5"
        ).pack(pady=(10, 5))
        
        # Create grid of stats
        grid_frame = tk.Frame(summary_frame, bg="#f5f5f5")
        grid_frame.pack(pady=5)
        
        stats_data = [
            ("Total Pings:", f"{summary['total_pings']}"),
            ("Successful:", f"{summary['successful']}"),
            ("Failed:", f"{summary['failed']}"),
            ("Success Rate:", f"{summary['success_rate']:.1f}%"),
            ("Avg Latency:", f"{summary['avg_latency']:.2f} ms"),
            ("Min Latency:", f"{summary['min_latency']:.2f} ms"),
            ("Max Latency:", f"{summary['max_latency']:.2f} ms"),
            ("Consecutive Failures:", f"{summary['consecutive_failures']}")
        ]
        
        for i, (label_text, value_text) in enumerate(stats_data):
            row = i // 4
            col = i % 4
            
            stat_frame = tk.Frame(grid_frame, bg="#f5f5f5")
            stat_frame.grid(row=row, column=col, padx=15, pady=2)
            
            tk.Label(
                stat_frame,
                text=label_text,
                font=("Arial", 9),
                bg="#f5f5f5",
                fg="#666"
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                stat_frame,
                text=value_text,
                font=("Arial", 9, "bold"),
                bg="#f5f5f5"
            )
            value_label.pack(side=tk.LEFT, padx=(5, 0))
            
            # Store reference for updating
            self.summary_widgets[label_text] = value_label
    
    def _create_stats_table(self, stats: List[StatsEntry]):
        """Create scrollable stats table."""
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.table_label = tk.Label(
            table_frame,
            text=f"Ping History ({len(stats)} entries) - Live Updates",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.table_label.pack(fill=tk.X, pady=(0, 5))
        
        # Create scrolled text widget
        self.stats_text = scrolledtext.ScrolledText(
            table_frame,
            font=("Consolas", 9),
            wrap=tk.NONE,
            bg="white",
            fg="#333"
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial population
        self._update_stats_table(stats)
    
    def _create_footer(self):
        """Create footer with buttons."""
        footer_frame = tk.Frame(self.window, bg="#f5f5f5")
        footer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        close_btn = tk.Button(
            footer_frame,
            text="Close",
            command=self.close,
            bg="#2196F3",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=5
        )
        close_btn.pack(side=tk.RIGHT)
    
    def _update_stats_table(self, stats: List[StatsEntry]):
        """Update the stats table with new data."""
        # Clear existing content
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        # Add header
        self.stats_text.insert(tk.END, f"{'Timestamp':<20} {'Latency':<15} {'Status':<10}\n")
        self.stats_text.insert(tk.END, "-" * 60 + "\n")
        
        # Add stats (newest first)
        for entry in reversed(stats):
            time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            if entry.latency is not None:
                latency_str = f"{entry.latency:.2f} ms"
                if entry.latency < 100:
                    status = "Excellent"
                elif entry.latency < 500:
                    status = "Good"
                elif entry.latency < 1000:
                    status = "Fair"
                else:
                    status = "Poor"
            else:
                latency_str = "NO RESPONSE"
                status = "Failed"
            
            self.stats_text.insert(tk.END, f"{time_str:<20} {latency_str:<15} {status:<10}\n")
        
        # Make read-only
        self.stats_text.config(state=tk.DISABLED)
        
        # Update table label
        self.table_label.config(text=f"Ping History ({len(stats)} entries) - Live Updates")
    
    def _update_summary(self, summary: Dict):
        """Update summary statistics."""
        stats_data = [
            ("Total Pings:", f"{summary['total_pings']}"),
            ("Successful:", f"{summary['successful']}"),
            ("Failed:", f"{summary['failed']}"),
            ("Success Rate:", f"{summary['success_rate']:.1f}%"),
            ("Avg Latency:", f"{summary['avg_latency']:.2f} ms"),
            ("Min Latency:", f"{summary['min_latency']:.2f} ms"),
            ("Max Latency:", f"{summary['max_latency']:.2f} ms"),
            ("Consecutive Failures:", f"{summary['consecutive_failures']}")
        ]
        
        for label_text, value_text in stats_data:
            if label_text in self.summary_widgets:
                self.summary_widgets[label_text].config(text=value_text)
    
    def _refresh_data(self):
        """Refresh the window with latest data."""
        try:
            # Get latest data
            stats = self.stats_tracker.get_all()
            summary = self.stats_tracker.get_summary()
            
            # Update summary
            self._update_summary(summary)
            
            # Update stats table
            self._update_stats_table(stats)
            
        except Exception as e:
            print(f"Error refreshing full stats: {e}")
    
    def _schedule_refresh(self):
        """Schedule the next refresh."""
        try:
            if self.window.winfo_exists():
                self._refresh_data()
                # Schedule next refresh in 3 seconds
                self.window.after(3000, self._schedule_refresh)
        except:
            # Window was closed
            pass
    
    def show(self):
        """Show the window."""
        self.window.mainloop()
    
    def close(self):
        """Close the window."""
        try:
            self.window.destroy()
        except:
            pass
