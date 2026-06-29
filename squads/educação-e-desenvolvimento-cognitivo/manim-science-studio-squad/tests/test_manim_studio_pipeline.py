from pathlib import Path
import importlib.util, json, sys
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'manim_studio_pipeline.py'
spec = importlib.util.spec_from_file_location('manim_studio_pipeline', SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules['manim_studio_pipeline'] = mod
spec.loader.exec_module(mod)

def test_pipeline_generates_complete_package(tmp_path):
    briefing = json.loads((ROOT / 'examples' / 'briefing_heisenberg.json').read_text(encoding='utf-8'))
    result = mod.generate_package(briefing, tmp_path / 'pkg', True)
    assert result['status'] == 'package_ready'
    assert Path(result['zip_path']).is_file()
    assert (tmp_path / 'pkg' / '03_manim').is_dir()
    assert list((tmp_path / 'pkg' / '05_review').glob('*.md'))

def test_invalid_briefing_reports_clear_errors():
    issues = mod.validate_briefing({'topic':'','complexity_level':'x','target_duration_sec':10})
    assert 'topic é obrigatório' in issues
    assert any('complexity_level' in issue for issue in issues)
    assert any('target_duration_sec' in issue for issue in issues)

def test_slugify_is_stable():
    assert mod.slugify('Princípio da Incerteza!') == 'princ-pio-da-incerteza'
