#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, shutil
from pathlib import Path

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    ap=argparse.ArgumentParser(description='Validate PDF syntax and render previews')
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--output-dir', default='validation/pdf-preview')
    args=ap.parse_args()
    pdf=Path(args.pdf); out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    issues=[]; fixes=[]
    if not pdf.exists(): issues.append('pdf_missing')
    data=pdf.read_bytes() if pdf.exists() else b''
    if not data.startswith(b'%PDF-'): issues.append('missing_pdf_header')
    if not data.rstrip().endswith(b'%%EOF'): issues.append('missing_eof_marker')
    qpdf_status='skipped'
    if shutil.which('qpdf') and pdf.exists():
        r=run(['qpdf','--check',str(pdf)]); qpdf_status='pass' if r.returncode==0 else 'fail'
        if r.returncode: issues.append('qpdf_failed:'+r.stderr[-500:])
    previews=[]
    if shutil.which('mutool') and pdf.exists():
        r=run(['mutool','draw','-o',str(out/'page-%02d.png'),'-r','72',str(pdf),'1-5'])
        if r.returncode==0:
            previews=[str(p) for p in sorted(out.glob('page-*.png'))]
        else:
            issues.append('mutool_render_failed:'+r.stderr[-500:])
    report={'visual_status':'warning' if not previews else 'pass','pdf_status':'pass' if not issues else 'fail','content_status':'warning','issues':issues,'fixes_applied':fixes,'qpdf_status':qpdf_status,'preview_pages':len(previews),'pdf_bytes':len(data)}
    (out.parent/'pdf-validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
    raise SystemExit(0 if report['pdf_status']=='pass' else 1)
if __name__=='__main__': main()
