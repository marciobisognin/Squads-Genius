import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'scripts/tracemosaic.py'
class TestTraceMosaic(unittest.TestCase):
 def test_pipeline(self):
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);case=t/'case';norm=t/'normalized.json';graph=t/'graph.json';report=t/'report.md'
   subprocess.run([sys.executable,str(CLI),'init','--input',str(ROOT/'examples/demo-input.json'),'--output',str(case)],check=True)
   subprocess.run([sys.executable,str(CLI),'normalize','--input',str(ROOT/'examples/demo-records.json'),'--output',str(norm)],check=True)
   subprocess.run([sys.executable,str(CLI),'correlate','--input',str(norm),'--output',str(graph)],check=True)
   subprocess.run([sys.executable,str(CLI),'report','--records',str(norm),'--graph',str(graph),'--output',str(report)],check=True)
   subprocess.run([sys.executable,str(CLI),'validate','--path',str(ROOT)],check=True)
   self.assertNotIn('synthetic-demo',norm.read_text());self.assertIn('[REDACTED]',norm.read_text());self.assertTrue(report.stat().st_size>100)
 def test_unicode_entities_do_not_collapse(self):
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);src=t/'records.json';norm=t/'normalized.json';graph=t/'graph.json'
   src.write_text(json.dumps([
    {'id':'R-A','entity':'Árvore Pública','claim':'Public record A','source_url':'https://example.org/a','source_type':'official','retrieved_at':'2026-01-01','confidence':'high'},
    {'id':'R-B','entity':'東京','claim':'Public record B','source_url':'https://example.org/b','source_type':'official','retrieved_at':'2026-01-01','confidence':'high'}
   ],ensure_ascii=False))
   subprocess.run([sys.executable,str(CLI),'normalize','--input',str(src),'--output',str(norm)],check=True)
   subprocess.run([sys.executable,str(CLI),'correlate','--input',str(norm),'--output',str(graph)],check=True)
   entities=[n['id'] for n in json.loads(graph.read_text())['nodes'] if n['type']=='entity']
   self.assertEqual(len(entities),2);self.assertEqual(len(set(entities)),2);self.assertNotIn('entity:',entities)
if __name__=='__main__':unittest.main()
