import unittest
import _helper  # noqa: F401
import obsidian_core as core


class TestFrontmatter(unittest.TestCase):
    def test_parse_and_strip(self):
        text = "---\ntitle: X\ntags: [a, b]\n---\n# H\ncorpo"
        fm = core.parse_frontmatter(text)
        self.assertEqual(fm.get("title"), "X")
        body = core.strip_frontmatter(text)
        self.assertNotIn("title: X", body)
        self.assertIn("corpo", body)

    def test_no_frontmatter(self):
        self.assertEqual(core.parse_frontmatter("# só corpo"), {})


if __name__ == "__main__":
    unittest.main()
