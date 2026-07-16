"""
Handles copying the database file to backups/ (manual or automatic),
listing existing backups, and restoring from one.

RULE: This is the only file that copies/restores the .db file directly.
main.py calls these functions rather than using shutil itself.
"""

import os
import shutil
import datetime

import config


def _generate_backup_filename():
    """
    Builds a timestamped backup filename, e.g.
    'smoking_tracker_backup_2026-07-16_1845.db'
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"smoking_tracker_backup_{timestamp}.db"


def create_backup():
    """
    Copies the current database file into backups/ with a timestamped
    name. Returns the full path of the new backup file.
    """
    if not os.path.exists(config.DATABASE_FILE):
        raise FileNotFoundError("No database file exists yet to back up.")

    filename = _generate_backup_filename()
    backup_path = os.path.join(config.BACKUP_DIR, filename)

    shutil.copy2(config.DATABASE_FILE, backup_path)
    return backup_path


def list_backups():
    """
    Returns a list of every backup file in backups/, most recent first.
    Each item is a tuple: (filename, full_path, modified_datetime)
    """
    if not os.path.exists(config.BACKUP_DIR):
        return []

    backups = []
    for filename in os.listdir(config.BACKUP_DIR):
        if filename.endswith(".db"):
            full_path = os.path.join(config.BACKUP_DIR, filename)
            modified_timestamp = os.path.getmtime(full_path)
            modified_datetime = datetime.datetime.fromtimestamp(modified_timestamp)
            backups.append((filename, full_path, modified_datetime))

    # Sort newest first, using the actual file modification time
    backups.sort(key=lambda item: item[2], reverse=True)
    return backups


def restore_backup(backup_path):
    """
    Replaces the current database with the chosen backup file.
    The current database is safety-backed-up first, in case the
    restore was a mistake.
    """
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup file not found: {backup_path}")

    # Safety net: back up whatever is currently active before overwriting it
    if os.path.exists(config.DATABASE_FILE):
        create_backup()

    shutil.copy2(backup_path, config.DATABASE_FILE)