from datetime import date
from pathlib import Path
from argos.graph import ArgosPipeline

def test_pipeline_fixture_gera_relatorio(tmp_path):
    result = ArgosPipeline(Path('.')).run('perfis/contratos-iffar-f0.yaml', date(2026, 7, 2), output_dir=tmp_path, fixture=True)
    assert Path(result.markdown_path).exists()
    md = Path(result.markdown_path).read_text(encoding='utf-8')
    assert 'EXTRATO DE CONTRATO' in md
    assert 'corpus_hash' in md
