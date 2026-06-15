#!/usr/bin/env python3
import json, zipfile, sys, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
files=[p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
required=['README.md','squad.yaml','LICENSE','NOTICE.md','AUTHORS.md','TEXTO_PUBLICACAO_REDES_BLOG.md','examples/demo_input.json']
missing=[r for r in required if not (root/r).exists()]
scan=[]
patterns = ['g'+'ho_', 'github_'+'pat_', 's'+'k-', 'BEGIN '+'PRIVATE KEY', 'BEGIN '+'OPENSSH PRIVATE KEY']
for p in files:
    if p.name in {'validate_package.py', 'package-validation-report.json'}:
        continue
    if p.suffix.lower() in ['.md','.json','.yaml','.yml','.py','.csv','.txt']:
        t=p.read_text(encoding='utf-8', errors='ignore')
        for pat in patterns:
            if pat in t: scan.append(str(p.relative_to(root))+':'+pat)
report={'ok':not missing and not scan,'file_count':len(files),'missing':missing,'secret_flags':scan}
(root/'validation/package-validation-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
sys.exit(0 if report['ok'] else 1)
