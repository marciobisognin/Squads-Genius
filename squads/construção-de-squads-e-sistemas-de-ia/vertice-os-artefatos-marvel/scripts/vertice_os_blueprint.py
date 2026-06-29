#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--catalog', default='references/agent_catalog.json')
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    root=Path.cwd()
    catalog_path=Path(args.catalog)
    if not catalog_path.is_absolute(): catalog_path=root/catalog_path
    out=Path(args.output)
    if not out.is_absolute(): out=root/out
    out.mkdir(parents=True, exist_ok=True)
    catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
    blueprint={
        'name':'VÉRTICE-OS',
        'version':'2.1.0',
        'scope':'Arquitetura interna temática',
        'generated_at':datetime.now(timezone.utc).isoformat(),
        'agents':catalog['agents'],
        'roadmap':catalog['roadmap'],
        'acceptance_criteria':catalog['acceptance_criteria'],
        'canonical_flow':[step.strip() for step in [
            'MANOPLA DO INFINITO recebe o pedido e cria um run imutável no NEXUS DE TODAS AS REALIDADES.',
            'PEDRA DA MENTE transforma linguagem natural em requisitos, riscos, critérios de aceite e plano.',
            'TESSERACT descobre capacidades, versões, custos e rotas permitidas.',
            'ORBE DO PODER reserva orçamento e define a combinação de modelos e ferramentas.',
            'PEDRA DA ALMA avalia consentimento, risco, política e necessidade de aprovação.',
            'PEDRA DO TEMPO executa o DAG com checkpoints, retries, cancelamento e idempotência.',
            'BIFROST BRIDGE transporta handoffs selados pelo ADAMANTIUM SEAL.',
            'QUANTUM REALM executa código e ferramentas de risco em isolamento.',
            'AETHER compõe artefatos finais e envia claims para o BOOK OF VISHANTI.',
            "M'KRAAN CRYSTAL registra traces, custos, QA, decisões e lineage.",
            'SIEGE PERILOUS coleta aprovação quando exigido e o VIBRANIUM VAULT publica a versão final.',
            'Em incidente crítico, ULTIMATE NULLIFIER interrompe, revoga e inicia rollback.'
        ]]
    }
    raw=json.dumps(blueprint, ensure_ascii=False, indent=2).encode('utf-8')
    (out/'blueprint.json').write_bytes(raw)
    (out/'agent_inventory.md').write_text('\n'.join(['# Inventário VÉRTICE-OS',''] + [f"- `{a['id']}` | **{a['codename']}** | {a['function']}" for a in catalog['agents']]), encoding='utf-8')
    approval="""# Pacote de aprovação VÉRTICE-OS\n\n## Escopo\nArquitetura interna temática conforme PRD 2.1.\n\n## Gates críticos\n- Ações irreversíveis exigem SIEGE PERILOUS.\n- Conteúdo suspeito deve ir para NEGATIVE ZONE.\n- Claims factuais passam por BOOK OF VISHANTI.\n- Incidente crítico aciona ULTIMATE NULLIFIER.\n"""
    (out/'approval_packet.md').write_text(approval, encoding='utf-8')
    print(json.dumps({'status':'ok','agents':len(catalog['agents']),'acceptance_criteria':len(catalog['acceptance_criteria']),'roadmap_phases':len(catalog['roadmap']),'blueprint_sha256':hashlib.sha256(raw).hexdigest()}, ensure_ascii=False))
if __name__ == '__main__': main()
