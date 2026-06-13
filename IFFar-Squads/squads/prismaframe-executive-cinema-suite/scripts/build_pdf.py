#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description='Export clean final HTML to PDF')
    ap.add_argument('--input', default=str(ROOT / 'generated/demo/final/print-ready.html'))
    ap.add_argument('--output', default=str(ROOT / 'generated/demo/final/presentation.pdf'))
    args = ap.parse_args()
    src = Path(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        from weasyprint import HTML
    except Exception as exc:
        print(json.dumps({'status': 'skip', 'reason': f'weasyprint unavailable: {exc}'}, ensure_ascii=False))
        return 0
    HTML(filename=str(src)).write_pdf(str(out))
    data = out.read_bytes()
    ok = data.startswith(b'%PDF-') and b'%%EOF' in data[-2048:] and len(data) > 5000
    report = {'status': 'pass' if ok else 'fail', 'pdf': str(out), 'bytes': len(data), 'header': data[:5].decode('latin1', 'ignore'), 'eof': b'%%EOF' in data[-2048:]}
    (ROOT / 'validation/pdf-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
