# 🪐 Mobius Chair — Inteligência Estratégica de Futuros

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> *"Qualquer pergunta feita à Cadeira é respondida com precisão absoluta."*

Squad premium de inteligência de futuros, operado por 9 agentes especializados, que
transforma incerteza estratégica em clareza acionável: varredura de megatendências STEEP,
detecção de sinais fracos, mapeamento de tecnologias emergentes, construção de quatro
cenários, análise de implicações, teste de robustez (wind tunnel) e roadmap estratégico
com indicadores de alerta precoce.

---

## Artefato de Inspiração: A Cadeira Mobius (DC Comics — Metron)

A **Cadeira Mobius** é o artefato mais poderoso do universo DC Comics, criada pelos New
Gods e pertencente a Metron — o eterno observador que possui acesso ilimitado ao
conhecimento do passado, presente e futuro. Qualquer pergunta feita à Cadeira é respondida
com precisão absoluta.

Este squad é o equivalente estratégico: transforma incerteza em inteligência, navega
futuros com rigor epistemológico e entrega clareza onde outros enxergam apenas caos.

- **A onisciência de Metron = rigor epistemológico absoluto.** Toda afirmação é rotulada:
  Fato Estabelecido, Tendência Confirmada, Tendência Emergente, Sinal Fraco, Especulação
  ou Wildcard — nunca confundindo um com o outro.
- **A observação imparcial de Metron = a metodologia de cenários.** O squad não aposta em
  um único futuro — constrói quatro futuros plausíveis e testa a estratégia contra todos.
- **A precisão absoluta da Cadeira = os indicadores de alerta precoce.** Cada cenário tem
  sinais observáveis que indicam, na realidade, qual futuro está se materializando.

---

## Visão Geral do Squad

O Mobius Chair Squad transforma uma questão estratégica focal em inteligência de futuros
completa: megatendências verificadas, sinais fracos catalogados, tecnologias emergentes
posicionadas no hype cycle, quatro cenários distintos e plausíveis, implicações
estratégicas específicas, teste de robustez das estratégias atuais e um roadmap que se
sustenta independentemente de qual futuro se materializar primeiro.

**Diferencial central:** Gate epistemológico obrigatório em todas as fases — nenhuma
especulação é apresentada como fato, e toda afirmação tem fonte e grau de confiança.

---

## Domínio e Casos de Uso

### Para quem este squad foi criado

- Lideranças executivas que precisam de visão estratégica de longo prazo
- Times de estratégia corporativa fazendo planejamento de cenários
- Boards e comitês de investimento avaliando robustez de teses estratégicas
- Organizações em setores de alta incerteza tecnológica ou regulatória

### Casos de uso típicos

| Situação | Como o Squad Ajuda |
|----------|-------------------|
| Planejamento estratégico de longo prazo | 4 cenários plausíveis + roadmap robusto |
| Incerteza sobre disrupção tecnológica | Mapa de tecnologias no Hype Cycle relacionado a sinais fracos |
| Validação de estratégia atual | Wind tunnel testando a estratégia contra múltiplos futuros |
| Necessidade de monitoramento contínuo | Dashboard de indicadores de alerta precoce |
| Decisão de investimento sob incerteza | Implicações estratégicas específicas por cenário |

---

## Agentes do Squad

### 1. mobius-orchestrator
Coordenador central com gate epistemológico obrigatório — distingue tendência de fato de especulação.

### 2. horizon-scanner
Varredura de megatendências STEEP (Social, Tecnológico, Econômico, Ambiental, Político).

### 3. weak-signal-detector
Identificação de sinais fracos e wildcards em fontes de fronteira e dados emergentes.

### 4. emerging-tech-analyst
Mapeamento de tecnologias emergentes e análise de curva de adoção (Gartner Hype Cycle).

### 5. scenario-architect
Construção de quatro cenários com lógicas narrativas distintas e consistência interna.

### 6. strategic-implications-analyst
Análise de implicações estratégicas por cenário para a organização específica.

### 7. windtunnel-tester
Teste de estratégias atuais contra cada cenário futuro para avaliar robustez.

### 8. roadmap-forger
Design de roadmap estratégico robusto que se sustenta em múltiplos futuros plausíveis.

### 9. early-indicator-designer
Indicadores líderes para monitorar qual cenário está se materializando em tempo real.

---

## Pipeline de Execução

1. **Intake** — recepção do contexto e aprovação da questão focal (HITL)
2. **Scanning** — varredura paralela de megatendências, sinais fracos e tecnologias
3. **Scenario Construction** — seleção de eixos de incerteza (HITL) e construção dos 4 cenários
4. **Implications and Testing** — implicações estratégicas e wind tunnel (HITL de revisão)
5. **Roadmap** — roadmap robusto e indicadores de alerta precoce (HITL de aprovação)
6. **Synthesis** — consolidação final com sign-off humano obrigatório

Workflow completo: [`workflows/strategic-foresight-pipeline.yaml`](workflows/strategic-foresight-pipeline.yaml)
Quality gates: [`workflows/quality-gates.yaml`](workflows/quality-gates.yaml)

---

## Entregáveis

- Relatório de Inteligência de Futuros Consolidado
- Documento dos Quatro Cenários
- Relatório de Megatendências STEEP
- Relatório de Sinais Fracos e Wildcards
- Mapa de Tecnologias Emergentes (Hype Cycle)
- Relatório de Implicações Estratégicas por Cenário
- Resultados do Wind Tunnel
- Roadmap Estratégico Robusto
- Dashboard de Indicadores de Alerta Precoce

---

## Quality Gates

- `epistemologia_confirmada`
- `tendencias_com_fonte_e_confianca`
- `sinais_fracos_catalogados`
- `tecnologias_mapeadas_no_hype_cycle`
- `cenarios_distintos_e_consistentes`
- `implicacoes_por_cenario`
- `estrategias_testadas_no_windtunnel`
- `roadmap_robusto_aprovado`
- `indicadores_de_alerta_definidos`
- `aprovacao_humana_explicita`

---

## Como Usar

1. Defina a questão estratégica focal, horizonte temporal e setor de atuação
2. Aprove a questão focal refinada (HITL obrigatório)
3. Acompanhe a varredura de megatendências, sinais fracos e tecnologias
4. Valide os eixos de incerteza antes da construção dos cenários (HITL obrigatório)
5. Revise as narrativas dos 4 cenários e implicações (HITL obrigatório)
6. Aprove o roadmap robusto (HITL obrigatório)
7. Receba o Relatório de Inteligência de Futuros após sign-off final

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/mobius-chair-strategic-foresight-squad/squad.yaml` e `squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/mobius-chair-strategic-foresight-squad/agents/mobius-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/mobius-chair-strategic-foresight-squad/agents/mobius-orchestrator.md`
> e conduza o fluxo definido em `squads/mobius-chair-strategic-foresight-squad/`. Siga `squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/mobius-chair-strategic-foresight-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/mobius-chair-strategic-foresight-squad/squad.yaml @squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/mobius-chair-strategic-foresight-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/mobius-chair-strategic-foresight-squad/squad.yaml #file:squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/mobius-chair-strategic-foresight-squad/squad.yaml @squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/mobius-chair-strategic-foresight-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/mobius-chair-strategic-foresight-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/mobius-chair-strategic-foresight-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/mobius-chair-strategic-foresight-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/mobius-chair-strategic-foresight-squad/squad.yaml` e `squads/mobius-chair-strategic-foresight-squad/workflows/strategic-foresight-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
