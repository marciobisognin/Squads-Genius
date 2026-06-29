#!/usr/bin/env python3
from pathlib import Path
import argparse, json, csv, datetime

REQUIRED_AI_RESPONSE_FOOTER = 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.'

try:
    import yaml
except Exception:
    yaml=None

def load_profile(path):
    text=Path(path).read_text(encoding='utf-8')
    if yaml:
        return yaml.safe_load(text)
    data={}
    for line in text.splitlines():
        if ':' in line and not line.startswith(' '):
            k,v=line.split(':',1); data[k.strip()]=v.strip().strip('"')
    return data

def clamp_minutes(raw):
    try: m=int(float(raw))
    except Exception: m=12
    return max(10, min(15, m))

def score_domain(profile):
    diary=(profile.get('diario_curto','')+' '+profile.get('dificuldade_percebida','')).lower()
    domains={
        'linguagem_clara': 50,
        'abstracao_modelos': 50,
        'metacognicao': 50,
        'consistencia_habito': 50,
        'raciocinio_logico': 50,
        'foco_execucao': 50,
    }
    signals={
        'linguagem_clara':['linguagem','clara','explicar','organizar','verbal'],
        'abstracao_modelos':['abstra','modelo','conceito','complexo','analog'],
        'metacognicao':['gap','processo mental','perceber','metacog'],
        'consistencia_habito':['repet','constância','procrast','hábito','rotina'],
        'raciocinio_logico':['problema','raciocínio','lógico','decidir'],
        'foco_execucao':['foco','atenção','distra','iniciar']
    }
    for d, words in signals.items():
        for word in words:
            if word in diary: domains[d]-=5
    last=profile.get('ultimo_resultado',{}) if isinstance(profile.get('ultimo_resultado',{}),dict) else {}
    foco=float(last.get('foco_0_10', profile.get('foco_0_10',6)) or 6)
    domains['foco_execucao'] += (foco-5)*4
    for d in domains: domains[d]=max(10,min(90,round(domains[d],1)))
    return domains

def choose_focus(domains):
    return sorted(domains.items(), key=lambda x:x[1])[0]

def allocate(minutes):
    # total always 10-15
    if minutes <= 10:
        return [('Priming metacognitivo',1),('Sprint cognitivo principal',6),('Recuperação ativa',1),('Compressão verbal',1),('Registro mínimo',1)]
    if minutes == 11:
        return [('Priming metacognitivo',1),('Sprint cognitivo principal',6),('Recuperação ativa',2),('Compressão verbal',1),('Registro mínimo',1)]
    if minutes == 12:
        return [('Priming metacognitivo',1),('Sprint cognitivo principal',7),('Recuperação ativa',2),('Compressão verbal',1),('Registro mínimo',1)]
    if minutes == 13:
        return [('Priming metacognitivo',1),('Sprint cognitivo principal',7),('Recuperação ativa',2),('Compressão verbal',2),('Registro mínimo',1)]
    if minutes == 14:
        return [('Priming metacognitivo',1),('Sprint cognitivo principal',8),('Recuperação ativa',2),('Compressão verbal',2),('Registro mínimo',1)]
    return [('Priming metacognitivo',1),('Sprint cognitivo principal',8),('Recuperação ativa',3),('Compressão verbal',2),('Registro mínimo',1)]

def drill_for(domain):
    drills={
        'linguagem_clara':'Pegue uma ideia difícil e transforme em: 1 frase simples, 3 frases explicativas e 1 exemplo concreto. Corte palavras vagas.',
        'abstracao_modelos':'Escolha um problema real. Crie uma analogia, depois extraia o princípio geral por trás dela.',
        'metacognicao':'Resolva uma microtarefa e narre seu pensamento: objetivo, hipótese, erro provável, correção.',
        'consistencia_habito':'Execute a menor versão possível do hábito-alvo por 7 minutos. O objetivo é iniciar rápido, não performar bonito.',
        'raciocinio_logico':'Use o quadro: dados → relação → hipótese → teste → conclusão em um problema pequeno.',
        'foco_execucao':'Remova uma distração, inicie em até 60 segundos e mantenha uma única tarefa até o alarme tocar.'
    }
    return drills.get(domain, drills['metacognicao'])

