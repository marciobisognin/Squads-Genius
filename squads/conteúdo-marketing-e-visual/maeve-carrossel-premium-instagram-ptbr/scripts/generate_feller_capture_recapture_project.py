#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math, re, html
from datetime import datetime

W,H=1080,1350
BG1=(8,25,43); BG2=(18,62,72); CREAM=(248,238,214); GOLD=(223,179,82); AQUA=(97,218,204); GREEN=(103,194,132); PINK=(233,103,143); BLUE=(71,150,214)
OUT=Path('/data/data/com.termux/files/home/squad-factory/workspaces/maeve-carrossel-premium-instagram-ptbr/output/feller-captura-recaptura-ptbr')
SLIDES=OUT/'slides'
SLIDES.mkdir(parents=True, exist_ok=True)

def font(size,bold=False):
    paths=[('/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf' if bold else '/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf'),('/system/fonts/Roboto-Bold.ttf' if bold else '/system/fonts/Roboto-Regular.ttf')]
    for p in paths:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def bg():
    small=Image.new('RGB',(108,135),BG1); px=small.load()
    for y in range(135):
        for x in range(108):
            t=x/108*.35+y/135*.65
            px[x,y]=tuple(int(BG1[i]*(1-t)+BG2[i]*t) for i in range(3))
    return small.resize((W,H),Image.Resampling.BICUBIC)

def wrap(d,text,fnt,width):
    lines=[]; cur=''
    for w in text.split():
        test=(cur+' '+w).strip()
        if d.textbbox((0,0),test,font=fnt)[2]<=width: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def text(d,xy,s,fnt,fill,width=None,gap=8,max_lines=None,center=False):
    x,y=xy
    lines=wrap(d,s,fnt,width) if width else s.split('\n')
    if max_lines: lines=lines[:max_lines]
    for line in lines:
        tx=x
        if center and width:
            bb=d.textbbox((0,0),line,font=fnt); tx=x+(width-(bb[2]-bb[0]))/2
        d.text((tx,y),line,font=fnt,fill=fill)
        y+=fnt.size+gap
    return y

def fish(d,x,y,marked=False,scale=1.0,alpha=255):
    col=(AQUA[0],AQUA[1],AQUA[2],alpha) if not marked else (GOLD[0],GOLD[1],GOLD[2],alpha)
    outline=(248,238,214,alpha)
    w=int(48*scale); h=int(24*scale)
    d.ellipse((x,y,x+w,y+h),fill=col,outline=outline,width=max(1,int(2*scale)))
    d.polygon([(x+w,y+h/2),(x+w+18*scale,y),(x+w+18*scale,y+h)],fill=col,outline=outline)
    d.ellipse((x+8*scale,y+7*scale,x+13*scale,y+12*scale),fill=(8,25,43,alpha))
    if marked:
        d.line((x+w*.45,y+4*scale,x+w*.45,y+h-4*scale),fill=(8,25,43,alpha),width=max(2,int(3*scale)))

def frame(d,num,total):
    d.rounded_rectangle((38,38,W-38,H-38),radius=36,outline=GOLD,width=3)
    d.text((70,70),'PIXEL GRID // FELLER • CAPTURA-RECAPTURA // INFOGRÁFICO',font=font(24,True),fill=(*CREAM,210))
    d.text((W-170,H-95),f'{num:02d}/{total:02d}',font=font(32,True),fill=GOLD)

