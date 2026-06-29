#!/usr/bin/env python3
from pathlib import Path
import argparse, html, re

def md_to_html(md):
    out=[]
    in_list=False
    for line in md.splitlines():
        s=line.strip()
        if not s:
            continue
        if s.startswith('# '): out.append(f'<h1>{html.escape(s[2:])}</h1>')
        elif s.startswith('## '): out.append(f'<h2>{html.escape(s[3:])}</h2>')
        elif s.startswith('- '): out.append(f'<p>• {html.escape(s[2:])}</p>')
        else: out.append(f'<p>{html.escape(s)}</p>')
    return '\n'.join(out)

def section_items(md, name, fallback):
    items=[]; capture=False
    for line in md.splitlines():
        s=line.strip()
        if s.lower().startswith('## '):
            capture=name.lower() in s.lower(); continue
        if capture and s.startswith('- '): items.append(s[2:])
        elif capture and s and not s.startswith('#'): items.append(s)
    return items or fallback

def esc(x): return html.escape(str(x))

def parse_finding(s):
    sev='MEDIUM'; lab='INFERRED'; text=s
    m=re.match(r'\[(HIGH|MEDIUM|LOW)\]\[(CONFIRMED|INFERRED|SPECULATED)\]\s*(.*)',s,re.I)
    if m: sev,lab,text=m.group(1).upper(),m.group(2).upper(),m.group(3)
    return sev,lab,text

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output-dir',required=True)
    ap.add_argument('--title',default='Relatório Premium')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    md=Path(args.input).read_text(encoding='utf-8')
    css=(root/'templates'/'pdf_print.css').read_text(encoding='utf-8')
    tpl=(root/'templates'/'report_template.html').read_text(encoding='utf-8')
    kpis=section_items(md,'kpis',['3 camadas','HTML revisável','PDF A4','QA visual'])[:6]
    findings=section_items(md,'findings',['[HIGH][INFERRED] Achado crítico sem evidência completa','[MEDIUM][SPECULATED] Gap de compliance pendente'])[:8]
    controls=section_items(md,'controles',['Processo | Risco | Controle | Evidência | Status'])[:8]
    compliance=section_items(md,'compliance',['LGPD — parcial','Controles internos — parcial','Cyber baseline — pendente','Governança IA — não conforme'])[:8]
    risks=section_items(md,'riscos',['Risco operacional','Risco regulatório','Risco reputacional'])[:6]
    kpi_cards=''.join([f'<article class="card"><div class="kpi">{i+1}</div><b>{esc(x)}</b><p class="small">Indicador extraído do relatório.</p><div class="bar"></div></article>' for i,x in enumerate(kpis)])
    finding_cards=[]
    for x in findings:
        sev,lab,text=parse_finding(x)
        klass={'HIGH':'sev-high','MEDIUM':'sev-medium','LOW':'sev-low'}.get(sev,'sev-medium')
        finding_cards.append(f'<article class="card {klass}"><b>{esc(text)}</b><p><span class="pill">{sev}</span><span class="pill">{lab}</span></p><p class="small">Impacto e causa raiz devem ser validados na auditoria de evidência.</p></article>')
    finding_cards=''.join(finding_cards)
    cells=[]
    for i in range(25):
        label=''
        if i < len(risks): label=risks[i][:42]
        cells.append(f'<div class="cell">{esc(label)}</div>')
    heatmap='<div class="heatmap">'+''.join(cells)+'</div><p class="small">Matriz 5×5 de impacto × probabilidade para priorização executiva.</p>'
    score_items=''.join([f'<div class="score"><b>{esc(x.split("—")[0].strip())}</b><p class="small">{esc(x)}</p></div>' for x in compliance])
    compliance_scorecard=f'<section class="card"><h3>Compliance scorecard</h3><div class="score-grid">{score_items}</div></section>'
    rows=[]
    for c in controls:
        parts=[p.strip() for p in c.split('|')]
        while len(parts)<4: parts.append('pendente')
        rows.append('<div class="matrix-row">' + ''.join(f'<div>{esc(p)}</div>' for p in parts[:4]) + '</div>')
    control_matrix='<section class="card"><h3>Matriz de controles</h3><div class="matrix-row"><b>Processo</b><b>Risco</b><b>Controle</b><b>Evidência</b></div>'+''.join(rows)+'</section>'
    maturity_radar='<section class="card"><h3>Radar de maturidade</h3>' + ''.join([f'<p>{esc(x)}<div class="bar" style="width:{40+i*10}%"></div></p>' for i,x in enumerate(['Governança','Dados','Controles','Tecnologia','Reporting'])]) + '</section>'
    mindmap_nodes=''.join([f'<span class="node">{esc(x)}</span>' for x in ['Escopo','Critérios','Evidências','Findings','Riscos','Controles','Roadmap']])
    flow_nodes=''.join([f'<span class="node">{esc(x)}</span>' for x in ['30 dias','60 dias','90 dias','Owner','Evidência','QA']])
    html_doc=tpl.replace('{{title}}',esc(args.title)).replace('{{subtitle}}','Relatório executivo com camada Big Four de auditoria, compliance, risco e trilha de evidência.').replace('{{css}}',css).replace('{{kpi_cards}}',kpi_cards).replace('{{mindmap_nodes}}',mindmap_nodes).replace('{{finding_cards}}',finding_cards).replace('{{heatmap}}',heatmap).replace('{{compliance_scorecard}}',compliance_scorecard).replace('{{control_matrix}}',control_matrix).replace('{{maturity_radar}}',maturity_radar).replace('{{flow_nodes}}',flow_nodes).replace('{{appendix}}',md_to_html(md))
    (out/'index.html').write_text(html_doc,encoding='utf-8')
    try:
        from weasyprint import HTML
        HTML(string=html_doc, base_url=str(out)).write_pdf(out/'report.pdf')
    except Exception as e:
        (out/'PDF_NOT_GENERATED.txt').write_text(str(e),encoding='utf-8')
    print(out/'index.html')
    if (out/'report.pdf').exists(): print(out/'report.pdf')
if __name__=='__main__': main()
