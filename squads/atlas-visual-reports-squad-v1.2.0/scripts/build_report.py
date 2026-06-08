#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def call(args):
    r=subprocess.run([sys.executable]+args,capture_output=True,text=True)
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr.strip(), file=sys.stderr)
        raise SystemExit(r.returncode)
def main():
    ap=argparse.ArgumentParser(description='Build full premium HTML/PDF report')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--brief')
    ap.add_argument('--data-profile')
    ap.add_argument('--orientation', default='portrait', choices=['portrait','landscape'])
    ap.add_argument('--no-pdf', action='store_true')
    args=ap.parse_args()
    out=Path(args.output); html=out/'index.html'; pdf=out/'report.pdf'
    cmd=[str(ROOT/'scripts'/'build_html.py'),'--input',args.input,'--output',args.output,'--orientation',args.orientation]
    if args.brief: cmd += ['--brief',args.brief]
    if args.data_profile: cmd += ['--data-profile',args.data_profile]
    call(cmd)
    if not args.no_pdf:
        call([str(ROOT/'scripts'/'build_pdf.py'),'--html',str(html),'--output',str(pdf),'--orientation',args.orientation])
        call([str(ROOT/'scripts'/'validate_pdf.py'),'--pdf',str(pdf),'--output-dir',str(out/'pdf-preview')])
    print(json.dumps({'status':'pass','html':str(html),'pdf':None if args.no_pdf else str(pdf)},ensure_ascii=False))
if __name__=='__main__': main()
