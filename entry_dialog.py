"""
A popup window (Toplevel) for logging a cigarette with full detail:
trigger, mood before, mood after, and a note.

This is opened from main.py when the user clicks "+ Add Cigarette".
It calls tracker.add_entry() with the values the user picked,
then closes itself.
"""

import tkinter as tk
from tkinter import ttk

import config
import tracker


TRIGGER_OPTIONS = [
    "Stress", "Work", "Habit", "Friends",
    "After Food", "Tea", "Coffee", "Other",
]

MOOD_OPTIONS = [
    "Happy", "Neutral", "Stressed", "Anxious", "Bored", "Sad",
]


class AddEntryDialog:
    """
    Builds and manages the popup window for adding a detailed entry.

    on_saved is a function passed in from main.py — we call it after
    a successful save so the dashboard knows to refresh itself.
    """

    def __init__(self, parent, on_saved):
        self.on_saved = on_saved

        # Toplevel creates a new window, separate from the main one,
        # but parent tells Tkinter which window "owns" it.
        self.window = tk.Toplevel(parent)
        self.window.title("Add Entry")
        self.window.geometry("400x420")
        self.window.configure(bg=config.COLOR_BG)
        self.window.resizable(False, False)

        # Makes this popup "modal" — the user must deal with it
        # before clicking back on the main window.
        self.window.transient(parent)
        self.window.grab_set()

        self._build_form()

    def _build_form(self):
        title_label = ttk.Label(self.window, text="Log a Cigarette", style="Title.TLabel")
        title_label.pack(pady=(20, 15))

        # --- Trigger dropdown ---
        trigger_label = ttk.Label(self.window, text="Trigger", style="TLabel")
        trigger_label.pack(anchor="w", padx=30)

        self.trigger_var = tk.StringVar(value=TRIGGER_OPTIONS[0])
        trigger_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.trigger_var,
            values=TRIGGER_OPTIONS,
            state="readonly",  # user can only pick from the list, not type freely
        )
        trigger_dropdown.pack(fill="x", padx=30, pady=(0, 15))

        # --- Mood before dropdown ---
        mood_before_label = ttk.Label(self.window, text="Mood Before", style="TLabel")
        mood_before_label.pack(anchor="w", padx=30)

        self.mood_before_var = tk.StringVar(value=MOOD_OPTIONS[0])
        mood_before_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.mood_before_var,
            values=MOOD_OPTIONS,
            state="readonly",
        )
        mood_before_dropdown.pack(fill="x", padx=30, pady=(0, 15))

        # --- Mood after dropdown ---
        mood_after_label = ttk.Label(self.window, text="Mood After", style="TLabel")
        mood_after_label.pack(anchor="w", padx=30)

        self.mood_after_var = tk.StringVar(value=MOOD_OPTIONS[0])
        mood_after_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.mood_after_var,
            values=MOOD_OPTIONS,
            state="readonly",
        )
        mood_after_dropdown.pack(fill="x", padx=30, pady=(0, 15))

        # --- Note text box ---
        note_label = ttk.Label(self.window, text="Note (optional)", style="TLabel")
        note_label.pack(anchor="w", padx=30)

        # tk.Text, not ttk — ttk has no multi-line text widget.
        self.note_text = tk.Text(
            self.window,
            height=4,
            bg=config.COLOR_BG_SECONDARY,
            fg=config.COLOR_TEXT,
            insertbackground=config.COLOR_TEXT,  # cursor color
            relief="flat",
        )
        self.note_text.pack(fill="x", padx=30, pady=(0, 20))

        # --- Save button ---
        save_button = ttk.Button(
            self.window,
            text="Save Entry",
            style="Accent.TButton",
            command=self._on_save,
        )
        save_button.pack(pady=5)

    def _on_save(self):
        """
        Reads all form values, saves the entry via tracker.py,
        notifies main.py to refresh, then closes this popup.
        """
        trigger = self.trigger_var.get()
        mood_before = self.mood_before_var.get()
        mood_after = self.mood_after_var.get()

        # "1.0" means "line 1, character 0" — Tkinter's way of saying
        # "start of the text box." "end-1c" means "end, minus 1 character"
        # which strips the automatic trailing newline Tkinter adds.
        note = self.note_text.get("1.0", "end-1c").strip()

        tracker.add_entry(
            trigger=trigger,
            mood_before=mood_before,
            mood_after=mood_after,
            note=note if note else None,
        )

        self.on_saved()
        self.window.destroy()