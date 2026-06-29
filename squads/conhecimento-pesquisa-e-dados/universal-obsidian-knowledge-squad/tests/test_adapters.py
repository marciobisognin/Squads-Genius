import unittest
from pathlib import Path
import _helper  # noqa: F401
import obsidian_core as core

ADAPTERS = Path(__file__).resolve().parents[1] / "config" / "adapters"


class TestAdapters(unittest.TestCase):
    def test_generic_and_maeve_exist(self):
        for name in ("generic", "maeve", "hermes"):
            self.assertTrue((ADAPTERS / f"{name}.yaml").is_file())

    def test_maeve_has_no_hardcoded_path(self):
        text = (ADAPTERS / "maeve.yaml").read_text(encoding="utf-8")
        self.assertNotIn("/storage/emulated", text)
        self.assertIn("MAEVE_DELIVERY_PATH", text)

    def test_adapters_load(self):
        cfg = core.load_config(str(ADAPTERS / "generic.yaml"))
        self.assertEqual(cfg["agent_adapter"]["name"], "generic")


if __name__ == "__main__":
    unittest.main()
