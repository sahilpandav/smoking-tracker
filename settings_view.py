"""
A popup window letting the user edit daily limit, price per
cigarette, and currency symbol — persisted via settings.py.

Opened from main.py via a "Settings" button.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import config
import settings


class SettingsDialog:
    """
    Builds and manages the settings popup window.

    on_saved is called after a successful save, so main.py can
    refresh the dashboard (since price/limit affect displayed stats).
    """

    def __init__(self, parent, on_saved):
        self.on_saved = on_saved
        current = settings.load_settings()

        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("380x320")
        self.window.configure(bg=config.COLOR_BG)
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self._build_form(current)

    def _build_form(self, current):
        title_label = ttk.Label(self.window, text="Settings", style="Title.TLabel")
        title_label.pack(pady=(20, 15))

        # --- Daily limit ---
        limit_label = ttk.Label(self.window, text="Daily Cigarette Limit", style="TLabel")
        limit_label.pack(anchor="w", padx=30)

        self.limit_var = tk.StringVar(value=str(current["daily_limit"]))
        limit_entry = ttk.Entry(self.window, textvariable=self.limit_var)
        limit_entry.pack(fill="x", padx=30, pady=(0, 15))

        # --- Price per cigarette ---
        price_label = ttk.Label(self.window, text="Price per Cigarette", style="TLabel")
        price_label.pack(anchor="w", padx=30)

        self.price_var = tk.StringVar(value=str(current["price_per_cigarette"]))
        price_entry = ttk.Entry(self.window, textvariable=self.price_var)
        price_entry.pack(fill="x", padx=30, pady=(0, 15))

        # --- Currency symbol ---
        currency_label = ttk.Label(self.window, text="Currency Symbol", style="TLabel")
        currency_label.pack(anchor="w", padx=30)

        self.currency_var = tk.StringVar(value=current["currency_symbol"])
        currency_entry = ttk.Entry(self.window, textvariable=self.currency_var)
        currency_entry.pack(fill="x", padx=30, pady=(0, 20))

        # --- Save button ---
        save_button = ttk.Button(
            self.window,
            text="Save Settings",
            style="Accent.TButton",
            command=self._on_save,
        )
        save_button.pack(pady=5)

    def _on_save(self):
        """
        Validates and saves all three settings. Shows an error popup
        instead of crashing if the user typed something invalid.
        """
        try:
            daily_limit = int(self.limit_var.get())
            price_per_cigarette = float(self.price_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Daily limit must be a whole number, and price must be a number (e.g. 15 or 15.50).",
            )
            return

        currency_symbol = self.currency_var.get().strip()
        if not currency_symbol:
            messagebox.showerror("Invalid Input", "Currency symbol cannot be empty.")
            return

        settings.save_settings({
            "daily_limit": daily_limit,
            "price_per_cigarette": price_per_cigarette,
            "currency_symbol": currency_symbol,
        })

        self.on_saved()
        self.window.destroy()