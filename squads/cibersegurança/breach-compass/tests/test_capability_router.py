import json,subprocess,sys,unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'scripts/capability_router.py'
class CapabilityRouterTests(unittest.TestCase):
 def run_cli(self,*a):return subprocess.run([sys.executable,str(SCRIPT),*a],text=True,capture_output=True)
 def test_catalog_and_audit(self):
  p=self.run_cli('catalog');self.assertEqual(p.returncode,0);self.assertGreater(json.loads(p.stdout)['count'],0)
  p=self.run_cli('audit');self.assertEqual(p.returncode,0);self.assertIn('summary',json.loads(p.stdout))
 def test_route_is_non_executing(self):
  p=self.run_cli('route','--technique','malware-dynamic-analysis','--context','isolated-external-lab','--band','3');self.assertEqual(p.returncode,0);d=json.loads(p.stdout);self.assertFalse(d['execution_performed']);self.assertIn(d['decision'],['PLAN_ONLY','GATED_HANDOFF'])
if __name__=='__main__':unittest.main()
