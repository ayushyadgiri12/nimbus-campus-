#!/usr/bin/env python3
# Compatible with Python 3.9+
"""
lookup_timetable.py — Deterministic timetable lookup for the
timetable-helper Skill (Nimbus Labs Campus Helpdesk Agent).

Usage:
  python lookup_timetable.py --batch CS2024A --day Monday
  python lookup_timetable.py --batch CS2024A --subject "Data Structures"
  python lookup_timetable.py --batch CS2024A --day Monday --period 1

All data is fictional and from data/timetable.csv only.
This script will NEVER fabricate information.
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VALID_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
VALID_PERIODS = [1, 2, 3, 4]

# Locate the CSV relative to this script's position in the repo
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent  # skills/timetable-helper/scripts -> repo root
CSV_PATH = _REPO_ROOT / "data" / "timetable.csv"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_timetable(csv_path: Path) -> list[dict]:
    """Load timetable CSV into a list of row dicts."""
    if not csv_path.exists():
        print(f"ERROR: Timetable CSV not found at: {csv_path}", file=sys.stderr)
        sys.exit(1)
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def normalise_day(day: str) -> str:
    """Normalise day string to Title Case and validate."""
    normed = day.strip().title()
    if normed not in VALID_DAYS:
        print(
            f"ERROR: '{day}' is not a valid weekday. "
            f"Use one of: {', '.join(VALID_DAYS)}",
            file=sys.stderr,
        )
        sys.exit(1)
    return normed


def normalise_batch(batch: str) -> str:
    """Normalise batch code to uppercase."""
    return batch.strip().upper()


def validate_period(period_str: str) -> int:
    """Parse and validate the period number."""
    try:
        period = int(period_str)
    except ValueError:
        print(f"ERROR: Period must be an integer, got '{period_str}'.", file=sys.stderr)
        sys.exit(1)
    if period not in VALID_PERIODS:
        print(
            f"ERROR: Period must be between 1 and 4, got {period}.",
            file=sys.stderr,
        )
        sys.exit(1)
    return period


# ---------------------------------------------------------------------------
# Query functions
# ---------------------------------------------------------------------------

def get_schedule_for_batch_day(rows: list[dict], batch: str, day: str) -> list[dict]:
    """Return all periods for a given batch and day, sorted by period."""
    matches = [
        r for r in rows
        if r["batch"] == batch and r["day"] == day
    ]
    return sorted(matches, key=lambda r: int(r["period"]))


def get_schedule_for_batch_subject(rows: list[dict], batch: str, subject: str) -> list[dict]:
    """Return all rows where subject matches (case-insensitive) for a batch."""
    subject_lower = subject.lower()
    return [
        r for r in rows
        if r["batch"] == batch and r["subject"].lower() == subject_lower
    ]


def get_period_detail(rows: list[dict], batch: str, day: str, period: int) -> Optional[dict]:
    """Return the single row for a specific batch, day, and period."""
    for r in rows:
        if r["batch"] == batch and r["day"] == day and int(r["period"]) == period:
            return r
    return None


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEPARATOR = "-" * 70


def format_row(row: dict) -> str:
    teacher = row["teacher"] if row["teacher"] else "(No teacher — Self-Study)"
    return (
        f"  Period {row['period']}: {row['subject']}\n"
        f"    Room:    {row['room']}\n"
        f"    Teacher: {teacher}\n"
        f"    Time:    {row['start_time']} – {row['end_time']}\n"
        f"    Type:    {row['type']}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Nimbus Labs Timetable Lookup — returns ONLY data present in the CSV."
    )
    parser.add_argument("--batch", required=True, help="Batch code, e.g. CS2024A")
    parser.add_argument("--day", help="Day of the week, e.g. Monday")
    parser.add_argument("--subject", help="Subject name, e.g. 'Data Structures'")
    parser.add_argument("--period", help="Period number (1-4)")
    args = parser.parse_args()

    # Load data
    rows = load_timetable(CSV_PATH)
    batch = normalise_batch(args.batch)

    # Check batch exists
    known_batches = sorted({r["batch"] for r in rows})
    if batch not in known_batches:
        print(
            f"ERROR: Batch '{batch}' not found in timetable.\n"
            f"Available batches: {', '.join(known_batches)}",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Query: batch + day + period ---
    if args.day and args.period:
        day = normalise_day(args.day)
        period = validate_period(args.period)
        result = get_period_detail(rows, batch, day, period)
        if result is None:
            print(f"No data found for batch={batch}, day={day}, period={period}.")
            sys.exit(0)
        print(SEPARATOR)
        print(f"Schedule: {batch} | {day} | Period {period}")
        print(SEPARATOR)
        print(format_row(result))
        print(SEPARATOR)
        return

    # --- Query: batch + day ---
    if args.day and not args.subject:
        day = normalise_day(args.day)
        results = get_schedule_for_batch_day(rows, batch, day)
        if not results:
            print(
                f"No schedule found for batch '{batch}' on {day}.\n"
                "This batch may not have classes on this day."
            )
            sys.exit(0)
        print(SEPARATOR)
        print(f"Schedule: {batch} | {day}")
        print(SEPARATOR)
        for row in results:
            print(format_row(row))
            print()
        print(SEPARATOR)
        return

    # --- Query: batch + subject ---
    if args.subject:
        results = get_schedule_for_batch_subject(rows, batch, args.subject)
        if not results:
            print(
                f"Subject '{args.subject}' was not found for batch '{batch}'.\n"
                "I will not fabricate information. Check the subject name and batch code."
            )
            sys.exit(0)
        print(SEPARATOR)
        print(f"Schedule: {batch} | Subject: {args.subject}")
        print(SEPARATOR)
        for row in results:
            print(f"  {row['day']}:")
            print(format_row(row))
            print()
        print(SEPARATOR)
        return

    # --- Fallback: show full batch schedule ---
    all_rows = [r for r in rows if r["batch"] == batch]
    if not all_rows:
        print(f"No data found for batch '{batch}'.")
        sys.exit(0)
    print(SEPARATOR)
    print(f"Full Schedule: {batch}")
    print(SEPARATOR)
    for day in VALID_DAYS:
        day_rows = [r for r in all_rows if r["day"] == day]
        if day_rows:
            print(f"\n{day}:")
            for row in sorted(day_rows, key=lambda r: int(r["period"])):
                print(format_row(row))
                print()
    print(SEPARATOR)


if __name__ == "__main__":
    main()
