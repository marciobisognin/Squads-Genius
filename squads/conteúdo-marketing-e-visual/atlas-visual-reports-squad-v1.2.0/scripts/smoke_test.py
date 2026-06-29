#!/usr/bin/env python3
from __future__ import annotations
import subprocess, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'outputs'/'demo-v1.2'
out.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,str(ROOT/'scripts'/'build_report.py'),'--input',str(ROOT/'examples'/'demo-report.md'),'--output',str(out),'--brief',str(ROOT/'examples'/'project_brief.demo.json'),'--data-profile',str(ROOT/'examples'/'data_profile.demo.json')]
r=subprocess.run(cmd,capture_output=True,text=True)
report={'status':'pass' if r.returncode==0 else 'fail','stdout':r.stdout[-2000:],'stderr':r.stderr[-2000:],'html_exists':(out/'index.html').exists(),'pdf_exists':(out/'report.pdf').exists(),'html_bytes':(out/'index.html').stat().st_size if (out/'index.html').exists() else 0,'pdf_bytes':(out/'report.pdf').stat().st_size if (out/'report.pdf').exists() else 0}
(ROOT/'validation').mkdir(exist_ok=True)
(ROOT/'validation'/'smoke-test-report-v1.2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['status']=='pass' and report['html_exists'] and report['pdf_exists'] else 1)
