#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
CRISIS = ['suicídio','suicidio','me matar','tirar minha vida','autoagressão','autoagressao','matar alguém','matar alguem','violência iminente','violencia iminente','overdose','surto','emergência','emergencia']
ROUTES = {
 'engenheiro-comportamental': ['procrastinar','hábito','habito','rotina','fobia','produtividade','ansiedade','evitar','comportamento','recompensa'],
 'arqueologo-dinamico': ['trauma','sonho','infância','infancia','culpa','vergonha','repetição','repeticao','inconsciente','defesa'],
 'arquiteto-neurobiologico': ['sono','medicação','medicacao','hormônio','hormonio','dopamina','serotonina','cansaço','fadiga','lesão','lesao','substância','substancia'],
 'dinamista-sistemico': ['família','familia','equipe','empresa','reunião','reuniao','grupo','conflito','cultura','chefe','funcionário','funcionario'],
 'fenomenologista-existencial': ['sentido','vazio','morte','propósito','proposito','valores','vida','existencial','autorrealização','autorrealizacao'],
 'analista-psicometrico': ['medir','teste','escala','indicador','evidência','evidencia','dados','validade','confiabilidade']
}
NOTES = {
 'engenheiro-comportamental': 'Mapear antecedentes, comportamento e consequências. Verificar reforços, esquivas, sobrecarga e contingências que mantêm o padrão.',
 'arqueologo-dinamico': 'Considerar conflitos latentes, defesas, repetição de padrões e significados subjetivos ainda não verbalizados, sem impor interpretação fechada.',
 'arquiteto-neurobiologico': 'Investigar sono, fadiga, substâncias, medicação, dor, saúde geral e sinais que justifiquem avaliação médica/neuropsicológica.',
 'dinamista-sistemico': 'Analisar papéis, cultura, incentivos, comunicação, poder, bode expiatório e padrões relacionais no sistema.',
 'fenomenologista-existencial': 'Explorar perda de sentido, desalinhamento de valores, liberdade, responsabilidade e possibilidades de reconstrução de propósito.',
 'analista-psicometrico': 'Definir indicadores observáveis, linha de base, frequência, intensidade e necessidade de instrumentos validados por profissional habilitado.'
}
def classify(text):
    low=text.lower()
    if any(x in low for x in CRISIS): return 'caótico', True
    hits=sum(1 for words in ROUTES.values() if any(w in low for w in words))
    return ('complexo' if hits>=3 else 'complicado' if hits>=1 else 'claro/indeterminado'), False
def select_agents(text):
    low=text.lower(); selected=[]
    for agent, words in ROUTES.items():
        score=sum(1 for w in words if w in low)
        if score: selected.append((agent,score))
    if not selected: selected=[('engenheiro-comportamental',1),('analista-psicometrico',1),('guardiao-etico-crise',1)]
    selected=sorted(selected,key=lambda x:-x[1])
    return [a for a,s in selected]
def main():
    ap=argparse.ArgumentParser(description='Formulação psicológica assistiva multilente, sem diagnóstico final.')
    ap.add_argument('--input', required=True, help='Arquivo .txt com relato')
    ap.add_argument('--output', required=True, help='Diretório de saída')
    args=ap.parse_args(); text=Path(args.input).read_text(encoding='utf-8', errors='ignore'); out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    domain, crisis=classify(text); agents=['guardiao-etico-crise','diretor-integrativo'] if crisis else ['diretor-integrativo']+select_agents(text)+['guardiao-etico-crise']
    agents=list(dict.fromkeys(agents))
    hypotheses=[]
    for a in agents:
        if a in NOTES: hypotheses.append({'agent':a,'hypothesis':NOTES[a],'status':'hipótese de formulação, não diagnóstico'})
    if crisis:
        summary='O relato contém possível marcador de crise. A análise complexa deve ser interrompida e substituída por orientação de busca imediata de ajuda presencial/emergencial.'
        actions=['Buscar serviço local de emergência ou profissional qualificado imediatamente.','Acionar rede de apoio presencial.','Não permanecer sozinho se houver risco iminente.']
    else:
        summary='Formulação assistiva: o caso deve ser lido por múltiplas lentes, preservando incerteza, contexto e limites profissionais.'
        actions=['Coletar dados adicionais antes de concluir.','Separar fatores comportamentais, sistêmicos, existenciais e biológicos.','Definir intervenções de baixo risco e indicadores observáveis.','Encaminhar para profissional qualificado se houver sofrimento intenso, prejuízo funcional ou risco.']
    result={'input_excerpt':text[:500],'cynefin_domain':domain,'crisis_flag':crisis,'selected_agents':agents,'hypotheses':hypotheses,'integrative_summary':summary,'safe_actions':actions,'legal_notice':'Material assistivo. Não é diagnóstico, psicoterapia, prescrição ou laudo. Requer revisão humana/profissional.'}
    (out/'formulation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# Relatório de Formulação — Prisma Psíquico Integrativo','',f'**Domínio Cynefin:** {domain}',f'**Sinal de crise:** {"sim" if crisis else "não"}','', '## Agentes selecionados']
    md += [f'- {a}' for a in agents]
    md += ['', '## Hipóteses por lente']
    if hypotheses:
        for h in hypotheses: md.append(f'- **{h["agent"]}:** {h["hypothesis"]} _({h["status"]})_')
    else: md.append('- Nenhuma hipótese especializada gerada porque o protocolo de crise tem prioridade.')
    md += ['', '## Síntese integrativa', summary, '', '## Plano de ação seguro']
    md += [f'{i+1}. {a}' for i,a in enumerate(actions)]
    md += ['', '## Aviso ético', result['legal_notice'], '', 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.']
    (out/'formulation_report.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'ok':True,'output':str(out),'domain':domain,'crisis':crisis,'agents':agents},ensure_ascii=False))
if __name__=='__main__': main()
