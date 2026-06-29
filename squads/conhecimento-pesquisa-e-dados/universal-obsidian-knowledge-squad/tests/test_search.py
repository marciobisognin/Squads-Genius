import unittest
import _helper
import obsidian_index as idx
import obsidian_search as search


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.cfg = _helper.write_temp_config(_helper.temp_config())
        idx.build_index(self.cfg, None)

    def test_lexical_search_returns_results(self):
        res = search.search(self.cfg, None, "segundo cerebro", top_k=5)
        self.assertTrue(res)
        self.assertIn("path", res[0])
        self.assertIn("heading", res[0])

    def test_accent_insensitive(self):
        res = search.search(self.cfg, None, "citacao verificavel", top_k=5)
        self.assertTrue(any("Citacoes" in r["path"] for r in res))


if __name__ == "__main__":
    unittest.main()
