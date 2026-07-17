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
    Builds and manages the popup window for adding OR editing an entry.

    If entry_id is None, this creates a new entry (original behavior).
    If entry_id is provided, this loads and edits that existing entry.

    on_saved is a function passed in from main.py — we call it after
    a successful save so the dashboard knows to refresh itself.
    """

    def __init__(self, parent, on_saved, entry_id=None):
        self.on_saved = on_saved
        self.entry_id = entry_id  # None = adding new, otherwise = editing this id

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Entry" if entry_id else "Add Entry")
        self.window.geometry("400x420")
        self.window.configure(bg=config.COLOR_BG)
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self._build_form()

        # If editing, pre-fill the form with this entry's current values
        if self.entry_id is not None:
            self._load_existing_values()

    def _build_form(self):
        title_text = "Edit Entry" if self.entry_id else "Log a Cigarette"
        title_label = ttk.Label(self.window, text=title_text, style="Title.TLabel")
        title_label.pack(pady=(20, 15))

        # --- Trigger dropdown ---
        trigger_label = ttk.Label(self.window, text="Trigger", style="TLabel")
        trigger_label.pack(anchor="w", padx=30)

        self.trigger_var = tk.StringVar(value=TRIGGER_OPTIONS[0])
        trigger_dropdown = ttk.Combobox(
            self.window,
            textvariable=self.trigger_var,
            values=TRIGGER_OPTIONS,
            state="readonly",
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

        self.note_text = tk.Text(
            self.window,
            height=4,
            bg=config.COLOR_BG_SECONDARY,
            fg=config.COLOR_TEXT,
            insertbackground=config.COLOR_TEXT,
            relief="flat",
        )
        self.note_text.pack(fill="x", padx=30, pady=(0, 20))

        # --- Save button ---
        save_text = "Save Changes" if self.entry_id else "Save Entry"
        save_button = ttk.Button(
            self.window,
            text=save_text,
            style="Accent.TButton",
            command=self._on_save,
        )
        save_button.pack(pady=5)

    def _load_existing_values(self):
        """
        Fetches the existing entry's data and fills the form fields
        with it, so editing starts from the current values instead
        of blank defaults.
        """
        entry = tracker.get_entry_by_id(self.entry_id)
        if entry is None:
            return  # entry was deleted elsewhere; form just stays at defaults

        _id, date, time, trigger, mood_before, mood_after, note = entry

        if trigger:
            self.trigger_var.set(trigger)
        if mood_before:
            self.mood_before_var.set(mood_before)
        if mood_after:
            self.mood_after_var.set(mood_after)
        if note:
            self.note_text.insert("1.0", note)

    def _on_save(self):
        """
        Reads all form values, then either creates a new entry or
        updates the existing one, depending on whether entry_id
        was provided when this dialog was opened.
        """
        trigger = self.trigger_var.get()
        mood_before = self.mood_before_var.get()
        mood_after = self.mood_after_var.get()
        note = self.note_text.get("1.0", "end-1c").strip()
        note = note if note else None

        if self.entry_id is None:
            tracker.add_entry(
                trigger=trigger,
                mood_before=mood_before,
                mood_after=mood_after,
                note=note,
            )
        else:
            tracker.update_entry(
                self.entry_id,
                trigger=trigger,
                mood_before=mood_before,
                mood_after=mood_after,
                note=note,
            )

        self.on_saved()
        self.window.destroy()