import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_cronograma import build as build_cronograma  # noqa: E402
from check_prazos import build as build_prazos, classify  # noqa: E402
from validate_plano_ensino import validate  # noqa: E402


def test_build_cronograma_sem_conflito():
    topicos = ["A", "B"]
    inicio = date(2026, 8, 3)  # segunda-feira
    fim = date(2026, 8, 7)  # sexta-feira
    resultado = build_cronograma(topicos, inicio, fim, set(), {5, 6})
    assert resultado["conflito_carga_horaria"] is False
    assert len(resultado["cronograma"]) == 2


def test_build_cronograma_com_conflito():
    topicos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    inicio = date(2026, 8, 3)
    fim = date(2026, 8, 4)
    resultado = build_cronograma(topicos, inicio, fim, set(), {5, 6})
    assert resultado["conflito_carga_horaria"] is True
    assert resultado["topicos_sem_aula_alocada"]


def test_validate_plano_ensino_campo_ausente():
    plano = {"componente_id": "C1"}
    resultado = validate(plano)
    assert resultado["valido"] is False
    assert any(a["campo"] == "ementa" for a in resultado["achados"])


def test_validate_plano_ensino_completo():
    plano = {
        "componente_id": "C1",
        "curso_id": "CURSO1",
        "ementa": "x",
        "objetivos": ["x"],
        "metodologia": "x",
        "conteudo_programatico": ["x"],
        "avaliacao": "x",
        "referencias": ["x"],
        "cronograma": [{"data_aula": "2026-08-03", "topico": "x"}],
        "veredito_curricular": "conforme",
        "status_homologacao": "homologado",
    }
    resultado = validate(plano)
    assert resultado["valido"] is True


def test_classify_prazo():
    assert classify(-1) == "vencido"
    assert classify(3) == "alerta_antecedencia_curta"
    assert classify(10) == "alerta_antecedencia_longa"
    assert classify(30) == "sem_alerta"


def test_build_prazos_checklist():
    agenda = [{"descricao": "x", "data_limite": "2026-06-19"}]
    resultado = build_prazos(agenda, date(2026, 6, 18))
    assert resultado["checklist_conformidade"]["total"] == 1
