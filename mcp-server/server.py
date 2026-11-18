#!/usr/bin/env python3
"""
server.py — Nimbus Labs Campus Helpdesk MCP Server

Built with the official modelcontextprotocol Python SDK (mcp == 2.3.0).
MCP protocol revision: 2024-11-05 (supported by mcp 2.x).
Uses stdio transport.

SDK migration note:
  mcp 2.x renamed FastMCP → MCPServer (mcp.server.mcpserver.MCPServer).
  The @tool, @resource, and .run() interfaces are identical.
  See: https://py.sdk.modelcontextprotocol.io/v2/migration/

Exposes:
  Tools:
    - get_timetable(batch, day)      -> schedule for a batch on a given day
    - get_fee_status(student_id)     -> mock fee status for a student

  Resources:
    - hostel://rules                 -> hostel rules text

IMPORTANT: All data is fictional / mock only.
Accepted student IDs: MOCK1001, MOCK1002, MOCK1003
No real student data, credentials, or API keys are used.
"""

import sys
from typing import Any

# mcp 2.x: FastMCP was renamed to MCPServer
from mcp.server.mcpserver import MCPServer

# ---------------------------------------------------------------------------
# Initialise the server
# ---------------------------------------------------------------------------
mcp = MCPServer(
    "campus-helpdesk",
    instructions=(
        "You are the Nimbus Labs Campus Helpdesk MCP server. "
        "You provide fictional timetable, fee status, and hostel rule data. "
        "Only accept student IDs: MOCK1001, MOCK1002, MOCK1003. "
        "Never invent real student data."
    ),
)

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_TIMETABLE: dict[str, dict[str, list[dict[str, str]]]] = {
    "CS2024A": {
        "Monday": [
            {"period": "1", "subject": "Data Structures",    "room": "LH-101", "teacher": "Dr. Priya Menon",    "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Operating Systems",  "room": "LH-101", "teacher": "Prof. Rahul Sharma", "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Mathematics III",    "room": "LH-203", "teacher": "Dr. Sunita Rao",     "start": "11:15", "end": "12:15", "type": "Lecture"},
            {"period": "4", "subject": "Data Structures Lab","room": "CL-01",  "teacher": "Dr. Priya Menon",    "start": "14:00", "end": "16:00", "type": "Lab"},
        ],
        "Tuesday": [
            {"period": "1", "subject": "Computer Networks",  "room": "LH-101", "teacher": "Dr. Anil Kumar",     "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Database Systems",   "room": "LH-205", "teacher": "Prof. Meena Joshi",  "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Operating Systems",  "room": "LH-101", "teacher": "Prof. Rahul Sharma", "start": "11:15", "end": "12:15", "type": "Lecture"},
            {"period": "4", "subject": "Mathematics III",    "room": "LH-203", "teacher": "Dr. Sunita Rao",     "start": "13:00", "end": "14:00", "type": "Lecture"},
        ],
        "Wednesday": [
            {"period": "1", "subject": "Data Structures",    "room": "LH-101", "teacher": "Dr. Priya Menon",    "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Computer Networks",  "room": "LH-101", "teacher": "Dr. Anil Kumar",     "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Database Systems Lab","room": "CL-02", "teacher": "Prof. Meena Joshi",  "start": "11:15", "end": "13:15", "type": "Lab"},
            {"period": "4", "subject": "Elective I",         "room": "LH-301", "teacher": "Prof. Vikram Nair",  "start": "14:00", "end": "15:00", "type": "Lecture"},
        ],
        "Thursday": [
            {"period": "1", "subject": "Database Systems",   "room": "LH-205", "teacher": "Prof. Meena Joshi",  "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Data Structures",    "room": "LH-101", "teacher": "Dr. Priya Menon",    "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Computer Networks Lab","room": "CL-01","teacher": "Dr. Anil Kumar",     "start": "11:15", "end": "13:15", "type": "Lab"},
            {"period": "4", "subject": "Elective I",         "room": "LH-301", "teacher": "Prof. Vikram Nair",  "start": "14:00", "end": "15:00", "type": "Lecture"},
        ],
        "Friday": [
            {"period": "1", "subject": "Operating Systems",  "room": "LH-101", "teacher": "Prof. Rahul Sharma", "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Mathematics III",    "room": "LH-203", "teacher": "Dr. Sunita Rao",     "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Seminar",            "room": "SEMHALL","teacher": "HOD",                "start": "11:15", "end": "12:15", "type": "Seminar"},
            {"period": "4", "subject": "Self-Study / Library","room": "LIBRARY","teacher": "",                  "start": "13:00", "end": "15:00", "type": "Self-Study"},
        ],
    },
    "CS2024B": {
        "Monday": [
            {"period": "1", "subject": "Computer Networks",  "room": "LH-102", "teacher": "Dr. Anil Kumar",     "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Database Systems",   "room": "LH-206", "teacher": "Prof. Meena Joshi",  "start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Data Structures",    "room": "LH-102", "teacher": "Dr. Priya Menon",    "start": "11:15", "end": "12:15", "type": "Lecture"},
            {"period": "4", "subject": "Computer Networks Lab","room": "CL-02","teacher": "Dr. Anil Kumar",     "start": "14:00", "end": "16:00", "type": "Lab"},
        ],
        "Tuesday": [
            {"period": "1", "subject": "Operating Systems",  "room": "LH-102", "teacher": "Prof. Rahul Sharma", "start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Mathematics III",    "room": "LH-204", "teacher": "Dr. Sunita Rao",     "start": "10:00", "end": "11:00", "type": "Lecture"},
        ],
    },
    "EC2024A": {
        "Monday": [
            {"period": "1", "subject": "Signals and Systems",   "room": "LH-401", "teacher": "Dr. Kavitha Reddy","start": "09:00", "end": "10:00", "type": "Lecture"},
            {"period": "2", "subject": "Digital Electronics",   "room": "LH-401", "teacher": "Prof. Suresh Babu","start": "10:00", "end": "11:00", "type": "Lecture"},
            {"period": "3", "subject": "Engineering Mathematics","room": "LH-402","teacher": "Dr. Sunita Rao",   "start": "11:15", "end": "12:15", "type": "Lecture"},
            {"period": "4", "subject": "Digital Electronics Lab","room": "EL-01", "teacher": "Prof. Suresh Babu","start": "14:00", "end": "16:00", "type": "Lab"},
        ],
    },
}

