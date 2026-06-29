#!/usr/bin/env python3
import argparse, json, re
parser=argparse.ArgumentParser(); parser.add_argument('complaint', nargs='+'); args=parser.parse_args()
text=' '.join(args.complaint)
slug=re.sub(r'[^a-z0-9]+','-', text.lower())[:48].strip('-') or 'new-skill'
proposal={'complaint':text,'recommended_output':'skill' if any(w in text.lower() for w in ['sempre','todo dia','toda semana','repet','rotina']) else 'workflow_or_prompt','suggested_skill_slug':slug,'questions':['Qual é a entrada?','Qual saída ideal?','Com que frequência ocorre?','Há dados sensíveis?','Como validar qualidade?']}
print(json.dumps(proposal, ensure_ascii=False, indent=2))
