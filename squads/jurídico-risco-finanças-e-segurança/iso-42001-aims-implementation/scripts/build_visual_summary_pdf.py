#!/usr/bin/env python3
from pathlib import Path
import re, html
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
BASE = Path('/data/data/com.termux/files/home/squad-factory/workspaces/iso-42001-aims-implementation')
SRC = BASE/'docs/RESUMO_VISUAL_DETALHADO.md'
OUT_DIR = Path('/storage/emulated/0/Download/Material herme/squads')
PDF = OUT_DIR/'iso-42001-aims-implementation-resumo-visual.pdf'
HTML = OUT_DIR/'iso-42001-aims-implementation-resumo-visual.html'
FONT_DIR = Path('/data/data/com.termux/files/usr/share/fonts/TTF')

def reg_fonts():
    reg = FONT_DIR/'DejaVuSans.ttf'; bold = FONT_DIR/'DejaVuSans-Bold.ttf'; mono=FONT_DIR/'DejaVuSansMono.ttf'
    if reg.exists(): pdfmetrics.registerFont(TTFont('MaeveSans', str(reg)))
    if bold.exists(): pdfmetrics.registerFont(TTFont('MaeveSans-Bold', str(bold)))
    if mono.exists(): pdfmetrics.registerFont(TTFont('MaeveMono', str(mono)))
    return ('MaeveSans' if reg.exists() else 'Helvetica', 'MaeveSans-Bold' if bold.exists() else 'Helvetica-Bold', 'MaeveMono' if mono.exists() else 'Courier')
REG,BOLD,MONO = reg_fonts()
PALETTE={
 'navy': colors.HexColor('#0F172A'), 'blue': colors.HexColor('#2563EB'), 'sky': colors.HexColor('#E0F2FE'),
 'mint': colors.HexColor('#DCFCE7'), 'amber': colors.HexColor('#FEF3C7'), 'rose': colors.HexColor('#FFE4E6'),
 'violet': colors.HexColor('#EDE9FE'), 'ink': colors.HexColor('#1F2937'), 'muted': colors.HexColor('#64748B'),
 'line': colors.HexColor('#CBD5E1'), 'paper': colors.HexColor('#FFFDF7'), 'white': colors.white
}

def esc(s):
    s=html.escape(s.strip())
    s=re.sub(r'`([^`]+)`', r'<font face="%s" color="#1D4ED8">\1</font>'%MONO, s)
    s=re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s

def styles():
    return {
      'title': ParagraphStyle('title', fontName=BOLD, fontSize=24, leading=30, textColor=PALETTE['white'], alignment=TA_CENTER, spaceAfter=10),
      'subtitle': ParagraphStyle('subtitle', fontName=REG, fontSize=11.5, leading=15, textColor=PALETTE['sky'], alignment=TA_CENTER),
      'h2': ParagraphStyle('h2', fontName=BOLD, fontSize=15.5, leading=20, textColor=PALETTE['navy'], spaceBefore=12, spaceAfter=7),
      'h3': ParagraphStyle('h3', fontName=BOLD, fontSize=12.7, leading=16, textColor=PALETTE['blue'], spaceBefore=7, spaceAfter=4),
      'p': ParagraphStyle('p', fontName=REG, fontSize=9.8, leading=14, textColor=PALETTE['ink'], spaceAfter=5),
      'bullet': ParagraphStyle('bullet', fontName=REG, fontSize=9.5, leading=13.5, leftIndent=13, firstLineIndent=-8, textColor=PALETTE['ink'], spaceAfter=3),
      'quote': ParagraphStyle('quote', fontName=BOLD, fontSize=11, leading=15, textColor=PALETTE['navy'], leftIndent=8, rightIndent=8, alignment=TA_LEFT, spaceBefore=5, spaceAfter=7),
      'code': ParagraphStyle('code', fontName=MONO, fontSize=7.8, leading=10.2, textColor=colors.HexColor('#E5E7EB'), backColor=colors.HexColor('#111827'), borderPadding=6, leftIndent=0, rightIndent=0, spaceBefore=4, spaceAfter=7),
      'small': ParagraphStyle('small', fontName=REG, fontSize=7.5, leading=9.5, textColor=PALETTE['muted'], alignment=TA_CENTER),
    }
S=styles()

def page_bg(c, doc):
    c.saveState(); w,h=A4
    c.setFillColor(PALETTE['paper']); c.rect(0,0,w,h,stroke=0,fill=1)
    c.setFillColor(PALETTE['navy']); c.rect(0,h-2.0*cm,w,2.0*cm,stroke=0,fill=1)
    c.setFillColor(PALETTE['blue']); c.circle(1.2*cm,h-1.0*cm,0.18*cm,stroke=0,fill=1)
    c.setFillColor(PALETTE['mint']); c.circle(w-1.2*cm,h-1.0*cm,0.18*cm,stroke=0,fill=1)
    c.setStrokeColor(PALETTE['line']); c.line(1.3*cm,1.15*cm,w-1.3*cm,1.15*cm)
    c.setFont(REG,7.4); c.setFillColor(PALETTE['muted'])
    c.drawCentredString(w/2,0.72*cm, f"ISO 42001 AIMS Implementation Squad • Página {doc.page} • {FOOTER}")
    c.restoreState()

