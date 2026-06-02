#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def classify(query):
    q=query.lower()
    agents=[]
    for key, aid in [('fed','squ-central'),('juros','squ-central'),('dólar','squ-forex'),('dolar','squ-forex'),('câmbio','squ-forex'),('opç','squ-deriva'),('deriv','squ-deriva'),('notícia','squ-news'),('noticia','squ-news'),('geopol','squ-geo'),('guerra','squ-geo'),('ações','squ-equities'),('acoes','squ-equities'),('bolsa','squ-equities'),('fundo','squ-letters')]:
        if key in q and aid not in agents: agents.append(aid)
    if not agents: agents=['squ-strategy','squ-news','squ-risk','squ-compliance']
    return agents

ap=argparse.ArgumentParser()
ap.add_argument('--query', required=True)
ap.add_argument('--output', default='output/demo_research_report.md')
args=ap.parse_args()
agents=classify(args.query)
report={
 'system':'SQU Oráculo de Aion',
 'query':args.query,
 'selected_agents':agents,
 'mandatory_gates':['squ-risk','squ-compliance'],
 'output_mode':'educational research / not financial advice',
 'sections':['facts','inferences','hypotheses','bull_case','bear_case','risk_matrix','missing_data','educational_conclusion']
}
out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('# Demo — SQU Oráculo de Aion\n\n```json\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n```\n\n> Material educacional. Não constitui recomendação financeira personalizada.\n')
print(json.dumps({'ok':True,'output':str(out),'selected_agents':agents}, ensure_ascii=False))
