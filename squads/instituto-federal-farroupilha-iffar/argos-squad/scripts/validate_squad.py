from __future__ import annotations
import argparse, json
from pathlib import Path
REQUIRED = ['README.md','PRD.md','squad.yaml','SKILL.md','model_profile.yaml','src/argos/cli.py','src/argos/contracts.py','src/argos/graph.py','src/argos/ophthalmoi/dou_inlabs.py','src/argos/engines/kanon_lex.py','tests/test_pipeline_and_gates.py','LICENSE','NOTICE.md','AUTHORS.md']
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default='.'); args = ap.parse_args(); root = Path(args.root)
    missing = [p for p in REQUIRED if not (root / p).exists()]
    counts = {'agents': len(list((root/'agents').glob('*.yaml'))), 'tasks': len(list((root/'tasks').glob('*.yaml'))), 'workflows': len(list((root/'workflows').glob('*.yaml')))}
    result = {'go_no_go': 'go' if not missing and counts['agents'] >= 8 and counts['tasks'] >= 5 and counts['workflows'] >= 1 else 'no-go', 'missing': missing, 'counts': counts}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['go_no_go'] == 'go' else 2
if __name__ == '__main__':
    raise SystemExit(main())
