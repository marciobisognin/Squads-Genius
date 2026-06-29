# 🛡️ Árgus — Conta Vinculada

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `argus-conta-vinculada-squad` | **Versão:** `1.0.0` | **Origem:** Dossiê Normativo + PRD da Conta Vinculada ([docs/prd_conta_vinculada.md](docs/prd_conta_vinculada.md))

Squad multiagente para **geração e manutenção automática da planilha da Conta-Depósito Vinculada** (Anexo XII da IN SEGES/MPDG 05/2017; art. 121 da Lei 14.133/2021) em contratos com dedicação exclusiva de mão de obra na administração pública federal: parâmetros → extração de contracheque e FGTS Digital → provisão mensal → conferência FGTS/INSS → liberações (13º, férias, rescisão, encerramento) → planilha `.xlsx` auditável, com **Human-in-the-Loop obrigatório** na parametrização jurídica e na autorização de cada liberação.

> ⚖️ **Automação não é parecer jurídico nem contábil.** Percentuais embarcados são referências a conferir contra a redação vigente e os Cadernos de Logística da SEGES. A multa sobre aviso (4% atual / 5% literal) deve ser confirmada com a Procuradoria/AGU local. Todo relatório exige "responsável pela validação".

Árgus Panoptes era o gigante de cem olhos que nunca dormia. Aqui, ele vigia cada depósito, cada provisão e cada liberação da conta bloqueada.

## Princípios (do PRD)

1. **Cálculo determinístico, raciocínio por LLM** — nenhum valor monetário é gerado por LLM; a engine (`scripts/conta_vinculada_core.py`) é a única fonte de números.
2. **Rastreabilidade total** — cada rubrica: `{valor, formula, percentual, fundamento, fonte}`.
3. **Fail-closed na liberação** — FGTS irregular, documentação incompleta ou justa causa BLOQUEIAM.
4. **HITL nos pontos críticos** — Gate 1: parâmetros jurídicos (multa/regime/SAT/FAP); Gate 2: autorização da liberação.
5. **Schema-first** — handoffs via JSON validado ([templates/schemas.md](templates/schemas.md)).

## Os 6 agentes

| Agente | Função |
|---|---|
| **A1** Orquestrador Árgus | classifica a demanda, monta o grafo, gerencia gates e consolida a saída |
| **A2** Extrator Documental | OCR/parse de contracheque e FGTS Digital (e SEFIP < 03/2024) → registros normalizados |
| **A3** Regras & Parâmetros | percentuais por regime/SAT/FAP/jornada/multa; **HITL Gate 1** |
| **A4** Engine de Cálculo | provisão, saldo, avos e liberações via `conta_vinculada_core.py` |
| **A5** Validador de Conformidade | FGTS 8% devido×recolhido + regras de negócio; bloqueio fail-closed |
| **A6** Gerador de Planilha | abas, fórmulas e memória de cálculo; exporta `.xlsx`; **HITL Gate 2** |

## Workflows

- `montagem_planilha_completa` — do zero: parâmetros + contracheques + FGTS → planilha completa.
- `provisao_mensal` — retenção da competência a destacar da fatura (≈31,82–33,25% da remuneração).
- `liberacao_evento` — 13º, férias, rescisão ou encerramento, com conferência e autorização do órgão.

## Scripts determinísticos (Python 3.11+, sem dependências) — testados

```bash
python3 scripts/conta_vinculada_core.py --input examples/exemplo_contrato_limpeza.json   # provisão + saldo
python3 scripts/validar_conta_vinculada.py --input examples/exemplo_conferencia.json      # conferência fail-closed
python3 scripts/gerar_planilha_xlsx.py --input consolidado.json --output planilha.xlsx     # .xlsx multi-abas (+ --csv)
python3 scripts/conta_vinculada_core.py --self-test                                        # golden tests do Anexo XII
```

## Percentuais de referência (item 14 do Anexo XII)

| Rubrica | % | Fonte |
|---|---|---|
| 13º | 8,33% | Anexo XII, item 14 (1/12) |
| Férias + 1/3 | 12,10% | 9,075% + 3,025% |
| Multa FGTS s/ aviso | **4% (default)** / 5% (literal) | Lei 13.932/2019; Orientação nº 26 |
| Incidência Submódulo 2.2 | 7,39 / 7,60 / 7,82% | SAT 1/2/3% (= 2.2 × 21,19%) |
| **Total mensal** | **31,82–32,25%** (multa 4%) | Lucro Real/Presumido |

> Simples Nacional: Submódulo 2.2 = só FGTS 8% (a incidência cai drasticamente).

## Base normativa

Lei 14.133/2021 (art. 121) · IN SEGES/MPDG 05/2017 + Anexo VII-D e Anexo XII · IN 07/2018 · IN 98/2022 · Decreto 11.246/2022 · Decreto 12.174/2024 + INs 190/2024, 381/2025, 148/2026 (jornada 40h) · Lei 13.932/2019 (multa 5%→4%) · Lei 14.973/2024 (reoneração) · FGTS Digital (Portaria MTE 240/2024) · Acórdãos TCU 1214/2013, 1186/2017 · Súmula 331/TST · Temas STF 246/1118 — detalhes e papel de cada norma em [docs/base_normativa.md](docs/base_normativa.md).

## Roadmap (PRD)

F0 Fundação (engine + tabela versionada + golden tests do item 14) → F1 MVP provisão mensal → F2 Liberações → F3 Conferência FGTS Digital → F4 Variantes (Simples, 40h, reembolso-creche, reoneração) → F5 Robustez (parser SEFIP, multa rescisória por extrato, dashboard). **Esta versão implementa a camada agentiva completa + engine F0–F2 e o gerador `.xlsx`**; OCR de produção e integração FGTS Digital transacional são a implantação descrita no PRD.

## Squads irmãos

- [`squad-pcfp`](../squad-pcfp/) — Planilha de Custos e Formação de Preços: fornece a remuneração-base e o Submódulo 2.2 que alimentam a provisão da conta vinculada.
- [`projur-contracts-squad`](../projur-contracts-squad/) · [`farol-contratos-licitacoes-iffar`](../farol-contratos-licitacoes-iffar/) · [`themis-contratos-publicos-squad`](../themis-contratos-publicos-squad/) — ciclo de vida e fiscalização do contrato.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml` e `IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/argus-conta-vinculada-squad/agents/a1-orquestrador-argus.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/argus-conta-vinculada-squad/agents/a1-orquestrador-argus.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/argus-conta-vinculada-squad/`. Siga `IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva o contrato, os documentos e o formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml @IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/argus-conta-vinculada-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml #file:IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml @IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/argus-conta-vinculada-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/argus-conta-vinculada-squad/squad.yaml` e `IFFar-Squads/squads/argus-conta-vinculada-squad/workflows/montagem_planilha_completa.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
