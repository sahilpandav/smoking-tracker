"""
Sends desktop notifications using plyer, which works across
Windows/Mac/Linux without OS-specific code.

RULE: This is the only file that calls plyer directly. Other files
call these functions instead of importing plyer themselves.
"""

from plyer import notification

import config


def send_notification(title, message):
    """
    Shows a desktop notification with the given title and message.
    Wrapped in try/except because notification support can be
    flaky across different systems — a failed notification should
    never crash the whole app.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name=config.APP_NAME,
            timeout=10,  # seconds the notification stays visible
        )
    except Exception as error:
        # We deliberately don't crash the app over a notification failure —
        # this is printed so you can see it during testing, but a real
        # user wouldn't be interrupted by it.
        print(f"Notification failed: {error}")


def notify_daily_reminder():
    """A general daily check-in reminder."""
    send_notification(
        f"{config.APP_NAME}",
        "Don't forget to log your entries today. Every log helps you understand your habit.",
    )


def notify_limit_warning(today_count, daily_limit):
    """Sent when the user is close to or has exceeded their daily limit."""
    if today_count >= daily_limit:
        send_notification(
            "Daily Limit Reached",
            f"You've hit your limit of {daily_limit} today. Consider taking a break.",
        )
    else:
        remaining = daily_limit - today_count
        send_notification(
            "Approaching Your Limit",
            f"You have {remaining} left before hitting today's limit of {daily_limit}.",
        )


def notify_motivational():
    """A random-feeling motivational nudge (static list for now)."""
    import random

    messages = [
        "Every cigarette you don't smoke is a win. Keep going.",
        "Your lungs start healing within hours of your last cigarette.",
        "Small reductions add up to big changes over time.",
        "You're building a healthier future, one day at a time.",
    ]
    send_notification(f"{config.APP_NAME}", random.choice(messages))


def notify_water_reminder():
    """Simple health-habit nudge, from your original feature list."""
    send_notification(f"{config.APP_NAME}", "Time for a glass of water — stay hydrated.")


def notify_breathing_reminder():
    """Simple breathing-exercise nudge, from your original feature list."""
    send_notification(
        f"{config.APP_NAME}",
        "Take a moment for a short breathing exercise: in for 4, hold for 4, out for 4.",
    )