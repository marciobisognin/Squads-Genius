import unittest
import _helper  # noqa: F401
import setup_user_profile as sp


class TestPermissions(unittest.TestCase):
    def test_read_only_blocks_write(self):
        prof = sp.build_profile("/tmp/x", "pt-BR", "generic", "read_only")
        self.assertFalse(prof["runtime"]["allow_write"])

    def test_suggest_blocks_write(self):
        prof = sp.build_profile("/tmp/x", "pt-BR", "generic", "suggest")
        self.assertFalse(prof["runtime"]["allow_write"])

    def test_curate_requires_explicit_mode(self):
        prof = sp.build_profile("/tmp/x", "pt-BR", "generic", "curate")
        self.assertTrue(prof["runtime"]["allow_write"])


if __name__ == "__main__":
    unittest.main()
