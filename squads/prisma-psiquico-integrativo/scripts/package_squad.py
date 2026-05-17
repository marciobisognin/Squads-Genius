#!/usr/bin/env python3
import argparse, zipfile
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--output',required=True); a=ap.parse_args()
root=Path(a.root).resolve(); out=Path(a.output).expanduser(); out.parent.mkdir(parents=True,exist_ok=True)
exclude={'.git','node_modules','__pycache__','.venv','venv','.pytest_cache','.mypy_cache','.DS_Store'}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if any(part in exclude for part in rel.parts): continue
        if p.is_file(): z.write(p, Path(root.name)/rel)
print(out)
