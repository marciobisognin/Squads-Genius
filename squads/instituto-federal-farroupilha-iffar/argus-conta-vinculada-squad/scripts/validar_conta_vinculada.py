#!/usr/bin/env python3
"""Conferência determinística da Conta-Depósito Vinculada.

Aplica as validações e as regras de negócio que decidem se uma liberação pode
ocorrer (fail-closed). Apenas biblioteca padrão.

Validações:
- CPF com dígitos verificadores válidos;
- soma de avos ≤ 12;
- FGTS recolhido ≥ devido por competência (devido = 8% da remuneração);
- saldo da conta nunca negativo;
- status regular/irregular por competência;
- regras de negócio: justa causa não libera; rescisão > 1 ano exige homologação
  sindical; documentação completa obrigatória.

Uso:
    python3 validar_conta_vinculada.py --self-test
    python3 validar_conta_vinculada.py --input conferencia.json

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, List

FGTS_ALIQUOTA = Decimal("0.08")
CENTAVO = Decimal("0.01")
DOC_OBRIGATORIOS = ["folha_pagamento", "fgts_digital", "gps_inss"]
DOC_POR_EVENTO = {
    "13º": ["recibo_13"],
    "férias": ["recibo_ferias"],
    "rescisão": ["trct"],
    "encerramento": ["trct", "quitacao_encargos"],
}


def _d(v: Any) -> Decimal:
    return v if isinstance(v, Decimal) else Decimal(str(v))


def _money(v: Decimal) -> Decimal:
    return v.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def cpf_valido(cpf: str) -> bool:
    """Valida CPF pelos dígitos verificadores."""
    nums = [c for c in str(cpf) if c.isdigit()]
    if len(nums) != 11:
        return False
    d = [int(c) for c in nums]
    if len(set(d)) == 1:  # todos iguais
        return False
    for i in (9, 10):
        soma = sum(d[j] * ((i + 1) - j) for j in range(i))
        resto = (soma * 10) % 11
        dig = 0 if resto == 10 else resto
        if dig != d[i]:
            return False
    return True


def conferir_fgts(remuneracao: Any, competencias: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compara FGTS devido (8% da remuneração) vs recolhido por competência."""
    A = _d(remuneracao)
    devido = _money(A * FGTS_ALIQUOTA)
    linhas: List[Dict[str, Any]] = []
    irregular = False
    for c in competencias:
        recolhido = _money(_d(c.get("deposito", 0)))
        divergencia = _money(devido - recolhido)
        status_extrato = c.get("status", "regular")
        regular = recolhido >= devido and status_extrato == "regular"
        if not regular:
            irregular = True
        linhas.append({
            "competencia": c.get("competencia"),
            "fgts_devido": str(devido),
            "fgts_recolhido": str(recolhido),
            "divergencia": str(divergencia),
            "status": "regular" if regular else "irregular",
        })
    return {"fgts_devido_mensal": str(devido), "competencias": linhas, "fgts_irregular": irregular}


def validar_liberacao(trabalhador: Dict[str, Any]) -> Dict[str, Any]:
    """Aplica as regras de negócio que liberam ou bloqueiam (fail-closed)."""
    bloqueios: List[str] = []

    # CPF
    cpf = trabalhador.get("cpf", "")
    if not cpf_valido(cpf):
        bloqueios.append("CPF inválido")

    # avos
    avos = trabalhador.get("avos")
    if avos is not None and not (0 <= int(avos) <= 12):
        bloqueios.append("soma de avos fora do intervalo 0..12")

    # FGTS
    rem = trabalhador.get("remuneracao")
    conf = None
    if rem is not None and trabalhador.get("fgts_competencias"):
        conf = conferir_fgts(rem, trabalhador["fgts_competencias"])
        if conf["fgts_irregular"]:
            bloqueios.append("FGTS irregular em ao menos uma competência do período")

    evento = trabalhador.get("evento")
    motivo = trabalhador.get("motivo_rescisao")
    tempo_meses = trabalhador.get("tempo_de_casa_meses")

    # justa causa não libera
    if motivo == "justa_causa":
        bloqueios.append("dispensa por justa causa não gera liberação")

    # rescisão > 1 ano exige homologação sindical
    if evento in ("rescisão", "encerramento") and tempo_meses is not None and int(tempo_meses) > 12:
        if not trabalhador.get("homologacao_sindical"):
            bloqueios.append("rescisão > 1 ano exige homologação sindical (TRCT homologado)")

    # documentação completa
    docs = set(trabalhador.get("documentos", []))
    faltantes = [d for d in DOC_OBRIGATORIOS if d not in docs]
    for d in DOC_POR_EVENTO.get(evento, []):
        if d not in docs:
            faltantes.append(d)
    if faltantes:
        bloqueios.append("documentação incompleta: " + ", ".join(sorted(set(faltantes))))

    # saldo nunca negativo
    saldo = trabalhador.get("saldo_apos_liberacao")
    if saldo is not None and _d(saldo) < 0:
        bloqueios.append("liberação excede o saldo acumulado da conta")

    return {
        "cpf": cpf,
        "evento": evento,
        "conferencia_fgts": conf,
        "libera": len(bloqueios) == 0,
        "bloqueios": bloqueios,
    }


