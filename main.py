"""
This is the entry point of the application — the file you run
to launch Smoking Tracker.

This version builds the real dashboard: live stats pulled from
analytics.py, and an "Add Cigarette" button wired to tracker.py.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import config
import database
import tracker
import analytics
import reports
import notifications

from entry_dialog import AddEntryDialog
from history_view import HistoryDialog
from charts_view import ChartsDialog
from settings_view import SettingsDialog
from backup_view import BackupDialog


class SmokingTrackerApp:
    """
    Main application class. Holds the window, the dashboard widgets,
    and the logic to refresh them after any change.
    """

    def __init__(self, root):
        self.root = root
        self.stat_labels = {}  # will store references to value labels so we can update them later

        self._setup_window()
        self._setup_style()
        self._build_dashboard()
        self.refresh_stats()
        self._start_notification_scheduler()

    def _setup_window(self):
        """Configures the main window: title, size, background color."""
        self.root.title(config.APP_NAME)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.root.configure(bg=config.COLOR_BG)

    def _setup_style(self):
        """Configures the ttk theme so widgets match our color scheme."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Muted.TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI Semibold", 18),
        )
        style.configure(
            "CardTitle.TLabel",
            background=config.COLOR_BG_SECONDARY,
            foreground=config.COLOR_TEXT_MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "CardValue.TLabel",
            background=config.COLOR_BG_SECONDARY,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI Semibold", 20),
        )
        style.configure(
            "RingBig.TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI Semibold", 34),
        )
        style.configure(
            "RingSmall.TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT_MUTED,
            font=("Segoe UI", 11),
        )

        # Primary action — filled, accent-colored, used ONCE (Add Cigarette)
        style.configure(
            "Primary.TButton",
            font=("Segoe UI Semibold", 11),
            padding=(16, 10),
            background=config.COLOR_ACCENT,
            foreground="#0B120E",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#3F9A63")],
        )

        # Sidebar nav buttons — flat, quiet, left-aligned
        style.configure(
            "Nav.TButton",
            font=("Segoe UI", 10),
            padding=(14, 9),
            background=config.COLOR_SIDEBAR,
            foreground=config.COLOR_TEXT,
            borderwidth=0,
            anchor="w",
        )
        style.map(
            "Nav.TButton",
            background=[("active", config.COLOR_BG_SECONDARY)],
        )

        style.configure(
            "Limit.Horizontal.TProgressbar",
            troughcolor=config.COLOR_BG_SECONDARY,
            background=config.COLOR_SUCCESS,
        )

    def _build_dashboard(self):
        """
        Builds the full window layout: a left sidebar for navigation
        (grouped by purpose), and a main panel led by today's progress
        ring, with secondary stats below it.
        """
        # Root-level horizontal split: sidebar on the left, main content on the right.
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_panel()

    def _build_sidebar(self):
        """
        Left navigation column. Buttons are grouped by purpose with
        small section labels, instead of one flat row of 8 buttons.
        """
        sidebar = tk.Frame(self.root, bg=config.COLOR_SIDEBAR, width=config.SIDEBAR_WIDTH)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        app_name_label = ttk.Label(
            sidebar, text=config.APP_NAME, style="Title.TLabel",
            background=config.COLOR_SIDEBAR,
        )
        app_name_label.pack(anchor="w", padx=20, pady=(24, 30))

        self._build_nav_section(sidebar, "TRACK", [
            ("View History", self.on_view_history),
            ("View Charts", self.on_view_charts),
        ])

        self._build_nav_section(sidebar, "MANAGE", [
            ("Settings", self.on_open_settings),
            ("Backup / Restore", self.on_open_backup),
        ])

        self._build_nav_section(sidebar, "REPORTS", [
            ("Export CSV", self.on_export_csv),
            ("Export PDF", self.on_export_pdf),
        ])

        self._build_nav_section(sidebar, "OTHER", [
            ("Send Test Reminder", self.on_test_notification),
        ])

    def _build_nav_section(self, parent, section_title, buttons):
        """
        Renders one labeled group of nav buttons in the sidebar,
        e.g. "TRACK" containing History and Charts. This is what
        replaces the old flat 4x2 button grid — buttons are now
        grouped by what they're actually for.
        """
        section_label = ttk.Label(
            parent, text=section_title, style="Muted.TLabel",
            background=config.COLOR_SIDEBAR,
        )
        section_label.pack(anchor="w", padx=20, pady=(14, 4))

        for label_text, command in buttons:
            button = ttk.Button(
                parent, text=label_text, style="Nav.TButton", command=command,
            )
            button.pack(fill="x", padx=10, pady=1)

    def _build_main_panel(self):
        """
        Right-hand content area: the "+ Add Cigarette" primary action,
        the today progress ring (the app's signature visual), and
        secondary stat cards below it.
        """
        main_panel = tk.Frame(self.root, bg=config.COLOR_BG)
        main_panel.grid(row=0, column=1, sticky="nsew")
        main_panel.grid_columnconfigure(0, weight=1)

        top_bar = tk.Frame(main_panel, bg=config.COLOR_BG)
        top_bar.pack(fill="x", padx=30, pady=(24, 0))

        add_button = ttk.Button(
            top_bar, text="+  Add Cigarette", style="Primary.TButton",
            command=self.on_add_cigarette,
        )
        add_button.pack(anchor="e")

        self._build_progress_ring(main_panel)
        self._build_secondary_stats(main_panel)

    def _build_progress_ring(self, parent):
        """
        The signature visual: a circular ring showing today's count
        against the daily limit, drawn on a plain tk.Canvas. Replaces
        the old horizontal progress bar as the app's central focus.
        """
        ring_frame = tk.Frame(parent, bg=config.COLOR_BG)
        ring_frame.pack(pady=(10, 20))

        self.ring_canvas = tk.Canvas(
            ring_frame, width=220, height=220,
            bg=config.COLOR_BG, highlightthickness=0,
        )
        self.ring_canvas.pack()

        # Text is placed on the canvas itself, centered inside the ring.
        self.ring_value_text = self.ring_canvas.create_text(
            110, 100, text="0", font=("Segoe UI Semibold", 34), fill=config.COLOR_TEXT,
        )
        self.ring_sub_text = self.ring_canvas.create_text(
            110, 135, text="of 0 today", font=("Segoe UI", 11), fill=config.COLOR_TEXT_MUTED,
        )

        self.progress_label = ttk.Label(ring_frame, text="", style="Muted.TLabel")
        self.progress_label.pack(pady=(10, 0))

    def _build_secondary_stats(self, parent):
        """Smaller supporting stat cards, arranged in a single row below the ring."""
        cards_frame = tk.Frame(parent, bg=config.COLOR_BG)
        cards_frame.pack(pady=(10, 20))

        stat_definitions = [
            ("yesterday", "Yesterday"),
            ("week", "This Week"),
            ("month", "This Month"),
            ("lifetime", "Lifetime"),
            ("streak", "Streak"),
            ("money_today", "Spent Today"),
            ("avg_per_day", "Avg / Day"),
        ]

        for index, (key, display_name) in enumerate(stat_definitions):
            row = index // 4
            column = index % 4
            self._create_stat_card(cards_frame, key, display_name, row, column)

    def _create_stat_card(self, parent, key, display_name, row, column):
        """
        Creates one small 'card' showing a label (e.g. 'Today') and
        a big value below it (e.g. '3'). Stores the value label in
        self.stat_labels so refresh_stats() can update it later.
        """
        card = tk.Frame(parent, bg=config.COLOR_BG_SECONDARY, width=200, height=90)
        card.grid(row=row, column=column, padx=10, pady=10)
        card.grid_propagate(False)  # stops the card from shrinking to fit its content

        name_label = ttk.Label(card, text=display_name, style="CardTitle.TLabel")
        name_label.pack(pady=(15, 5))

        value_label = ttk.Label(card, text="—", style="CardValue.TLabel")
        value_label.pack()

        self.stat_labels[key] = value_label

    def refresh_stats(self):
        """
        Recalculates every stat from analytics.py and updates each
        card's value label, plus the daily limit progress bar.
        Called once at startup, and again every time an entry
        is added, deleted, or settings change.
        """
        currency = config.DEFAULT_CURRENCY_SYMBOL

        #!self.stat_labels["today"].config(text=str(analytics.count_today()))
        self.stat_labels["yesterday"].config(text=str(analytics.count_yesterday()))
        self.stat_labels["week"].config(text=str(analytics.count_this_week()))
        self.stat_labels["month"].config(text=str(analytics.count_this_month()))
        self.stat_labels["lifetime"].config(text=str(analytics.count_lifetime()))
        self.stat_labels["streak"].config(text=f"{analytics.current_streak_days()}d")
        self.stat_labels["money_today"].config(
            text=f"{currency}{analytics.money_spent_today():.2f}"
        )
        self.stat_labels["avg_per_day"].config(
            text=f"{analytics.average_per_day():.1f}"
        )

        self._refresh_progress_bar()

    def _refresh_progress_bar(self):
        """
        Redraws the progress ring based on today's count vs. the
        daily limit: an arc fills proportionally, colored green/
        amber/red depending on how close to or over the limit.
        """
        today_count, daily_limit, percentage = analytics.daily_limit_progress()

        # Remove the previous ring drawing before drawing the new one —
        # Canvas doesn't auto-clear, so old arcs would stack up otherwise.
        self.ring_canvas.delete("ring_arc")

        if today_count >= daily_limit:
            ring_color = config.COLOR_DANGER
            status_text = "Limit reached for today"
        elif percentage >= 70:
            ring_color = config.COLOR_WARNING
            status_text = "Getting close to your limit"
        else:
            ring_color = config.COLOR_ACCENT
            status_text = "Within your daily limit"

        # Background track (the full, unfilled circle), drawn first so
        # the colored arc sits visually on top of it.
        self.ring_canvas.create_oval(
            15, 15, 205, 205,
            outline=config.COLOR_BG_SECONDARY, width=14,
            tags="ring_arc",
        )

        # The filled portion. Angles in Tkinter go counter-clockwise from
        # 3 o'clock by default, so start=90 begins at the top of the circle,
        # and a negative extent sweeps clockwise — the natural reading direction.
        sweep_angle = 360 * (percentage / 100)
        if sweep_angle > 0:
            self.ring_canvas.create_arc(
                15, 15, 205, 205,
                start=90, extent=-sweep_angle,
                style="arc", outline=ring_color, width=14,
                tags="ring_arc",
            )

        # Update the text sitting in the center of the ring.
        self.ring_canvas.itemconfig(self.ring_value_text, text=str(today_count), fill=config.COLOR_TEXT)
        self.ring_canvas.itemconfig(self.ring_sub_text, text=f"of {daily_limit} today")

        self.progress_label.config(text=status_text)

    def _start_notification_scheduler(self):
        """
        Kicks off all repeating background reminders. Each one is
        independent — they don't block each other or the GUI,
        since they're all built on Tkinter's non-blocking .after().
        """
        self._schedule_limit_check()
        self._schedule_motivational_nudge()
        self._schedule_water_reminder()

    def _schedule_limit_check(self):
        """Checks today's count against the daily limit, notifies if close/over."""
        today_count, daily_limit, percentage = analytics.daily_limit_progress()

        # Only actually notify if reasonably close to or over the limit,
        # so this doesn't spam a notification every 30 minutes regardless.
        if percentage >= 70:
            notifications.notify_limit_warning(today_count, daily_limit)

        # Reschedule itself to run again after the same interval —
        # this is the "self-repeating chain" pattern explained above.
        self.root.after(config.LIMIT_CHECK_INTERVAL_MS, self._schedule_limit_check)

    def _schedule_motivational_nudge(self):
        """Sends a motivational notification periodically."""
        notifications.notify_motivational()
        self.root.after(config.MOTIVATIONAL_INTERVAL_MS, self._schedule_motivational_nudge)

    def _schedule_water_reminder(self):
        """Sends a water reminder periodically."""
        notifications.notify_water_reminder()
        self.root.after(config.WATER_REMINDER_INTERVAL_MS, self._schedule_water_reminder)

    def on_add_cigarette(self):
        """
        Called when the '+ Add Cigarette' button is clicked.
        Opens the detailed entry popup instead of logging a blind entry.
        The popup calls self.refresh_stats when it saves.
        """
        AddEntryDialog(self.root, on_saved=self.refresh_stats)

    def on_view_history(self):
        """
        Called when 'View History' is clicked. Opens the history
        popup. on_changed is refresh_stats, so deleting an entry
        updates the dashboard too.
        """
        HistoryDialog(self.root, on_changed=self.refresh_stats)

    def on_view_charts(self):
        """Called when 'View Charts' is clicked. Opens the charts popup."""
        ChartsDialog(self.root)

    def on_open_settings(self):
        """
        Called when 'Settings' is clicked. Opens the settings popup.
        Refreshes the dashboard after saving, since price/limit
        changes affect displayed stats.
        """
        SettingsDialog(self.root, on_saved=self.refresh_stats)

    def on_export_csv(self):
        """Exports all entries to a CSV file and shows where it was saved."""
        filepath = reports.export_csv()
        messagebox.showinfo("Export Complete", f"CSV saved to:\n{filepath}")

    def on_export_pdf(self):
        """Exports a full PDF report and shows where it was saved."""
        filepath = reports.export_pdf()
        messagebox.showinfo("Export Complete", f"PDF saved to:\n{filepath}")

    def on_open_backup(self):
        """Called when 'Backup / Restore' is clicked. Opens the backup popup."""
        BackupDialog(self.root)

    def on_test_notification(self):
        """
        Manually triggers a limit-warning notification using today's
        real data, so we can confirm plyer notifications work on
        this machine before wiring up automatic scheduling.
        """
        today_count, daily_limit, _ = analytics.daily_limit_progress()
        notifications.notify_limit_warning(today_count, daily_limit)


def main():
    """
    Starts the application:
    1. Make sure required folders exist.
    2. Make sure the database table exists.
    3. Open the window.
    """
    config.ensure_folders_exist()
    database.initialize_database()

    root = tk.Tk()
    app = SmokingTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()