# ⚒️ Hefesto Forja Licitatória

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `hefesto-forja-licitatoria-squad`
**Versão:** `1.0.0` | **Tier:** Premium

Squad que transforma a **documentação inicial do órgão** em um **processo de licitação completo**, na modalidade solicitada (pregão, concorrência, diálogo competitivo, leilão, concurso, dispensa ou inexigibilidade), gerando todos os artefatos da fase preparatória e os instrumentos do certame — com base na **Lei 14.133/2021**, na estrutura dos **modelos oficiais da AGU/CNMLC** e nas **INs SEGES** e referenciais da **CGU**.

> ⚖️ **Ressalva obrigatória:** os artefatos são minutas de apoio técnico. Na esfera federal, os modelos AGU/CNMLC são de uso obrigatório ou exigem justificativa (art. 19, IV). O processo real exige parecer jurídico (art. 53) e autorização da autoridade competente. Revisão humana obrigatória.

## Diferencial premium: intake que pergunta

O agente **`intake-requisitos-clarifier`** é um gate bloqueante: ele inventaria o que você entregou, roda uma checagem determinística de campos por modalidade e — se faltar informação essencial — **devolve perguntas numeradas, com o motivo legal de cada uma, e pausa a forja até você responder**. Nada é inventado: lacuna vira pergunta ou premissa explícita confirmada por você.

## O que o squad gera (dossiê completo)

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de intake | suficiência documental |
| 2 | Nota de enquadramento | modalidade/rito — arts. 28-33, 74-75 |
| 3 | DFD | Decreto 10.947/2022 |
| 4 | ETP | art. 18, §1º + IN SEGES 58/2022 |
| 5 | Pesquisa de preços + planilha CSV | art. 23 + IN SEGES 65/2021, estatísticas por script |
| 6 | Matriz de riscos | art. 22 + IN Conjunta MP/CGU 01/2016 |
| 7 | Termo de referência | art. 6º, XXIII, estrutura AGU/CNMLC |
| 8 | Edital + anexos (ou aviso de contratação direta) | art. 25 (ou art. 72) |
| 9 | Minuta de contrato | art. 92, cláusula a cláusula com refs |
| 10 | Nota de conformidade + dossiê indexado | checklists e coerência cruzada |

## Agentes (9)

`hefesto-orchestrator` · `intake-requisitos-clarifier` · `enquadramento-modalidade-strategist` · `planejamento-dfd-etp-architect` · `termo-referencia-writer` · `pesquisa-precos-planilhista` · `matriz-riscos-engineer` · `edital-minutas-redator` · `conformidade-dossie-auditor`

## Workflows (3)

- `processo_licitacao_completo` — 11 etapas, 6 gates, handoff humano final.
- `contratacao_direta` — dispensa/inexigibilidade com a documentação do art. 72.
- `complementar_informacoes` — ciclo curto quando o usuário retorna com respostas.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/intake_suficiencia.py --solicitacao examples/exemplo_solicitacao_pregao.json
python3 scripts/analise_pesquisa_precos.py --planilha examples/exemplo_cotacoes.csv
python3 scripts/montar_dossie.py --pasta <pasta-do-processo> --fluxo licitacao
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/hefesto-orchestrator.md`.
2. Preencha `templates/solicitacao_contratacao.yaml` (ou descreva livremente) e entregue os documentos que tiver.
3. Responda às perguntas do intake e aprove os gates.
4. Receba o dossiê e siga o handoff humano (modelos oficiais AGU → jurídico → autoridade).

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_e_modelos.md`](docs/base_normativa_e_modelos.md). Para revisão jurídica cruzada do resultado, use o squad irmão [`themis-contratos-publicos-squad`](../themis-contratos-publicos-squad/).

## Princípios

- Informação faltante NUNCA é inventada: o intake pergunta.
- Decisões do órgão são marcadas `[[DECISÃO DO ÓRGÃO]]`, nunca tomadas pela forja.
- Cálculos de preço sempre por script determinístico.
- Estrutura dos modelos oficiais, sem cópia literal; tudo `a confirmar` é listado na nota de conformidade.
- Consistência cruzada de objeto, valores e prazos em todos os artefatos.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml` e `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/agents/hefesto-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/agents/hefesto-orchestrator.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/`. Siga `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml @IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml #file:IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml @IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/hefesto-forja-licitatoria-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/squad.yaml` e `IFFar-Squads/squads/hefesto-forja-licitatoria-squad/workflows/processo_licitacao_completo.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