MOCK_FEE_STATUS: dict[str, dict[str, Any]] = {
    "MOCK1001": {
        "student_id": "MOCK1001",
        "name": "Arjun Sharma",
        "batch": "CS2024A",
        "tuition_fee": {"status": "PAID",    "amount": 85000, "paid_on": "2024-07-10"},
        "hostel_fee":  {"status": "PENDING", "amount": 45000, "due_date": "2024-12-15"},
        "exam_fee":    {"status": "PAID",    "amount": 2500,  "paid_on": "2024-10-01"},
    },
    "MOCK1002": {
        "student_id": "MOCK1002",
        "name": "Sneha Patel",
        "batch": "CS2024B",
        "tuition_fee": {"status": "PAID",    "amount": 85000, "paid_on": "2024-07-05"},
        "hostel_fee":  {"status": "PAID",    "amount": 45000, "paid_on": "2024-07-05"},
        "exam_fee":    {"status": "PENDING", "amount": 2500,  "due_date": "2024-11-30"},
    },
    "MOCK1003": {
        "student_id": "MOCK1003",
        "name": "Rahul Desai",
        "batch": "EC2024A",
        "tuition_fee": {"status": "OVERDUE", "amount": 85000, "due_date": "2024-10-01"},
        "hostel_fee":  {"status": "PAID",    "amount": 45000, "paid_on": "2024-07-08"},
        "exam_fee":    {"status": "PAID",    "amount": 2500,  "paid_on": "2024-10-01"},
    },
}

HOSTEL_RULES_TEXT = """# Nimbus Labs Hostel Rules (Fictional — for demonstration only)

## General Conduct
1. All residents must carry their ID cards at all times within hostel premises.
2. Ragging in any form is strictly prohibited and will lead to immediate expulsion.
3. Residents must maintain cleanliness in their rooms and common areas.
4. Wilful damage to hostel property will result in penalty charges.

## Timings
5. Main gate curfew: 22:00 (Sunday–Thursday), 23:00 (Friday–Saturday).
6. Quiet hours: 22:00–06:00. No loud music or gatherings after 22:00.
7. Mess timings: Breakfast 07:00–09:00, Lunch 12:00–14:00, Dinner 19:00–21:00.

## Guests
8. External guests are not permitted inside hostel rooms at any time.
9. Visitors may meet residents in the designated visitor lounge only, before 20:00.

## Electrical & Safety
10. Personal cooking appliances (electric kettles, irons, heaters) are prohibited.
11. Residents must switch off lights and fans when leaving the room.
12. Fire exits must remain unobstructed at all times.

## Disciplinary Action
13. Three violations of curfew in a semester will result in parental notification.
14. Any resident found with substances prohibited under institutional policy will face suspension.
"""

