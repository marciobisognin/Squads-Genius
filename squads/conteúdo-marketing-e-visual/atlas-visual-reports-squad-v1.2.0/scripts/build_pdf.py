#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Build A4 PDF from generated HTML')
    ap.add_argument('--html', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--orientation', default='portrait', choices=['portrait','landscape'])
    args=ap.parse_args()
    html_path=Path(args.html); out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    text=html_path.read_text(encoding='utf-8')
    size=f'A4 {args.orientation}'
    text=re.sub(r'@page\{size:A4 (portrait|landscape);', f'@page{{size:{size};', text)
    tmp=out.with_suffix('.print.html')
    tmp.write_text(text, encoding='utf-8')
    try:
        from weasyprint import HTML
        HTML(filename=str(tmp)).write_pdf(str(out))
    except Exception as e:
        raise SystemExit(f'PDF generation failed: {e}')
    # Clean common generator metadata when pypdf is available
    try:
        from pypdf import PdfReader, PdfWriter
        reader=PdfReader(str(out)); writer=PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.add_metadata({'/Title':'Premium Report','/Author':'','/Creator':'','/Producer':'','/Subject':'','/Keywords':''})
        cleaned=out.with_suffix('.clean.pdf')
        with cleaned.open('wb') as f: writer.write(f)
        cleaned.replace(out)
    except Exception:
        pass
    print(json.dumps({'status':'pass','pdf':str(out),'bytes':out.stat().st_size},ensure_ascii=False))
if __name__=='__main__': main()
