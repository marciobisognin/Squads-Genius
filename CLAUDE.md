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

## Playbook completo de construção e publicação de squads (AUTORIZAÇÃO PERMANENTE)

> **Autorização permanente concedida por Marcio Bisognin:** sempre que o pedido for "criar/construir
> um squad" (com ou sem PRD/briefing anexado), execute TODO o fluxo abaixo de ponta a ponta, **sem
> pedir autorização e sem indicar/perguntar a cada etapa** — incluindo commit, push, abertura de PR,
> **merge na `main`**, publicação no site e melhoria do README. Só pare se faltar uma informação que
> impeça a construção, ou se houver risco fora do escopo de "construir squad" (ex.: apagar conteúdo de
> terceiros, expor segredos). Esta autorização sobrescreve a regra antiga de "não publicar sem pedir".

Sequência exata, validada na prática (ex.: squad **KÊRYX** / `squad-keryx`):

1. **Briefing.** Se houver PRD/material anexado, use-o como briefing consolidado. Salve um YAML em
   `squads/maeve-genius-forge-squad/examples/briefing_<nome>.yaml` com o schema do `briefing_parser.py`:
   `project_name, objective, problem, target_audience, expected_outputs, constraints, integrations,
   security_level, human_approval_requirements, success_metrics, budget_limit, preferred_models`.
2. **Scaffold determinístico (boilerplate).** A partir de `squads/maeve-genius-forge-squad/`:
   `python3 scripts/forge_squad.py --briefing <b.yaml> --output <scratchpad> --overwrite`.
   Reaproveite os arquivos prontos: `LICENSE`, `NOTICE.md`, `AUTHORS.md`, `.ip/ownership.json`,
   `.ip/response-footer.md`.
3. **Construção real** em `squads/<nome-tecnico>/` (ou `IFFar-Squads/squads/<nome>/` se institucional).
   Requisitos do `validate_squad.py` (precisam existir, senão dá no-go):
   - **Diretórios:** `agents/`, `tasks/`, `workflows/`, `scripts/`, `examples/`, `docs/`.
   - **Arquivos:** `squad.yaml`, `README.md`, `LICENSE`, `NOTICE.md`, `AUTHORS.md`.
   - `squad.yaml` deve ter arrays `agents[].file`, `tasks[].file`, `workflows[].file` e **todos os
     caminhos devem existir**. Todo `.py` precisa compilar; todo YAML válido; **zero segredos**.
   - Agentes em Markdown (missão, étimo, schemas I/O, regras, comandos); scripts determinísticos reais
     (stdlib quando possível) com `if __name__ == "__main__"`; schemas Pydantic com fallback dataclasses;
     footer obrigatório em todos os arquivos.
4. **Validar até `go`:** `python3 scripts/validate_squad.py --root squads/<nome>` (corrigir e repetir).
5. **Registrar:** adicionar linha em `SQUAD_INDEX.md` (e em `IFFar-Squads/README.md` se institucional).
6. **Git + GitHub (autônomo):** trabalhar no branch de feature designado; `git commit`; `git push -u
   origin <branch>` (retry com backoff em erro de rede). Abrir PR com `mcp__github__create_pull_request`
   (base `main`) e **mesclar** com `mcp__github__merge_pull_request` (`merge_method: squash`).
   - Footer de commit: `Co-Authored-By: Claude ...` + `Claude-Session: ...`. Footer de PR: bloco
     "🤖 Generated with Claude Code". **Nunca** incluir o ID do modelo em artefatos.
7. **Publicar no site** (`https://marciobisognin.github.io/Squads-Genius/`, servido de `docs/` na `main`):
   - Editar `docs/build/squads_data.json` adicionando a entrada do squad (`id, name, tagline, color,
     card_icon, agents[], tools[], steps[], output, category`). **Categoria** deve ser uma de
     `CATEGORY_ORDER` em `docs/build/generate_site.py`. **Ícones** só os de `VALID_ICONS`.
   - Campo opcional `links[]` (`{label, url}`) gera chips de acesso na página (GitHub, README,
     squad.yaml, manual). Regenerar: `python3 docs/build/generate_site.py docs/build/squads_data.json`.
   - Commitar/PR/merge como no passo 6 (página + index só do squad novo devem mudar).
8. **README premium** (padrão da galeria — referências: `scriptorium-squad`, `darkhold-...`):
   título centralizado + badges shields.io (versão/status/licença/idioma + stats), bloco de **Navegação**,
   metáfora do nome, callouts (`> [!IMPORTANT|NOTE|TIP|CAUTION]`), tabela de agentes, diagrama **Mermaid**
   do pipeline, design system em tabela, **Início rápido**, e a seção **"🤝 Como usar nos principais LLMs
   de codificação"** com prompt de ativação copiável + blocos `<details>` por ferramenta (Claude Code,
   Cursor, GitHub Copilot, Windsurf, Cline/Roo, Continue.dev/Aider/Zed, ChatGPT/Gemini), contratos,
   métricas, stack, nota de IP e footer. Manter fences/`<details>`/`<div>` balanceados.

### Limitações conhecidas do ambiente
- **Release/tag do GitHub:** o MCP só tem leitura de releases (sem `create_release`) e `git push` de
  **tags** retorna **403** (credenciais com escopo do branch). Release formal fica para o usuário (UI);
  entregar as notas prontas quando pedirem.
- Render real de PNG/PDF exige `jinja2 + playwright + pillow`; sem eles, os motores degradam para
  manifesto + `render_hash` (ainda determinístico/auditável).

### Categorias do site (`CATEGORY_ORDER`)
`Construção de Squads & Sistemas de IA` · `Negócios, Estratégia & Vendas` · `Conhecimento, Pesquisa &
Dados` · `Conteúdo, Marketing & Visual` · `Educação & Desenvolvimento Cognitivo` · `Jurídico, Risco,
Finanças & Segurança` · `Saúde, Bem-estar & Expressão` · `Instituto Federal Farroupilha (IFFar)`.

## Convenções gerais do repositório

- Idioma principal: pt-BR.
- Licença MIT; manter os créditos de autoria (Marcio Bisognin) em README, AUTHORS e footer.
- **Construção de squads:** fluxo totalmente autônomo (ver "Playbook completo" acima) — criar, validar,
  registrar, commitar, PR, **merge na `main`**, publicar no site e README premium, sem pedir autorização.
- Para ações **fora** do escopo de construir squads (ex.: mexer em repositórios de terceiros, releases
  formais, mudanças destrutivas amplas), manter a cautela e confirmar antes.
