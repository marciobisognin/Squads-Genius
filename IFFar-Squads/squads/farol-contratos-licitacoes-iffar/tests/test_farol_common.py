from farol_common import date_range_default, norm, num, price_stats, similarity, tokens


def test_num_brazilian_format():
    assert num("1.234,56") == 1234.56
    assert num("10,5") == 10.5
    assert num(7) == 7.0
    assert num(None) is None
    assert num("") is None
    assert num("abc") is None


def test_num_plain_decimal_format_is_not_multiplied_by_100():
    # Regressão: célula/API em formato decimal simples (sem separador de milhar)
    # era tratada como BR e multiplicada por 100 (ex.: "1234.56" -> 123456.0).
    assert num("1234.56") == 1234.56
    assert num("45.90") == 45.90
    assert num("12.345.678") == 12345678.0


def test_norm_collapses_whitespace_and_uppercases():
    assert norm("  caneta   azul ") == "CANETA AZUL"
    assert norm(None) == ""


def test_tokens_remove_stopwords_and_accents():
    t = tokens("Panela de pressão em alumínio")
    assert "PANELA" in t and "PRESSAO" in t and "ALUMINIO" in t
    assert "DE" not in t and "EM" not in t


def test_similarity_bounds():
    assert similarity("caneta esferográfica azul", "caneta esferográfica azul") == 1.0
    assert similarity("caneta azul", "parafuso sextavado inox") == 0.0
    parcial = similarity("caneta esferográfica azul escrita média", "caneta esferográfica preta")
    assert 0.0 < parcial < 1.0
    assert similarity("", "qualquer coisa") == 0.0


def test_price_stats():
    stats = price_stats([10.0, 20.0, 30.0, 40.0])
    assert stats["min"] == 10.0
    assert stats["max"] == 40.0
    assert stats["mediana"] == 25.0
    assert "q1" in stats and "q3" in stats
    assert price_stats([]) == {}


def test_date_range_default_is_relative():
    inicio, fim = date_range_default(730)
    assert inicio < fim
    assert len(inicio) == 10 and len(fim) == 10
