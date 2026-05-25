#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json
root = Path(__file__).resolve().parents[1]
required = ['squad.yaml','README.md','scripts/song_blueprint.py','references/analise_estetica_tem_um_manto.md','templates/prompt_suno_udio.md']
missing = [p for p in required if not (root/p).exists()]
if missing:
    print('MISSING', missing)
    sys.exit(1)
cmd = [sys.executable, str(root/'scripts/song_blueprint.py'), '--tema', 'um pai cansado que reencontra Deus', '--emocao', 'consolo', '--simbolo', 'colo']
out = subprocess.check_output(cmd, text=True)
data = json.loads(out)
for key in ['sinopse_emocional','tags_heartmula','prompt_geracao','checklist_originalidade']:
    assert key in data, key
print('SMOKE_OK canto-manto-emocional')
