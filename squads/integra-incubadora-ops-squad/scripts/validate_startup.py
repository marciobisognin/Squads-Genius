"""Script: validate_startup.py

Este script implementa a validação de um perfil de startup recebido em formato JSON.  Ele
usa o modelo `StartupProfile` definido em `schemas.py` para validar a estrutura e
aplica uma rotina simples de scoring baseada nos critérios listados no PRD.  O
script será chamado pelo workflow `startup-pipeline` na etapa de triagem.

Para ser usado em um ambiente de produção basta executar:

```
poetry run python scripts/validate_startup.py --input data/startup.json --output data/validated.json
```
"""

from __future__ import annotations

import json
import argparse
from pathlib import Path

# Import schema for validation
try:
    from schemas import StartupProfile
except Exception as exc:  # pragma: no cover - défault environment may not have schemas yet
    raise ImportError("Unable to import schemas module. Make sure it is in PYTHONPATH.") from exc


def score_startup(profile: dict) -> float:
    """Calcula um score de admissibilidade simples.

    O critério usado aqui é apenas ilustrativo: 0 a 50 pontos são
    ganhos para cada critério satisfatório.
    """
    score = 0
    criteria = [
        profile.get("candidato").get("formacao_institucional"),  # bool
        profile.get("candidato").get("convocatoria_participante"),
        profile.get("startup").get("has_prototipo"),
        profile.get("startup").get("modelo_negocio_validado"),
    ]
    for c in criteria:
        if c:
            score += 10
    return min(score, 100)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate startup profile input")
    parser.add_argument("--input", required=True, help="Path to the input JSON file")
    parser.add_argument("--output", required=True, help="Path for the validated output JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        parser.error(f"Input file {input_path} not found")

    with input_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    # Validate structure
    startup = StartupProfile(**data)

    # Compute score
    startup.score_admissao = score_startup(data)

    # Write validated JSON
    with output_path.open("w", encoding="utf-8") as fp:
        json.dump(startup.dict(), fp, ensure_ascii=False, indent=2)

    print(f"Startup validated and written to {output_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
