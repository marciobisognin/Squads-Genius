#!/usr/bin/env python3
import argparse,zipfile
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--output',required=True); args=ap.parse_args(); root=Path(args.root).resolve(); out=Path(args.output).expanduser().resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in root.rglob('*'):
            if p.is_file() and not any(x in p.parts for x in ['.git','node_modules','__pycache__']): z.write(p,Path(root.name)/p.relative_to(root))
    print(out)
if __name__=='__main__': main()
