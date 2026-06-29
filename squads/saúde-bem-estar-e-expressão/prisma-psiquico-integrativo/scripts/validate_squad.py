#!/usr/bin/env python3
import json, sys, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','TEXTO_PUBLICACAO_REDES_BLOG.md','EXPLICACAO_SQUAD.md','scripts/formulate_case.py','scripts/run_demo.py','scripts/validate_squad.py','scripts/package_squad.py','templates/crisis_protocol.md']
missing=[x for x in required if not (root/x).exists()]
agent_files=list((root/'agents').glob('*.md'))
workflow_files=list((root/'workflows').glob('*.yaml'))
agent_ok=[]
for p in agent_files:
    txt=p.read_text(encoding='utf-8', errors='ignore')
    agent_ok.append(('*help' in txt) and ('*exit' in txt) and ('diagnóstico' in txt.lower() or 'diagnostico' in txt.lower()))
readme=(root/'README.md').read_text(encoding='utf-8', errors='ignore') if (root/'README.md').exists() else ''
guardrails=all(term in readme.lower() for term in ['não diagnostica','não substitui','crise'])
report={'go_no_go':'go' if not missing and len(agent_files)>=8 and len(workflow_files)>=3 and all(agent_ok) and guardrails else 'no-go','missing':missing,'agents':len(agent_files),'workflows':len(workflow_files),'agent_command_guardrails_ok':all(agent_ok),'readme_guardrails_ok':guardrails}
(root/'validation').mkdir(exist_ok=True)
(root/'validation/quality_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['go_no_go']=='go' else 1)
