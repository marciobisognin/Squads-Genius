"""Testes de fumaça do Harness Foundry Squad — só stdlib + PyYAML, sem pytest."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELF_SQUAD = ROOT  # o próprio squad é um candidato válido a harness


class TestScoreSquadFit(unittest.TestCase):
    def test_score_runs_on_self(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "score_squad_fit.py"), "--root", str(SELF_SQUAD)],
            capture_output=True,
            text=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertIn("harness_fit", report)
        self.assertIn("go_no_go", report)
        self.assertGreaterEqual(report["harness_fit"], 0)


class TestSquadToHarnessSpec(unittest.TestCase):
    def test_builds_spec_with_capabilities(self):
        out_path = ROOT / "output" / "test" / "harnessspec.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "squad_to_harnessspec.py"),
                "--squad",
                str(SELF_SQUAD),
                "--out",
                str(out_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        spec = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertEqual(spec["name"], "harness-foundry-squad")
        self.assertTrue(spec["capabilities"])
        self.assertTrue(spec["commands"])
        out_path.unlink()


class TestHermesPackageAndDoctor(unittest.TestCase):
    def test_generates_package_and_passes_doctor(self):
        spec_path = ROOT / "output" / "test2" / "harnessspec.json"
        hermes_dir = ROOT / "output" / "test2" / "hermes"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "squad_to_harnessspec.py"),
                "--squad",
                str(SELF_SQUAD),
                "--out",
                str(spec_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "generate_hermes_package.py"),
                "--harnessspec",
                str(spec_path),
                "--out",
                str(hermes_dir),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertTrue((hermes_dir / "cli-config.yaml").exists())
        self.assertTrue((hermes_dir / "SKILL.md").exists())

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "harness_doctor.py"),
                "--hermes-dir",
                str(hermes_dir),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        report = json.loads(result.stdout)
        self.assertIn(report["status"], {"HEALTHY", "WARN", "BLOCKED"})


if __name__ == "__main__":
    unittest.main()
