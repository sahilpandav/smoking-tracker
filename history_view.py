"""
A popup window showing every logged entry in a scrollable table,
with the ability to delete individual entries.

Opened from main.py via a "History" button.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import config
import tracker

from entry_dialog import AddEntryDialog


class HistoryDialog:
    """
    Builds and manages the entry history popup window.

    on_changed is called after a delete, so main.py can refresh
    the dashboard stats (since deleting an entry changes the counts).
    """

    def __init__(self, parent, on_changed):
        self.parent = parent
        self.on_changed = on_changed

        self.window = tk.Toplevel(parent)
        self.window.title("Entry History")
        self.window.geometry("700x450")
        self.window.configure(bg=config.COLOR_BG)

        self.window.transient(parent)
        self.window.grab_set()

        self._build_table()
        self._build_delete_button()
        self.load_entries()

    def _build_table(self):
        """Creates the Treeview table and its scrollbar."""
        columns = ("date", "time", "trigger", "mood_before", "mood_after", "note")

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",  # hides the default empty first "tree" column
            height=15,
        )

        # Column headers (what the user sees at the top)
        headers = {
            "date": "Date",
            "time": "Time",
            "trigger": "Trigger",
            "mood_before": "Mood Before",
            "mood_after": "Mood After",
            "note": "Note",
        }
        widths = {
            "date": 90, "time": 80, "trigger": 90,
            "mood_before": 100, "mood_after": 100, "note": 180,
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="w")

        self.tree.pack(fill="both", expand=True, padx=15, pady=(15, 5))
        self.tree.bind("<Double-1>", self.on_double_click_row)

        # Scrollbar linked to the tree's vertical view
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _build_delete_button(self):
        button_row = tk.Frame(self.window, bg=config.COLOR_BG)
        button_row.pack(pady=10)

        edit_button = ttk.Button(
            button_row,
            text="Edit Selected Entry",
            style="Accent.TButton",
            command=self.on_edit_selected,
        )
        edit_button.grid(row=0, column=0, padx=5)

        delete_button = ttk.Button(
            button_row,
            text="Delete Selected Entry",
            style="Accent.TButton",
            command=self.on_delete_selected,
        )
        delete_button.grid(row=0, column=1, padx=5)

    def on_double_click_row(self, event):
        """Double-clicking a row opens it for editing, as a shortcut."""
        self.on_edit_selected()

    def on_edit_selected(self):
        """Opens the edit popup for whichever row is currently selected."""
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo("No Selection", "Please select an entry to edit first.")
            return

        entry_id = int(selected[0])
        AddEntryDialog(self.parent, on_saved=self._on_edit_saved, entry_id=entry_id)

    def _on_edit_saved(self):
        """
        Called after an edit is saved. Refreshes this history table
        AND tells main.py's dashboard to refresh too (edited mood/
        trigger could matter for future stats/charts).
        """
        self.load_entries()
        self.on_changed()

    def load_entries(self):
        """
        Clears the table and reloads every entry fresh from the
        database via tracker.py. Called on open, and again after
        any delete.
        """
        # Remove all existing rows before reloading
        for row in self.tree.get_children():
            self.tree.delete(row)

        entries = tracker.get_all_entries()
        # Each entry is: (id, date, time, trigger, mood_before, mood_after, note)
        for entry in entries:
            entry_id, date, time, trigger, mood_before, mood_after, note = entry
            self.tree.insert(
                "",              # "" means insert at the top level, no parent row
                "end",           # insert at the end of the current list
                iid=str(entry_id),  # iid = unique row identifier, we use the DB id
                values=(date, time, trigger or "-", mood_before or "-", mood_after or "-", note or "-"),
            )

    def on_delete_selected(self):
        """
        Deletes whichever row is currently selected in the table.
        Asks for confirmation first, per the "confirmation before
        deleting" feature from the requirements.
        """
        selected = self.tree.selection()  # returns a tuple of selected row iids

        if not selected:
            messagebox.showinfo("No Selection", "Please select an entry to delete first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this entry? This cannot be undone.",
        )
        if not confirm:
            return

        entry_id = int(selected[0])  # the iid we set earlier was the entry's real id
        tracker.delete_entry_by_id(entry_id)

        self.load_entries()
        self.on_changed()