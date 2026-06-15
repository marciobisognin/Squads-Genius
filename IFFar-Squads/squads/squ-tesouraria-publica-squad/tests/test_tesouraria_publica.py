from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import tesouraria_publica as tp


def test_consolidate_records_totals():
    rows = list(csv.DictReader((ROOT / 'examples' / 'execution_sample.csv').open(encoding='utf-8')))
    report = tp.consolidate_records(rows, source='test')
    assert report['records_count'] == 4
    assert report['totals']['dotacao'] == '1850000.00'
    assert report['totals']['empenhado'] == '1225000.00'
    assert report['totals']['saldo_disponivel'] == '625000.00'
    assert report['human_review_required'] is True


def test_checklist_edital_detects_pending_items():
    data = json.loads((ROOT / 'examples' / 'edital_sample.json').read_text(encoding='utf-8'))
    report = tp.checklist_edital(data)
    assert report['status'] == 'requires_human_review'
    assert report['critical_pending_count'] >= 1
    assert any(item['id'] == 'aprovacao_juridica' for item in report['pending_items'])


def test_run_demo_generates_expected_outputs(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'tesouraria_publica.py'), 'run-demo', '--output', str(tmp_path / 'demo')], text=True, capture_output=True, check=True)
    data = json.loads(result.stdout)
    assert data['status'] == 'completed'
    assert (tmp_path / 'demo' / 'execucao' / 'consolidated_execution.json').is_file()
    assert (tmp_path / 'demo' / 'simulacao' / 'scenario_simulation.md').is_file()
    assert (tmp_path / 'demo' / 'edital' / 'edital_checklist.md').is_file()


def test_contracts_have_required_fields():
    manifest = yaml.safe_load((ROOT / 'squad.yaml').read_text(encoding='utf-8'))
    assert len(manifest['agents']) == 6
    for item in manifest['agents']:
        data = yaml.safe_load((ROOT / item['file']).read_text(encoding='utf-8'))
        assert data['responsibilities']
        assert data['non_responsibilities']
        assert data['human_review_required'] is True
    for item in manifest['tasks']:
        data = yaml.safe_load((ROOT / item['file']).read_text(encoding='utf-8'))
        assert data['human_approval'] is True
        assert 'failure_behavior' in data