def processar(data: Dict[str, Any]) -> Dict[str, Any]:
    resultados = [validar_liberacao(t) for t in data.get("trabalhadores", [])]
    go = all(r["libera"] for r in resultados) if resultados else False
    return {
        "competencia": data.get("competencia"),
        "responsavel_validacao": data.get("responsavel_validacao") or "PENDENTE — preencher antes de autorizar",
        "por_trabalhador": resultados,
        "go_no_go": "go" if go else "no-go",
        "total_bloqueados": sum(1 for r in resultados if not r["libera"]),
    }


def self_test() -> int:
    falhas: List[str] = []

    # CPF conhecido válido / inválido
    if not cpf_valido("529.982.247-25"):
        falhas.append("CPF válido reprovado")
    if cpf_valido("111.111.111-11"):
        falhas.append("CPF de dígitos repetidos deveria ser inválido")
    if cpf_valido("123"):
        falhas.append("CPF curto deveria ser inválido")

    # FGTS: devido 8% de 2000 = 160; recolhido 160 regular, 150 irregular
    conf = conferir_fgts("2000", [
        {"competencia": "2026-01", "deposito": "160.00", "status": "regular"},
        {"competencia": "2026-02", "deposito": "150.00", "status": "regular"},
    ])
    if conf["fgts_devido_mensal"] != "160.00":
        falhas.append("FGTS devido deveria ser 160.00")
    if not conf["fgts_irregular"]:
        falhas.append("competência com recolhimento a menor deveria marcar irregular")

    # liberação bloqueada: justa causa
    r = validar_liberacao({
        "cpf": "529.982.247-25", "evento": "rescisão", "motivo_rescisao": "justa_causa",
        "documentos": ["folha_pagamento", "fgts_digital", "gps_inss", "trct"],
    })
    if r["libera"]:
        falhas.append("justa causa deveria bloquear a liberação")

    # liberação ok
    r2 = validar_liberacao({
        "cpf": "529.982.247-25", "evento": "férias", "avos": 12,
        "remuneracao": "2000", "fgts_competencias": [{"competencia": "2026-01", "deposito": "160.00"}],
        "documentos": ["folha_pagamento", "fgts_digital", "gps_inss", "recibo_ferias"],
        "saldo_apos_liberacao": "100.00",
    })
    if not r2["libera"]:
        falhas.append(f"liberação regular deveria passar; bloqueios={r2['bloqueios']}")

    # rescisão > 1 ano sem homologação bloqueia
    r3 = validar_liberacao({
        "cpf": "529.982.247-25", "evento": "rescisão", "tempo_de_casa_meses": 18,
        "documentos": ["folha_pagamento", "fgts_digital", "gps_inss", "trct"],
    })
    if r3["libera"]:
        falhas.append("rescisão > 1 ano sem homologação sindical deveria bloquear")

    if falhas:
        print("SELF-TEST: FALHOU")
        for f in falhas:
            print("  -", f)
        return 1
    print("SELF-TEST: OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Conferência/validação da Conta Vinculada.")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--input", help="Arquivo JSON de conferência.")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.input:
        data = json.loads(open(args.input, encoding="utf-8").read())
        print(json.dumps(processar(data), ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
