# Smoking Tracker

A personal desktop app to log, track, and gradually reduce smoking — built with Python, Tkinter, and SQLite.

This is a practice project focused on learning real backend/application architecture: clean separation between data storage, business logic, and GUI, rather than one large script.

## Features

- **Dashboard** — live daily/weekly/monthly/lifetime stats, plus a circular progress ring showing today's count against your daily limit
- **Detailed logging** — record trigger, mood before/after, and notes for each entry
- **History** — view, edit, and delete past entries
- **Charts** — 14-day trend line and trigger breakdown (pie chart)
- **Settings** — editable daily limit, price per cigarette, and currency, all persisted and live-affecting stats
- **Reports** — export your data as CSV or a formatted PDF summary
- **Backup & restore** — manual backups with a safety net before any restore
- **Notifications** — automatic desktop reminders (daily limit warnings, motivational nudges, water reminders) on independent schedules

## Project structure

SmokingTracker/
├── main.py              # Entry point — builds and runs the GUI
├── config.py             # App-wide constants: paths, colors, defaults
├── database.py            # SQLite connection and schema
├── tracker.py             # Add/edit/delete/fetch entries
├── analytics.py            # Stats and calculations (streaks, money, limits)
├── settings.py             # User settings persistence (JSON)
├── notifications.py          # Desktop notifications (plyer)
├── reports.py              # CSV/PDF export (reportlab)
├── backup.py               # Database backup/restore
├── entry_dialog.py           # Add/Edit entry popup
├── history_view.py           # Entry history table popup
├── charts_view.py            # Charts popup (matplotlib)
├── settings_view.py           # Settings popup
├── backup_view.py            # Backup/restore popup
├── requirements.txt
├── database/              # SQLite .db file + settings.json (not tracked in git)
├── backups/               # Backup .db copies (not tracked in git)
├── reports/                # Generated CSV/PDF exports (not tracked in git)
└── logs/


## Setup

1. Clone the repo:
git clone https://github.com/sahilpandav/smoking-tracker.git
cd smoking-tracker

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
python main.py

The first run automatically creates the required folders and an empty database — no manual setup needed beyond the steps above.

## Architecture notes

- `database.py` is the only file that talks to SQLite directly. Other files call its functions rather than writing their own SQL.
- `settings.py` is the only file that reads/writes `settings.json` directly, following the same pattern.
- All colors, paths, and app-wide constants live in `config.py` — no other file hardcodes them.
- Business logic (`tracker.py`, `analytics.py`) is fully separate from the GUI — the GUI calls these functions but contains no calculations or SQL of its own.

## Status

Built incrementally, file by file, as a learning project. Core features are complete; this remains a practice project rather than a polished/distributed release.
