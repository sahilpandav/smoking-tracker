"""
A popup window showing visual charts built from your logged data:
- Daily trend (last 14 days)
- Trigger breakdown (pie chart)

Uses matplotlib, embedded inside a Tkinter window via
FigureCanvasTkAgg (matplotlib's official Tkinter bridge).
"""

import tkinter as tk
from tkinter import ttk
import datetime
from collections import Counter

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
import tracker


class ChartsDialog:
    """Builds and manages the charts popup window."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Charts")
        self.window.geometry("800x500")
        self.window.configure(bg=config.COLOR_BG)

        self.window.transient(parent)
        self.window.grab_set()

        self._build_tabs()

    def _build_tabs(self):
        """
        Uses a Notebook (tabbed interface) so multiple charts can
        live in one window without cluttering a single screen.
        """
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        daily_tab = tk.Frame(notebook, bg=config.COLOR_BG)
        trigger_tab = tk.Frame(notebook, bg=config.COLOR_BG)

        notebook.add(daily_tab, text="Daily Trend")
        notebook.add(trigger_tab, text="Triggers")

        self._build_daily_trend_chart(daily_tab)
        self._build_trigger_pie_chart(trigger_tab)

    def _get_last_14_days_counts(self):
        """
        Returns two parallel lists: day labels (e.g. 'Jul 03') and
        the cigarette count for each of the last 14 days, oldest first.
        """
        entries = tracker.get_all_entries()
        # Build a quick lookup: {"2026-07-11": 3, "2026-07-10": 1, ...}
        counts_by_date = Counter(entry[1] for entry in entries)  # entry[1] is the date string

        today = datetime.date.today()
        labels = []
        values = []

        for days_ago in range(13, -1, -1):  # 13 down to 0, so oldest day comes first
            day = today - datetime.timedelta(days=days_ago)
            day_str = day.strftime("%Y-%m-%d")
            labels.append(day.strftime("%b %d"))  # e.g. "Jul 11"
            values.append(counts_by_date.get(day_str, 0))

        return labels, values

    def _build_daily_trend_chart(self, parent):
        """Draws a line chart of cigarette counts for the last 14 days."""
        labels, values = self._get_last_14_days_counts()

        # Figure is the overall chart canvas; figsize is in inches.
        figure = Figure(figsize=(7, 4), dpi=100)
        figure.patch.set_facecolor(config.COLOR_BG)

        ax = figure.add_subplot(111)  # "111" = 1 row, 1 column, 1st plot
        ax.set_facecolor(config.COLOR_BG_SECONDARY)

        ax.plot(labels, values, color=config.COLOR_ACCENT, marker="o", linewidth=2)
        ax.set_title("Last 14 Days", color=config.COLOR_TEXT)
        ax.tick_params(axis="x", colors=config.COLOR_TEXT_MUTED, rotation=45)
        ax.tick_params(axis="y", colors=config.COLOR_TEXT_MUTED)
        for spine in ax.spines.values():
            spine.set_color(config.COLOR_TEXT_MUTED)

        figure.tight_layout()  # prevents labels from getting cut off at the edges

        # This is the bridge: turns the matplotlib Figure into a
        # widget that can be packed into a Tkinter window like any other.
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_trigger_pie_chart(self, parent):
        """Draws a pie chart showing the proportion of each trigger."""
        entries = tracker.get_all_entries()
        # entry[3] is the trigger column; skip entries with no trigger set
        triggers = [entry[3] for entry in entries if entry[3]]

        figure = Figure(figsize=(7, 4), dpi=100)
        figure.patch.set_facecolor(config.COLOR_BG)
        ax = figure.add_subplot(111)

        if not triggers:
            # Handle the empty-data case explicitly instead of drawing a broken chart.
            ax.text(
                0.5, 0.5, "No trigger data yet.\nLog some entries with a trigger set.",
                ha="center", va="center", color=config.COLOR_TEXT, fontsize=11,
            )
            ax.axis("off")
        else:
            trigger_counts = Counter(triggers)
            labels = list(trigger_counts.keys())
            values = list(trigger_counts.values())

            ax.pie(
                values,
                labels=labels,
                autopct="%1.0f%%",  # shows percentage on each slice, no decimals
                textprops={"color": config.COLOR_TEXT},
            )
            ax.set_title("Triggers Breakdown", color=config.COLOR_TEXT)

        figure.patch.set_facecolor(config.COLOR_BG)

        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)