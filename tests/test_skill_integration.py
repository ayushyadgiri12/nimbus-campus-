#!/usr/bin/env python3
"""
test_skill_integration.py — Integration tests for the timetable-helper Skill.
Added in branch: feature/skill-tests
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "skills" / "timetable-helper" / "scripts" / "lookup_timetable.py"
PYTHON = sys.executable


def run_lookup(*args):
    cmd = [PYTHON, str(SCRIPT)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


class TestSkillIntegration(unittest.TestCase):

    def test_ec2024a_monday(self):
        """EC2024A Monday should return Electronics schedule."""
        code, out, err = run_lookup("--batch", "EC2024A", "--day", "Monday")
        self.assertEqual(code, 0)
        self.assertIn("Signals and Systems", out)
        self.assertIn("Digital Electronics", out)

    def test_all_batches_friday(self):
        """CS2024A Friday has Seminar. CS2024B/EC2024A may have no Friday data."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Friday")
        self.assertEqual(code, 0)
        self.assertIn("Seminar", out)
        self.assertIn("Self-Study", out)

    def test_lab_session_type(self):
        """Lab sessions should show type=Lab."""
        code, out, err = run_lookup("--batch", "CS2024A", "--day", "Monday", "--period", "4")
        self.assertEqual(code, 0)
        self.assertIn("Lab", out)
        self.assertIn("CL-01", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
