"""
This file contains the core logic for logging cigarette entries:
adding, editing, deleting, and fetching them.

It talks to database.py for actual storage — it never writes
raw SQL itself. This keeps a clean separation:
    tracker.py  = "what the app is allowed to do"
    database.py = "how that gets saved"
"""

import datetime
import database


def add_entry(trigger=None, mood_before=None, mood_after=None, note=None):
    """
    Adds a new cigarette entry using the current date and time.

    All parameters are optional (default None) since the feature list
    says trigger/mood/note are optional per entry.
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")   # e.g. "2026-07-11"
    time_str = now.strftime("%H:%M:%S")   # e.g. "14:32:07"

    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO entries (date, time, trigger, mood_before, mood_after, note)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_str, time_str, trigger, mood_before, mood_after, note))

    connection.commit()
    connection.close()


def get_all_entries():
    """
    Returns every entry in the database, most recent first.
    Each entry comes back as a tuple:
    (id, date, time, trigger, mood_before, mood_after, note)
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, time, trigger, mood_before, mood_after, note
        FROM entries
        ORDER BY date DESC, time DESC
    """)

    rows = cursor.fetchall()
    connection.close()
    return rows


def delete_last_entry():
    """
    Deletes the single most recently added entry.
    Used for the "Remove last cigarette" feature (undo-style).
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM entries
        WHERE id = (SELECT MAX(id) FROM entries)
    """)

    connection.commit()
    connection.close()


def delete_entry_by_id(entry_id):
    """
    Deletes one specific entry, identified by its unique id.
    """
    connection = database.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))

    connection.commit()
    connection.close()