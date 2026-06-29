#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json
root=Path(__file__).resolve().parents[1]
out=root/'outputs'/'demo'
out.mkdir(parents=True, exist_ok=True)
cmd=[sys.executable, str(root/'scripts'/'build_report.py'), '--input', str(root/'examples'/'demo-report.md'), '--output-dir', str(out), '--title', 'Relatório Demo — Atlas Visual Reports v1.1']
subprocess.check_call(cmd)
subprocess.check_call([sys.executable, str(root/'scripts'/'validate_squad.py')])
checks={'html':(out/'index.html').exists(),'pdf':(out/'report.pdf').exists(),'pdf_bytes':(out/'report.pdf').stat().st_size if (out/'report.pdf').exists() else 0,'agents':len(list((root/'agents').glob('*.md')))}
(root/'validation'/'smoke-test-report.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(checks, ensure_ascii=False, indent=2))
if not checks['html'] or not checks['pdf'] or checks['pdf_bytes']<1000 or checks['agents']<28: sys.exit(1)
