---
name: timetable-helper
description: >
  Looks up class schedules, room allocations, teacher assignments and
  timetable details from the Nimbus Labs campus CSV database.
  Triggers when a user asks about classes, lecture times, lab schedules,
  room numbers, or teacher information for a specific batch or day.
  Do NOT fabricate any class, subject, room, teacher, or time that is
  not present in data/timetable.csv. Refuse politely if the requested
  entity does not exist in the data.
---

# Timetable Helper

A campus timetable lookup skill for Nimbus Labs. Answers questions about
class schedules using **only** data from `data/timetable.csv`.

## What This Skill Does

- Retrieves the schedule for a given **batch** and **day**
- Looks up **room allocations** for a subject or period
- Returns **teacher information** per subject
- Validates inputs and refuses to invent information

## When To Trigger

Trigger this skill when the user asks questions such as:
- "What classes does CS2024A have on Monday?"
- "Who teaches Data Structures?"
- "Which room is the Database Lab in?"
- "What time does the OS lecture start for CS2024A on Friday?"

Do **not** trigger for administrative fee queries, hostel rules, or
general information — those are handled by the MCP server tools.

## Usage

Call the lookup script:

```bash
python skills/timetable-helper/scripts/lookup_timetable.py \
  --batch CS2024A \
  --day Monday
```

Or query interactively:

```bash
python skills/timetable-helper/scripts/lookup_timetable.py \
  --subject "Data Structures" \
  --batch CS2024A
```

## Progressive Disclosure

**Level 1 — Quick answer:** Return only the requested field (time, room, teacher).

**Level 2 — Full period details:** Return all columns for the matching row(s).

**Level 3 — Conflict / multi-match:** List all matches and ask the user to
narrow the query.

## Fabrication Policy

> **Never invent data.** If a batch, day, subject, teacher, or room is not
> in `data/timetable.csv`, respond:
> "I could not find [X] in the timetable. Please check the batch code or
> day name and try again."

See `references/edge-cases.md` for a full list of error scenarios.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — skill instructions |
| `references/column-dictionary.md` | Column definitions for the CSV |
| `references/edge-cases.md` | Known edge cases and error handling |
| `scripts/lookup_timetable.py` | Deterministic lookup script |
| `../../data/timetable.csv` | Fictional timetable data |
