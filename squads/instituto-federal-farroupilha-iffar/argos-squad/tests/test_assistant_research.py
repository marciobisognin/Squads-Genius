from datetime import date
from pathlib import Path

from argos.assistant_research import run_assisted_research
from argos.contracts import EdicaoRef
from argos.official_sources import STATE_SOURCES, state_by_code
from argos.ophthalmoi.registry import build_adapter, roster


def test_catalogo_tem_27_ufs_mais_df():
    rs = state_by_code("RS")
    df = state_by_code("DODF")
    assert len(STATE_SOURCES) == 27
    assert rs is not None and rs.codigo == "DOE-RS"
    assert df is not None and df.uf == "DF"
    assert "DOE-SP" in roster()
    assert "DODF" in roster()


def test_adapter_estadual_catalogado_sem_publicacao_falsa():
    adapter = build_adapter("DOE-SP")
    ref = EdicaoRef(fonte="DOE-SP", data=date(2026, 7, 2), edicao="assistido", url="https://www.doe.sp.gov.br/")
    assert adapter.codigo == "DOE-SP"
    assert adapter.obter_publicacoes(ref) == []


def test_pesquisa_assistida_cria_arquivos():
    root = Path(".")
    result = run_assisted_research(root, "repactuação", municipio_ids=["4305207"], ufs=["RS", "SC"], size=1, check_states=False)
    out = Path(result["output_dir"])
    assert (out / "perfil.yaml").exists()
    assert (out / "fontes_consultadas.json").exists()
    assert (out / "relatorio_pesquisa.md").exists()
    assert (out / "links_estaduais.md").exists()
