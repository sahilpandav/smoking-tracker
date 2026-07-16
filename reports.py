"""
Generates exportable reports from your logged data:
- CSV export (raw entries, opens in Excel/Sheets)
- PDF export (formatted summary report)

Files are saved into the reports/ folder (path from config.py).
"""

import csv
import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import config
import tracker
import analytics


def _generate_filename(extension):
    """
    Builds a timestamped filename so repeated exports never
    overwrite each other, e.g. 'smoking_report_2026-07-16_1830.csv'
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"smoking_report_{timestamp}.{extension}"


def export_csv():
    """
    Writes every logged entry into a CSV file inside reports/.
    Returns the full file path, so the GUI can tell the user
    exactly where it was saved.
    """
    filename = _generate_filename("csv")
    filepath = config.REPORTS_DIR + "\\" + filename  # Windows path join, matches config.py's style

    entries = tracker.get_all_entries()

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Time", "Trigger", "Mood Before", "Mood After", "Note"])
        for entry in entries:
            writer.writerow(entry)

    return filepath


def export_pdf():
    """
    Builds a formatted PDF summary report: key stats up top,
    followed by a table of every entry. Returns the file path.
    """
    filename = _generate_filename("pdf")
    filepath = config.REPORTS_DIR + "\\" + filename

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # --- Title ---
    elements.append(Paragraph(f"{config.APP_NAME} — Report", styles["Title"]))
    elements.append(Paragraph(
        f"Generated on {datetime.date.today().strftime('%B %d, %Y')}",
        styles["Normal"],
    ))
    elements.append(Spacer(1, 20))

    # --- Summary stats section ---
    elements.append(Paragraph("Summary", styles["Heading2"]))

    summary_data = [
        ["Metric", "Value"],
        ["Today", str(analytics.count_today())],
        ["This Week", str(analytics.count_this_week())],
        ["This Month", str(analytics.count_this_month())],
        ["Lifetime", str(analytics.count_lifetime())],
        ["Current Streak", f"{analytics.current_streak_days()} days"],
        ["Average per Day", f"{analytics.average_per_day():.1f}"],
        ["Money Spent (Lifetime)", f"{config.DEFAULT_CURRENCY_SYMBOL}{analytics.money_spent_lifetime():.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[8 * cm, 8 * cm])
    summary_table.setStyle(_get_table_style())
    elements.append(summary_table)
    elements.append(Spacer(1, 25))

    # --- Full entry log section ---
    elements.append(Paragraph("Entry Log", styles["Heading2"]))

    entries = tracker.get_all_entries()
    entry_data = [["Date", "Time", "Trigger", "Mood Before", "Mood After", "Note"]]
    for entry in entries:
        _id, date, time, trigger, mood_before, mood_after, note = entry
        entry_data.append([
            date, time, trigger or "-", mood_before or "-", mood_after or "-", note or "-",
        ])

    entry_table = Table(entry_data, colWidths=[2.3 * cm, 2 * cm, 2.5 * cm, 2.7 * cm, 2.7 * cm, 4 * cm])
    entry_table.setStyle(_get_table_style())
    elements.append(entry_table)

    doc.build(elements)
    return filepath


def _get_table_style():
    """
    Shared table styling so both tables in the PDF look consistent:
    dark header row, alternating readable borders, small readable font.
    """
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#282838")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])