def card(flowables, bg, border=None):
    data=[[flowables]]
    t=Table(data, colWidths=[16.2*cm])
    t.setStyle(TableStyle([
      ('BACKGROUND',(0,0),(-1,-1),bg), ('BOX',(0,0),(-1,-1),0.8,border or PALETTE['line']),
      ('LEFTPADDING',(0,0),(-1,-1),10), ('RIGHTPADDING',(0,0),(-1,-1),10), ('TOPPADDING',(0,0),(-1,-1),8), ('BOTTOMPADDING',(0,0),(-1,-1),8)
    ]))
    return t

def parse(md):
    lines=md.splitlines(); story=[]; code=[]; in_code=False
    # cover
    story.append(Spacer(1,0.55*cm))
    story.append(Paragraph('ISO 42001 AIMS<br/>Implementation Squad', S['title']))
    story.append(Paragraph('Resumo visual detalhado • Governança de IA • Risco contratual • Exemplo concreto', S['subtitle']))
    story.append(Spacer(1,0.75*cm))
    story.append(card([Paragraph('<b>Ideia-força:</b> transformar IA invisível e arriscada em governança rastreável, vendável e auditável.', S['quote'])], PALETTE['sky'], PALETTE['blue']))
    story.append(Spacer(1,0.25*cm))
    story.append(card([Paragraph('<b>Aplicação concreta:</b> SaaS B2B com 5 produtos LLM precisa responder uma RFP enterprise com inventário, riscos, AIIA, SoA e evidências.', S['p'])], PALETTE['mint']))
    story.append(PageBreak())
    for line in lines:
        if line.startswith('# '):
            continue
        if line.strip().startswith('```'):
            if not in_code:
                in_code=True; code=[]
            else:
                in_code=False
                story.append(Paragraph('<br/>'.join(html.escape(x) for x in code), S['code']))
            continue
        if in_code:
            code.append(line); continue
        if not line.strip():
            continue
        if line.startswith('---'):
            story.append(Spacer(1,0.14*cm)); continue
        if line.startswith('## '):
            story.append(Paragraph(esc(line[3:]), S['h2'])); continue
        if line.startswith('### '):
            story.append(Paragraph(esc(line[4:]), S['h3'])); continue
        if line.startswith('> '):
            story.append(card([Paragraph(esc(line[2:]), S['quote'])], PALETTE['amber'])); story.append(Spacer(1,0.08*cm)); continue
        if line.startswith('- '):
            story.append(Paragraph('• '+esc(line[2:]), S['bullet'])); continue
        if re.match(r'^\d+\. ', line.strip()):
            story.append(Paragraph(esc(line.strip()), S['bullet'])); continue
        # highlight sentence
        if line.startswith('**') and line.endswith('**'):
            story.append(card([Paragraph(esc(line), S['quote'])], PALETTE['violet'])); continue
        story.append(Paragraph(esc(line), S['p']))
    return story

def build_html(md):
    body = html.escape(md)
    # simple md-ish to html after escaping
    body = re.sub(r'^# (.*)$', r'<h1>\1</h1>', body, flags=re.M)
    body = re.sub(r'^## (.*)$', r'<h2>\1</h2>', body, flags=re.M)
    body = re.sub(r'^### (.*)$', r'<h3>\1</h3>', body, flags=re.M)
    body = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', body)
    body = body.replace('\n', '<br>\n')
    css='''body{font-family:Arial,sans-serif;background:#FFFDF7;color:#1F2937;line-height:1.55;max-width:980px;margin:0 auto;padding:32px}h1{background:#0F172A;color:white;padding:32px;border-radius:24px;text-align:center}h2{color:#0F172A;border-left:8px solid #2563EB;padding-left:12px;margin-top:30px}h3{color:#2563EB}.card{background:#E0F2FE;border:1px solid #CBD5E1;border-radius:18px;padding:16px}code{background:#111827;color:#E5E7EB;padding:2px 5px;border-radius:5px}'''
    HTML.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>', encoding='utf-8')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md=SRC.read_text(encoding='utf-8')
    build_html(md)
    doc=BaseDocTemplate(str(PDF), pagesize=A4, leftMargin=1.55*cm, rightMargin=1.55*cm, topMargin=2.45*cm, bottomMargin=1.55*cm)
    frame=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=page_bg)])
    story=parse(md)
    doc.build(story)
    print({'pdf':str(PDF),'html':str(HTML),'bytes':PDF.stat().st_size})
if __name__=='__main__': main()