def protocol(profile, domains):
    minutes=clamp_minutes(profile.get('tempo_disponivel_min',12))
    focus, score=choose_focus(domains)
    blocks=allocate(minutes)
    md=[]
    md.append('# Protocolo Diário Neurocognitivo — MicroSprint 10–15\n')
    md.append(f"Data: {profile.get('data', datetime.date.today().isoformat())}\n")
    md.append(f'Tempo total: **{minutes} minutos**\n')
    md.append('\n## Gap dominante do dia\n')
    md.append(f'- **{focus}** — indicador atual: {score}/100.\n')
    md.append('- Regra: hoje o treino mira apenas esse gap. O restante fica fora para preservar intensidade.\n')
    md.append('\n## Sessão MicroSprint\n')
    for name,m in blocks:
        if name=='Priming metacognitivo': inst='Escreva uma intenção: “Hoje vou melhorar este gap fazendo uma repetição curta e correta”. Nomeie o erro provável.'
        elif name=='Sprint cognitivo principal': inst=drill_for(focus)
        elif name=='Recuperação ativa': inst='Feche qualquer fonte. Recupere de memória o que fez, o princípio usado e onde errou. Sem consulta.'
        elif name=='Compressão verbal': inst='Explique em 3 frases ou 1 analogia. Se não conseguir explicar, o conhecimento ainda não consolidou.'
        else: inst='Preencha: foco 0–10, clareza 0–5, itens lembrados, erro dominante e próxima repetição.'
        md.append(f'### {name} — {m} min\n{inst}\n')
    md.append('\n## Microprotocolo de hábito\n')
    md.append('- Gatilho: perceber tarefa abstrata, grande ou incômoda.\n')
    md.append('- Resposta antiga provável: adiar, coletar informação demais ou trocar de tarefa.\n')
    md.append('- Resposta nova: iniciar cronômetro e produzir uma versão imperfeita em 60 segundos.\n')
    md.append('- Reforço: registrar execução feita. A vitória é iniciar e fechar o ciclo.\n')
    md.append('\n## Métrica rápida\n')
    md.append('- Iniciei em até 60 segundos? sim/não\n- Foco 0–10: __\n- Clareza 0–5: __\n- Recuperação ativa: __ itens lembrados\n- Próxima repetição: amanhã / 3 dias / 7 dias\n')
    md.append('\n## Nota psicométrica responsável\n')
    md.append('Este treino acompanha desempenho por domínio. Não mede QI formal e não substitui avaliação profissional.\n')
    md.append('\n---\n')
    md.append(REQUIRED_AI_RESPONSE_FOOTER + '\n')
    return ''.join(md)

def metrics(profile, domains, minutes):
    focus,score=choose_focus(domains)
    return {
        'version':'1.1.0-microsprint-10-15',
        'total_minutes': minutes,
        'dominant_focus': focus,
        'dominant_focus_score': score,
        'domains_0_100': domains,
        'daily_metrics': ['iniciou_em_60s_sim_nao','foco_0_10','clareza_0_5','recuperacao_ativa_itens','erro_dominante','proxima_repeticao'],
        'weekly_review': ['aderencia_10_15','foco_medio','clareza_media','gaps_recorrentes','melhor_microdrill'],
        'psychometrics_guardrail': 'Não interpretar como QI. Usar avaliação profissional para QI formal; ICAR apenas como medida aberta exploratória.',
        'required_ai_response_footer': REQUIRED_AI_RESPONSE_FOOTER
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--profile', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    profile=load_profile(args.profile)
    minutes=clamp_minutes(profile.get('tempo_disponivel_min',12))
    domains=score_domain(profile)
    (out/'daily_protocol.md').write_text(protocol(profile,domains),encoding='utf-8')
    metric=metrics(profile,domains,minutes)
    (out/'metrics_plan.json').write_text(json.dumps(metric,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'micro_sprint_plan.json').write_text(json.dumps({'minutes':minutes,'blocks':allocate(minutes),'dominant_focus':metric['dominant_focus']},ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'dashboard_seed.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f); writer.writerow(['date','domain','score'])
        for d,s in domains.items(): writer.writerow([profile.get('data',datetime.date.today().isoformat()),d,s])
    print(json.dumps({'ok':True,'version':'1.1.0-microsprint-10-15','minutes':minutes,'output':str(out),'dominant_focus':metric['dominant_focus'],'domains':domains},ensure_ascii=False))
if __name__=='__main__': main()
