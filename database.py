"""
This is the ONLY file that talks directly to SQLite.
Every other file (tracker.py, analytics.py, etc.) calls functions
from here instead of writing raw SQL themselves.

Why this matters: if we ever rename a column or change how data
is stored, we only fix it in this one file.
"""

import sqlite3
import config


def get_connection():
    """
    Opens and returns a connection to the SQLite database file.
    The path comes from config.py, never hardcoded here.
    """
    connection = sqlite3.connect(config.DATABASE_FILE)
    return connection


def initialize_database():
    """
    Creates the 'entries' table if it doesn't already exist.
    Safe to call every time the app starts — CREATE TABLE IF NOT EXISTS
    does nothing if the table is already there.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            trigger TEXT,
            mood_before TEXT,
            mood_after TEXT,
            note TEXT
        )
    """)

    connection.commit()
    connection.close()