#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

MONEY_FIELDS = ['dotacao', 'empenhado', 'liquidado', 'pago', 'restos_processados', 'restos_nao_processados']
KEY_FIELDS = ['unidade', 'acao', 'natureza_despesa', 'fonte']
REQUIRED_EDITAL_DOCS = [
    {'id': 'dfd', 'name': 'Documento de Formalização da Demanda', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — fase preparatória, a confirmar dispositivo específico'},
    {'id': 'etp', 'name': 'Estudo Técnico Preliminar', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — planejamento da contratação'},
    {'id': 'tr', 'name': 'Termo de Referência ou Projeto Básico', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — instrução do processo'},
    {'id': 'pesquisa_precos', 'name': 'Pesquisa de preços', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — estimativa do valor da contratação'},
    {'id': 'matriz_riscos', 'name': 'Matriz de riscos quando aplicável', 'severity': 'média', 'normative_reference': 'Lei 14.133/2021 — gestão de riscos, quando pertinente'},
    {'id': 'minuta_edital', 'name': 'Minuta de edital', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — edital'},
    {'id': 'minuta_contrato', 'name': 'Minuta de contrato ou instrumento equivalente', 'severity': 'média', 'normative_reference': 'Lei 14.133/2021 — contrato administrativo'},
    {'id': 'aprovacao_juridica', 'name': 'Aprovação ou análise jurídica quando exigível', 'severity': 'alta', 'normative_reference': 'Lei 14.133/2021 — controle prévio de legalidade'},
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def money(value: Any) -> Decimal:
    if value in (None, ''):
        return Decimal('0')
    return Decimal(str(value).replace('.', '').replace(',', '.') if isinstance(value, str) and ',' in value else str(value))


def q2(value: Decimal) -> str:
    return str(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def load_table(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == '.csv':
        with path.open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict) and 'records' in data:
        data = data['records']
    if not isinstance(data, list):
        raise ValueError('entrada deve ser CSV ou JSON com lista/records')
    return data


def validate_records(records: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for i, row in enumerate(records, 1):
        for field in KEY_FIELDS + MONEY_FIELDS:
            if field not in row:
                issues.append(f'linha {i}: campo ausente {field}')
        if any(not str(row.get(k, '')).strip() for k in KEY_FIELDS):
            issues.append(f'linha {i}: chave orçamentária incompleta')
    return issues


def consolidate_records(records: list[dict[str, Any]], source: str = 'user_supplied') -> dict[str, Any]:
    issues = validate_records(records)
    if issues:
        raise ValueError('; '.join(issues))
    grouped: dict[tuple[str, str, str, str], dict[str, Decimal]] = defaultdict(lambda: {f: Decimal('0') for f in MONEY_FIELDS})
    for row in records:
        key = tuple(str(row[k]).strip() for k in KEY_FIELDS)
        for field in MONEY_FIELDS:
            grouped[key][field] += money(row.get(field, 0))
    lines = []
    totals = {f: Decimal('0') for f in MONEY_FIELDS}
    for key, vals in sorted(grouped.items()):
        dotacao = vals['dotacao']
        saldo_disponivel = dotacao - vals['empenhado']
        percentual_empenhado = (vals['empenhado'] / dotacao * Decimal('100')) if dotacao else Decimal('0')
        percentual_pago = (vals['pago'] / dotacao * Decimal('100')) if dotacao else Decimal('0')
        alerts = []
        if saldo_disponivel < 0:
            alerts.append('saldo_negativo_ou_execucao_acima_da_dotacao')
        if vals['liquidado'] < vals['pago']:
            alerts.append('pago_maior_que_liquidado')
        if vals['empenhado'] < vals['liquidado']:
            alerts.append('liquidado_maior_que_empenhado')
        if vals['restos_nao_processados'] > Decimal('0'):
            alerts.append('restos_nao_processados_exigem_acompanhamento')
        for f in MONEY_FIELDS:
            totals[f] += vals[f]
        lines.append({
            'unidade': key[0], 'acao': key[1], 'natureza_despesa': key[2], 'fonte': key[3],
            **{f: q2(vals[f]) for f in MONEY_FIELDS},
            'saldo_disponivel': q2(saldo_disponivel),
            'percentual_empenhado': q2(percentual_empenhado),
            'percentual_pago': q2(percentual_pago),
            'alerts': alerts,
        })
    total_dotacao = totals['dotacao']
    return {
        'generated_at': now(),
        'source': source,
        'version': '1.0.0',
        'records_count': len(records),
        'group_count': len(lines),
        'totals': {f: q2(v) for f, v in totals.items()} | {
            'saldo_disponivel': q2(totals['dotacao'] - totals['empenhado']),
            'percentual_empenhado': q2((totals['empenhado'] / total_dotacao * Decimal('100')) if total_dotacao else Decimal('0')),
            'percentual_pago': q2((totals['pago'] / total_dotacao * Decimal('100')) if total_dotacao else Decimal('0')),
        },
        'lines': lines,
        'human_review_required': True,
        'limitations': ['Relatório calculado sobre dados fornecidos pelo usuário; não substitui registros oficiais.'],
    }


def markdown_execution(report: dict[str, Any]) -> str:
    out = ['# Relatório de Execução Orçamentária', '', f"Gerado em: {report['generated_at']}", f"Fonte: {report['source']}", '', '## Totais', '']
    for k, v in report['totals'].items():
        out.append(f'- {k}: {v}')
    out += ['', '## Linhas consolidadas', '', '| Unidade | Ação | Natureza | Fonte | Dotação | Empenhado | Liquidado | Pago | Saldo | Alertas |', '|---|---|---|---|---:|---:|---:|---:|---:|---|']
    for line in report['lines']:
        alerts = ', '.join(line['alerts']) if line['alerts'] else 'sem alerta'
        out.append(f"| {line['unidade']} | {line['acao']} | {line['natureza_despesa']} | {line['fonte']} | {line['dotacao']} | {line['empenhado']} | {line['liquidado']} | {line['pago']} | {line['saldo_disponivel']} | {alerts} |")
    out += ['', '> Minuta analítica sujeita a revisão humana.']
    return '\n'.join(out) + '\n'


def simulate(execution: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    percent = Decimal(str(scenario.get('percentage', 0)))
    if percent < 0 or percent > 100:
        raise ValueError('percentage deve estar entre 0 e 100')
    affected = set(scenario.get('affected_units') or [])
    lines = []
    total_impact = Decimal('0')
    for line in execution['lines']:
        applies = not affected or line['unidade'] in affected
        saldo = money(line['saldo_disponivel'])
        impact = (saldo * percent / Decimal('100')) if applies else Decimal('0')
        total_impact += impact
        lines.append({
            'unidade': line['unidade'],
            'acao': line['acao'],
            'natureza_despesa': line['natureza_despesa'],
            'fonte': line['fonte'],
            'scenario_applies': applies,
            'saldo_base': line['saldo_disponivel'],
            'impacto_estimado': q2(impact),
            'saldo_pos_cenario': q2(saldo - impact),
        })
    return {
        'generated_at': now(),
        'scenario': scenario,
        'total_impacto_estimado': q2(total_impact),
        'lines': lines,
        'premises': scenario.get('premises', []),
        'human_review_required': True,
        'warning': 'Simulação de apoio à decisão; não representa decisão orçamentária final.',
    }


def markdown_simulation(report: dict[str, Any]) -> str:
    out = ['# Simulação de Cenário Orçamentário', '', f"Gerado em: {report['generated_at']}", f"Impacto total estimado: {report['total_impacto_estimado']}", '', '## Premissas']
    for p in report.get('premises') or ['Premissas não informadas.']:
        out.append(f'- {p}')
    out += ['', '## Impacto por linha', '', '| Unidade | Ação | Natureza | Impacto | Saldo pós-cenário |', '|---|---|---|---:|---:|']
    for line in report['lines']:
        out.append(f"| {line['unidade']} | {line['acao']} | {line['natureza_despesa']} | {line['impacto_estimado']} | {line['saldo_pos_cenario']} |")
    out += ['', '> Revisão humana obrigatória antes de decisão administrativa.']
    return '\n'.join(out) + '\n'


def checklist_edital(data: dict[str, Any]) -> dict[str, Any]:
    provided = set(data.get('documents_present') or [])
    pending = []
    ok = []
    for item in REQUIRED_EDITAL_DOCS:
        if item['id'] in provided:
            ok.append(item)
        else:
            pending.append(item | {'required_action': f"Anexar ou justificar ausência de: {item['name']}"})
    critical = sum(1 for p in pending if p['severity'] == 'alta')
    return {
        'generated_at': now(),
        'process_id': data.get('process_id', 'a_confirmar'),
        'object': data.get('object', 'a_confirmar'),
        'documents_ok': ok,
        'pending_items': pending,
        'critical_pending_count': critical,
        'status': 'requires_human_review' if pending else 'checklist_complete_subject_to_review',
        'human_review_required': True,
    }


def markdown_checklist(report: dict[str, Any]) -> str:
    out = ['# Checklist de Conformidade de Edital', '', f"Processo: {report['process_id']}", f"Objeto: {report['object']}", f"Status: {report['status']}", '', '## Pendências', '']
    if not report['pending_items']:
        out.append('Nenhuma pendência no checklist automatizado. Revisão humana permanece obrigatória.')
    for p in report['pending_items']:
        out.append(f"- **{p['severity']}** — {p['name']}: {p['required_action']} ({p['normative_reference']})")
    out += ['', '## Documentos presentes', '']
    for item in report['documents_ok']:
        out.append(f"- {item['name']}")
    return '\n'.join(out) + '\n'


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def command_consolidate(args: argparse.Namespace) -> dict[str, Any]:
    records = load_table(Path(args.input))
    report = consolidate_records(records, source=str(args.input))
    out = Path(args.output)
    write_json(out / 'consolidated_execution.json', report)
    write_text(out / 'consolidated_execution.md', markdown_execution(report))
    return {'status': 'completed', 'output': str(out), 'files': ['consolidated_execution.json', 'consolidated_execution.md']}


def command_simulate(args: argparse.Namespace) -> dict[str, Any]:
    execution = json.loads(Path(args.execution).read_text(encoding='utf-8'))
    scenario = json.loads(Path(args.scenario).read_text(encoding='utf-8'))
    report = simulate(execution, scenario)
    out = Path(args.output)
    write_json(out / 'scenario_simulation.json', report)
    write_text(out / 'scenario_simulation.md', markdown_simulation(report))
    return {'status': 'completed', 'output': str(out), 'files': ['scenario_simulation.json', 'scenario_simulation.md']}


def command_checklist(args: argparse.Namespace) -> dict[str, Any]:
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    report = checklist_edital(data)
    out = Path(args.output)
    write_json(out / 'edital_checklist.json', report)
    write_text(out / 'edital_checklist.md', markdown_checklist(report))
    return {'status': 'completed', 'output': str(out), 'files': ['edital_checklist.json', 'edital_checklist.md']}


def command_run_demo(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    out = Path(args.output)
    exec_dir = out / 'execucao'
    sim_dir = out / 'simulacao'
    edital_dir = out / 'edital'
    command_consolidate(argparse.Namespace(input=str(root / 'examples' / 'execution_sample.csv'), output=str(exec_dir)))
    command_simulate(argparse.Namespace(execution=str(exec_dir / 'consolidated_execution.json'), scenario=str(root / 'examples' / 'scenario_cut_10.json'), output=str(sim_dir)))
    command_checklist(argparse.Namespace(input=str(root / 'examples' / 'edital_sample.json'), output=str(edital_dir)))
    metadata = {'status': 'completed', 'generated_at': now(), 'human_review_required': True, 'outputs': [str(exec_dir), str(sim_dir), str(edital_dir)]}
    write_json(out / 'metadata.json', metadata)
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='SQU Tesouraria & Conformidade Pública — protótipo determinístico')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('consolidate')
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.set_defaults(func=command_consolidate)
    p = sub.add_parser('simulate')
    p.add_argument('--execution', required=True)
    p.add_argument('--scenario', required=True)
    p.add_argument('--output', required=True)
    p.set_defaults(func=command_simulate)
    p = sub.add_parser('checklist-edital')
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.set_defaults(func=command_checklist)
    p = sub.add_parser('run-demo')
    p.add_argument('--output', required=True)
    p.set_defaults(func=command_run_demo)
    args = parser.parse_args(argv)
    result = args.func(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
