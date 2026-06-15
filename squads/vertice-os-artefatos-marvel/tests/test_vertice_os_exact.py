import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class VerticeOSExactTests(unittest.TestCase):
    def test_agent_catalog_exact_count(self):
        cat=json.loads((ROOT/'references/agent_catalog.json').read_text(encoding='utf-8'))
        self.assertEqual(len(cat['agents']),21)
        self.assertEqual(cat['agents'][0]['codename'],'MANOPLA DO INFINITO')
        self.assertEqual(cat['agents'][-1]['codename'],'DARKHOLD CHAMBER')
    def test_source_prd_preserved(self):
        text=(ROOT/'PRD.md').read_text(encoding='utf-8')
        self.assertIn('PRD VÉRTICE-OS', text)
        self.assertIn('MANOPLA DO INFINITO', text)
        self.assertIn('ULTIMATE NULLIFIER', text)
    def test_validator_go(self):
        p=subprocess.run([sys.executable,'scripts/validate_squad.py','--path','.'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn('"status": "go"',p.stdout)
if __name__=='__main__': unittest.main()
