"""
config.py

This file holds all the constant, unchanging settings for the entire app:
file paths, colors, fonts, and default values.

RULE: No other file should hardcode a file path or a color code.
Every other file imports what it needs from here.
This means if we ever move the database or change the theme color,
we change it in exactly ONE place.
"""

import os

# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# FOLDER PATHS
# ---------------------------------------------------------
DATABASE_DIR = os.path.join(BASE_DIR, "database")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")

# ---------------------------------------------------------
# DATABASE FILE
# ---------------------------------------------------------
DATABASE_FILE = os.path.join(DATABASE_DIR, "smoking_tracker.db")
SETTINGS_FILE = os.path.join(DATABASE_DIR, "settings.json")

# ---------------------------------------------------------
# APP INFO
# ---------------------------------------------------------
APP_NAME = "Smoking Tracker"
APP_VERSION = "0.1.0"

# ---------------------------------------------------------
# WINDOW SETTINGS
# ---------------------------------------------------------
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 500

# ---------------------------------------------------------
# COLOR THEME (Dark mode)
# ---------------------------------------------------------
COLOR_BG = "#1e1e2e"
COLOR_BG_SECONDARY = "#282838"
COLOR_TEXT = "#ffffff"
COLOR_TEXT_MUTED = "#a0a0b0"
COLOR_ACCENT = "#f38ba8"
COLOR_SUCCESS = "#a6e3a1"
COLOR_WARNING = "#f9e2af"
COLOR_DANGER = "#eb6f92"

# ---------------------------------------------------------
# DEFAULT USER SETTINGS
# ---------------------------------------------------------
DEFAULT_DAILY_LIMIT = 10
DEFAULT_PRICE_PER_CIGARETTE = 15.0
DEFAULT_CURRENCY_SYMBOL = "₹"

# ---------------------------------------------------------
# ENSURE REQUIRED FOLDERS EXIST
# ---------------------------------------------------------
def ensure_folders_exist():
    folders = [DATABASE_DIR, BACKUP_DIR, REPORTS_DIR, LOGS_DIR, ICONS_DIR]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# ---------------------------------------------------------
# NOTIFICATION SCHEDULING (in milliseconds, since Tkinter's
# .after() method expects milliseconds, not seconds)
# ---------------------------------------------------------
LIMIT_CHECK_INTERVAL_MS = 30 * 60 * 1000       # check limit every 30 minutes
MOTIVATIONAL_INTERVAL_MS = 3 * 60 * 60 * 1000  # motivational nudge every 3 hours
WATER_REMINDER_INTERVAL_MS = 2 * 60 * 60 * 1000  # water reminder every 2 hours