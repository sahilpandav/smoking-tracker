import tkinter as tk
from tkinter import ttk

import config
import database


class SmokingTrackerApp:
    """
    Main application class. Holds the window and will hold
    all the widgets we add in future steps.
    """

    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._setup_style()
        self._build_placeholder_ui()

    def _setup_window(self):
        """Configures the main window: title, size, background color."""
        self.root.title(config.APP_NAME)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.root.configure(bg=config.COLOR_BG)

    def _setup_style(self):
        """
        Configures the ttk theme so our widgets match the dark color
        scheme defined in config.py, instead of using ttk's defaults.
        """
        style = ttk.Style(self.root)
        style.theme_use("clam")  # 'clam' is a ttk built-in theme that allows custom colors

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

    def _build_placeholder_ui(self):
        """
        Temporary UI just to prove the window works and the database
        is reachable. This gets replaced by the real dashboard soon.
        """
        title_label = ttk.Label(
            self.root,
            text=config.APP_NAME,
            style="Title.TLabel",
        )
        title_label.pack(pady=30)

        status_label = ttk.Label(
            self.root,
            text="Database connected. Dashboard coming in the next step.",
            style="TLabel",
        )
        status_label.pack()


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