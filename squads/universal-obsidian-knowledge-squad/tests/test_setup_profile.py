import unittest
import _helper  # noqa: F401
import setup_user_profile as sp


class TestSetupProfile(unittest.TestCase):
    def test_default_mode_read_only(self):
        prof = sp.build_profile("/tmp/x", "pt-BR", "generic", "read_only")
        self.assertEqual(prof["runtime"]["default_mode"], "read_only")
        self.assertFalse(prof["runtime"]["allow_write"])

    def test_write_mode_enables_write(self):
        prof = sp.build_profile("/tmp/x", "pt-BR", "generic", "write")
        self.assertTrue(prof["runtime"]["allow_write"])

    def test_invalid_mode_raises(self):
        with self.assertRaises(ValueError):
            sp.build_profile("/tmp/x", "pt-BR", "generic", "banana")


if __name__ == "__main__":
    unittest.main()
