# ISO 42001 AIMS Implementation Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-5.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `iso-42001-aims-implementation`
**Slug no repositório:** `iso-42001-aims-implementation`
**Versão:** `5.0.0`
**Número na seleção original:** 1

## Visão geral

ISO 42001 AIMS Implementation Squad — Protocol v5.0

## Para que serve

Implementar, diagnosticar e preparar evidências de um Sistema de Gestão de Inteligência Artificial alinhado à ISO/IEC 42001, com pipeline de governança, riscos, impacto, controles e prontidão de auditoria.

## Estrutura operacional

- **Agentes:** 8
- **Tasks:** 8
- **Workflows:** 3
- **Scripts:** 2
- **Arquivos totais publicados:** 66

## Agentes

- `agents/ai-inventory-mapper.md` — Mapeador de Inventário de IA — `ai-inventory-mapper`
- `agents/aiia-executor.md` — Executor de AIIA — `aiia-executor`
- `agents/audit-evidence-collector.md` — Coletor de Evidências de Auditoria — `audit-evidence-collector`
- `agents/certification-readiness-checker.md` — Verificador de Prontidão de Certificação — `certification-readiness-checker`
- `agents/gap-analyzer.md` — Analisador de Lacunas ISO 42001 — `gap-analyzer`
- `agents/policy-template-writer.md` — Redator de Políticas e Templates — `policy-template-writer`
- `agents/risk-register-builder.md` — Construtor de Registro de Riscos — `risk-register-builder`
- `agents/soa-architect.md` — Arquiteto de SoA — `soa-architect`

## Tasks principais

- `tasks/01_map_ai_inventory.yaml` — title: "Mapear inventário de IA
- `tasks/02_analyze_iso42001_gaps.yaml` — title: "Analisar gaps ISO/IEC 42001
- `tasks/03_execute_aiia.yaml` — title: "Executar AIIA
- `tasks/04_build_risk_register.yaml` — title: "Construir registro de riscos
- `tasks/05_architect_soa.yaml` — title: "Arquitetar SoA
- `tasks/06_write_policy_templates.yaml` — title: "Escrever políticas e templates
- `tasks/07_collect_audit_evidence.yaml` — title: "Coletar evidências auditáveis
- `tasks/08_check_certification_readiness.yaml` — title: "Checar prontidão de certificação

## Workflows

- `workflows/audit_readiness_4_6_weeks.yaml`
- `workflows/full_implementation_9_12_months.yaml`
- `workflows/gap_analysis_2_4_weeks.yaml`

## Scripts e automação

- `scripts/build_visual_summary_pdf.py`
- `scripts/generate_aims_pack.py`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `TUTORIAL_DIDATICO.md`
- `squad.yaml`
- `docs/RESUMO_VISUAL_DETALHADO.md`
- `docs/estrutura_solicitada_mapeamento.md`
- `docs/pipeline_16_fases.md`

## Propriedade intelectual e licença

- Licença padrão adotada para novos squads de Marcio: MIT.
- Criado por: Marcio Bisognin.
- Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
- Observação: squads legados foram publicados preservando sua estrutura original; quando não houver arquivo de licença interno, considere a política do repositório e a documentação de cada pasta.

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/iso-42001-aims-implementation/squad.yaml` e `squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/iso-42001-aims-implementation/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/iso-42001-aims-implementation/agents/`)
> e conduza o fluxo definido em `squads/iso-42001-aims-implementation/`. Siga `squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/iso-42001-aims-implementation/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/iso-42001-aims-implementation/squad.yaml @squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/iso-42001-aims-implementation/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/iso-42001-aims-implementation/squad.yaml #file:squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/iso-42001-aims-implementation/squad.yaml @squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/iso-42001-aims-implementation/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/iso-42001-aims-implementation/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/iso-42001-aims-implementation/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/iso-42001-aims-implementation/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/iso-42001-aims-implementation/squad.yaml` e `squads/iso-42001-aims-implementation/workflows/full_implementation_9_12_months.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
