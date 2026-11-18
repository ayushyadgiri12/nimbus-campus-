# Column Dictionary — Timetable CSV

This document defines every column in `data/timetable.csv`.
All values are **fictional** and generated for demonstration purposes only.

## CSV Schema

| Column | Type | Required | Description | Example |
|--------|------|----------|-------------|---------|
| `batch` | string | Yes | Student batch identifier. Format: `<DEPT><YEAR><SECTION>` | `CS2024A` |
| `day` | string | Yes | Day of the week. Must be `Monday`–`Friday` (capitalized). | `Monday` |
| `period` | integer | Yes | Period number within the day. Range: 1–4. | `1` |
| `subject` | string | Yes | Full subject name as it appears in the syllabus. | `Data Structures` |
| `room` | string | Yes | Room/lab code. Prefix: `LH` = Lecture Hall, `CL` = Computer Lab, `EL` = Electronics Lab, `SEMHALL` = Seminar Hall, `LIBRARY` = Library. | `LH-101` |
| `teacher` | string | Yes* | Faculty name. May be empty for self-study rows. Format: `Prof.` or `Dr.` prefix. | `Dr. Priya Menon` |
| `start_time` | string | Yes | Period start time in 24-hour `HH:MM` format. | `09:00` |
| `end_time` | string | Yes | Period end time in 24-hour `HH:MM` format. | `10:00` |
| `type` | string | Yes | Session type. One of: `Lecture`, `Lab`, `Seminar`, `Self-Study`. | `Lecture` |

## Batch Codes Present in CSV

| Batch | Department | Year | Section |
|-------|-----------|------|---------|
| `CS2024A` | Computer Science | 2024 | A |
| `CS2024B` | Computer Science | 2024 | B |
| `EC2024A` | Electronics & Communication | 2024 | A |

## Notes

- `teacher` is intentionally blank for Self-Study rows; this is **not** an error.
- `HOD` appears as teacher for Seminar rows — this indicates the Head of Department chairs the session.
- Room codes are fictional and do not correspond to any real institution.
