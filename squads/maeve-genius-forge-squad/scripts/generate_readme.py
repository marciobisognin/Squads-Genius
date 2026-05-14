#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); args=ap.parse_args(); root=Path(args.root)
    m=json.loads((root/'squad.yaml').read_text(encoding='utf-8'))
    lines=['# '+m.get('commercial_name',m['name']),'','## Agentes']+[f"- `{a['id']}` — {a['role']}" for a in m.get('agents',[])]
    (root/'README.generated.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print(root/'README.generated.md')
if __name__=='__main__': main()
