#!/usr/bin/env python3
"""
test_timetable.py — Unit tests for the timetable-helper Skill lookup script.

Covers:
  - 3 positive tests (valid queries)
  - 2 negative tests (invalid batch, invalid day)
  - 1 adversarial test (invented subject)

Run from the repo root:
  python3 tests/test_timetable.py
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "skills" / "timetable-helper" / "scripts" / "lookup_timetable.py"
PYTHON = sys.executable


def run_lookup(*args) -> tuple[int, str, str]:
    """Run lookup_timetable.py with the given args; return (returncode, stdout, stderr)."""
    cmd = [PYTHON, str(SCRIPT)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


class TestPositiveLookups(unittest.TestCase):
    """TEST GROUP 1: Valid queries that should succeed."""

    def test_positive_1_batch_day(self):
        """P1: Query CS2024A schedule for Monday — should return 4 periods."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Monday")
        self.assertEqual(code, 0, f"Expected exit 0, got {code}. stderr: {err}")
        self.assertIn("Data Structures", out)
        self.assertIn("Operating Systems", out)
        self.assertIn("Dr. Priya Menon", out)
        self.assertIn("Period 1", out)
        self.assertIn("Period 4", out)

    def test_positive_2_subject_lookup(self):
        """P2: Query subject 'Data Structures' for CS2024A — should appear on Mon/Wed/Thu."""
        code, out, err = run_lookup("--batch", "CS2024A", "--subject", "Data Structures")
        self.assertEqual(code, 0, f"Expected exit 0, got {code}. stderr: {err}")
        self.assertIn("Monday", out)
        self.assertIn("Wednesday", out)
        self.assertIn("Thursday", out)
        self.assertIn("LH-101", out)

    def test_positive_3_period_detail(self):
        """P3: Query CS2024A Monday Period 1 — should return single period detail."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Monday", "--period", "1")
        self.assertEqual(code, 0, f"Expected exit 0, got {code}. stderr: {err}")
        self.assertIn("Period 1", out)
        self.assertIn("Data Structures", out)
        self.assertIn("09:00", out)
        self.assertIn("10:00", out)
        self.assertIn("LH-101", out)


class TestNegativeLookups(unittest.TestCase):
    """TEST GROUP 2: Invalid inputs that should fail gracefully."""

    def test_negative_1_unknown_batch(self):
        """N1: Unknown batch ME2024A — should exit non-zero with helpful message."""
        code, out, err = run_lookup("--batch", "ME2024A", "--day", "Monday")
        self.assertNotEqual(code, 0, "Expected non-zero exit for unknown batch")
        self.assertIn("ME2024A", err)
        self.assertIn("not found", err.lower())
        # Must list valid batches in error message
        self.assertIn("CS2024A", err)

    def test_negative_2_invalid_day(self):
        """N2: 'Saturday' is not a weekday — should exit non-zero with helpful message."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Saturday")
        self.assertNotEqual(code, 0, "Expected non-zero exit for invalid day")
        self.assertIn("Saturday", err)
        self.assertIn("Monday", err)   # Should list valid days


class TestAdversarial(unittest.TestCase):
    """TEST GROUP 3: Adversarial prompt — requests an invented class."""

    def test_adversarial_invented_subject(self):
        """
        A1: 'Quantum Computing' does not exist in the CSV for CS2024A.

        EXPECTED BEHAVIOUR: Script refuses to fabricate.
        Returns exit 0 (not an error per se) but output must clearly state
        the subject was NOT found and must NOT contain invented room/teacher data.

        This tests the FABRICATION REFUSAL policy from references/edge-cases.md EC-05.
        """
        code, out, err = run_lookup("--batch", "CS2024A", "--subject", "Quantum Computing")
        # The script exits 0 for "not found" (it's not a system error)
        self.assertEqual(code, 0, f"Expected exit 0 for not-found subject, got {code}")
        # Must refuse and explain
        combined = out + err
        self.assertIn("not found", combined.lower(),
                      "Script must say the subject was not found")
        self.assertIn("fabricate", combined.lower(),
                      "Script must mention fabrication refusal")
        # Must NOT contain plausible-sounding but invented data
        self.assertNotIn("LH-", combined,
                         "Script must not invent a room for a non-existent class")
        self.assertNotIn("Dr.", combined,
                         "Script must not invent a teacher for a non-existent class")


class TestEdgeCases(unittest.TestCase):
    """TEST GROUP 4: Edge cases from references/edge-cases.md."""

    def test_case_insensitive_batch(self):
        """EC-09: Lowercase batch code should be normalised and work."""
        code, out, err = run_lookup("--batch", "cs2024a", "--day", "Monday")
        self.assertEqual(code, 0, f"Case normalisation failed: {err}")
        self.assertIn("Data Structures", out)

    def test_case_insensitive_day(self):
        """EC-02: Lowercase day should be normalised and work."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "monday")
        self.assertEqual(code, 0, f"Day case normalisation failed: {err}")
        self.assertIn("Data Structures", out)

    def test_self_study_no_teacher(self):
        """EC-04: Friday Period 4 (Self-Study) should show no teacher."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Friday", "--period", "4")
        self.assertEqual(code, 0)
        self.assertIn("Self-Study", out)
        self.assertIn("No teacher", out)

    def test_invalid_period(self):
        """EC-08: Period 5 is out of range — should exit non-zero."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Monday", "--period", "5")
        self.assertNotEqual(code, 0, "Expected non-zero exit for period=5")
        self.assertIn("5", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
