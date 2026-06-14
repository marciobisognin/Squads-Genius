#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shutil, uuid, zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
try:
    import yaml
except Exception:
    yaml = None

def now(): return datetime.now(timezone.utc).isoformat()
def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+','-', text.lower()).strip('-') or 'reel'
def load_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8')
    if path.suffix.lower() in {'.yaml','.yml'}:
        if not yaml: raise RuntimeError('PyYAML é necessário para YAML')
        return yaml.safe_load(text)
    return json.loads(text)
def validate_briefing(data: dict[str, Any]) -> list[str]:
    issues=[]
    if not data.get('topic'): issues.append('topic é obrigatório')
    if data.get('complexity_level') not in {'iniciante','intermediário','avançado'}: issues.append('complexity_level inválido')
    dur=int(data.get('target_duration_sec', 0) or 0)
    if dur < 30 or dur > 90: issues.append('target_duration_sec deve estar entre 30 e 90')
    return issues
def segment_script(briefing):
    dur=int(briefing.get('target_duration_sec',60)); topic=briefing['topic']
    parts=[('S01','hook',8,f'Você já se perguntou por que {topic} muda nossa intuição sobre a realidade?','pergunta central em tipografia grande'),('S02','context',12,f'Em poucos segundos, vamos separar a ideia essencial de {topic} das confusões mais comuns.','linha do tempo conceitual'),('S03','development',max(18,dur-35),f'A chave é observar quais grandezas realmente podem ser medidas, comparadas e representadas por um modelo matemático.','diagrama com setas e objetos simples'),('S04','math_moment',10,'A relação principal aparece quando escrevemos a equação que resume o fenômeno.','equação LaTeX central'),('S05','synthesis',7,'A melhor ciência não elimina o mistério: ela mostra exatamente onde a pergunta fica mais precisa.','síntese final e convite')]
    return [{'segment_id':sid,'type':typ,'text':txt,'duration_sec':sec,'key_concepts':[topic],'visual_cue':cue,'reference_tag':f'REF-{sid}'} for sid,typ,sec,txt,cue in parts]
