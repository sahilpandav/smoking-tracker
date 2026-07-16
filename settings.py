"""
Handles loading and saving user-editable settings (daily limit,
price per cigarette, currency symbol) to a JSON file.

RULE: This is the only file that reads/writes settings.json directly.
Other files call get_settings() / update_setting() instead of
touching the file themselves — same pattern as database.py.
"""

import json
import os
import config


# Fallback values used only if settings.json doesn't exist yet
# (e.g. first time the app ever runs).
DEFAULT_SETTINGS = {
    "daily_limit": config.DEFAULT_DAILY_LIMIT,
    "price_per_cigarette": config.DEFAULT_PRICE_PER_CIGARETTE,
    "currency_symbol": config.DEFAULT_CURRENCY_SYMBOL,
}


def load_settings():
    """
    Reads settings.json and returns it as a dictionary.
    If the file doesn't exist yet, creates it with defaults first.
    """
    if not os.path.exists(config.SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(config.SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings_dict):
    """
    Writes the given dictionary to settings.json, fully replacing
    whatever was there before.
    """
    with open(config.SETTINGS_FILE, "w") as file:
        json.dump(settings_dict, file, indent=4)


def update_setting(key, value):
    """
    Updates a single setting (e.g. update_setting('daily_limit', 5))
    without needing to know or touch the other settings.
    """
    current = load_settings()
    current[key] = value
    save_settings(current)