#!/usr/bin/env python3
import argparse, json, shutil
from pathlib import Path
def read_briefing(path):
    text=Path(path).read_text(encoding='utf-8')
    try: return json.loads(text)
    except Exception:
        data={}
        for line in text.splitlines():
            if ':' in line and not line.strip().startswith('#'):
                k,v=line.split(':',1); data[k.strip()]=v.strip().strip('"')
        return data
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--briefing',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    b=read_briefing(args.briefing); out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    name=b.get('project_name','Projeto sem nome')
    footer='Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.'
    (out/'01_briefing_map.md').write_text(f'# Mapa de briefing\n\nProjeto: {name}\n\nObjetivo: {b.get("objective","")}\n\nPúblico: {b.get("audience","")}\n\nHipóteses: validar público, canal e critério de sucesso.\n\n{footer}\n',encoding='utf-8')
    (out/'02_research_plan.md').write_text('# Plano de pesquisa\n\n## Observado\nBriefing recebido.\n\n## Inferido\nNecessidade de fontes públicas e validação humana.\n\n## Recomendações\nListar 5 fontes primárias e 3 concorrentes antes da execução comercial.\n',encoding='utf-8')
    (out/'03_design_system_seed.json').write_text(json.dumps({'project':name,'palette':['#0B1020','#2525FF','#F5B84B','#F8FAFC'],'components':['hero','card','cta','evidence-box'],'originality_rule':'referências não devem ser copiadas'},ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'04_monetization_pack.md').write_text(f'# Monetization Pack — {name}\n\n- Oferta mínima: diagnóstico + ativo operacional + treinamento.\n- Precificação inicial: pacote fechado ou sprint.\n- Upsell: manutenção mensal e variações verticais.\n\n{footer}\n',encoding='utf-8')
    (out/'quality_report.json').write_text(json.dumps({'go_no_go':'go-with-human-review','issues':[],'recommendations':['executar pesquisa real com fontes antes de venda']},ensure_ascii=False,indent=2),encoding='utf-8')
    print(str(out))
if __name__=='__main__': main()
