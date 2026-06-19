import unittest
import _helper
import obsidian_index as idx
import obsidian_query as q


class TestCitations(unittest.TestCase):
    def setUp(self):
        self.cfg = _helper.write_temp_config(_helper.temp_config())
        idx.build_index(self.cfg, None)

    def test_verified_citations(self):
        res = q.query(self.cfg, None, "metodo PARA organizacao", top_k=5)
        self.assertTrue(res["has_sources"])
        self.assertTrue(all(c["verified"] for c in res["citations"]))

    def test_no_source_message(self):
        res = q.query(self.cfg, None, "zzzqxyw inexistente termo", top_k=5)
        self.assertFalse(res["has_sources"])
        self.assertIsNotNone(res["message"])


if __name__ == "__main__":
    unittest.main()
