import unittest
import _helper  # noqa: F401
import obsidian_core as core


class TestLinks(unittest.TestCase):
    def test_wikilinks(self):
        body = "ver [[Nota A]] e [[Nota B|alias]]"
        links = core.extract_wikilinks(body)
        self.assertIn("Nota A", links)
        self.assertIn("Nota B", links)

    def test_headings_and_tags(self):
        body = "# Titulo\n## Sub\ntexto #pkm #org"
        self.assertEqual(core.extract_headings(body), ["Titulo", "Sub"])
        self.assertIn("pkm", core.extract_tags(body, {}))


if __name__ == "__main__":
    unittest.main()
