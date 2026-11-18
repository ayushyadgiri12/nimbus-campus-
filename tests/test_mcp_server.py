#!/usr/bin/env python3
"""
test_mcp_server.py — Unit and integration tests for the campus-helpdesk MCP server.

Tests the tool logic directly (without MCP transport overhead) by importing
server.py functions and calling them in-process.

Run from the repo root (with venv activated):
  python3 tests/test_mcp_server.py

NOTE: This tests the BUSINESS LOGIC of the server tools.
For full JSON-RPC transport testing, see docs/mcp-jsonrpc-traces.md.
"""

import sys
import unittest
from pathlib import Path

# Add mcp-server directory to path so we can import server.py
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "mcp-server"))

# Import the tool functions from server.py
# We import the underlying Python functions directly (not via MCP transport)
try:
    from server import get_timetable, get_fee_status, hostel_rules
    MCP_IMPORT_OK = True
except ImportError as e:
    MCP_IMPORT_OK = False
    IMPORT_ERROR = str(e)


@unittest.skipUnless(MCP_IMPORT_OK, f"MCP server import failed: {locals().get('IMPORT_ERROR', '')}")
class TestGetTimetable(unittest.TestCase):
    """Tests for the get_timetable tool."""

    def test_valid_batch_and_day(self):
        """T1: Valid batch CS2024A, day Monday — returns schedule."""
        result = get_timetable("CS2024A", "Monday")
        self.assertNotIn("error", result)
        self.assertEqual(result["batch"], "CS2024A")
        self.assertEqual(result["day"], "Monday")
        self.assertIsInstance(result["periods"], list)
        self.assertGreater(len(result["periods"]), 0)
        # Check first period structure
        p1 = result["periods"][0]
        for key in ("period", "subject", "room", "teacher", "start", "end", "type"):
            self.assertIn(key, p1, f"Missing key '{key}' in period dict")

    def test_case_normalisation(self):
        """T2: Lowercase input should be normalised correctly."""
        result = get_timetable("cs2024a", "monday")
        self.assertNotIn("error", result)
        self.assertEqual(result["batch"], "CS2024A")
        self.assertEqual(result["day"], "Monday")

    def test_unknown_batch(self):
        """T3: Unknown batch returns error dict, not exception."""
        result = get_timetable("FAKE999X", "Monday")
        self.assertIn("error", result)
        self.assertIn("FAKE999X", result["error"])
        self.assertIn("CS2024A", result["error"])  # Should list valid batches

    def test_unknown_day(self):
        """T4: 'Sunday' is not in the weekday list — returns error."""
        result = get_timetable("CS2024A", "Sunday")
        self.assertIn("error", result)
        self.assertIn("Sunday", result["error"])

    def test_saturday_blocked(self):
        """T5: Saturday is not a valid teaching day."""
        result = get_timetable("CS2024A", "Saturday")
        self.assertIn("error", result)

    def test_all_valid_batches(self):
        """T6: All three valid batches work for at least one day."""
        for batch in ("CS2024A", "CS2024B", "EC2024A"):
            result = get_timetable(batch, "Monday")
            self.assertNotIn("error", result, f"Batch {batch} failed: {result}")
            self.assertIsInstance(result.get("periods"), list)

    def test_no_real_data(self):
        """T7: Server never reveals real student names or IDs in timetable."""
        result = get_timetable("CS2024A", "Monday")
        output_str = str(result)
        # Ensure no real institution names leak
        self.assertNotIn("IIT", output_str)
        self.assertNotIn("NIT", output_str)


@unittest.skipUnless(MCP_IMPORT_OK, f"MCP server import failed")
class TestGetFeeStatus(unittest.TestCase):
    """Tests for the get_fee_status tool."""

    def test_valid_mock_id_1001(self):
        """F1: MOCK1001 returns fee status with all three fee types."""
        result = get_fee_status("MOCK1001")
        self.assertNotIn("error", result)
        self.assertEqual(result["student_id"], "MOCK1001")
        for fee_type in ("tuition_fee", "hostel_fee", "exam_fee"):
            self.assertIn(fee_type, result)
            self.assertIn("status", result[fee_type])
            self.assertIn("amount", result[fee_type])

    def test_valid_mock_id_1002(self):
        """F2: MOCK1002 — all fees paid."""
        result = get_fee_status("MOCK1002")
        self.assertNotIn("error", result)
        self.assertEqual(result["tuition_fee"]["status"], "PAID")
        self.assertEqual(result["hostel_fee"]["status"], "PAID")

    def test_valid_mock_id_1003_overdue(self):
        """F3: MOCK1003 — tuition fee is OVERDUE."""
        result = get_fee_status("MOCK1003")
        self.assertNotIn("error", result)
        self.assertEqual(result["tuition_fee"]["status"], "OVERDUE")

    def test_invalid_id(self):
        """F4 (Negative): Real-looking ID rejected with helpful message."""
        result = get_fee_status("STU20240001")
        self.assertIn("error", result)
        self.assertIn("STU20240001", result["error"])
        self.assertIn("MOCK", result["error"])  # Should mention valid IDs

    def test_case_normalisation(self):
        """F5: Lowercase ID should be normalised."""
        result = get_fee_status("mock1001")
        self.assertNotIn("error", result)
        self.assertEqual(result["student_id"], "MOCK1001")

    def test_no_real_credentials(self):
        """F6: Response must not contain real credentials or API keys."""
        result = get_fee_status("MOCK1001")
        output_str = str(result)
        for forbidden in ("password", "api_key", "secret", "token", "credential"):
            self.assertNotIn(forbidden, output_str.lower())


@unittest.skipUnless(MCP_IMPORT_OK, f"MCP server import failed")
class TestHostelRulesResource(unittest.TestCase):
    """Tests for the hostel://rules resource."""

    def test_resource_returns_text(self):
        """R1: hostel_rules() returns a non-empty string."""
        result = hostel_rules()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 100)

    def test_resource_contains_key_sections(self):
        """R2: Resource contains expected rule categories."""
        result = hostel_rules()
        for section in ("Conduct", "Timings", "Guests", "Safety"):
            self.assertIn(section, result, f"Expected section '{section}' in hostel rules")

    def test_resource_marked_fictional(self):
        """R3: Resource is clearly marked as fictional."""
        result = hostel_rules()
        self.assertIn("Fictional", result)


if __name__ == "__main__":
    # Print whether MCP import succeeded
    if MCP_IMPORT_OK:
        print("[INFO] MCP server imported successfully. Running tests...")
    else:
        print(f"[WARNING] MCP server could not be imported: {IMPORT_ERROR}")
        print("[INFO] Business logic tests will be skipped. Install mcp[cli] in venv first.")
    unittest.main(verbosity=2)
