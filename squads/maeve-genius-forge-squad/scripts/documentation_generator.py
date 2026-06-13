"""Documentation generation for produced squads."""
from __future__ import annotations

import json
from typing import Any, Dict

import yaml

from briefing_parser import BRIEFING_SCHEMA, Briefing

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _yaml_block(value: Any) -> str:
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False).strip()


def generate_documentation(briefing: Briefing, architecture: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, str]:
    agents_list = "\n".join(f"- `{agent['id']}` — {agent['role']}: {agent['objective']}" for agent in architecture["agents"])
    outputs = "\n".join(f"- {item}" for item in briefing.expected_outputs)
    metrics = "\n".join(f"- {item}" for item in briefing.success_metrics) or "- Métricas não informadas no briefing; revisão humana exigida."
    integrations = analysis["observed"].get("integrations", [])
    integrations_text = "\n".join(f"- {item}" for item in integrations) or "- Nenhuma integração foi informada no briefing."
    budget_text = str(briefing.budget_limit) if briefing.budget_limit not in (None, "") else "Não informado; este squad não cria preços fixos sem fundamento."
    readme = f'''# {briefing.project_name}

Squad gerado pelo **Maeve Genius Forge** a partir de briefing estruturado. A documentação abaixo reflete somente funcionalidades efetivamente geradas neste pacote.

## Objetivo

{briefing.objective}

## Problema

{briefing.problem}

## Público-alvo

{briefing.target_audience}

## Artefatos esperados

{outputs}

## Agentes gerados

{agents_list}

## Integrações declaradas

{integrations_text}

## Segurança e aprovações

- Nível de segurança: `{briefing.security_level}`
- Aprovações humanas: {', '.join(briefing.human_approval_requirements) if briefing.human_approval_requirements else 'não informadas; revisar antes de uso externo'}

## Métricas de sucesso

{metrics}

## Orçamento

{budget_text}

## Execução local

```bash
python scripts/validate_generated_squad.py --root .
python scripts/run_squad.py --input examples/sample_input.json --output output/result.json
pytest -q
```

## Limites conhecidos

- A geração é determinística e não consulta fontes externas no modo `--no-llm`.
- Integrações declaradas são documentadas como contratos; chamadas externas exigem implementação e aprovação humana específicas.
- Recomendações comerciais, paletas ou preços só devem ser acrescentados quando o briefing trouxer fundamento verificável.

{FOOTER}
'''
    return {
        "README.md": readme,
        "docs/briefing_schema.md": f"# Schema formal do briefing\n\n```yaml\n{_yaml_block(BRIEFING_SCHEMA)}\n```\n",
        "docs/operating_manual.md": f"# Manual operacional\n\n1. Validar entradas com `scripts/validate_generated_squad.py`.\n2. Executar tasks na ordem definida por `workflows/full_generation_workflow.yaml`.\n3. Bloquear qualquer etapa que exija aprovação humana até registro explícito.\n4. Registrar falhas em `quality_report.json`.\n\n## Briefing normalizado\n\n```yaml\n{_yaml_block(briefing.to_dict())}\n```\n",
        "docs/limitations.md": "# Limitações ainda existentes\n\n- Sem chamadas LLM ou pesquisa web no modo determinístico.\n- Sem publicação externa automática.\n- Sem inferência de preço, paleta visual ou recomendação genérica quando o briefing não fornece base.\n- Validação jurídica, institucional ou de segurança permanece humana quando aplicável.\n",
        "examples/sample_input.json": json.dumps({"request": "Executar fluxo mínimo", "requires_human_review": bool(briefing.human_approval_requirements)}, ensure_ascii=False, indent=2),
        "examples/briefing.normalized.yaml": _yaml_block(briefing.to_dict()) + "\n",
    }
