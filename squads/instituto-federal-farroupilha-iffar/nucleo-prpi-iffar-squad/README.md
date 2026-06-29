# 🔬 Núcleo PRPI IFFar

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `nucleo-prpi-iffar-squad`
**Versão:** `1.0.0`

Squad institucional de apoio à **Pró-Reitoria/Diretoria de Pesquisa, Pós-Graduação e Extensão (PRPI)** do Instituto Federal Farroupilha (IFFar): elaboração de editais internos de fomento (PIBIC, PIBITI, PIBID, extensão), triagem formal de propostas submetidas, acompanhamento do cronograma de bolsas concedidas, consolidação de relatórios de produção científica/técnica e apoio à prestação de contas de bolsas e de convênios/parcerias de extensão.

> ⚖️ **Ressalva obrigatória:** os artefatos gerados são minutas e relatórios de apoio técnico-administrativo. Mérito científico/técnico de propostas, aprovação de edital e decisões de concessão ou corte de bolsa são exclusivos dos comitês de avaliação e da Pró-Reitoria. Revisão humana é obrigatória em todos os artefatos.

## Problema que resolve

A elaboração de editais de fomento e a triagem de propostas hoje dependem de verificação manual de documentação, enquadramento e limite de bolsas por orientador — processo sujeito a inconsistências e retrabalho. O acompanhamento do cronograma de bolsas (mensalidades, relatórios, TCR) e a prestação de contas de bolsas e convênios são feitos sem alerta sistemático de prazos, gerando descumprimentos que só aparecem tarde. A consolidação da produção científica/técnica para Lattes, SUAP, relatório de gestão e Plataforma Nilo Peçanha é manual e propensa a duplicidades. Este squad automatiza a parte determinística desse trabalho (checklists, triagem documental, monitoramento de prazos, deduplicação) e organiza a parte textual (editais, relatórios, dossiês), preservando toda decisão de mérito e toda decisão administrativa sensível como humana.

## O que o squad gera

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de intake da demanda PRPI | tipo de demanda, documentos disponíveis, lacunas |
| 2 | Minuta de edital interno de fomento | checklist de campos obrigatórios por script determinístico |
| 3 | Relatório de triagem de propostas submetidas | documentação, enquadramento e limite de bolsas por script determinístico |
| 4 | Relatório de cronograma de bolsas | mensalidades, relatórios e TCR comparados à data de referência |
| 5 | Relatório de produção científica/técnica consolidado | produção declarada (Lattes/SUAP), deduplicada por script determinístico |
| 6 | Dossiê de prestação de contas de convênio/parceria de extensão | plano de aplicação aprovado x comprovantes declarados |
| 7 | Relatório de auditoria de prestação de contas de bolsas | documentos exigidos x entregues, vigência x período coberto |

## Agentes (5)

`prpi-orchestrator` · `triagem-propostas-fomento` · `cronograma-bolsas-acompanhador` · `producao-cientifica-redator` · `prestacao-contas-fomento-auditor`

## Workflows (3)

- `ciclo_edital_fomento` — intake → elaboração do edital → aprovação humana → triagem das propostas → avaliação de mérito pelo comitê.
- `acompanhamento_bolsas` — intake → cronograma de bolsas → auditoria de prestação de contas → decisão humana da coordenação.
- `producao_e_prestacao_contas` — intake → consolidação da produção científica → dossiê de prestação de contas de convênio/parceria → validação humana final.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/checklist_edital_fomento.py --edital examples/exemplo_edital.json
python3 scripts/triagem_propostas.py --edital examples/exemplo_edital.json --propostas examples/exemplo_propostas.json
python3 scripts/cronograma_bolsas.py --bolsas examples/exemplo_bolsas_cronograma.json --data-referencia 2026-06-17
python3 scripts/consolidador_producao.py --producao examples/exemplo_producao.json
python3 scripts/auditoria_prestacao_contas_bolsas.py --bolsas examples/exemplo_bolsas_prestacao_contas.json
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/prpi-orchestrator.md`.
2. Descreva a demanda ou preencha `templates/solicitacao_demanda_prpi.yaml`.
3. Acompanhe o roteamento para o workflow correspondente e responda às perguntas de intake.
4. Aprove os gates humanos quando solicitado — o squad nunca decide em lugar do comitê de avaliação ou da Pró-Reitoria.
5. Receba os artefatos consolidados.

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_prpi.md`](docs/base_normativa_prpi.md). Para conformidade e prazos institucionais cruzados, ver o squad irmão [`compliance-ia-iffar-squad`](../compliance-ia-iffar-squad/).

## Princípios

- Nenhuma decisão de mérito científico, aprovação de edital ou concessão/corte de bolsa é tomada pelo squad: ele prepara, audita e sinaliza — a decisão é sempre humana.
- Triagem de propostas é estritamente formal (documentação, enquadramento, conflitos) e checada por script determinístico, nunca por inferência do agente.
- Dados pessoais de bolsistas, orientadores e pesquisadores tratados com minimização (LGPD): apenas os campos necessários à tarefa.
- Toda fonte normativa citada com versão/data; o que não foi verificado na fonte oficial é marcado `a confirmar`.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml` e `IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/nucleo-prpi-iffar-squad/agents/prpi-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/nucleo-prpi-iffar-squad/agents/prpi-orchestrator.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/nucleo-prpi-iffar-squad/`. Siga `IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml @IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/nucleo-prpi-iffar-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml #file:IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml @IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/nucleo-prpi-iffar-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/nucleo-prpi-iffar-squad/squad.yaml` e `IFFar-Squads/squads/nucleo-prpi-iffar-squad/workflows/ciclo_edital_fomento.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
