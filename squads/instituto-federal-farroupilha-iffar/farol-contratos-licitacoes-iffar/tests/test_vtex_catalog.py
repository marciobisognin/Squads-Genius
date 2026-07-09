"""Testes offline do coletor de varejo VTEX (sem rede)."""
from vtex_catalog import (
    SIM_ALTA,
    SIM_MEDIA,
    build_query,
    classify_varejo,
    confidence_label,
    extract_offers,
    parse_lojas,
    summarize_item,
)

PAYLOAD_VTEX = [
    {
        "productName": "Caneta Esferográfica Azul Escrita Média BIC Cristal",
        "link": "https://www.loja.com.br/caneta-bic/p",
        "items": [
            {
                "itemId": "12345",
                "name": "Caneta Azul unidade",
                "sellers": [
                    {
                        "sellerName": "Loja Oficial",
                        "commertialOffer": {"Price": 2.5, "ListPrice": 3.0, "AvailableQuantity": 100, "IsAvailable": True},
                    },
                    {
                        "sellerName": "Marketplace Sem Estoque",
                        "commertialOffer": {"Price": 2.9, "AvailableQuantity": 0, "IsAvailable": False},
                    },
                ],
            }
        ],
    },
    {
        "productName": "Suporte de Parede para TV",
        "link": "https://www.loja.com.br/suporte-tv/p",
        "items": [
            {
                "itemId": "999",
                "name": "Suporte",
                "sellers": [
                    {"sellerName": "X", "commertialOffer": {"Price": 0, "IsAvailable": True}},
                ],
            }
        ],
    },
]


def _offers(descricao="Caneta esferográfica azul escrita média"):
    return extract_offers(
        PAYLOAD_VTEX,
        loja="www.loja.com.br",
        url_consulta="https://www.loja.com.br/api/catalog_system/pub/products/search?ft=caneta",
        consultado_em="2026-07-09T10:00:00-03:00",
        descricao_ref=descricao,
    )


def test_build_query_keeps_order_drops_stopwords_and_accents():
    q = build_query("Caneta esferográfica de tinta azul, escrita média")
    assert q.split(" ")[0] == "caneta"
    assert "de" not in q.split(" ")
    assert "esferografica" in q
    assert len(q.split(" ")) <= 5
    assert build_query("") == ""
    assert build_query(None) == ""


def test_extract_offers_flattens_and_keeps_traceability():
    offers = _offers()
    # oferta com Price 0 é descartada; as duas ofertas da caneta permanecem
    assert len(offers) == 2
    o = offers[0]
    assert o["loja"] == "www.loja.com.br"
    assert o["preco"] == 2.5
    assert o["disponivel"] is True
    assert o["url_consulta"].startswith("https://")
    assert o["consultado_em"]
    assert 0 < o["similaridade"] <= 1
    # vendedor sem estoque marcado como indisponível
    assert offers[1]["disponivel"] is False


def test_confidence_label_thresholds():
    assert confidence_label(None) == "sem_match"
    assert confidence_label(0.0) == "sem_match"
    assert confidence_label(SIM_MEDIA - 0.01) == "baixa"
    assert confidence_label(SIM_MEDIA) == "media"
    assert confidence_label(SIM_ALTA) == "alta"
    assert confidence_label(1.0) == "alta"


def test_summarize_item_uses_only_available_comparable_offers():
    resumo = summarize_item("Caneta esferográfica azul escrita média", _offers())
    # apenas a oferta disponível (2.50) entra na estatística
    assert resumo["ofertas"] == 1
    assert resumo["comparaveis"] == 1
    assert resumo["mediana"] == 2.5
    assert resumo["confianca"] in {"media", "alta"}
    assert resumo["melhor_loja"] == "www.loja.com.br"


def test_summarize_item_low_similarity_has_no_stats():
    resumo = summarize_item("Reagente laboratorial sulfato de cobre", _offers("Reagente laboratorial sulfato de cobre"))
    assert resumo["comparaveis"] == 0
    assert "mediana" not in resumo
    assert resumo["confianca"] in {"baixa", "sem_match"}


def test_classify_varejo_only_alerts_on_high_confidence():
    acima = classify_varejo(10.0, 5.0, "alta")
    assert "Acima" in acima and "complementar" in acima
    abaixo = classify_varejo(2.0, 5.0, "alta")
    assert "Abaixo" in abaixo
    ok = classify_varejo(5.0, 5.0, "alta")
    assert "Compatível" in ok
    indicativo = classify_varejo(10.0, 5.0, "media")
    assert "Indicativo" in indicativo and "revisar" in indicativo.lower()
    assert classify_varejo(None, 5.0, "alta") == "Sem comparação de varejo suficiente"
    assert classify_varejo(10.0, None, "alta") == "Sem comparação de varejo suficiente"


def test_parse_lojas_normalizes_domains():
    lojas = parse_lojas(" https://www.a.com.br/ , www.b.com.br ")
    assert lojas == ["www.a.com.br", "www.b.com.br"]
    assert parse_lojas(None)  # padrão não vazio
