import json
from pathlib import Path

from baixar_atas_assinadas import (
    baixar,
    item_folder_name,
    localizar_item,
    montar_manifesto,
    parse_controle_pncp,
    slugify,
)


def test_slugify_and_folder_name():
    assert slugify("Caneca de Alumínio 300ml") == "caneca-de-aluminio-300ml"
    nome = item_folder_name({"codigo": "150240", "descricao": "Caneca de alumínio"})
    assert nome.startswith("150240-")


def test_parse_controle_pncp():
    parts = parse_controle_pncp("00394452000103-1-000123/2024")
    assert parts == {"cnpj": "00394452000103", "tipo": "1", "sequencial": "123", "ano": "2024"}
    assert parse_controle_pncp("texto sem controle") is None


def test_montar_manifesto_from_resumo():
    resumo = [{"codigoItemCatalogo": 150240, "descricaoAmostra": "CANECA ALUMÍNIO", "mediana": 12.5}]
    manifest = montar_manifesto(resumo, "caso-1", "resumo.json")
    assert manifest["itens"][0]["codigo"] == 150240
    assert manifest["itens"][0]["valor_usado"] == 12.5
    assert manifest["itens"][0]["atas"] == []


def test_baixar_offline_localiza_pagina_e_valor(tmp_path):
    # "ata assinada" simulada como .txt para teste offline e sem dependência de PDF.
    ata_txt = tmp_path / "ata_12_2025.txt"
    ata_txt.write_text(
        "ATA DE REGISTRO DE PRECOS 12/2025\n"
        "Item 150240 - CANECA DE ALUMINIO 300ML\n"
        "Valor unitario homologado: 12,50 por unidade\n",
        encoding="utf-8",
    )
    manifest = {
        "case_id": "caso-1",
        "itens": [
            {
                "codigo": "150240",
                "descricao": "Caneca de alumínio 300ml",
                "valor_usado": 12.5,
                "atas": [
                    {
                        "numeroAtaRegistroPreco": "12/2025",
                        "numeroControlePncpAta": "00394452000103-1-000123/2025",
                        "valorUnitario": 12.5,
                        "arquivo_local": str(ata_txt),
                    }
                ],
            }
        ],
    }
    out = tmp_path / "atas-assinadas"
    result = baixar(manifest, out, download=False)

    assert Path(result["index_html"]).exists()
    assert Path(result["index_json"]).exists()
    item = result["itens"][0]
    pasta = out / item["pasta"]
    assert pasta.is_dir()
    arq = item["arquivos"][0]
    assert arq["status"] == "copiado"
    assert len(arq["sha256"]) == 64
    locs = arq["localizacoes"]
    assert locs[0]["pagina"] == 1
    assert locs[0]["valor_encontrado"] is True
    assert locs[0]["codigo_encontrado"] is True

    # o índice HTML aponta para a pasta e cita o arquivo
    html = Path(result["index_html"]).read_text(encoding="utf-8")
    assert item["pasta"] in html
    assert arq["arquivo"] in html


def test_baixar_registra_pendencia_sem_fonte(tmp_path):
    manifest = {"case_id": "c", "itens": [{"codigo": "1", "descricao": "Item sem ata", "atas": [{}]}]}
    result = baixar(manifest, tmp_path / "out", download=False)
    arq = result["itens"][0]["arquivos"][0]
    assert arq["status"] == "pendente"
