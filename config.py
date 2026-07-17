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
import sys

if getattr(sys, "frozen", False):
    # Running as a PyInstaller-built .exe — use the folder the .exe
    # itself lives in, not the temporary extraction folder.
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running normally as a .py script (what we've been doing this whole time)
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
# COLOR THEME
# A calm, health-focused dark palette — deliberately not the
# common purple/pink "AI dark mode" look. Built around one
# grounded green accent (growth/progress), used sparingly.
# ---------------------------------------------------------
COLOR_BG = "#0F1512"            # near-black, slight green undertone
COLOR_BG_SECONDARY = "#1A2420"  # cards/panels, one step lighter than bg
COLOR_SIDEBAR = "#131A16"       # sidebar — sits between bg and card in value
COLOR_TEXT = "#EDEEE9"          # warm off-white, not pure white
COLOR_TEXT_MUTED = "#8A9591"    # muted sage-grey for secondary text
COLOR_ACCENT = "#4FB477"        # the ONE accent — grounded green
COLOR_ACCENT_DIM = "#2E4038"    # accent's low-opacity equivalent, for subtle fills
COLOR_SUCCESS = "#4FB477"       # same as accent — success IS the brand color here
COLOR_WARNING = "#D97A56"       # warm amber-orange
COLOR_DANGER = "#C15B4F"        # muted brick red, not neon — informational, not alarming
COLOR_BORDER = "#243029"        # subtle hairline borders/dividers

# ---------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------
SIDEBAR_WIDTH = 190

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