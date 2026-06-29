from pathlib import Path
import json, py_compile, yaml
ROOT = Path(__file__).resolve().parents[1]

def test_required_files_exist():
    for rel in ['README.md','PRD.md','squad.yaml','LICENSE','NOTICE.md','AUTHORS.md','quality_report.json']:
        assert (ROOT / rel).is_file(), rel

def test_agents_have_required_contract_fields():
    fields={'id','name','role','objective','responsibilities','non_responsibilities','input_schema','output_schema','allowed_tools','denied_tools','memory_policy','escalation_policy','quality_criteria'}
    for path in (ROOT/'agents').glob('*.yaml'):
        assert fields <= set(yaml.safe_load(path.read_text(encoding='utf-8'))), path

def test_tasks_have_required_contract_fields():
    fields={'id','description','assigned_agent','dependencies','input_schema','output_schema','validation_rules','timeout','retry_policy','human_approval','failure_behavior'}
    for path in (ROOT/'tasks').glob('*.yaml'):
        assert fields <= set(yaml.safe_load(path.read_text(encoding='utf-8'))), path

def test_workflow_has_review_loop_and_failure_paths():
    data=yaml.safe_load((ROOT/'workflows'/'manim-science-reel-production.yaml').read_text(encoding='utf-8'))
    assert data['review_loop']['max_cycles'] == 2
    assert data['failure_paths']
    assert data['parallel_branches']

def test_scripts_compile():
    for path in (ROOT/'scripts').glob('*.py'):
        py_compile.compile(str(path), doraise=True)

def test_quality_report_is_not_empty():
    report=json.loads((ROOT/'quality_report.json').read_text(encoding='utf-8'))
    assert report['score'] >= 90
    assert report['go_no_go'] == 'go'
