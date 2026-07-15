import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'scripts/breachcompass.py'
class TestBreachCompass(unittest.TestCase):
 def test_pipeline(self):
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);tri=t/'triage.json';timeline=t/'timeline.csv';iocs=t/'iocs.json';report=t/'report.md'
   subprocess.run([sys.executable,str(CLI),'triage','--input',str(ROOT/'examples/demo-input.json'),'--output',str(tri)],check=True)
   subprocess.run([sys.executable,str(CLI),'timeline','--input',str(ROOT/'examples/demo-events.json'),'--output',str(timeline)],check=True)
   subprocess.run([sys.executable,str(CLI),'ioc-extract','--input',str(ROOT/'examples/demo-log.txt'),'--output',str(iocs)],check=True)
   subprocess.run([sys.executable,str(CLI),'report','--triage',str(tri),'--timeline',str(timeline),'--iocs',str(iocs),'--output',str(report)],check=True)
   subprocess.run([sys.executable,str(CLI),'validate','--path',str(ROOT)],check=True)
   d=json.loads(iocs.read_text());self.assertEqual(d['counts']['hash'],1);self.assertEqual(d['counts']['ip'],1);self.assertTrue(report.stat().st_size>100)
if __name__=='__main__':unittest.main()
