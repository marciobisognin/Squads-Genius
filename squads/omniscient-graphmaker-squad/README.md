<div align="center">

# 🧠 OMNISCIENT GRAPHMAKER Squad v6.5

### Um ecossistema multiagente para transformar um Master Pitch em estratégia, blueprint quantitativo e execução tática em DAG.

<p>
  <img src="https://img.shields.io/badge/Squad-Premium-7C3AED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Arquitetura-Multiagentes-06B6D4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Framework-IDBALANCE%20%7C%20RELATION%20%7C%20GRAPHMAKER-F59E0B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licença-MIT-10B981?style=for-the-badge" />
</p>

</div>

---

## ✨ Ideia central

O **OMNISCIENT GRAPHMAKER Squad v6.5** é um sistema de agentes especializados para analisar uma ideia, tese de negócio ou produto digital e convertê-la em uma arquitetura operacional pronta para execução.

Ele evita o problema típico de conselhos multiagentes caóticos — a chamada “Torre de Babel” — substituindo debates livres por um fluxo estruturado de decisão, síntese, tradução para JSON e execução por grafo de dependências.

Em termos simples: o squad pega uma ideia ampla e transforma em **blueprint estratégico, métricas, tarefas, arquitetura de execução e entregáveis acionáveis**.

---

## 🎯 Para que serve?

Este squad serve para estruturar produtos, negócios, lançamentos, squads internos e experimentos de inovação com mais rigor técnico.

Ele foi desenhado para responder perguntas como:

- A ideia é simples, complicada ou complexa?
- Quais riscos podem destruir o modelo?
- O plano é frágil, robusto ou antifrágil?
- Como transformar heurísticas qualitativas em métricas e JSON quantitativo?
- Quais agentes devem agir primeiro?
- Quais tarefas dependem de quais entregas?
- Qual orçamento de tokens, custo e latência deve ser respeitado?
- O que deve ser entregue ao final para permitir execução real?

---

## 🧭 Como o squad trabalha

```mermaid
flowchart TD
    A[Master Pitch do usuário] --> B[Cynefin Classifier]
    B --> C[Token Latency Governor]
    B --> D[IDBALANCE VHM Compiler]
    D --> E[Taleb Engine]
    E --> F[Munger Engine]
    C --> G[Cognitive Boardroom N-Rounds]
    F --> G
    G --> H[RELATION / SACP Compiler]
    H --> I[Venture Synthesis Matrix]
    I --> J[GRAPHMAKER DAG]
    J --> K[Visual Axiom]
    J --> L[Neural Cloning Foundry]
    J --> M[Conversion Alchemy]
    K --> N[Frictionless Conversion]
    L --> N
    M --> N
    N --> O[Blueprint, landing spec, métricas e plano de execução]
```

---

## 🧩 Estrutura dos agentes

```mermaid
flowchart LR
    subgraph Diagnóstico
      A1[Cynefin Classifier]
      A2[Token Latency Governor]
    end
    subgraph Identidade_e_Risco
      B1[IDBALANCE VHM Compiler]
      B2[Taleb Engine]
      B3[Munger Engine]
    end
    subgraph Estratégia
      C1[Cognitive Boardroom]
      C2[RELATION / SACP Compiler]
      C3[Venture Synthesis Matrix]
    end
    subgraph Execução
      D1[GRAPHMAKER Orchestrator]
      D2[Visual Axiom]
      D3[Neural Cloning Foundry]
      D4[Conversion Alchemy]
      D5[Frictionless Conversion]
    end
    subgraph Distribuição_e_Aprimoramento
      E1[Turing Architect Guild]
      E2[Memetic Propagation]
    end
    A1 --> A2 --> B1 --> B2 --> B3 --> C1 --> C2 --> C3 --> D1
    D1 --> D2
    D1 --> D3
    D1 --> D4
    D2 --> D5
    D3 --> D5
    D4 --> D5
    D5 --> E1 --> E2
```

---

## ✦ O que cada agente faz?