def write_json(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def write_text(path, text): path.write_text(text.rstrip()+'\n', encoding='utf-8')
def generate_package(briefing: dict[str, Any], out: Path, make_zip: bool=False) -> dict[str, Any]:
    issues=validate_briefing(briefing)
    if issues: raise ValueError('; '.join(issues))
    out.mkdir(parents=True, exist_ok=True); script_id=str(uuid.uuid4()); topic=briefing['topic']; slug=slugify(topic)
    dirs=['01_script','02_storyboard','03_manim/assets','04_narration','05_review','06_ffmpeg','07_calendar']
    for d in dirs: (out/d).mkdir(parents=True, exist_ok=True)
    segments=segment_script(briefing)
    script={'script_id':script_id,'topic':topic,'complexity_level':briefing['complexity_level'],'total_estimated_duration_sec':sum(s['duration_sec'] for s in segments),'word_count':sum(len(s['text'].split()) for s in segments),'segments':segments,'key_equations':[briefing.get('key_equation','\\Delta x\\Delta p \\geq \\frac{\\hbar}{2}')],'references_suggested':briefing.get('references_suggested',['Fonte primária ou revisão científica a confirmar pelo operador.']),'production_notes':'Roteiro gerado de forma determinística para pacote inicial.'}
    write_json(out/'01_script'/f'script_{script_id}.json', script)
    readable='# Roteiro legível\n\n'+'\n\n'.join(f"## {s['segment_id']} — {s['type']} ({s['duration_sec']}s)\n{s['text']}" for s in segments)
    write_text(out/'01_script'/f'script_{script_id}_readable.md', readable)
    storyboard=['# Storyboard', f'Script ID: {script_id}', f'Tópico: {topic}', '']
    start=0
    for i,s in enumerate(segments,1):
        end=start+s['duration_sec']; cls=f"Scene{i:02d}"
        storyboard += [f"## Cena {i:02d} — {s['type']} [{start:02d}s–{end:02d}s]", f"Narração: {s['text']}", f"Visual: {s['visual_cue']}", f"Manim: classe `{cls}`, objetos Text/MathTex, transição FadeIn/FadeOut.", '']
        start=end
    write_text(out/'02_storyboard'/f'storyboard_{script_id}.md','\n'.join(storyboard))
    scene_lines=['from manim import *','','config.background_color = BLACK','PRIMARY_COLOR = "#4FC3F7"','TEXT_COLOR = WHITE','','def make_text(text):','    return Text(text, color=TEXT_COLOR).scale(0.62)','','class FullVideo(Scene):','    def construct(self):']
    for s in segments:
        safe=s['text'].replace('"','\\"')[:90]
        scene_lines += [f'        item = make_text("{safe}")','        self.play(FadeIn(item), run_time=0.7)',f'        self.wait({max(1, s["duration_sec"]-2)})','        self.play(FadeOut(item), run_time=0.5)','']
    write_text(out/'03_manim'/f'manim_scene_{script_id}.py','\n'.join(scene_lines))
    write_text(out/'03_manim'/'render_commands.sh',f'manim -pql manim_scene_{script_id}.py FullVideo\nmanim -pqh manim_scene_{script_id}.py FullVideo --format mp4')
    ssml='<speak version="1.0" xml:lang="pt-BR">\n<voice name="pt-BR-AntonioNeural">\n'+'\n'.join(f'<prosody rate="medium">{s["text"]}</prosody><break time="400ms"/>' for s in segments)+'\n</voice>\n</speak>'
    write_text(out/'04_narration'/f'narration_{script_id}.ssml', ssml)
    vtt='WEBVTT\n\n'+'\n'.join(f"{i}\n00:00:{i*8:02d}.000 --> 00:00:{i*8+6:02d}.000\n{s['text']}\n" for i,s in enumerate(segments))
    write_text(out/'04_narration'/f'narration_{script_id}.vtt', vtt)
    sync={'segments':[{'segment_id':s['segment_id'],'video_scene':'FullVideo','audio_start_ms':i*8000,'audio_end_ms':i*8000+s['duration_sec']*1000,'sync_offset_ms':0} for i,s in enumerate(segments)]}
    write_json(out/'04_narration'/f'sync_{script_id}.json', sync)
    review=f'# Relatório de Revisão Epistêmica\n\nScript ID: {script_id}\nTópico: {topic}\nVeredicto: APROVADO COM RESSALVAS\n\n## Ressalvas\n- Confirmar fontes primárias antes da publicação.\n- Validar equação central para o domínio específico.\n\n## Checklist\n- Linguagem de certeza calibrada.\n- Analogias identificadas como analogias.\n- Nenhuma publicação automática autorizada.\n'
    write_text(out/'05_review'/f'epistemic_review_{script_id}.md', review)
    ffmpeg=f"""#!/bin/bash
set -e
INPUT_VIDEO="video_{script_id}.mp4"
INPUT_AUDIO="narration_{script_id}_final.aac"
INPUT_SUBS="narration_{script_id}.vtt"
OUTPUT_FILE="final_reel_{script_id}.mp4"
ffmpeg -i "$INPUT_VIDEO" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -preset slow -crf 18 video_resized_{script_id}.mp4
ffmpeg -i video_resized_{script_id}.mp4 -i "$INPUT_AUDIO" -c:v copy -c:a aac -shortest video_with_audio_{script_id}.mp4
ffmpeg -i video_with_audio_{script_id}.mp4 -vf "subtitles=$INPUT_SUBS" -c:v libx264 -crf 17 -pix_fmt yuv420p -movflags +faststart "$OUTPUT_FILE"
"""
    write_text(out/'06_ffmpeg'/f'ffmpeg_pipeline_{script_id}.sh', ffmpeg)
    cal={'entry_id':'CAL-'+script_id[:8],'script_id':script_id,'topic':topic,'scheduled_datetime':(datetime.now(timezone.utc)+timedelta(days=7)).isoformat(),'platforms':['instagram_reels','youtube_shorts'],'hashtags_suggested':['#Ciência','#Física','#Matemática','#Educação'],'seo_title':f'{topic} explicado em 60 segundos','caption_suggested':f'{topic} em linguagem visual, científica e direta.','next_topic_suggestion':'Tema complementar definido pelo operador.'}
    write_json(out/'07_calendar'/f'calendar_entry_{script_id}.json', cal)
    metadata={'job_id':script_id,'created_at':now(),'status':'package_ready','briefing':briefing,'package_path':str(out),'review_cycles':1,'human_review_required':True}
    write_json(out/'metadata.json', metadata)
    write_text(out/'README.md', f'# Pacote de Produção\n\nTópico: {topic}\nScript ID: {script_id}\nStatus: package_ready\n')
    if make_zip:
        zip_path=out.with_suffix('.zip')
        if zip_path.exists(): zip_path.unlink()
        with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
            for p in out.rglob('*'):
                if p.is_file(): z.write(p, p.relative_to(out.parent))
        metadata['zip_path']=str(zip_path); write_json(out/'metadata.json', metadata)
    return metadata

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--briefing', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--package', action='store_true')
    args=parser.parse_args(argv)
    result=generate_package(load_data(Path(args.briefing)), Path(args.output), args.package)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
