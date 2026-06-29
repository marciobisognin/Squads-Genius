#!/usr/bin/env python3
"""Smoke test do squad: estrutura de arquivos, compilação e auditoria offline na planilha de exemplo."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
required = [
    'squad.yaml',
    'README.md',
    'CHANGELOG.md',
    'requirements.txt',
    'scripts/farol_common.py',
    'scripts/analisar_dfd.py',
    'scripts/compras_gov.py',
    'scripts/enriquecer_dfd_compras_gov.py',
    'scripts/farol_iffar.py',
    'scripts/pncp_busca_termo.py',
    'scripts/historico_farol.py',
    'scripts/painel_saneamento.py',
    'scripts/base_conhecimento.py',
    'scripts/previsao_quantitativos.py',
    'scripts/farol_30_contracts.py',
    'scripts/baixar_atas_assinadas.py',
    'examples/gerar_dfd_exemplo.py',
    'tests/test_analisar_dfd.py',
    'tests/test_farol_30_contracts.py',
    'workflows/auditoria-dfd.yaml',
    'workflows/farol-30-procurement-intelligence.yaml',
    'workflows/baixar-atas-assinadas.yaml',
    'references/compras-gov-integracao.md',
    'references/uso-com-codex-claude-antigravity.md',
    'references/normative_rules.yaml',
    'schemas/finding.schema.json',
    'schemas/evidence.schema.json',
    'schemas/case.schema.json',
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit('Arquivos ausentes: ' + ', '.join(missing))
scripts = sorted(str(p.relative_to(root)) for p in (root / 'scripts').glob('*.py'))
for script in scripts:
    subprocess.run([sys.executable, '-m', 'py_compile', str(root / script)], check=True)

# auditoria offline de ponta a ponta na planilha de exemplo
with tempfile.TemporaryDirectory() as tmp:
    fixture = Path(tmp) / 'dfd_exemplo.xlsx'
    subprocess.run([sys.executable, str(root / 'examples' / 'gerar_dfd_exemplo.py'), '--out', str(fixture)], check=True, capture_output=True)
    proc = subprocess.run([sys.executable, str(root / 'scripts' / 'analisar_dfd.py'), str(fixture), '--out', str(Path(tmp) / 'auditoria')], check=True, capture_output=True, text=True)
    summary = json.loads(proc.stdout)
    assert summary['items_analisados'] == 12, summary
    for out in summary['outputs'].values():
        assert Path(out).exists(), f'output ausente: {out}'

print(json.dumps({'status': 'ok', 'required_files': required, 'python_compile': 'ok', 'auditoria_exemplo': 'ok'}, ensure_ascii=False, indent=2))
