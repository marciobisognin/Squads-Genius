# Squads-Genius — Guia para o Claude Code

Repositório de squads AIOS/OpenSquad criados por Marcio Bisognin. Cada squad vive em `squads/<nome>/` com manifesto `squad.yaml`, agentes em `agents/`, tarefas em `tasks/`, fluxos em `workflows/` e automações em `scripts/`.

## Construtor de squads (ATIVO)

O construtor oficial de squads deste repositório é o **Maeve Genius Forge Squad** (`squads/maeve-genius-forge-squad/`). Ele transforma um briefing livre em um squad completo: pesquisa, oferta, design system, agentes, tasks, workflows, scripts e documentação.

### Como ativar em uma sessão

- Comando rápido: use o slash command **`/criar-squad <briefing ou nome do projeto>`**.
- Ativação manual: leia `squads/maeve-genius-forge-squad/squad.yaml` e assuma a persona do agente `forge-orchestrator` (`agents/forge-orchestrator.md`), seguindo o pipeline `workflows/full_forge_pipeline.yaml` (15 fases, com quality gates e humano no loop).

### Regras obrigatórias do construtor

- Separar sempre: observado, inferido, hipótese, recomendação e risco.
- Registrar fontes, decisões e premissas.
- Priorizar scripts determinísticos quando a etapa não exigir LLM.
- Não copiar marca, texto, prompt ou ativo proprietário de terceiros.
- Nunca publicar `.env`, tokens, chaves ou credenciais.
- Encerrar entregas finais com o footer: `Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.`

### Scripts determinísticos do construtor

Executar a partir de `squads/maeve-genius-forge-squad/` (Python 3.11+, sem dependências externas):

```bash
python3 scripts/forge_squad.py --briefing <briefing.yaml> --output <pasta>   # scaffold inicial a partir do briefing
python3 scripts/validate_squad.py --root <pasta-do-squad>                    # quality gates / go-no-go
python3 scripts/generate_readme.py ...                                       # README do squad
python3 scripts/estimate_costs.py --root <pasta> --manual-hours N --hourly-rate X
python3 scripts/package_squad.py --root <pasta> --output <zip>
```

Briefings de exemplo em `squads/maeve-genius-forge-squad/examples/`. Template de briefing em `templates/briefing.yaml`.

### Onde os novos squads devem ser criados

- Squads gerais: `squads/<nome-tecnico-do-squad>/`.
- Squads institucionais/IFFar: `IFFar-Squads/squads/<nome-tecnico-do-squad>/`.
- Estrutura mínima: `squad.yaml`, `README.md`, `agents/`, `tasks/`, `workflows/` (e `scripts/`, `templates/` quando aplicável).
- Após criar, registrar o squad em `SQUAD_INDEX.md` e, quando for institucional/IFFar, também em `IFFar-Squads/README.md`.
- Validar com `validate_squad.py` antes de considerar concluído.

## Convenções gerais do repositório

- Idioma principal: pt-BR.
- Licença MIT; manter os créditos de autoria (Marcio Bisognin) em README, AUTHORS e footer.
- Não criar pull requests nem publicar releases sem autorização explícita do usuário.
