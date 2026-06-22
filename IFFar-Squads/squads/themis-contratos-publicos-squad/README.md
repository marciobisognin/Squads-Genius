# Themis Contratos Públicos

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `themis-contratos-publicos-squad`
**Versão:** `1.0.0`

Equipe jurídica de IA para **análise de documentos de contratos administrativos da administração pública brasileira**, com verificação de conformidade fundamentada nas normas e entendimentos usados pela **CGU** (controle interno, integridade e transparência) e pelos **Tribunais de Contas** (TCU e TCEs — legalidade, jurisprudência e riscos ao erário).

> ⚖️ **Ressalva obrigatória:** o squad produz apoio técnico automatizado. Não substitui parecer de advogado, procurador ou órgão de assessoramento jurídico (art. 53 da Lei 14.133/2021). Toda saída exige revisão humana qualificada.

## O que o squad analisa

- Contratos, termos aditivos, apostilamentos e atas de registro de preços.
- Peças de planejamento (ETP, termo de referência, pesquisa de preços) e de seleção (edital, julgamento).
- Justificativas de dispensa e inexigibilidade (arts. 74 e 75 da Lei 14.133/2021).
- Execução e gestão: fiscalização, medições, garantias, sanções e extinção.

## O que ele entrega

| Artefato | Conteúdo |
|---|---|
| Ficha de triagem | tipo de peça, regime legal, metadados, lacunas |
| Checklist de conformidade | cláusulas necessárias (art. 92, Lei 14.133/2021) item a item |
| Relatório de legalidade | apontamentos com lei, artigo e parágrafo |
| Nota de jurisprudência | súmulas/acórdãos TCU aplicáveis, com grau de confiança |
| Relatório de integridade | transparência, CEIS/CNEP, nepotismo, conflito de interesses |
| Matriz de riscos | sobrepreço, jogo de planilha, aditivos, direcionamento — com severidade |
| Parecer consolidado | relatório, fundamentação, quadro de apontamentos, recomendações e conclusão |

## Agentes

- `themis-orchestrator` — coordena o pipeline, consolida achados e aciona quality gates.
- `intake-document-triager` — triagem documental e identificação do regime legal.
- `legalidade-lei14133-analyst` — legalidade formal e material (Lei 14.133/2021 e regimes legados).
- `jurisprudencia-tcu-researcher` — confronto com súmulas e acórdãos do TCU/TCEs.
- `cgu-integridade-compliance-analyst` — integridade, transparência e controle interno (referenciais CGU).
- `riscos-sobrepreco-auditor` — matriz de riscos, sobrepreço e análise de aditivos.
- `parecer-relator-juridico` — parecer técnico-jurídico consolidado.

## Workflows

- `analise_completa_contrato.yaml` — pipeline completo em 9 etapas, 6 quality gates, revisão humana final obrigatória.
- `triagem_rapida_red_flags.yaml` — triagem expressa para priorizar carteiras de contratos.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
# pré-triagem heurística de cláusulas necessárias
python3 scripts/checklist_clausulas.py --contrato examples/exemplo_contrato_trecho.txt

# limites legais de termos aditivos (25% / 50%)
python3 scripts/validar_limites_aditivos.py --valor-inicial 480000 --aditivos 90000 40000 --regime 14133
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/themis-orchestrator.md`.
2. Rode o workflow `analise_completa_contrato` fornecendo os documentos do processo.
3. Aprove cada quality gate e faça a revisão humana final.

Exemplos completos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Base normativa em [`docs/base_normativa.md`](docs/base_normativa.md).

## Princípios de qualidade

- Todo apontamento cita norma, súmula ou acórdão; citações de memória são marcadas `a confirmar`.
- Separação explícita entre observado, inferido, hipótese, recomendação e risco.
- Cálculos (percentuais de aditivo) sempre por script determinístico.
- Indício nunca é afirmado como irregularidade consumada.
- Nenhum dado pessoal sensível ou segredo nos artefatos.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml` e `IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/themis-contratos-publicos-squad/agents/themis-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/themis-contratos-publicos-squad/agents/themis-orchestrator.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/themis-contratos-publicos-squad/`. Siga `IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml @IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/themis-contratos-publicos-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml #file:IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml @IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/themis-contratos-publicos-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/themis-contratos-publicos-squad/squad.yaml` e `IFFar-Squads/squads/themis-contratos-publicos-squad/workflows/analise_completa_contrato.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
