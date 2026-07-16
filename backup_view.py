"""
A popup window for creating manual backups, viewing existing
backups, and restoring from one.

Opened from main.py via a "Backup" button.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import config
import backup


class BackupDialog:
    """Builds and manages the backup/restore popup window."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Backup & Restore")
        self.window.geometry("550x400")
        self.window.configure(bg=config.COLOR_BG)

        self.window.transient(parent)
        self.window.grab_set()

        self._build_create_button()
        self._build_list()
        self.load_backups()

    def _build_create_button(self):
        create_button = ttk.Button(
            self.window,
            text="Create Backup Now",
            style="Accent.TButton",
            command=self.on_create_backup,
        )
        create_button.pack(pady=15)

    def _build_list(self):
        """Table listing every existing backup, with restore action."""
        columns = ("filename", "modified")

        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        self.tree.heading("filename", text="Backup File")
        self.tree.heading("modified", text="Created")
        self.tree.column("filename", width=280, anchor="w")
        self.tree.column("modified", width=180, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        restore_button = ttk.Button(
            self.window,
            text="Restore Selected Backup",
            style="Accent.TButton",
            command=self.on_restore_selected,
        )
        restore_button.pack(pady=(0, 15))

    def load_backups(self):
        """Clears and reloads the backup list from disk."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for filename, full_path, modified_datetime in backup.list_backups():
            display_time = modified_datetime.strftime("%b %d, %Y — %I:%M %p")
            self.tree.insert("", "end", iid=full_path, values=(filename, display_time))

    def on_create_backup(self):
        """Creates a new manual backup and refreshes the list."""
        try:
            backup.create_backup()
            self.load_backups()
            messagebox.showinfo("Backup Created", "A new backup was saved successfully.")
        except FileNotFoundError as error:
            messagebox.showerror("Backup Failed", str(error))

    def on_restore_selected(self):
        """Restores whichever backup is selected, after confirmation."""
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo("No Selection", "Please select a backup to restore first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Restore",
            "This will replace your current data with this backup.\n"
            "Your current data will be backed up first, just in case.\n\n"
            "Continue?",
        )
        if not confirm:
            return

        backup_path = selected[0]  # the iid we set was the full file path
        backup.restore_backup(backup_path)

        messagebox.showinfo(
            "Restore Complete",
            "Backup restored. Please restart the app to see the restored data.",
        )
        self.window.destroy()