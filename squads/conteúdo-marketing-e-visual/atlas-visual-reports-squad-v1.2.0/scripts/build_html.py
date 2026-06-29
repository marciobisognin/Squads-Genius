#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, html, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def esc(s: str) -> str:
    return html.escape(str(s), quote=False)

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "report"

def md_inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s

def md_to_html(text: str) -> str:
    out=[]; in_ul=False
    def flush():
        nonlocal in_ul
        if in_ul:
            out.append('</ul>'); in_ul=False
    for line in text.splitlines():
        s=line.strip()
        if not s:
            flush(); continue
        if s.startswith('#'):
            flush(); level=min(len(s)-len(s.lstrip('#')),4); out.append(f'<h{level}>{md_inline(s[level:].strip())}</h{level}>')
        elif s.startswith('- '):
            if not in_ul: out.append('<ul>'); in_ul=True
            out.append(f'<li>{md_inline(s[2:])}</li>')
        elif re.match(r'^\d+\.\s+', s):
            if not in_ul: out.append('<ul>'); in_ul=True
            out.append(f'<li>{md_inline(re.sub(r"^\d+\.\s+", "", s))}</li>')
        else:
            flush(); out.append(f'<p>{md_inline(s)}</p>')
    flush(); return '\n'.join(out)

def extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith('# '): return line[2:].strip()
    return 'Relatório Premium'

def extract_bullets(text: str, limit=6):
    bullets=[re.sub(r'^[-*]\s+','',l.strip()) for l in text.splitlines() if re.match(r'^[-*]\s+', l.strip())]
    return bullets[:limit] or ['Tese executiva', 'Evidências principais', 'Riscos e oportunidades', 'Plano recomendado']

def load_json(path: Path | None, default):
    if path and path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return default

def kpi_cards(items):
    htmls=[]
    for i,item in enumerate(items[:4]):
        label=item.get('label') if isinstance(item,dict) else f'Indicador {i+1}'
        value=item.get('value') if isinstance(item,dict) else str(item)
        note=item.get('note','') if isinstance(item,dict) else ''
        htmls.append(f'<article class="kpi-card"><span>{esc(label)}</span><b>{esc(value)}</b><small>{esc(note)}</small></article>')
    while len(htmls)<4:
        htmls.append(f'<article class="kpi-card"><span>Camada {len(htmls)+1}</span><b>Visual-first</b><small>Componente executivo</small></article>')
    return ''.join(htmls)

def render(input_md: Path, out_dir: Path, brief_path: Path|None=None, data_path: Path|None=None, orientation='portrait'):
    text=read_text(input_md)
    title=extract_title(text)
    bullets=extract_bullets(text)
    brief=load_json(brief_path, {})
    data=load_json(data_path, {})
    thesis=brief.get('thesis') or (bullets[0] if bullets else 'Síntese executiva visual do relatório')
    kpis=data.get('kpis') or [{'label':'Documento','value':'1 relatório','note':'entrada original preservada'}, {'label':'Camadas','value':'3','note':'executiva, analítica e técnica'}, {'label':'QA','value':'ativo','note':'visual, PDF e conteúdo'}, {'label':'Formato','value':'HTML + PDF','note':'revisão antes da impressão'}]
    decision_map='<div class="roadmap">' + ''.join(f'<span>{esc(x)}</span>' for x in bullets[:4]) + '</div>'
    risk_matrix='<div class="risk-matrix">' + ''.join(f'<div class="risk-cell"><b>{esc(r.get("name", f"Risco {i+1}"))}</b><p>{esc(r.get("note","Mitigação e materialidade a validar."))}</p></div>' for i,r in enumerate((data.get('risks') or [{'name':'Densidade textual'},{'name':'Corte no PDF'},{'name':'Fonte ausente'},{'name':'Gráfico inadequado'}])[:4])) + '</div>'
    analytical_cards=''.join(f'<article class="insight-card"><h3>{esc(b)}</h3><p>Insight estruturado para análise visual, evidência, implicação e decisão.</p></article>' for b in bullets[:6])
    charts='<article class="panel"><h3>Seleção de gráficos</h3><p>Barras para comparação, linhas para tendência, heatmap para concentração, matriz para decisão.</p></article><article class="panel"><h3>Auditabilidade</h3><p>Números e fontes preservados no apêndice técnico.</p></article>'
    roadmap='<div class="roadmap"><span>Intake</span><span>Direção visual</span><span>Arquitetura editorial</span><span>HTML</span><span>PDF + QA</span></div>'
    appendix=md_to_html(text)
    css=read_text(ROOT/'templates'/'premium_report.css')
    exec_t=read_text(ROOT/'templates'/'executive-visual-layer.html')
    ana_t=read_text(ROOT/'templates'/'analytical-visual-layer.html')
    app_t=read_text(ROOT/'templates'/'technical-appendix.html')
    exec_html=exec_t.replace('{{title}}', esc(title)).replace('{{thesis}}', esc(thesis)).replace('{{kpi_cards}}', kpi_cards(kpis)).replace('{{decision_map}}', decision_map).replace('{{risk_matrix}}', risk_matrix)
    ana_html=ana_t.replace('{{analytical_cards}}', analytical_cards).replace('{{charts}}', charts).replace('{{roadmap}}', roadmap)
    app_html=app_t.replace('{{appendix_content}}', appendix)
    nav='<nav class="nav"><div class="shell"><a href="#executive">Executivo</a><a href="#analysis">Análise</a><a href="#appendix">Apêndice</a></div></nav>'
    cover=f'<header class="shell"><section class="cover"><div><span class="badge">Premium Report Design Squad · v1.2</span><h1>{esc(title)}</h1><p>{esc(thesis)}</p></div><div class="orb"><b>Visual<br>Decision<br>Report</b></div></section></header>'
    doc=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{css}</style></head><body>{nav}{cover}<main class="shell">{exec_html}{ana_html}{app_html}</main><footer class="footer">Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.</footer></body></html>'
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/'index.html').write_text(doc, encoding='utf-8')
    (out_dir/'styles.css').write_text(css, encoding='utf-8')
    spec={'title':title,'orientation':orientation,'source':str(input_md),'sha256':hashlib.sha256(text.encode()).hexdigest(),'layers':['executive','analytical','technical_appendix'],'status':'html_ready'}
    (out_dir/'visual_spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
    return out_dir/'index.html'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description='Build premium HTML report from Markdown')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--brief')
    ap.add_argument('--data-profile')
    ap.add_argument('--orientation', default='portrait', choices=['portrait','landscape'])
    args=ap.parse_args()
    p=render(Path(args.input), Path(args.output), Path(args.brief) if args.brief else None, Path(args.data_profile) if args.data_profile else None, args.orientation)
    print(json.dumps({'status':'pass','html':str(p)},ensure_ascii=False))
