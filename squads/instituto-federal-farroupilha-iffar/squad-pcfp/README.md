# 🧮 Squad PCFP — Planilhas de Custos e Formação de Preços

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `squad-pcfp` | **Versão:** `1.0.0` | **Origem:** PRD Squad PCFP v1.0 ([docs/prd_squad_pcfp_v1.md](docs/prd_squad_pcfp_v1.md))

Squad multi-agente para **elaboração, validação e auditoria de PCFP** em contratos com dedicação exclusiva de mão de obra (administração pública federal): intake → pesquisa normativa → cálculo determinístico → conformidade → exequibilidade → artefatos → gestão contratual (repactuação/reajuste), com **Human-in-the-Loop obrigatório** nos pontos de decisão jurídica.

> ⚖️ **Automação não é parecer jurídico.** Percentuais embarcados são referências a conferir contra a redação vigente e os Cadernos Técnicos SEGES. Todo relatório exige "responsável pela validação".

## Princípios (do PRD)

1. **Cálculo determinístico, raciocínio por LLM** — nenhum valor monetário é gerado por LLM; a engine (`scripts/pcfp_core.py`) é a única fonte de números.
2. **Rastreabilidade total** — cada rubrica: `{valor, formula, fundamento, fonte, renovavel, conta_vinculada}`.
3. **HITL nos pontos jurídicos** — Gate 1: enquadramento sindical; Gate 2: aprovação final/parecer de repactuação.
4. **Schema-first** — handoffs via JSON validado ([templates/schemas.md](templates/schemas.md)).

## Os 8 agentes

| Agente | Função |
|---|---|
| **A1** Orquestrador | classifica a demanda, monta o grafo, gerencia gates |
| **A2** Intake & Classificação | ServiceProfile (CBO, escala, postos); parser de propostas |
| **A3** Normativo (RAG) | checklist por caso, índice temporal de vigência das normas |
| **A4** CCT & Sindical | CCTProfile cláusula a cláusula; **HITL Gate 1** |
| **A5** Engine de Cálculo | módulos 1–6 do Anexo VII-D via `pcfp_core.py` |
| **A6** Auditor de Conformidade | checklist TCU/CGU + exequibilidade verde/amarelo/vermelho |
| **A7** Gestão Contratual | repactuação × reajuste, preclusão, conta vinculada; **HITL Gate 2** |
| **A8** Gerador de Artefatos | planilha Anexo VII-D, relatório técnico, checklist assinável |

## Workflows

- `elaboracao_pcfp_nova` — fluxo principal (loop de correção A6→A5, máx. 3 iterações).
- `analise_proposta_licitante` — recálculo paralelo + diff célula a célula para o pregoeiro.
- `repactuacao_reajuste` — demonstração analítica por nova CCT/índice (arts. 54–60 da IN 05/2017).

## Scripts determinísticos (Python 3.11+, sem dependências) — testados

```bash
python3 scripts/pcfp_core.py --input examples/exemplo_input_limpeza44h.json   # módulos 1-6 → CostSheet
python3 scripts/validar_pcfp.py --costsheet costsheet.json                    # ComplianceReport
python3 scripts/diff_proposta.py --referencia ref.json --proposta prop.json   # diff de exequibilidade
```

## Base normativa

Lei 14.133/2021 · IN SEGES 05/2017 + Anexo VII-D e Anexo XII · IN 07/2018 · IN 98/2022 · IN 176/2024 · IN 147/2026 · Decreto 12.174/2024 · LC 214/2025 (CBS/IBS) · Lei 14.973/2024 · Acórdãos TCU 1207/2024, 1442/2010, 593/2010, 614/2008 · IN Conjunta MP/CGU 01/2016 — detalhes e papel de cada norma em [docs/base_normativa.md](docs/base_normativa.md).

## Roadmap (PRD, seção 6)

F0 Fundação (corpus + pcfp-core com golden tests) → F1 MVP limpeza 44h → F2 Conformidade → F3 CCT & multi-serviço → F4 Ciclo de vida → F5 Reforma Tributária. **Esta versão do repositório implementa a camada agentiva completa + engine F0**; XLSX/RAG/LangGraph são a implantação de produção descrita no PRD (seção 4).

## Squads irmãos

- [`hefesto-forja-licitatoria-squad`](../hefesto-forja-licitatoria-squad/) — monta o processo licitatório (a PCFP instrui o TR/edital); candidato a "A9 pesquisa de preços" da questão aberta nº 3 do PRD.
- [`themis-contratos-publicos-squad`](../themis-contratos-publicos-squad/) — análise jurídica independente de contratos e aditivos.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/squad-pcfp/squad.yaml` e `IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/squad-pcfp/agents/a1-orquestrador-maestro.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/squad-pcfp/agents/a1-orquestrador-maestro.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/squad-pcfp/`. Siga `IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/squad-pcfp/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/squad-pcfp/squad.yaml @IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/squad-pcfp/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/squad-pcfp/squad.yaml #file:IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/squad-pcfp/squad.yaml @IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/squad-pcfp/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/squad-pcfp/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/squad-pcfp/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/squad-pcfp/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/squad-pcfp/squad.yaml` e `IFFar-Squads/squads/squad-pcfp/workflows/elaboracao_pcfp_nova.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
