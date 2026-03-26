#!/usr/bin/env python3
"""
Analyze the Course JSON from Integrations GCP bucket to determine
business on particular dates and weekdays.
"""

import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from sys import argv
from typing import Any

# Load the JSON courses file
file_path: str = argv[1] if len(argv) > 1 else ""
if not file_path:
    print("Usage: python analyze_courses.py <path_to_course_section_data.json>")
    exit(1)
if not Path(file_path).is_file():
    print(f"Error: File '{file_path}' not found.")
    exit(1)
with open(file_path) as f:
    courses = json.load(f)

# Dictionary to store active course count per day
daily_counts: dict[Any, int] = defaultdict(int)

# First pass: find the semester date range
# Initialize as datetime only to stop None.date() type warnings later
initial_date: datetime = datetime(1970, 1, 1)
semester_start: datetime = initial_date
semester_end: datetime = initial_date

for course in courses:
    start_date_str: str = course.get("start_date", "")
    end_date_str: str = course.get("end_date", "")

    if start_date_str and end_date_str:
        # Parse dates (format: "2026-05-18-07:00")
        start_date: datetime = datetime.strptime(start_date_str, "%Y-%m-%d-%H:%M")
        end_date: datetime = datetime.strptime(end_date_str, "%Y-%m-%d-%H:%M")

        if semester_start is initial_date or start_date < semester_start:
            semester_start = start_date
        if semester_end is initial_date or end_date > semester_end:
            semester_end = end_date

# Second pass: count active courses per day
for course in courses:
    start_date_str: str = course.get("start_date", "")
    end_date_str: str = course.get("end_date", "")

    if start_date_str and end_date_str:
        # Parse dates
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d-%H:%M")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d-%H:%M")

        # Count this course for each day it runs
        current_date: datetime = start_date
        while current_date <= end_date:
            daily_counts[current_date.date()] += 1
            current_date += timedelta(days=1)

# Print results
width: int = 50
print(f"\n{'=' * width}")
print("AP Summer 2026 - Daily Active Course Count")
print(f"{'=' * width}\n")
print(f"{'Date':<12} {'Day':<10} {'Active Courses':<15}")
print(f"{'-' * width}")

total_day_courses = 0
max_courses = 0
peak_date: date = initial_date.date()

for day_date in sorted(daily_counts.keys()):
    day_name: str = day_date.strftime("%A")
    count: int = daily_counts[day_date]
    total_day_courses += count

    if count > max_courses:
        max_courses: int = count
        peak_date = day_date

    print(f"{str(day_date):<12} {day_name:<10} {count:<15}")

print(f"{'-' * width}")

# Analyze by day of week (from actual meeting schedule)
print("\nClass Sessions by Day of Week:")
print(f"{'-' * width}")
print(f"{'Day':<15} {'Total Sessions':<15}")
print(f"{'-' * width}")

meeting_day_counts: dict[str, int] = defaultdict(int)
day_abbreviation_map: dict[str, str] = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday",
}
day_order: list[str] = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

for course in courses:
    meetings: list[dict] = course.get("meetings", [])
    for meeting in meetings:
        meeting_day_abbr: str = meeting.get("meeting_day", "")
        # Handle multi-day meetings like "Mon/Wed/Fri"
        for day_abbr in meeting_day_abbr.split("/"):
            day_abbr: str = day_abbr.strip()
            if day_abbr in day_abbreviation_map:
                meeting_day_counts[day_abbreviation_map[day_abbr]] += 1

for day in day_order:
    if day in meeting_day_counts:
        print(f"{day:<15} {meeting_day_counts[day]:<15}")

print(f"{'-' * width}")
print("\nSemester Statistics:")
print(f"  Start Date: {semester_start.date()}")
print(f"  End Date: {semester_end.date()}")
print(f"  Total Days: {len(daily_counts)}")
print(f"  Peak Day: {peak_date} ({peak_date.strftime('%A')}) {max_courses} courses")
print(f"  Total Course-Days: {total_day_courses}")
print(f"  Average Courses/Day: {total_day_courses / len(daily_counts):.1f}")
print(f"\nTotal Courses: {len(courses)}\n")
