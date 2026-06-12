#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/build_product.py'),'--brief',str(ROOT/'examples/demo/project_brief.json'),'--output',str(ROOT/'generated/demo/final')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build_pdf.py'),'--input',str(ROOT/'generated/demo/final/print-ready.html'),'--output',str(ROOT/'generated/demo/final/presentation.pdf')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/validate_squad.py')],check=True)
out=ROOT/'generated/demo/final'
required=['index.html','deck.html','motion-composition.html','print-ready.html','presentation.pdf','final-manifest.json','qa-cleanroom-report.json']
missing=[x for x in required if not (out/x).exists()]
qa=json.loads((out/'qa-cleanroom-report.json').read_text(encoding='utf-8'))
report={'status':'fail' if missing or qa.get('status')!='pass' else 'pass','output':str(out),'missing':missing,'qa':qa}
(ROOT/'validation/smoke-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
sys.exit(0 if report['status']=='pass' else 1)
