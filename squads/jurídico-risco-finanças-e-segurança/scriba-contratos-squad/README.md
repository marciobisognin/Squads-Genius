# 📜 SCRIBA — Geração Assistida de Instrumentos Contratuais

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>

**Nome técnico:** `scriba-contratos-squad` | **Versão:** `1.0.0` | **Origem:** PRD "Squad SCRIBA v1.0" + Compêndio — Contratos Administrativos da Administração Pública Federal

Squad multiagente que, dado um tipo de situação contratual, produz o **instrumento pronto para assinatura** — minuta inicial · termo aditivo · apostilamento · repactuação/reajuste — para universidades e institutos federais: classificação Cynefin → extração → RAG normativo → roteamento do instrumento → seleção de minuta → motor de cálculo determinístico → redação de cláusulas → validação adversarial → geração do pacote final, com **citação obrigatória de fundamento por cláusula** e **Human-in-the-Loop obrigatório** nos dois pontos jurídicos críticos.

> ⚖️ **Automação não é parecer jurídico.** A tabela-decisão do Instrument Router e as fórmulas da engine implementam o compêndio normativo (Lei 14.133/2021 + IN SEGES/MPDG 05/2017), mas não substituem o parecer técnico/jurídico da procuradoria/CLCFW responsável. Nenhum instrumento é final sem homologação humana (HITL Gate B).

## Princípios (do PRD)

1. **Determinismo no cálculo, criatividade zero no número** — todo valor sai do motor Python (`scripts/scriba_engine.py`), nunca da geração livre do LLM.
2. **Texto rastreável** — cada cláusula cita a fonte (artigo/modelo AGU/acórdão); sem citação válida, bloqueio.
3. **HITL como invariante** — classificação de CCT, escolha aditivo×apostila e homologação final nunca são automáticas.
4. **Segregação de funções** — quem calcula (Engine) ≠ quem valida (Validator) ≠ quem redige (Drafter).
5. **Anti-sycophancy** — o Validator é adversarial, procura motivos para reprovar.

## Os 11 agentes

| Agente | Função |
|---|---|
| **scriba-orchestrator** | Coordena o StateGraph (S0-S11), HITL Gates A/B, Turing loop e o handoff SACP |
| **scriba-cynefin-classifier** | Classifica a complexidade do caso (Clear/Complicated/Complex/Chaotic) |
| **scriba-extractor** | Normaliza `contract_facts` e lista pendências (datas, CNPJ, valores) |
| **scriba-normative-rag** | Recupera dispositivos aplicáveis (Lei 14.133, IN 05/2017, AGU, TCU) |
| **scriba-instrument-router** | **Tabela-decisão determinística** (§11 do compêndio) entre os 4 instrumentos |
| **scriba-template-selector** | Seleciona a minuta AGU/CNMLC vigente por objeto/regime; guarda de vigência |
| **scriba-calculator** | **Engine determinística** — reajuste, limites de aditivo, repactuação, conta vinculada/PFG |
| **scriba-drafter** | Preenche cláusulas com citação obrigatória de fonte |
| **scriba-validator** | Checklist AGU (art. 92) + riscos TCU; **adversarial** — aciona o Turing Guild |
| **scriba-doc-generator** | Gera o instrumento final em DOCX/Markdown com identidade institucional |
| **scriba-explainer** | Gera a memória explicativa (decisões, fundamentos por cláusula, memória de cálculo) |

## Workflows

- `scriba_full_pipeline` — pipeline completo S0-S11 (entrada → instrumento homologado).
- `scriba_termo_aditivo_prorrogacao` — acréscimo/supressão/prorrogação, com limites de 25%/50%.
- `scriba_apostilamento_reajuste` — apostilamento por reajuste de índice já previsto em cláusula.
- `scriba_repactuacao_demo` — repactuação com demonstração analítica + alerta crítico de preclusão.

## Scripts determinísticos (Python 3.11+, sem dependências obrigatórias) — testados

