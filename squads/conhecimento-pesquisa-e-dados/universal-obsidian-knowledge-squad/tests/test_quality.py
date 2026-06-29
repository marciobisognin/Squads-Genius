import unittest
import _helper
import obsidian_index as idx
import obsidian_quality_audit as audit


class TestQuality(unittest.TestCase):
    def test_quality_report_go(self):
        cfg = _helper.write_temp_config(_helper.temp_config())
        idx.build_index(cfg, None)
        report = audit.audit(cfg, None)
        self.assertEqual(report["citation_anchor_failures"], 0)
        self.assertEqual(report["secret_hits"], [])
        self.assertEqual(report["go_no_go"], "go")


if __name__ == "__main__":
    unittest.main()
