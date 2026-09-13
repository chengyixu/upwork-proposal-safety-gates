import unittest
from gate import check


class GateTests(unittest.TestCase):
    def job(self):
        return {"job_id":"fresh", "title":"API work", "posted_at":"2026-09-13", "client_verified":True, "scope_confirmed":True, "allowance_confirmed":True, "estimated_hours":8, "skills":["typescript"]}

    def test_accepts_complete_sanitized_inputs(self):
        issues = check(self.job(), "Hi.\n1. Map.\n2. Build.\n3. Validate.\n", [{"claim":"typed work", "evidence":"https://github.com/example/work"}], [])
        self.assertEqual(issues, [])

    def test_blocks_cross_gate_failures(self):
        issues = check(self.job(), "Hi [client]\n", [{"claim":"x", "evidence":"http://not-safe"}], ["fresh"])
        self.assertIn("duplicate job", issues)
        self.assertIn("unresolved placeholder", issues)
        self.assertIn("missing delivery steps", issues)
        self.assertIn("unsupported proof", issues)


if __name__ == "__main__":
    unittest.main()