<div align="center">
<table>
<tr>
<td><b>🧭 Cynefin Classifier</b><br/>Classifica o problema como simples, complicado, complexo ou caótico e define o tipo de roteamento.</td>
<td><b>⏱️ Token Latency Governor</b><br/>Controla orçamento de tokens, custo, latência, cache e escolha de modelos por camada.</td>
</tr>
<tr>
<td><b>🧬 IDBALANCE VHM Compiler</b><br/>Transforma mind-clones em matrizes de heurísticas vetorizadas para reduzir deriva de persona e alucinação cruzada.</td>
<td><b>⚠️ Taleb Engine</b><br/>Executa teste de estresse, identifica riscos de cauda longa e avalia fragilidade ou antifragilidade.</td>
</tr>
<tr>
<td><b>🔁 Munger Engine</b><br/>Aplica o protocolo de inversão: antes de perguntar como vencer, mapeia como o modelo pode falhar.</td>
<td><b>🏛️ Cognitive Boardroom</b><br/>Organiza o conselho em rodadas: divergência, antítese e síntese, evitando debate caótico.</td>
</tr>
<tr>
<td><b>🧩 RELATION / SACP Compiler</b><br/>Converte ideias abstratas e qualitativas em um Meta-Blueprint JSON estruturado e validável.</td>
<td><b>⚙️ Venture Synthesis Matrix</b><br/>Transforma a síntese estratégica em tarefas atômicas, dependências e critérios de aceite.</td>
</tr>
<tr>
<td><b>🕸️ GRAPHMAKER Orchestrator</b><br/>Monta o grafo de execução em DAG, indicando quais nós dependem de quais entregas.</td>
<td><b>🎨 Visual Axiom</b><br/>Define sistema visual, branding, tokens de design e direção estética.</td>
</tr>
<tr>
<td><b>🗣️ Neural Cloning Foundry</b><br/>Cria a lógica de tom de voz e DNA verbal do produto ou marca.</td>
<td><b>🧪 Conversion Alchemy</b><br/>Gera copywriting, promessa, objeções, provas e chamadas para ação.</td>
</tr>
<tr>
<td><b>🚀 Frictionless Conversion</b><br/>Integra design, voz e copy em uma especificação completa de landing page ou funil.</td>
<td><b>🛠️ Turing Architect Guild</b><br/>Revisa falhas técnicas e aplica lógica de correção/self-healing quando necessário.</td>
</tr>
<tr>
<td><b>📣 Memetic Propagation</b><br/>Planeja distribuição, adaptação de mensagens e loop de telemetria de mercado.</td>
<td><b>✅ Resultado integrado</b><br/>Consolida blueprint, DAG, métricas, artefatos e plano tático de execução.</td>
</tr>
</table>
</div>

---

## ✦ Como o Conselho evita a “Torre de Babel”?

```mermaid
sequenceDiagram
    participant U as Usuário
    participant C as Cynefin
    participant I as IDBALANCE
    participant T as Taleb
    participant M as Munger
    participant B as Boardroom
    participant S as SACP
    participant G as GRAPHMAKER
    U->>C: Envia Master Pitch
    C->>I: Define complexidade e necessidade de conselho
    I->>T: Compila identidades heurísticas vetorizadas
    T->>M: Envia riscos e fragilidades
    M->>B: Envia mapa de falhas por inversão
    B->>B: Rodada 1: divergência
    B->>B: Rodada 2: antítese
    B->>B: Rodada 3: síntese
    B->>S: Entrega síntese estruturada
    S->>G: Gera Meta-Blueprint JSON
    G->>U: Entrega plano acionável em DAG
```

---

## 📦 O que o squad entrega no final?

<div align="center">
<table>
<tr>
<td><b>📘 Meta-Blueprint JSON</b><br/>Documento estruturado com classificação, VHM, riscos, inversão, síntese, métricas e governança.</td>
<td><b>🕸️ Execution DAG</b><br/>Grafo de dependências que mostra a ordem correta de execução dos agentes e tarefas.</td>
</tr>
<tr>
<td><b>📊 Token & Latency Budget</b><br/>Plano de custo, latência, cache e modelo por camada para evitar execução cara e lenta.</td>
<td><b>🧱 Product / Landing Spec</b><br/>Especificação didática do produto, promessa, mecanismo, CTA, métricas e estrutura de conversão.</td>
</tr>
<tr>
<td><b>🧪 Relatório de validação</b><br/>Evidência de que o fluxo foi executado e validado por smoke test.</td>
<td><b>🚦 Critérios de aceite</b><br/>Conjunto de checks para saber se a estratégia virou execução auditável.</td>
</tr>
</table>
</div>

---

<div align="center">

### Resultado esperado

**Uma ideia abstrata entra.**<br/>
**Um blueprint quantitativo, um DAG de execução e artefatos táticos saem.**

<br/>

<b>Licença:</b> MIT<br/>
<b>Criado por:</b> Marcio Bisognin<br/>
<b>Instagram:</b> @marciobisognin

</div>
