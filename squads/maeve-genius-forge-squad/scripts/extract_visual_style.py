#!/usr/bin/env python3
import argparse, re, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',default='output/visual_style_report.json'); args=ap.parse_args()
    txt=Path(args.input).read_text(encoding='utf-8',errors='ignore')
    colors=sorted(set(re.findall(r'#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)',txt)))[:30]
    fonts=sorted(set(re.findall(r'font-family\s*:\s*([^;\n}]+)',txt,re.I)))[:20]
    report={'observed_colors':colors,'observed_fonts':fonts,'recommendation':'usar como referência analítica; gerar identidade original, sem cópia literal.'}
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
