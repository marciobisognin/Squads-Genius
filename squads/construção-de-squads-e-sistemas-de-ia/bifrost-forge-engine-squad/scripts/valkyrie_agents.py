#!/usr/bin/env python3
"""Valkyrie Agent Marshal — materializa os agentes escolhidos como personas Markdown.

A Valquíria escolhe os Einherjar para o salão; aqui escolhemos e escrevemos o
roster mínimo de agentes do squad-alvo, cada um com missão, contratos I/O,
regras, ferramentas permitidas/negadas e footer obrigatório.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _bullets(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- (nenhum)"


def render_agent(agent: Dict[str, Any]) -> str:
    return f"""# {agent['name']} (`{agent['id']}`)

## Missão
{agent['objective']}

## Papel
{agent['role']}

## Capacidades
{_bullets(agent.get('capabilities', []))}

## Responsabilidades
{_bullets(agent['responsibilities'])}

## Não faz
{_bullets(agent['non_responsibilities'])}

## Contrato de entrada
```json
{json.dumps(agent['input_schema'], ensure_ascii=False, indent=2)}
```

## Contrato de saída
```json
{json.dumps(agent['output_schema'], ensure_ascii=False, indent=2)}
```

## Ferramentas permitidas
{_bullets(agent['allowed_tools'])}

## Ferramentas negadas
{_bullets(agent['denied_tools'])}

## Política de memória
{agent['memory_policy']}

## Política de escalonamento
{agent['escalation_policy']}

## Critérios de qualidade
{_bullets(agent['quality_criteria'])}

## Comandos
- `*help` — lista comandos e orienta o uso deste agente.
- `*run` — executa a etapa principal do agente.
- `*review` — revisa o artefato contra os quality gates.
- `*exit` — encerra e devolve o controle ao fluxo principal.

---
{FOOTER}
"""


def generate_agent_files(agents: List[Dict[str, Any]]) -> Dict[str, str]:
    return {f"agents/{agent['id']}.md": render_agent(agent) for agent in agents}


if __name__ == "__main__":  # pragma: no cover
    print("Valkyrie Agent Marshal — módulo de geração de agentes.\n" + FOOTER)
