"""
This is the entry point of the application — the file you run
to launch Smoking Tracker.

This version builds the real dashboard: live stats pulled from
analytics.py, and an "Add Cigarette" button wired to tracker.py.
"""

import tkinter as tk
from tkinter import ttk

import config
import database
import tracker
import analytics

from entry_dialog import AddEntryDialog
from history_view import HistoryDialog


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

    def _setup_window(self):
        """Configures the main window: title, size, background color."""
        self.root.title(config.APP_NAME)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.root.configure(bg=config.COLOR_BG)

    def _setup_style(self):
        """Configures the ttk theme so widgets match our dark color scheme."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure(
            "TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Title.TLabel",
            background=config.COLOR_BG,
            foreground=config.COLOR_TEXT,
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "CardTitle.TLabel",
            background=config.COLOR_BG_SECONDARY,
            foreground=config.COLOR_TEXT_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardValue.TLabel",
            background=config.COLOR_BG_SECONDARY,
            foreground=config.COLOR_ACCENT,
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
        )

    def _build_dashboard(self):
        """Builds the full dashboard layout: title, stat cards, and action button."""
        title_label = ttk.Label(self.root, text=config.APP_NAME, style="Title.TLabel")
        title_label.pack(pady=(20, 10))

        # A frame is an invisible container used to group and position other widgets.
        cards_frame = tk.Frame(self.root, bg=config.COLOR_BG)
        cards_frame.pack(pady=10)

        # Each tuple is: (key used internally, label shown to user)
        stat_definitions = [
            ("today", "Today"),
            ("yesterday", "Yesterday"),
            ("week", "This Week"),
            ("month", "This Month"),
            ("lifetime", "Lifetime"),
            ("streak", "Current Streak"),
            ("money_today", "Spent Today"),
            ("avg_per_day", "Avg per Day"),
        ]

        # Arrange 4 cards per row using grid positions.
        for index, (key, display_name) in enumerate(stat_definitions):
            row = index // 4
            column = index % 4
            self._create_stat_card(cards_frame, key, display_name, row, column)

        button_frame = tk.Frame(self.root, bg=config.COLOR_BG)
        button_frame.pack(pady=25)

        add_button = ttk.Button(
            button_frame,
            text="+ Add Cigarette",
            style="Accent.TButton",
            command=self.on_add_cigarette,
        )
        add_button.grid(row=0, column=0, padx=10)

        history_button = ttk.Button(
            button_frame,
            text="View History",
            style="Accent.TButton",
            command=self.on_view_history,
        )
        history_button.grid(row=0, column=1, padx=10)

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
        card's value label. Called once at startup, and again every
        time an entry is added.
        """
        currency = config.DEFAULT_CURRENCY_SYMBOL

        self.stat_labels["today"].config(text=str(analytics.count_today()))
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