# ---------------------------------------------------------------------------
# Validation helpers (pure Python — no MCP dependency; importable by tests)
# ---------------------------------------------------------------------------

VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
VALID_BATCHES = set(MOCK_TIMETABLE.keys())
VALID_STUDENT_IDS = set(MOCK_FEE_STATUS.keys())


def get_timetable(batch: str, day: str) -> dict[str, Any]:
    """
    Return the class schedule for a given student batch on a specific day.

    Args:
        batch: Student batch code. Must be one of: CS2024A, CS2024B, EC2024A.
        day:   Day of the week. Must be one of: Monday, Tuesday, Wednesday,
               Thursday, Friday.

    Returns a JSON-serialisable dict with the batch, day, and a list of period
    objects. Each period object contains: period, subject, room, teacher, start,
    end, type.

    Errors are returned as {"error": "<message>"} — never raises exceptions.

    Security note: Tool descriptions are injected into LLM context and are an
    attack surface for prompt injection. Keep descriptions factual and do not
    embed credentials, instructions, or secrets.
    """
    batch = batch.strip().upper()
    day = day.strip().title()

    if batch not in VALID_BATCHES:
        return {
            "error": (
                f"Unknown batch '{batch}'. "
                f"Valid batches: {', '.join(sorted(VALID_BATCHES))}."
            )
        }

    if day not in VALID_DAYS:
        return {
            "error": (
                f"'{day}' is not a valid weekday. "
                f"Use one of: {', '.join(sorted(VALID_DAYS))}."
            )
        }

    schedule = MOCK_TIMETABLE.get(batch, {}).get(day, [])

    if not schedule:
        return {
            "batch": batch,
            "day": day,
            "note": "No timetable data available for this batch/day in the mock dataset.",
            "periods": [],
        }

    return {"batch": batch, "day": day, "periods": schedule}


def get_fee_status(student_id: str) -> dict[str, Any]:
    """
    Return the mock fee payment status for a student.

    Args:
        student_id: Student identifier. Only fictional IDs are accepted:
                    MOCK1001, MOCK1002, MOCK1003.

    Returns a dict with fee details for tuition, hostel, and exam fees.
    Each fee entry has: status (PAID/PENDING/OVERDUE), amount (INR), and
    either paid_on or due_date.

    Real student data, real IDs, or personal information is NOT stored.
    Errors are returned as {"error": "<message>"}.
    """
    student_id = student_id.strip().upper()

    if student_id not in VALID_STUDENT_IDS:
        return {
            "error": (
                f"Student ID '{student_id}' not found. "
                f"This server only accepts fictional IDs: "
                f"{', '.join(sorted(VALID_STUDENT_IDS))}. "
                "No real student data is stored."
            )
        }

    return MOCK_FEE_STATUS[student_id]


def hostel_rules() -> str:
    """
    Return the fictional Nimbus Labs hostel rules document.

    URI: hostel://rules
    MIME type: text/plain (markdown)
    """
    return HOSTEL_RULES_TEXT


# ---------------------------------------------------------------------------
# MCP tool/resource registrations
# ---------------------------------------------------------------------------

@mcp.tool()
def mcp_get_timetable(batch: str, day: str) -> dict[str, Any]:
    """Get the class schedule for a student batch on a given weekday."""
    return get_timetable(batch, day)


@mcp.tool()
def mcp_get_fee_status(student_id: str) -> dict[str, Any]:
    """Get mock fee payment status for a student (MOCK IDs only)."""
    return get_fee_status(student_id)


@mcp.resource("hostel://rules")
def mcp_hostel_rules() -> str:
    """Fictional Nimbus Labs hostel rules (demonstration only)."""
    return hostel_rules()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # MCPServer.run() defaults to stdio transport
    mcp.run()
