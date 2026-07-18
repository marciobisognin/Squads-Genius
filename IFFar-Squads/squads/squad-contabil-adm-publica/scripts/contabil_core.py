#!/usr/bin/env python3
"""Engine determinística do Squad Contábil Adm Pública.

Analisa exclusivamente dados fornecidos pelo usuário. Não acessa o SIAFI, não
produz lançamentos transacionais e não substitui o julgamento do contador.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, Iterable, List

SCHEMA_VERSION = "contabil-publica-analysis-v1"
FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def money(value: Any) -> Decimal:
    try:
        return Decimal(str(value or "0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Valor monetário inválido: {value!r}") from exc


def canonical_hash(data: Dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def make_finding(
    code: str,
    severity: str,
    title: str,
    description: str,
    object_ref: str,
    evidence_ids: Iterable[str],
    normative_ref: str,
    action_class: str,
) -> Dict[str, Any]:
    return {
        "id": "",
        "code": code,
        "severity": severity,
        "title": title,
        "description": description,
        "object_ref": object_ref,
        "evidence_ids": sorted(set(evidence_ids)),
        "normative_ref": normative_ref,
        "action_class": action_class,
        "requires_human_approval": True,
        "status": "proposto_para_revisao",
    }


def validate_case(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    for field in ("case_id", "ug", "competencia", "sources"):
        if not data.get(field):
            errors.append(f"Campo obrigatório ausente ou vazio: {field}")
    if not isinstance(data.get("sources", []), list):
        errors.append("sources deve ser uma lista")
    if not isinstance(data.get("accounts", []), list):
        errors.append("accounts deve ser uma lista")
    if not isinstance(data.get("equations", []), list):
        errors.append("equations deve ser uma lista")
    if data.get("statements") is not None and not isinstance(data.get("statements"), dict):
        errors.append("statements deve ser um objeto")
    return errors


def _known_evidence(data: Dict[str, Any]) -> set[str]:
    return {str(item.get("id")) for item in data.get("sources", []) if item.get("id")}


def _evidence_findings(
    evidence_ids: List[str], known: set[str], object_ref: str
) -> List[Dict[str, Any]]:
    missing = sorted(item for item in evidence_ids if item not in known)
    if evidence_ids and not missing:
        return []
    description = "Objeto sem evidência vinculada." if not evidence_ids else f"Evidências não localizadas: {', '.join(missing)}"
    return [
        make_finding(
            "EVIDENCIA_INSUFICIENTE",
            "high",
            "Evidência insuficiente",
            description,
            object_ref,
            evidence_ids,
            "Macrofunção 02.03.15 — evidência e qualidade do registro",
            "complementar_evidencia",
        )
    ]


def analyse_accounts(data: Dict[str, Any], known: set[str]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    default_tolerance = money(data.get("rules", {}).get("balance_tolerance", "0.01"))
    for account in data.get("accounts", []):
        code = str(account.get("code", "SEM_CODIGO"))
        ref = f"conta:{code}"
        evidence_ids = [str(x) for x in account.get("evidence_ids", [])]
        findings.extend(_evidence_findings(evidence_ids, known, ref))
        nature = str(account.get("nature", "debit")).lower()
        opening = money(account.get("opening_balance"))
        debits = money(account.get("debits"))
        credits = money(account.get("credits"))
        closing = money(account.get("closing_balance"))
        expected = opening + debits - credits if nature == "debit" else opening - debits + credits
        expected = expected.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        tolerance = money(account.get("tolerance", default_tolerance))
        if abs(expected - closing) > tolerance:
            findings.append(
                make_finding(
                    "SALDO_NAO_RECONCILIADO",
                    "high",
                    "Saldo não reconciliado",
                    f"Saldo informado {closing} difere do saldo calculado {expected}.",
                    ref,
                    evidence_ids,
                    "Macrofunção 02.03.15 — qualidade dos registros contábeis",
                    "reconciliar_movimentacao",
                )
            )
        if closing < 0:
            findings.append(
                make_finding(
                    "SALDO_INVERTIDO",
                    "high",
                    "Saldo com sinal incompatível",
                    f"A conta de natureza {nature} apresenta saldo {closing}.",
                    ref,
                    evidence_ids,
                    "Macrofunção 02.10.06 — regularizações contábeis",
                    "investigar_saldo_invertido",
                )
            )
        age_days = account.get("age_days")
        max_age_days = account.get("max_age_days")
        if age_days is not None and max_age_days is not None and int(age_days) > int(max_age_days):
            findings.append(
                make_finding(
                    "SALDO_ALONGADO",
                    "medium",
                    "Saldo acima do prazo de análise informado",
                    f"Permanência de {age_days} dias supera o limite parametrizado de {max_age_days} dias.",
                    ref,
                    evidence_ids,
                    "Macrofunção 02.10.06 — regularizações contábeis; parâmetro do caso",
                    "avaliar_regularizacao_saldo",
                )
            )
    return findings


def analyse_equations(data: Dict[str, Any], known: set[str]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for equation in data.get("equations", []):
        equation_id = str(equation.get("id", "SEM_ID"))
        ref = f"equacao:{equation_id}"
        evidence_ids = [str(x) for x in equation.get("evidence_ids", [])]
        findings.extend(_evidence_findings(evidence_ids, known, ref))
        left = money(equation.get("left_value"))
        right = money(equation.get("right_value"))
        tolerance = money(equation.get("tolerance", "0.01"))
        difference = (left - right).copy_abs()
        if difference > tolerance:
            findings.append(
                make_finding(
                    "EQUACAO_DESEQUILIBRADA",
                    str(equation.get("severity", "high")),
                    "Equação contábil desequilibrada",
                    f"Diferença {difference} entre os lados da equação {equation_id}.",
                    ref,
                    evidence_ids,
                    "Macrofunção 02.03.15 e regra/equação fornecida pelo caso",
                    "investigar_origem_equacao",
                )
            )
    return findings


def analyse_statements(data: Dict[str, Any], known: set[str]) -> List[Dict[str, Any]]:
    statements = data.get("statements") or {}
    if not statements:
        return []
    findings: List[Dict[str, Any]] = []
    evidence_ids = [str(x) for x in statements.get("evidence_ids", [])]
    findings.extend(_evidence_findings(evidence_ids, known, "demonstracoes"))
    assets = money(statements.get("assets"))
    liabilities = money(statements.get("liabilities"))
    equity = money(statements.get("net_equity"))
    tolerance = money(statements.get("tolerance", "0.01"))
    difference = (assets - liabilities - equity).copy_abs()
    if difference > tolerance:
        findings.append(
            make_finding(
                "DEMONSTRACAO_DESEQUILIBRADA",
                "critical",
                "Demonstração contábil desequilibrada",
                f"Ativo difere de passivo mais patrimônio líquido em {difference}.",
                "demonstracoes:balanco_patrimonial",
                evidence_ids,
                "Macrofunção 02.03.19 — Demonstrações Contábeis",
                "reconciliar_demonstrativos",
            )
        )
    return findings


def import_external_findings(data: Dict[str, Any], known: set[str]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for item in data.get("external_findings", []):
        evidence_ids = [str(x) for x in item.get("evidence_ids", [])]
        object_ref = f"{item.get('source', 'consulta')}:{item.get('code', 'SEM_CODIGO')}"
        findings.extend(_evidence_findings(evidence_ids, known, object_ref))
        findings.append(
            make_finding(
                str(item.get("code", "ACHADO_EXTERNO")),
                str(item.get("severity", "medium")),
                str(item.get("title", "Achado de consulta externa")),
                str(item.get("description", "Achado fornecido pelo usuário.")),
                object_ref,
                evidence_ids,
                str(item.get("normative_ref", "Referência normativa a confirmar na fonte oficial")),
                str(item.get("action_class", "analisar_achado_externo")),
            )
        )
    return findings


def build_regularization_plan(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    plan: List[Dict[str, Any]] = []
    for item in findings:
        plan.append(
            {
                "finding_id": item["id"],
                "action_class": item["action_class"],
                "recommended_action": (
                    "Confirmar a causa e a evidência; consultar a redação vigente da Macrofunção "
                    "02.10.06 e o procedimento específico aplicável; submeter a proposta ao contador responsável."
                ),
                "procedure_reference": item["normative_ref"],
                "transaction_command": None,
                "approval_status": "pendente_contador",
                "execution_status": "nao_executado",
            }
        )
    return plan


def analyse_case(data: Dict[str, Any]) -> Dict[str, Any]:
    errors = validate_case(data)
    known = _known_evidence(data)
    findings: List[Dict[str, Any]] = []
    if not errors:
        findings.extend(analyse_accounts(data, known))
        findings.extend(analyse_equations(data, known))
        findings.extend(analyse_statements(data, known))
        findings.extend(import_external_findings(data, known))
    findings.sort(key=lambda x: (SEVERITY_ORDER.get(x["severity"], 9), x["code"], x["object_ref"]))
    for index, item in enumerate(findings, start=1):
        item["id"] = f"ACH-{index:04d}"
    severities = {level: sum(1 for item in findings if item["severity"] == level) for level in SEVERITY_ORDER}
    if errors:
        conclusion = "pendente_dados"
    elif severities["critical"] or severities["high"]:
        conclusion = "com_restricao_proposta"
    elif severities["medium"]:
        conclusion = "com_ressalvas_para_revisao"
    else:
        conclusion = "sem_restricao_proposta"
    return {
        "schema": SCHEMA_VERSION,
        "case_id": data.get("case_id"),
        "ug": data.get("ug"),
        "competencia": data.get("competencia"),
        "input_sha256": canonical_hash(data),
        "validation_errors": errors,
        "conclusion_proposal": conclusion,
        "final_decision": None,
        "requires_accountant_approval": True,
        "findings": findings,
        "severity_counts": severities,
        "regularization_plan": build_regularization_plan(findings),
        "limits": [
            "Não acessa nem altera o SIAFI.",
            "Não gera comando ou lançamento contábil executável.",
            "Conclusões são propostas para validação do contador responsável.",
        ],
    }


def _write_markdown(result: Dict[str, Any], output_dir: Path) -> None:
    report_lines = [
        "# Relatório de Conformidade Contábil — proposta para revisão",
        "",
        f"- **Caso:** {result.get('case_id')}",
        f"- **UG:** {result.get('ug')}",
        f"- **Competência:** {result.get('competencia')}",
        f"- **Conclusão proposta:** `{result.get('conclusion_proposal')}`",
        f"- **Hash do input:** `{result.get('input_sha256')}`",
        "",
        "> Este relatório não substitui a certificação do contador responsável e não registra conformidade no SIAFI.",
        "",
        "## Achados",
        "",
    ]
    if not result["findings"]:
        report_lines.append("Nenhum achado determinístico no conjunto de dados fornecido.")
    for item in result["findings"]:
        report_lines.extend(
            [
                f"### {item['id']} — {item['title']}",
                f"- Severidade: `{item['severity']}`",
                f"- Objeto: `{item['object_ref']}`",
                f"- Evidências: {', '.join(item['evidence_ids']) or 'não vinculadas'}",
                f"- Descrição: {item['description']}",
                f"- Referência: {item['normative_ref']}",
                "",
            ]
        )
    report_lines.extend(["## Aprovação", "", "**Contador responsável:** ____________________", "", FOOTER])
    (output_dir / "relatorio_conformidade.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    plan_lines = ["# Plano Assistido de Regularização", "", "> Nenhuma ação abaixo foi executada no SIAFI.", ""]
    for item in result["regularization_plan"]:
        plan_lines.extend(
            [
                f"## {item['finding_id']} — {item['action_class']}",
                f"- Ação recomendada: {item['recommended_action']}",
                f"- Referência: {item['procedure_reference']}",
                f"- Aprovação: `{item['approval_status']}`",
                "",
            ]
        )
    plan_lines.append(FOOTER)
    (output_dir / "plano_regularizacao.md").write_text("\n".join(plan_lines) + "\n", encoding="utf-8")


def write_outputs(result: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "matriz_achados.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "code", "severity", "title", "object_ref", "evidence_ids", "normative_ref", "action_class", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        for item in result["findings"]:
            row = dict(item)
            row["evidence_ids"] = ";".join(item["evidence_ids"])
            writer.writerow({key: row.get(key) for key in writer.fieldnames})
    _write_markdown(result, output_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analisa um caso contábil exportado, sem acessar o SIAFI.")
    parser.add_argument("--input", required=True, help="Caso JSON")
    parser.add_argument("--output-dir", required=True, help="Diretório de saída")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = analyse_case(data)
    write_outputs(result, Path(args.output_dir))
    print(json.dumps({"status": "ok" if not result["validation_errors"] else "blocked", "conclusion": result["conclusion_proposal"], "findings": len(result["findings"]), "output_dir": str(Path(args.output_dir).resolve())}, ensure_ascii=False))
    return 0 if not result["validation_errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
