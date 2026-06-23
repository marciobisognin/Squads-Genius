#!/usr/bin/env python3
"""Gerador da planilha .xlsx da Conta-Depósito Vinculada — apenas biblioteca padrão.

Escreve um arquivo .xlsx (OOXML) multi-abas válido usando somente `zipfile` e XML
gerado à mão (células `inlineStr` para texto e `<v>` para números), sem qualquer
dependência externa (sem openpyxl/pandas). Também oferece fallback CSV por aba.

Abas (estrutura do dossiê):
  Cadastro, Trabalhadores, Provisão mensal, Liberações, Conferência FGTS

Uso:
    python3 gerar_planilha_xlsx.py --self-test
    python3 gerar_planilha_xlsx.py --input dados.json --output conta_vinculada.xlsx
    python3 gerar_planilha_xlsx.py --input dados.json --output saida --csv

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import zipfile
from typing import Any, Dict, List, Sequence
from xml.sax.saxutils import escape

Row = Sequence[Any]


def _col_letter(idx: int) -> str:
    """0->A, 25->Z, 26->AA ..."""
    s = ""
    idx += 1
    while idx:
        idx, rem = divmod(idx - 1, 26)
        s = chr(65 + rem) + s
    return s


def _is_number(value: Any) -> bool:
    """True quando o valor deve ir como número na célula (<v>), não como texto.

    Strings que parseiam como float contam como número, EXCETO inteiros com zero à
    esquerda (ex.: códigos/competências) — esses preservam-se como texto.
    """
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        s = value.strip()
        if s == "":
            return False
        try:
            float(s)
        except ValueError:
            return False
        if len(s) > 1 and s[0] == "0" and s[1].isdigit():  # "0123" -> texto
            return False
        return True
    return False


def _cell_xml(col: str, row: int, value: Any) -> str:
    ref = f"{col}{row}"
    if _is_number(value):
        return f'<c r="{ref}"><v>{escape(str(value))}</v></c>'
    text = "" if value is None else str(value)
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(text)}</t></is></c>'


def _sheet_xml(rows: List[Row]) -> str:
    parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    parts.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
    parts.append("<sheetData>")
    for r_idx, row in enumerate(rows, start=1):
        cells = "".join(_cell_xml(_col_letter(c_idx), r_idx, val) for c_idx, val in enumerate(row))
        parts.append(f'<row r="{r_idx}">{cells}</row>')
    parts.append("</sheetData></worksheet>")
    return "".join(parts)


def write_xlsx(path: str, sheets: List[Dict[str, Any]]) -> str:
    """sheets: [{"name": str, "rows": [[...], ...]}]. Retorna o caminho gravado."""
    if not sheets:
        raise ValueError("nenhuma aba para gravar")
    content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                     '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
                     '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
                     '<Default Extension="xml" ContentType="application/xml"/>',
                     '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    for i in range(1, len(sheets) + 1):
        content_types.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
                             f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    content_types.append("</Types>")

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
                 'Target="xl/workbook.xml"/></Relationships>')

    sheets_xml = "".join(
        f'<sheet name="{escape(s["name"])[:31]}" sheetId="{i}" r:id="rId{i}"/>'
        for i, s in enumerate(sheets, start=1)
    )
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                f'<sheets>{sheets_xml}</sheets></workbook>')

    wb_rels_parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                     '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i in range(1, len(sheets) + 1):
        wb_rels_parts.append(f'<Relationship Id="rId{i}" '
                             f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                             f'Target="worksheets/sheet{i}.xml"/>')
    wb_rels_parts.append("</Relationships>")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(content_types))
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", "".join(wb_rels_parts))
        for i, s in enumerate(sheets, start=1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", _sheet_xml(s["rows"]))
    return path


def write_csv(prefix: str, sheets: List[Dict[str, Any]]) -> List[str]:
    paths = []
    for s in sheets:
        safe = s["name"].lower().replace(" ", "_").replace("/", "_")
        p = f"{prefix}_{safe}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(s["rows"])
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------
# Montagem das abas a partir do dado consolidado do squad
# ---------------------------------------------------------------------------
def montar_sheets(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    contrato = data.get("contrato", {})
    cadastro_rows: List[Row] = [["Campo", "Valor"]]
    for k in ["orgao", "contrato", "empresa", "cnpj", "regime", "sat", "fap",
              "banco", "agencia", "conta_vinculada", "vigencia", "indice_remuneracao"]:
        if k in contrato:
            cadastro_rows.append([k, contrato[k]])

    trab_rows: List[Row] = [["Nome", "CPF", "CBO", "Admissão", "Início contrato",
                             "Salário-base", "Adicionais", "Remuneração (A)", "Jornada"]]
    prov_rows: List[Row] = [["Competência", "Trabalhador", "A (Remuneração)", "B (13º)",
                             "C (Férias+1/3)", "D (Multa)", "E (Incid. 2.2)", "Total mensal", "Saldo acumulado"]]
    for t in data.get("trabalhadores", []):
        trab_rows.append([t.get("nome"), t.get("cpf"), t.get("cbo"), t.get("admissao"),
                          t.get("inicio_contrato"), t.get("salario_base"),
                          t.get("adicionais"), t.get("remuneracao"), t.get("jornada")])
        prov = t.get("provisao_mensal", {})
        rub = {r["nome"]: r["valor"] for r in prov.get("rubricas", [])}
        for comp in t.get("competencias", [None]):
            prov_rows.append([comp, t.get("nome"), prov.get("remuneracao"),
                              rub.get("13º salário"), rub.get("Férias + 1/3"),
                              rub.get("Multa FGTS s/ aviso prévio"), rub.get("Incidência Submódulo 2.2"),
                              prov.get("total_mensal"), t.get("saldo_acumulado")])

    lib_rows: List[Row] = [["Evento", "Data", "Trabalhador", "Avos", "Principal", "Encargos",
                            "Total", "Documento", "Autorização", "Ordem bancária", "Saldo após"]]
    for lb in data.get("liberacoes", []):
        lib_rows.append([lb.get("evento"), lb.get("data"), lb.get("trabalhador"), lb.get("avos"),
                         lb.get("principal"), lb.get("encargos"), lb.get("total"),
                         lb.get("documento"), lb.get("autorizacao"), lb.get("ordem_bancaria"),
                         lb.get("saldo_apos")])

    conf_rows: List[Row] = [["Competência", "Trabalhador", "FGTS devido (8%)", "FGTS recolhido",
                             "Divergência", "Status", "INSS"]]
    for c in data.get("conferencia", []):
        conf_rows.append([c.get("competencia"), c.get("trabalhador"), c.get("fgts_devido"),
                          c.get("fgts_recolhido"), c.get("divergencia"), c.get("status"), c.get("inss")])

    return [
        {"name": "Cadastro", "rows": cadastro_rows},
        {"name": "Trabalhadores", "rows": trab_rows},
        {"name": "Provisão mensal", "rows": prov_rows},
        {"name": "Liberações", "rows": lib_rows},
        {"name": "Conferência FGTS", "rows": conf_rows},
    ]


def _validar_xlsx(path: str) -> bool:
    """Confere que o arquivo é um zip válido com as partes mínimas do OOXML."""
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            req = {"[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/worksheets/sheet1.xml"}
            return req.issubset(names) and z.testzip() is None
    except zipfile.BadZipFile:
        return False


def self_test() -> int:
    import tempfile
    falhas: List[str] = []
    if _col_letter(0) != "A" or _col_letter(26) != "AA" or _col_letter(27) != "AB":
        falhas.append("conversão de coluna incorreta")
    sheets = montar_sheets({
        "contrato": {"orgao": "IFFar", "regime": "lucro_real_presumido", "sat": "1"},
        "trabalhadores": [{
            "nome": "Fulano de Tal", "cpf": "529.982.247-25", "remuneracao": "2000.00",
            "competencias": ["2026-01"],
            "provisao_mensal": {"remuneracao": "2000.00", "total_mensal": "636.08", "rubricas": [
                {"nome": "13º salário", "valor": "166.60"},
                {"nome": "Férias + 1/3", "valor": "242.00"},
                {"nome": "Multa FGTS s/ aviso prévio", "valor": "80.00"},
                {"nome": "Incidência Submódulo 2.2", "valor": "147.48"},
            ]},
            "saldo_acumulado": "636.08",
        }],
    })
    if len(sheets) != 5:
        falhas.append("deveriam ser 5 abas")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "t.xlsx")
        write_xlsx(out, sheets)
        if not _validar_xlsx(out):
            falhas.append("arquivo .xlsx gerado é inválido")
        csvs = write_csv(os.path.join(tmp, "t"), sheets)
        if len(csvs) != 5 or not all(os.path.exists(p) for p in csvs):
            falhas.append("fallback CSV incompleto")
    if falhas:
        print("SELF-TEST: FALHOU")
        for f in falhas:
            print("  -", f)
        return 1
    print("SELF-TEST: OK (.xlsx válido + CSV de fallback)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera a planilha .xlsx da Conta Vinculada (stdlib).")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--input", help="JSON consolidado (contrato + trabalhadores + liberacoes + conferencia).")
    ap.add_argument("--output", default="conta_vinculada.xlsx")
    ap.add_argument("--csv", action="store_true", help="Também gera CSV por aba.")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.input:
        ap.print_help()
        return 0
    data = json.loads(open(args.input, encoding="utf-8").read())
    sheets = montar_sheets(data)
    out = args.output if args.output.endswith(".xlsx") else args.output + ".xlsx"
    write_xlsx(out, sheets)
    msg = {"xlsx": out, "valido": _validar_xlsx(out)}
    if args.csv:
        prefix = out[:-5]
        msg["csv"] = write_csv(prefix, sheets)
    print(json.dumps(msg, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
