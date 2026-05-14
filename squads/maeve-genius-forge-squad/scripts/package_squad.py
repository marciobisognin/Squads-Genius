#!/usr/bin/env python3
import argparse, zipfile
from pathlib import Path
EXCLUDE={'.git','node_modules','__pycache__','.venv','venv','.pytest_cache','.mypy_cache'}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--output',required=True); args=ap.parse_args()
    root=Path(args.root).resolve(); out=Path(args.output).expanduser().resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as zf:
        for p in root.rglob('*'):
            if any(part in EXCLUDE for part in p.parts): continue
            if p.is_file(): zf.write(p, Path(root.name)/p.relative_to(root))
    print(str(out))
if __name__=='__main__': main()