def diagram(d,kind):
    if kind=='lake':
        d.rounded_rectangle((100,760,980,1110),radius=170,fill=(36,103,118,190),outline=AQUA,width=4)
        for i in range(36): fish(d,145+(i%9)*88,815+(i//9)*65,marked=i in [2,7,13,21,29],scale=.8,alpha=240)
        d.rounded_rectangle((620,780,910,842),radius=20,fill=(8,25,43,210),outline=GOLD,width=2)
        text(d,(642,795),'dourados = marcados',font(24,True),GOLD,245,center=True)
    elif kind=='steps':
        xs=[150,430,710]; labels=['1ª amostra\nmarca M','mistura\nno lago','2ª amostra\nacha R']
        for i,x in enumerate(xs):
            d.rounded_rectangle((x,790,x+220,1030),radius=30,fill=(255,255,255,28),outline=[GOLD,AQUA,GREEN][i],width=4)
            text(d,(x+18,835),labels[i],font(32,True),CREAM,180,gap=10,center=True)
            fish(d,x+75,950,marked=i!=1,scale=1.1)
            if i<2: d.line((x+230,910,x+270,910),fill=GOLD,width=6); d.polygon([(x+270,910),(x+250,895),(x+250,925)],fill=GOLD)
    elif kind=='formula':
        d.rounded_rectangle((115,760,965,1080),radius=38,fill=(255,255,255,30),outline=GOLD,width=4)
        text(d,(145,815),'proporção marcada no lago ≈ proporção marcada na 2ª amostra',font(34,True),CREAM,790,gap=12,center=True)
        text(d,(210,940),'M / N  ≈  R / n',font(64,True),GOLD,660,center=True)
        text(d,(230,1035),'então:  N ≈ M × n / R',font(40,True),AQUA,620,center=True)
    elif kind=='hyper':
        d.rounded_rectangle((95,735,985,1125),radius=42,fill=(255,255,255,28),outline=AQUA,width=4)
        text(d,(135,775),'Distribuição hipergeométrica',font(42,True),GOLD,810,center=True)
        text(d,(145,850),'Se o lago tivesse N peixes, qual a chance de observar R marcados na segunda amostra?',font(34,False),CREAM,790,gap=12,center=True)
        text(d,(170,990),'P(R=r) = C(M,r) C(N-M,n-r) / C(N,n)',font(34,True),AQUA,740,center=True)
        text(d,(165,1060),'N total • M marcados • n segunda amostra • R recapturados',font(24,True),CREAM,760,center=True)
    elif kind=='estimator':
        vals=[('M',100,GOLD),('n',80,AQUA),('R',20,PINK),('N?',400,GREEN)]
        for i,(lab,val,col) in enumerate(vals):
            x=115+i*240; d.rounded_rectangle((x,780,x+190,1015),radius=32,fill=(255,255,255,26),outline=col,width=4)
            text(d,(x+20,815),lab,font(50,True),col,150,center=True)
            text(d,(x+20,900),str(val),font(58,True),CREAM,150,center=True)
        text(d,(180,1060),'100 × 80 / 20 = 400 peixes estimados',font(38,True),GOLD,720,center=True)
    elif kind=='bias':
        for i,(lab,col,h) in enumerate([('poucos\nrecapturados',PINK,260),('muitos\nrecapturados',GREEN,120)]):
            x=220+i*360; d.rounded_rectangle((x,760,x+240,1100),radius=32,fill=(255,255,255,24),outline=col,width=4)
            d.rectangle((x+90,1050-h,x+150,1050),fill=col)
            text(d,(x+35,790),lab,font(32,True),CREAM,170,center=True)
    else:
        d.rounded_rectangle((105,760,975,1110),radius=42,fill=(255,255,255,26),outline=GOLD,width=4)
        for i in range(5):
            x=160+i*160; d.ellipse((x,880,x+90,970),outline=[GOLD,AQUA,GREEN,PINK,BLUE][i],width=6)
            d.line((x+90,925,x+140,925),fill=CREAM,width=3)
        text(d,(165,1010),'observa → marca → mistura → recaptura → estima',font(32,True),CREAM,750,center=True)

def html_slide(s,total):
    safe_body=html.escape(s['body']); safe_title=html.escape(s['title'])
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{safe_title}</title><style>body{{margin:0;background:#08192B}}.slide{{width:1080px;height:1350px;background:linear-gradient(145deg,#08192B,#123E48);color:#F8EED6;font-family:Inter,Arial,sans-serif;padding:70px;box-sizing:border-box}}.frame{{height:1210px;border:3px solid #DFB352;border-radius:36px;padding:42px}}.k{{color:#DFB352;letter-spacing:3px;font-weight:800}}h1{{font-size:78px;line-height:.94;letter-spacing:-2px;max-width:860px}}p{{font-size:38px;line-height:1.18;color:#F8EED6;max-width:850px}}.card{{margin-top:70px;border:2px solid #61DACC;border-radius:36px;padding:35px;background:rgba(255,255,255,.08);font-size:34px}}.page{{position:absolute;right:80px;bottom:70px;color:#DFB352;font-weight:800;font-size:32px}}</style></head><body><main class="slide"><section class="frame"><div class="k">▣ FELLER • CAPTURA-RECAPTURA ▣</div><h1>{safe_title}</h1><p>{safe_body}</p><div class="card">Infográfico: lago fechado + peixes marcados + recaptura + estimativa.</div><div class="page">{s['num']:02d}/{total:02d}</div></section></main></body></html>'''

slides=[
('O lago invisível','Como estimar quantos peixes existem se não dá para contar um por um? A estatística resolve olhando uma parte bem escolhida.','lake'),
('A ideia de Feller','Capture alguns peixes, marque, solte de volta e espere eles se misturarem. Depois capture outra amostra.','steps'),
('O segredo está na proporção','Se muitos marcados reaparecem, o lago provavelmente é menor. Se poucos reaparecem, o lago provavelmente é maior.','formula'),
('Primeira amostra: M','M é a quantidade de peixes marcados na primeira captura. Eles viram “sinalizadores” dentro do lago.','lake'),
('Segunda amostra: n','Depois da mistura, capturamos n peixes. Alguns terão a marca; outros não. Essa mistura carrega informação.','steps'),
('Recapturados: R','R é a quantidade de peixes marcados encontrados na segunda amostra. Ele é o número-chave da estimativa.','estimator'),
('Estimativa intuitiva','A fração de marcados na amostra deve parecer a fração de marcados no lago: M/N ≈ R/n.','formula'),
('A fórmula prática','Reorganizando a proporção, obtemos N ≈ M × n / R. É uma regra simples para estimar o total oculto.','estimator'),
('Onde entra a hipergeométrica?','A distribuição hipergeométrica calcula a chance de recapturar R marcados quando retiramos n peixes de uma população finita sem reposição.','hyper'),
('Exemplo numérico','Se marquei 100, recapturei 80 e encontrei 20 marcados, a estimativa é 100×80/20 = 400 peixes.','estimator'),
('Condições importantes','O lago precisa ser fechado, as marcas não podem desaparecer, e os peixes marcados devem se misturar como os outros.','bias'),
('O poder do método','A captura-recaptura mostra como uma pequena amostra pode revelar uma população inteira — quando o modelo é bem usado.','flow')]
manifest={'generated_at':datetime.now().isoformat(),'language':'pt-BR','topic':'Problema de captura-recaptura de Feller','slides':[],'size':'1080x1350'}
roteiro=['# Roteiro — Problema de captura-recaptura de Feller\n']
for i,(title,body,kind) in enumerate(slides,1):
    im=bg(); d=ImageDraw.Draw(im,'RGBA'); frame(d,i,len(slides))
    y=text(d,(74,155),title,font(74,True),CREAM,880,gap=4,max_lines=3)
    text(d,(80,y+26),body,font(38,False),(*CREAM,245),850,gap=12,max_lines=4)
    diagram(d,kind)
    # bottom tag
    d.rounded_rectangle((80,1140,840,1212),radius=24,fill=(255,255,255,18),outline=(*AQUA,120),width=1)
    text(d,(110,1158),'estatística visual • amostragem • probabilidade',font(27,True),AQUA,700)
    png=SLIDES/f'slide-{i:02d}.png'; jpg=SLIDES/f'slide-{i:02d}-premium.jpg'; hp=SLIDES/f'slide-{i:02d}.html'
    im.save(png,quality=96); im.save(jpg,quality=95); hp.write_text(html_slide({'num':i,'title':title,'body':body},len(slides)),encoding='utf-8')
    roteiro.append(f'## Slide {i:02d}\n\n**{title}**\n\n{body}\n')
    manifest['slides'].append({'num':i,'title':title,'body':body,'html':str(hp.relative_to(OUT)),'png':str(png.relative_to(OUT)),'jpg':str(jpg.relative_to(OUT))})
(OUT/'roteiro.md').write_text('\n'.join(roteiro),encoding='utf-8')
(OUT/'carrossel-feller-captura-recaptura.md').write_text('\n'.join(roteiro),encoding='utf-8')
(OUT/'legenda.txt').write_text('''Como estimar uma população que você não consegue contar diretamente?\n\nO problema de captura-recaptura, apresentado por Feller, mostra uma resposta elegante: marcar uma primeira amostra, misturar novamente no ambiente e observar quantos marcados reaparecem na segunda captura.\n\nA intuição é simples: se muitos marcados voltam, a população tende a ser menor; se poucos voltam, ela tende a ser maior. Por trás disso está a distribuição hipergeométrica, que modela retiradas sem reposição em uma população finita.\n\nSalve este infográfico para revisar estatística e probabilidade de um jeito visual.\n''',encoding='utf-8')
(OUT/'hashtags.txt').write_text('#estatistica #probabilidade #capturarecaptura #feller #hipergeometrica #infografico #matematica #cienciadedados #educacao #ptbr #instagrameducativo\n',encoding='utf-8')
(OUT/'source-log.txt').write_text('''Fonte conceitual: solicitação do usuário sobre Feller\'s Capture-Recapture Problem.\nTema: método de captura-recaptura, amostragens sequenciais e distribuição hipergeométrica para estimar população fechada.\nExemplo usado: peixes marcados em um lago fechado.\n''',encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ok':True,'output':str(OUT),'slides':len(slides)},ensure_ascii=False))
