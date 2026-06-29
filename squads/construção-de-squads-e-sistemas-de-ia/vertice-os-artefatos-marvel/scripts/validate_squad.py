#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
EXPECTED_AGENTS=['CTL-00','CTX-00','CORE-01','CORE-02','CORE-03','CORE-04','CORE-05','CORE-06','OPS-01','OPS-02','OPS-03','OPS-04','SEC-01','QA-01','OBS-01','GATE-01','SAFE-01','POL-01','ADP-01','META-01','RED-01']
EXPECTED_CODENAMES=['MANOPLA DO INFINITO','NEXUS DE TODAS AS REALIDADES','PEDRA DA MENTE','TESSERACT','PEDRA DO TEMPO','AETHER','ORBE DO PODER','PEDRA DA ALMA','VIBRANIUM VAULT','ADAMANTIUM SEAL','BIFROST BRIDGE','QUANTUM REALM','NEGATIVE ZONE','BOOK OF VISHANTI',"M'KRAAN CRYSTAL",'SIEGE PERILOUS','ULTIMATE NULLIFIER','NORN STONES','QUANTUM BANDS','COSMIC CUBE FORGE','DARKHOLD CHAMBER']
REQUIRED_FILES=['README.md','PRD.md','squad.yaml','references/agent_catalog.json','references/PRD_VERTICE_OS_Artefatos_Marvel_EXTRAIDO.md','schemas/canonical_envelope.schema.json','schemas/agent_manifest.schema.json','workflows/order_lifecycle.yaml','workflows/security_governance.yaml','scripts/vertice_os_blueprint.py','scripts/validate_squad.py','LICENSE','NOTICE.md','AUTHORS.md']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--path', default='.'); args=ap.parse_args(); root=Path(args.path).resolve(); errors=[]
    for rel in REQUIRED_FILES:
        if not (root/rel).exists(): errors.append(f'arquivo obrigatório ausente: {rel}')
    try:
        cat=json.loads((root/'references/agent_catalog.json').read_text(encoding='utf-8'))
        ids=[a['id'] for a in cat['agents']]
        codenames=[a['codename'] for a in cat['agents']]
        if ids != EXPECTED_AGENTS: errors.append('lista de IDs não corresponde exatamente ao PRD')
        if codenames != EXPECTED_CODENAMES: errors.append('lista de codinomes não corresponde exatamente ao PRD')
        if len(cat.get('acceptance_criteria',[])) != 12: errors.append('critérios de aceite deveriam ser 12')
        if len(cat.get('roadmap',[])) != 7: errors.append('roadmap deveria ter 7 fases')
    except Exception as e:
        errors.append(f'catálogo inválido: {e}')
    for codename in EXPECTED_CODENAMES:
        hits=list((root/'agents').glob('*'))
        combined='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in hits if p.is_file())
        if codename not in combined: errors.append(f'codinome ausente nos agentes: {codename}')
    if (root/'generated/demo/blueprint.json').exists():
        try:
            bp=json.loads((root/'generated/demo/blueprint.json').read_text(encoding='utf-8'))
            if len(bp.get('agents',[])) != 21: errors.append('blueprint deveria conter 21 agentes')
            if bp.get('name') != 'VÉRTICE-OS': errors.append('blueprint não preserva nome principal VÉRTICE-OS')
        except Exception as e: errors.append(f'blueprint inválido: {e}')
    else: errors.append('blueprint demo ausente')
    scan=[]
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.md','.yaml','.json','.py','.txt'}:
            txt=p.read_text(encoding='utf-8', errors='ignore')
            if re.search(r'\\u[0-9A-Fa-f]{4}', txt): scan.append(str(p.relative_to(root)))
    if scan: errors.append('arquivos com escape Unicode JSON-style: '+', '.join(scan))
    result={'status':'go' if not errors else 'no-go','errors':errors,'agents_expected':21,'checked_required_files':len(REQUIRED_FILES)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1
if __name__ == '__main__': raise SystemExit(main())
