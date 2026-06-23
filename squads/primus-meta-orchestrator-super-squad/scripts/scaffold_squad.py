#!/usr/bin/env python3
"""Scaffolder determinístico de novos squads do Primus Meta-Orchestrator.

Cria o esqueleto completo de um squad novo (estrutura mínima exigida pelo
repositório), pronto para ser validado por validate_squad.py e refinado pelo
Maeve Genius Forge. Usado pelo Primus quando o roteador detecta uma lacuna.

Uso:
  python3 scaffold_squad.py \
      --name meu-novo-squad \
      --commercial-name "Meu Novo Squad" \
      --positioning "Resolve X para Y" \
      --agents "orquestrador:Coordena o squad;executor:Executa a tarefa" \
      --output ../meu-novo-squad
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

LICENSE_TEXT = """MIT License

Copyright (c) 2026 Marcio Bisognin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

AGENT_TEMPLATE = """# {agent_id}

## Missão
{role}

## Regras obrigatórias
- Separar sempre: observado, inferido, hipótese, recomendação e risco.
- Registrar fontes, decisões e premissas quando aplicável.
- Priorizar scripts determinísticos quando a etapa não exigir LLM.
- Não copiar marca, texto, prompt ou ativo proprietário de terceiros.
- Encerrar entrega final com: `{footer}`

## Entradas
- Briefing do usuário.
- Artefatos das etapas anteriores.

## Saídas
- Artefato Markdown/YAML/JSON validável.
- Lista de decisões e riscos.

## Comandos
- `*help` — lista comandos disponíveis e orienta como usar este agente.
- `*run` — executa a etapa principal do agente.
- `*review` — revisa o artefato produzido contra os quality gates.
- `*exit` — encerra a interação e devolve o controle ao fluxo principal.
"""

TASK_TEMPLATE = """id: 01_execute
title: "Executar a tarefa principal do squad."
owner: {owner}
objective: "Produzir o artefato principal do squad com rastreabilidade."
inputs:
  - briefing
  - previous_outputs
outputs:
  - artifact
  - assumptions
  - risks
acceptance_criteria:
  - "Saída separa observado, inferido, hipótese e recomendação quando aplicável"
  - "Riscos e limitações registrados"
  - "Footer obrigatório incluído em entregas finais"
required_footer: "{footer}"
"""

WORKFLOW_TEMPLATE = {
    "id": "main_pipeline",
    "description": "Pipeline principal do squad.",
    "human_in_loop": True,
    "rollback": "retornar ao último gate reprovado",
    "steps": [
        {"order": 1, "name": "Intake", "gate_required": False},
        {"order": 2, "name": "Execução", "gate_required": True},
        {"order": 3, "name": "Validação", "gate_required": True},
    ],
}


def parse_agents(spec: str) -> list[dict[str, str]]:
    agents: list[dict[str, str]] = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            aid, role = part.split(":", 1)
        else:
            aid, role = part, ""
        aid = re.sub(r"[^a-z0-9\-]", "-", aid.strip().lower()).strip("-")
        if aid:
            agents.append({"id": aid, "role": role.strip() or f"Agente {aid}."})
    if not agents:
        agents = [{"id": "orquestrador", "role": "Coordena o squad."}]
    return agents


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Cria o esqueleto de um novo squad.")
    ap.add_argument("--name", required=True, help="nome técnico (kebab-case).")
    ap.add_argument("--commercial-name", default="")
    ap.add_argument("--positioning", default="")
    ap.add_argument("--agents", default="orquestrador:Coordena o squad;executor:Executa a tarefa")
    ap.add_argument("--output", required=True, help="pasta de destino do novo squad.")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    name = re.sub(r"[^a-z0-9\-]", "-", args.name.strip().lower()).strip("-")
    out = Path(args.output).resolve()
    if out.exists() and any(out.iterdir()) and not args.force:
        print(json.dumps({"error": f"destino não vazio: {out} (use --force)"}, ensure_ascii=False))
        return 2

    agents = parse_agents(args.agents)
    commercial = args.commercial_name or name.replace("-", " ").title()

    manifest = {
        "name": name,
        "commercial_name": commercial,
        "version": "0.1.0",
        "language": "pt-BR",
        "license": "MIT",
        "creator": "Marcio Bisognin",
        "instagram": "@marciobisognin",
        "positioning": args.positioning or f"Squad {commercial}.",
        "required_footer": FOOTER,
        "agents": [
            {"id": a["id"], "file": f"agents/{a['id']}.md", "role": a["role"]}
            for a in agents
        ],
        "tasks": [{"id": "01_execute", "file": "tasks/01_execute.yaml", "owner": agents[0]["id"],
                   "objective": "Executar a tarefa principal do squad."}],
        "workflows": [{"id": "main_pipeline", "file": "workflows/main_pipeline.yaml"}],
    }

    # Estrutura mínima exigida pelo validador do repositório.
    for d in ["agents", "tasks", "workflows", "scripts", "examples", "docs", ".ip"]:
        (out / d).mkdir(parents=True, exist_ok=True)

    write(out / "squad.yaml", json.dumps(manifest, ensure_ascii=False, indent=2))
    write(out / "LICENSE", LICENSE_TEXT)
    write(out / "NOTICE.md", f"# Notice\n\n{commercial}.\n\n{FOOTER}\n")
    write(out / "AUTHORS.md",
          "# Autores\n\n- Marcio Bisognin — criador e titular do squad. Instagram: @marciobisognin\n")
    write(out / "README.md",
          f"# {commercial}\n\n{manifest['positioning']}\n\n"
          f"- Nome técnico: `{name}`\n- Versão: 0.1.0\n- Licença: MIT\n\n"
          f"## Agentes\n\n" +
          "".join(f"- `{a['id']}` — {a['role']}\n" for a in agents) +
          f"\n## Status\n\nEsqueleto gerado pelo Primus Meta-Orchestrator. "
          f"Refine com o Maeve Genius Forge e valide antes de publicar.\n\n---\n\n{FOOTER}\n")
    write(out / ".ip" / "ownership.json", json.dumps({
        "project": name, "commercial_name": commercial, "license": "MIT",
        "creator": "Marcio Bisognin", "instagram": "@marciobisognin",
        "footer_required": True, "footer": FOOTER,
    }, ensure_ascii=False, indent=2))
    write(out / ".ip" / "response-footer.md", FOOTER + "\n")
    write(out / ".gitkeep" if False else out / "examples" / ".gitkeep", "")
    write(out / "docs" / ".gitkeep", "")
    write(out / "scripts" / ".gitkeep", "")

    for a in agents:
        write(out / "agents" / f"{a['id']}.md",
              AGENT_TEMPLATE.format(agent_id=a["id"], role=a["role"], footer=FOOTER))
    write(out / "tasks" / "01_execute.yaml",
          TASK_TEMPLATE.format(owner=agents[0]["id"], footer=FOOTER))
    write(out / "workflows" / "main_pipeline.yaml",
          json.dumps(WORKFLOW_TEMPLATE, ensure_ascii=False, indent=2))

    print(json.dumps({
        "created": str(out),
        "name": name,
        "agents": [a["id"] for a in agents],
        "next": "Valide com validate_squad.py --root <pasta> e refine com o Maeve Genius Forge.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
