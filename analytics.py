"""
This file calculates everything the dashboard needs to display:
counts, money spent, streaks, averages.

It reads data via database.py, but never modifies data — that's
tracker.py's job. analytics.py only looks at data and does math on it.
"""

import datetime
import database
import config
import settings


def _get_all_rows():
    """
    Internal helper (the underscore prefix means "not meant to be
    called from outside this file") that fetches every entry as
    raw rows, oldest first — easier to reason about for calculations
    than tracker.py's newest-first ordering.
    """
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT date, time FROM entries ORDER BY date ASC, time ASC")
    rows = cursor.fetchall()
    connection.close()
    return rows


def count_today():
    """Counts how many cigarettes were logged today."""
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    rows = _get_all_rows()
    return sum(1 for date, time in rows if date == today_str)


def count_yesterday():
    """Counts how many cigarettes were logged yesterday."""
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    rows = _get_all_rows()
    return sum(1 for date, time in rows if date == yesterday_str)


def count_this_week():
    """
    Counts cigarettes from the last 7 days, including today.
    """
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=6)  # 6 days back + today = 7 days
    rows = _get_all_rows()

    count = 0
    for date_str, time_str in rows:
        entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if week_ago <= entry_date <= today:
            count += 1
    return count


def count_this_month():
    """Counts cigarettes logged in the current calendar month."""
    today = datetime.date.today()
    rows = _get_all_rows()

    count = 0
    for date_str, time_str in rows:
        entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if entry_date.year == today.year and entry_date.month == today.month:
            count += 1
    return count


def count_lifetime():
    """Total number of cigarettes ever logged."""
    rows = _get_all_rows()
    return len(rows)


def current_streak_days():
    """
    Calculates the current smoke-free streak in whole days,
    counting backward from today until it finds a day with an entry.

    Example: if today and yesterday have zero entries, but the day
    before has entries, the streak is 2 days.
    """
    rows = _get_all_rows()
    smoked_dates = set(date for date, time in rows)  # unique dates only

    streak = 0
    check_date = datetime.date.today()

    while True:
        check_str = check_date.strftime("%Y-%m-%d")
        if check_str in smoked_dates:
            break
        streak += 1
        check_date -= datetime.timedelta(days=1)

        # Safety limit: stop after 10 years to avoid an infinite loop
        # if the database is completely empty.
        if streak > 3650:
            break

    return streak


def money_spent_today():
    """Money spent today, based on the current price-per-cigarette setting."""
    price = settings.load_settings()["price_per_cigarette"]
    return count_today() * price


def money_spent_this_week():
    """Money spent in the last 7 days."""
    price = settings.load_settings()["price_per_cigarette"]
    return count_this_week() * price


def money_spent_this_month():
    """Money spent in the current calendar month."""
    price = settings.load_settings()["price_per_cigarette"]
    return count_this_month() * price


def money_spent_lifetime():
    """Total money spent across all logged entries."""
    price = settings.load_settings()["price_per_cigarette"]
    return count_lifetime() * price


def average_per_day():
    """
    Average cigarettes per day, across every day that has at least
    one entry (not counting smoke-free days as zeros, since that
    would need every calendar day tracked — good enough approximation
    for now, can be refined later).
    """
    rows = _get_all_rows()
    if not rows:
        return 0

    unique_days = set(date for date, time in rows)
    return len(rows) / len(unique_days)


def daily_limit_progress():
    """
    Returns (today_count, daily_limit, percentage) so the dashboard
    can show a progress bar. Percentage is capped at 100 even if
    the user has exceeded their limit, so the bar doesn't overflow.
    """
    today_count = count_today()
    daily_limit = settings.load_settings()["daily_limit"]

    if daily_limit <= 0:
        percentage = 0  # avoid dividing by zero if limit is somehow 0
    else:
        percentage = min(100, int((today_count / daily_limit) * 100))

    return today_count, daily_limit, percentage