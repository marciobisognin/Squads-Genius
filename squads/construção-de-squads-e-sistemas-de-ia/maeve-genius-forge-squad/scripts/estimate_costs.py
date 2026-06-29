#!/usr/bin/env python3
import argparse, json, time
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--manual-hours',type=float,default=8); ap.add_argument('--hourly-rate',type=float,default=120); args=ap.parse_args()
    root=Path(args.root); files=sum(1 for p in root.rglob('*') if p.is_file()) if root.exists() else 0
    deterministic=max(5, files//3); llm=max(3, files//8)
    report={'estimated_manual_hours_saved':args.manual_hours,'estimated_value_saved':round(args.manual_hours*args.hourly_rate,2),'llm_dependent_steps':llm,'deterministic_steps':deterministic,'estimated_token_cost':'variável; reduzir com scripts locais','scripts_generated':7,'roi_notes':['Scripts locais reduzem repetição e custo marginal.','Revisão humana continua obrigatória nos gates.'],'generated_at':time.strftime('%Y-%m-%d %H:%M:%S')}
    out=Path('output/cost_report.json') if root.name!='output' else root/'cost_report.json'; out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
