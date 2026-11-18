# /campus-status

Show the current operational status of the Nimbus Labs campus.

## What This Command Does

Queries the campus-helpdesk MCP server to report:

1. **Today's schedule summary** — lectures and labs currently in progress or upcoming for the next two hours
2. **Open labs** — which computer labs and electronics labs are currently available
3. **Fee deadline alerts** — any pending fee deadlines from the fee status tool (requires a student ID)
4. **Hostel rule highlights** — a brief summary of key hostel rules

## Usage

```
/campus-status
```

Or with a student ID for fee information:

```
/campus-status MOCK1001
```

## Instructions for Claude

When this command is invoked:

1. Call the `get_timetable` MCP tool with today's batch (default: `CS2024A`) and today's day name.
2. Filter periods whose `start_time` is within the next 2 hours of the current time.
3. If a student ID argument was provided, call `get_fee_status` with that ID.
4. Read the `hostel://rules` MCP resource and extract the top 3 rules.
5. Present a compact, bulleted status report with emoji for quick scanning.

## Example Output

```
📅 Campus Status — Monday, CS2024A

🏫 Next Up:
  • 10:00–11:00  Operating Systems  →  LH-101  (Prof. Rahul Sharma)
  • 11:15–12:15  Mathematics III    →  LH-203  (Dr. Sunita Rao)

💻 Open Labs:
  • CL-01 (booked 14:00–16:00), CL-02 (open all day)

💰 Fee Status (MOCK1001):
  • Tuition: PAID ✅
  • Hostel:  PENDING ⚠️ — Due: 2024-12-15

🏠 Hostel Reminder:
  • Quiet hours: 22:00–06:00
  • Sign out before 23:00
  • No external guests after 21:00
```

## Notes

- Only fictional MOCK IDs are accepted: `MOCK1001`, `MOCK1002`, `MOCK1003`
- If no MCP server is running, explain the connection failure and suggest running `python3 mcp-server/server.py`