```bash
python3 tests/test_golden_cases.py                                                       # 21 casos-ouro
python3 scripts/run_scriba.py --input examples/sample_input_reajuste.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_aditivo.json --outdir output
python3 scripts/run_scriba.py --input examples/sample_input_repactuacao.json --outdir output
python3 scripts/scriba_router.py                                                         # inspeciona o router
python3 scripts/scriba_engine.py                                                         # inspeciona a engine
```

## O que a engine acerta (PRD §7)

| Cálculo | Regra |
|---|---|
| Reajuste | fator = índice_final/índice_inicial sobre o valor base |
| Limites de aditivo | 25% (comum) / 50% (reforma de edifício/equipamento), **vedada compensação entre os dois** (art. 125, §1º) |
| Repactuação | anualidade por componente a partir da `data_base_anterior`, com **alerta crítico de preclusão** (art. 57, §7º da IN 05/2017) |
| Conta vinculada/PFG | provisão mensal sobre o salário-base |
| Prorrogação | teto de 60 meses |

## Gates humanos (invariantes)

1. **HITL Gate A** — confirmação do instrumento decidido e, se DEMO, da classificação de CCT.
2. **HITL Gate B** — homologação humana final da peça redigida, antes do pacote definitivo.

## Base normativa

Lei 14.133/2021 (arts. 89-155, 92, 107, 124-125, 130, 135, 136) · Lei 8.666/1993 (regime legado) · IN SEGES/MPDG 05/2017 (arts. 54-61, 57 §7º) · Lei 10.192/2001 · modelos AGU/CNMLC · Acórdãos TCU 749/2010-P, 1.827/2008-P, 1.643/2024-P — detalhes em [docs/base_normativa.md](docs/base_normativa.md).

## Roadmap (PRD)

**F1 — Router + Engine + Validator + testes-ouro** ✅ entregue (21/21 verde) → F2 Extractor + Normative RAG → F3 Template Selector (catálogo AGU/CNMLC com guarda de vigência) → F4 Drafter + Doc Generator (DOCX/MD) → F5 Orquestração LangGraph completa + Turing loop + HITL Gates + Explainer → F6 Integração com PCFP Squad e Farol Contratos. Detalhes em [docs/arquitetura.md](docs/arquitetura.md).

## Limitações

O catálogo de minutas AGU/CNMLC vigentes e a geração de DOCX não estão embarcados nesta versão. Ver [docs/limitations.md](docs/limitations.md). Este squad é apoio e **não substitui** o parecer jurídico da procuradoria/CLCFW responsável.

## Squads irmãos

- [`farol-pcfp-squad`](../farol-pcfp-squad/) — Planilha de Custos e Formação de Preços: fornece os custos de mão de obra que alimentam aditivos/repactuações de contratos de serviço continuado.
- Integração futura com **Farol Contratos** (gestão e fiscalização do ciclo de vida contratual).

## Documentação

- [docs/operating_manual.md](docs/operating_manual.md) — como operar.
- [docs/arquitetura.md](docs/arquitetura.md) — arquitetura e mapeamento PRD → repositório.
- [docs/base_normativa.md](docs/base_normativa.md) — fontes normativas e jurisprudência TCU.
- [docs/limitations.md](docs/limitations.md) — premissas, riscos e mitigações.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/scriba-contratos-squad/squad.yaml` e `squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/scriba-contratos-squad/agents/scriba-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os HITL Gates A/B e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/scriba-contratos-squad/agents/scriba-orchestrator.md`
> e conduza o fluxo definido em `squads/scriba-contratos-squad/`. Siga `squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml`.
> Valide cada handoff/contrato e respeite os HITL Gates A e B.
> Meu briefing é: <descreva a situação contratual, os dados do contrato e o instrumento esperado>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/scriba-contratos-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/scriba-contratos-squad/squad.yaml @squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/scriba-contratos-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/scriba-contratos-squad/squad.yaml #file:squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/scriba-contratos-squad/squad.yaml @squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/scriba-contratos-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/scriba-contratos-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/scriba-contratos-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/scriba-contratos-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/scriba-contratos-squad/squad.yaml` e `squads/scriba-contratos-squad/workflows/scriba_full_pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
