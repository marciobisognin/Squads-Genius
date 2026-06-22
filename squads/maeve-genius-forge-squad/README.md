# Maeve Genius Forge Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `maeve-genius-forge-squad`

**Nome comercial:** Maeve Genius Forge — fábrica funcional de squads

O Maeve Genius Forge transforma um briefing YAML ou JSON em um squad completo, consistente, validável, testável e executável. A implementação atual é determinística no modo `--no-llm` e gera artefatos reais em disco, não apenas documentos estáticos.

## O que está implementado

O executor `scripts/forge_squad.py` foi refatorado em módulos especializados:

- `briefing_parser.py` — leitura YAML/JSON com parser YAML real e schema formal.
- `requirements_analyzer.py` — análise de lacunas, riscos e revisões humanas.
- `squad_architect.py` — arquitetura de agentes sem redundância de responsabilidades.
- `agent_generator.py` — geração de `agents/*.yaml` com contrato completo.
- `task_generator.py` — geração de tasks com schema, timeout, retry e falha.
- `workflow_generator.py` — workflows com condições, dependências, gates e caminhos de falha.
- `script_generator.py` — scripts Python do squad gerado.
- `documentation_generator.py` — README, docs e exemplos.
- `test_generator.py` — testes automatizados dos arquivos gerados.
- `package_generator.py` — LICENSE, NOTICE, AUTHORS, requirements e relatório de qualidade calculado.

## Schema formal do briefing

Campos suportados:

- `project_name`
- `objective`
- `problem`
- `target_audience`
- `expected_outputs`
- `constraints`
- `integrations`
- `security_level`
- `human_approval_requirements`
- `success_metrics`
- `budget_limit`
- `preferred_models`

Em `--strict`, campos obrigatórios ausentes, tipos inválidos ou campos desconhecidos produzem erro claro. Sem `--strict`, aliases legados como `audience` e `success_criteria` são normalizados com aviso.

## Uso rápido

```bash
python scripts/forge_squad.py \
  --briefing examples/briefing_atena_contratos_publicos.yaml \
  --output output/atena-contratos-publicos \
  --overwrite \
  --strict \
  --no-llm

python scripts/validate_squad.py --root output/atena-contratos-publicos
pytest -q
```

## Modos do executor

- `--dry-run`: analisa o briefing e mostra componentes planejados sem gravar arquivos.
- `--strict`: valida o briefing com rigidez de schema.
- `--overwrite`: substitui o diretório de saída quando já existe.
- `--format yaml|json`: força o formato de leitura.
- `--no-llm`: executa em modo determinístico, sem chamadas externas.
- `--budget-limit`: sobrescreve o limite de orçamento informado no briefing.

## Artefatos obrigatórios gerados

Cada execução completa gera:

- `squad.yaml`
- `README.md`
- `agents/*.yaml`
- `tasks/*.yaml`
- `workflows/*.yaml`
- `scripts/*.py`
- `tests/`
- `examples/`
- `docs/`
- `LICENSE`
- `NOTICE.md`
- `AUTHORS.md`
- `requirements.txt`
- `quality_report.json`

## Critérios de qualidade

O `quality_report.json` registra componentes gerados, validações executadas, testes aprovados, testes reprovados, riscos, itens de revisão humana e nota calculada. A nota não é fixa: deriva da proporção de validações aprovadas, penalidades por risco, testes reprovados e revisões pendentes.

## Limitações conhecidas

- O modo atual é determinístico e não executa pesquisa web nem chamadas LLM.
- Integrações declaradas viram contratos e gates; chamadas externas reais exigem implementação específica e aprovação humana.
- O Forge não cria preços, paletas ou recomendações comerciais quando o briefing não fornece base verificável.
- Publicação GitHub permanece bloqueada até autorização humana explícita.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-genius-forge-squad/squad.yaml` e `squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/maeve-genius-forge-squad/agents/forge-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/maeve-genius-forge-squad/agents/forge-orchestrator.md`
> e conduza o fluxo definido em `squads/maeve-genius-forge-squad/`. Siga `squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-genius-forge-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml. Conduza o fluxo para o briefing: <...>
```
- Use **`@caminho/arquivo`** para dar contexto preciso (autocompleta no prompt).
- Disponível em **CLI, app desktop/web (claude.ai/code) e extensões VS Code / JetBrains**.

</details>

<details>
<summary><b>🟦 Cursor</b></summary>

<br>

1. Abra a pasta do repositório no Cursor.
2. No **Chat / Composer (⌘/Ctrl + I)**, referencie os arquivos com `@`:
   ```text
   @squads/maeve-genius-forge-squad/squad.yaml @squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-genius-forge-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-genius-forge-squad/squad.yaml #file:squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-genius-forge-squad/squad.yaml @squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-genius-forge-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-genius-forge-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-genius-forge-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-genius-forge-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-genius-forge-squad/squad.yaml` e `squads/maeve-genius-forge-squad/workflows/full_forge_pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
