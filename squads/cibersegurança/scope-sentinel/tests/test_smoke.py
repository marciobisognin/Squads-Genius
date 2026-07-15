import importlib.util,json,subprocess,sys,tempfile,threading,unittest
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[1];CLI=ROOT/'scripts/scopesentinel.py'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path.startswith('/redirect'):
   self.send_response(302);self.send_header('Location','/index.html?session=synthetic-secret');self.end_headers();return
  return super().do_GET()
class TestScopeSentinel(unittest.TestCase):
 def test_end_to_end_local_fixture(self):
  with tempfile.TemporaryDirectory() as td:
   t=Path(td);(t/'index.html').write_text('<title>Fixture</title>ok')
   handler=lambda *a,**k:Quiet(*a,directory=td,**k);srv=ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=srv.serve_forever,daemon=True).start()
   try:
    eng=json.loads((ROOT/'examples/demo-input.json').read_text());eng['assets']=[f'http://127.0.0.1:{srv.server_port}'];ep=t/'eng.json';ep.write_text(json.dumps(eng));out=t/'out';ev=t/'evidence.json';rep=t/'report.md'
    subprocess.run([sys.executable,str(CLI),'plan','--input',str(ep),'--output',str(out)],check=True)
    subprocess.run([sys.executable,str(CLI),'collect','--input',str(ep),'--output',str(ev)],check=True)
    subprocess.run([sys.executable,str(CLI),'report','--input',str(ev),'--output',str(rep)],check=True)
    subprocess.run([sys.executable,str(CLI),'validate','--path',str(ROOT)],check=True)
    self.assertTrue(ev.stat().st_size>100 and rep.stat().st_size>100)
    self.assertEqual(json.loads(ev.read_text())['assets'][0]['responses'][0]['status'],200)
    spec=importlib.util.spec_from_file_location('scopesentinel',CLI)
    if spec is None or spec.loader is None:self.fail('cannot load Scope Sentinel module')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    redir=mod.fetch(f'http://127.0.0.1:{srv.server_port}/redirect')
    self.assertEqual(redir['status'],302);self.assertFalse(redir['redirect_followed']);self.assertNotIn('synthetic-secret',json.dumps(redir));self.assertIn('REDACTED',json.dumps(redir))
   finally:
    srv.shutdown();srv.server_close()
if __name__=='__main__':unittest.main()
