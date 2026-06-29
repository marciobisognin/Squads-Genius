import unittest
import _helper
import obsidian_index as idx


class TestIndex(unittest.TestCase):
    def test_builds_index(self):
        cfg = _helper.write_temp_config(_helper.temp_config())
        result = idx.build_index(cfg, None)
        self.assertGreaterEqual(result["notes_indexed"], 3)
        self.assertGreater(result["chunks_indexed"], 0)
        self.assertEqual(result["skipped_secrets"], [])


if __name__ == "__main__":
    unittest.main()
