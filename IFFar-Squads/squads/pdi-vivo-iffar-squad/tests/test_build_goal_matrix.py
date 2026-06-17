from build_goal_matrix import dedupe, parse_lines

TEXTO = """\
Dimensão: Acesso e Inclusão
Objetivo: Ampliar o acesso com equidade.
Meta 1.1 Elevar a taxa de ocupação de vagas para 95%.
Meta 1.2 Ampliar ingressantes por ações afirmativas.

Dimensão: Permanência e Êxito
Objetivo: Reduzir a evasão.
Meta 2.1 Reduzir a taxa de evasão para abaixo de 12%.
"""


def test_parse_lines_extrai_metas_com_contexto():
    rows = parse_lines(TEXTO)
    assert len(rows) >= 3
    primeira = rows[0]
    assert primeira["dimensao"] == "Acesso e Inclusão"
    assert "ocupação de vagas" in primeira["meta"]
    assert primeira["status"] == "não iniciada"


def test_parse_lines_mantem_dimensao_corrente():
    rows = parse_lines(TEXTO)
    evasao = [r for r in rows if "evasão" in r["meta"]][0]
    assert evasao["dimensao"] == "Permanência e Êxito"


def test_dedupe_remove_metas_repetidas():
    rows = [
        {"meta": "Reduzir evasão", "codigo": "M-001"},
        {"meta": "reduzir   EVASÃO", "codigo": "M-002"},
        {"meta": "Outra meta distinta", "codigo": "M-003"},
    ]
    unique = dedupe(rows)
    assert len(unique) == 2
