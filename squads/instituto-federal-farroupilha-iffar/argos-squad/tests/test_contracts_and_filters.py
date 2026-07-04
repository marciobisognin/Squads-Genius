from pathlib import Path
from argos.graph import load_profile
from argos.ophthalmoi.dou_inlabs import parse_article
from argos.engines.kanon_lex import filtrar_publicacoes

def test_perfil_valida():
    perfil = load_profile(Path('perfis/contratos-iffar-f0.yaml'))
    assert perfil.nome == 'contratos-iffar-f0'

def test_dou_fixture_parse_e_filtro():
    perfil = load_profile(Path('perfis/contratos-iffar-f0.yaml'))
    pubs = [parse_article(Path('tests/fixtures/dou_inlabs/2026-07-02-do3-iffar.xml').read_text(encoding='utf-8'))]
    out = filtrar_publicacoes(perfil, pubs)
    assert len(out) == 1
    assert out[0].fonte == 'DOU-INLABS'
    assert 'IFFar' in out[0].texto
