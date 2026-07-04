from datetime import date
from pathlib import Path
from argos.graph import ArgosPipeline
if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = ArgosPipeline(root).run(root / 'perfis' / 'contratos-iffar-f0.yaml', date(2026, 7, 2), output_dir=root / 'generated' / 'demo', fixture=True)
    print(result.model_dump_json(indent=2))
