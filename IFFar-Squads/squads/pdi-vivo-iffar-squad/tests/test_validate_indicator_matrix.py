from validate_indicator_matrix import validate


def _meta_completa(**over):
    base = {
        "codigo": "M-001",
        "ciclo": "2027-2034",
        "dimensao": "Acesso",
        "meta": "Elevar ocupação",
        "indicador": "Taxa de ocupação",
        "fonte_dados": "SISTEC",
        "responsavel_nome": "Coordenação",
        "periodicidade": "semestral",
        "status": "em execução",
        "risco": "médio",
        "evidencia_obrigatoria": "Relatório",
        "proxima_revisao": "2030-01-01",
    }
    base.update(over)
    return base


def test_matriz_completa_sem_achados_altos():
    report = validate([_meta_completa()])
    assert report["por_severidade"]["alto"] == 0
    assert report["go_no_go"] == "go"


def test_meta_sem_indicador_gera_achado_alto():
    report = validate([_meta_completa(indicador="")])
    assert report["por_severidade"]["alto"] >= 1
    assert report["go_no_go"] == "no-go"


def test_status_invalido_detectado():
    report = validate([_meta_completa(status="inventado")])
    cats = {f["categoria"] for f in report["achados"]}
    assert "vocabulario" in cats


def test_codigo_duplicado_detectado():
    report = validate([_meta_completa(), _meta_completa()])
    cats = {f["categoria"] for f in report["achados"]}
    assert "duplicidade" in cats


def test_proxima_revisao_vencida():
    report = validate([_meta_completa(proxima_revisao="2000-01-01")])
    cats = {f["categoria"] for f in report["achados"]}
    assert "prazo" in cats
