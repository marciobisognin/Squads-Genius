#!/usr/bin/env python3
from pathlib import Path
import json, datetime
root=Path(__file__).resolve().parents[1]
context=root/'context'; out=root/'output'; out.mkdir(exist_ok=True)
files={p.name:p.read_text(encoding='utf-8') for p in context.glob('*.md')}
report={'generated_at':datetime.datetime.now().isoformat(), 'files':list(files), 'summary':'Context pack inicial gerado.'}
(out/'context-pack.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
(out/'context-pack.md').write_text('\n\n'.join(f'# {k}\n\n{v}' for k,v in files.items()), encoding='utf-8')
print(json.dumps({'ok':True,'output':str(out/'context-pack.md')}, ensure_ascii=False))
