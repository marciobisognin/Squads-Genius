# Resumo Visual Detalhado — ISO 42001 AIMS Implementation Squad

**Protocol v5.0 | SGIA/AIMS | ISO/IEC 42001 | Governança de IA | Risco Contratual**

## 1. A ideia central

Este squad foi criado para transformar governança de IA em vantagem comercial. A pergunta que ele responde é simples:

> Se um grande cliente pedir amanhã evidências de governança de IA, a organização entrega uma matriz estruturada ou apenas uma justificativa improvisada?

O squad organiza inventário, riscos, avaliações de impacto, controles, políticas, evidências e prontidão de auditoria para empresas que usam IA em processos internos, produtos digitais, atendimento, jurídico, RH, crédito, automação, vendas ou desenvolvimento de software.

**Importante:** o squad não certifica a empresa. Ele prepara a empresa para diagnóstico, organização de evidências, implantação do SGIA/AIMS e eventual auditoria formal.

---

## 2. Visão em mapa

```text
PROBLEMA COMERCIAL
Cliente exige governança de IA em RFP, contrato ou auditoria
        ↓
SQUAD ISO 42001 AIMS IMPLEMENTATION
Organiza SGIA/AIMS, riscos, evidências e controles
        ↓
3 MODOS DE USO
Gap Analysis | Audit Readiness | Full Implementation
        ↓
8 AGENTES ESPECIALIZADOS
Inventário → Gaps → AIIA → Riscos → SoA → Políticas → Evidências → Readiness
        ↓
ENTREGÁVEIS
Inventário, matriz de riscos, AIIA, SoA, policy pack, evidence index, roadmap
        ↓
RESULTADO
Empresa preparada para responder clientes, diretoria, auditoria e mercado
```

---

## 3. Os 3 modos de operação

### Modo 1 — Gap analysis only

**Prazo típico:** 2–4 semanas.

Use quando a empresa ainda não sabe o tamanho do problema e precisa responder rapidamente a diretoria, comercial, cliente estratégico ou RFP.

**Entregas principais:**

- inventário inicial de IA;
- lacunas frente à ISO/IEC 42001;
- riscos por processo;
- roadmap 30/60/90 dias;
- resposta executiva para contrato ou due diligence.

### Modo 2 — Audit readiness sprint

**Prazo típico:** 4–6 semanas.

Use quando a empresa já tem controles, políticas ou evidências, mas está tudo disperso.

**Entregas principais:**

- índice de evidências;
- SoA preliminar;
- simulação de auditoria;
- lista de não conformidades;
- plano de correção.

### Modo 3 — Full implementation

**Prazo típico:** 9–12 meses.

Use quando a empresa deseja implantar um SGIA/AIMS completo, com governança contínua e possibilidade futura de certificação.

**Entregas principais:**

- sistema de gestão de IA;
- políticas formais;
- comitê, papéis e responsabilidades;
- registros recorrentes;
- auditoria interna;
- análise crítica da direção;
- melhoria contínua.

---

## 4. Os 8 agentes do squad

### 1. `ai-inventory-mapper`

Mapeia onde a IA está sendo usada: sistemas, modelos, produtos, automações, fornecedores, dados e responsáveis.

**Pergunta-chave:** onde a empresa usa IA, mesmo informalmente?

### 2. `gap-analyzer`

Compara a situação atual com a estrutura esperada de um SGIA/AIMS alinhado à ISO/IEC 42001.

**Pergunta-chave:** o que falta para transformar uso de IA em governança auditável?

### 3. `aiia-executor`

Executa a Avaliação de Impacto de IA — AIIA.

**Pergunta-chave:** quem pode ser afetado pela IA e quais danos podem ocorrer?

### 4. `risk-register-builder`

Constrói o registro de riscos de IA.

**Pergunta-chave:** quais riscos existem, qual severidade, quem é dono e qual controle reduz o risco?

### 5. `soa-architect`

Monta o Statement of Applicability — SoA.

**Pergunta-chave:** quais controles são aplicáveis e quais evidências provam isso?

### 6. `policy-template-writer`

Cria políticas, procedimentos, registros e modelos documentais.

**Pergunta-chave:** que documentos precisam existir para a governança funcionar?

### 7. `audit-evidence-collector`

Organiza as evidências para auditoria, RFP, due diligence ou cliente estratégico.

**Pergunta-chave:** se alguém pedir prova, onde está a prova?

### 8. `certification-readiness-checker`

Faz a revisão final de prontidão.

**Pergunta-chave:** a organização está pronta, quase pronta ou ainda está vulnerável?

---

## 5. Pipeline visual de 16 fases

```text
01 Intake
   ↓
02 Contexto organizacional
   ↓
03 Inventário de IA
   ↓
04 Classificação de criticidade
   ↓
05 Gap mapping ISO/IEC 42001
   ↓
06 Mapeamento legal/regulatório
   ↓
07 Identificação de riscos
   ↓
08 Análise de riscos
   ↓
09 AIIA — Avaliação de Impacto de IA
   ↓
10 Desenho de controles
   ↓
11 SoA — Statement of Applicability
   ↓
12 Policy pack
   ↓
13 Coleta de evidências
   ↓
14 Auditoria interna simulada
   ↓
15 Management review
   ↓
16 Certification readiness
```

---

## 6. Artefatos que o squad gera

### Artefatos executivos

- `00_EXECUTIVE_SUMMARY.md`
- `07_ROADMAP.md`
- `08_CERTIFICATION_READINESS.md`

### Artefatos técnicos e de governança

- `01_AI_INVENTORY.md`
- `02_GAP_ANALYSIS.md`
- `03_RISK_REGISTER.md`
- `04_AIIA.md`
- `05_SOA.md`
- `06_EVIDENCE_INDEX.md`

### Artefatos estruturais do squad

- `squad.yaml`
- `README.md`
- `TUTORIAL_DIDATICO.md`
- `agents/*.md`
- `tasks/*.yaml`
- `workflows/*.yaml`
- `templates/*.md`
- `scripts/generate_aims_pack.py`

---

## 7. Exemplo concreto de aplicação

### Cenário

Uma empresa SaaS B2B vende para bancos e grandes empresas. Ela possui 5 produtos ou recursos baseados em LLM:

1. chatbot de atendimento;
2. pontuação de leads comerciais;
3. analisador de cláusulas contratuais;
4. assistente de triagem de currículos;
5. copiloto de código para equipe de engenharia.

Um cliente enterprise envia uma RFP perguntando:

- onde a empresa usa IA;
- se há avaliação de riscos;
- se existe revisão humana;
- se há proteção de dados pessoais;
- se há gestão de fornecedores;
- se existe documentação de governança;
- se há evidências auditáveis.

Sem o squad, a empresa provavelmente responderia com generalidades: “usamos IA com responsabilidade”.

Com o squad, a resposta passa a ser documentada.

---

## 8. Aplicação prática no exemplo

### Etapa 1 — Inventário

O `ai-inventory-mapper` identifica os 5 usos de IA e registra:

- área responsável;
- ferramenta/modelo;
- dados usados;
- fornecedor;
- tipo de decisão;
- criticidade;
- evidência disponível.

### Etapa 2 — Gap analysis

O `gap-analyzer` aponta lacunas:

- ausência de política formal de uso de IA;
- falta de avaliação de impacto para RH e jurídico;
- logs incompletos;
- fornecedor de LLM sem avaliação documentada;
- inexistência de SoA;
- ausência de análise crítica da direção.

### Etapa 3 — AIIA

O `aiia-executor` prioriza sistemas de maior impacto:

- triagem de currículos, por risco de viés e discriminação;
- análise contratual, por risco jurídico material;
- chatbot, por risco de alucinação e exposição de dados.

### Etapa 4 — Registro de riscos

O `risk-register-builder` cria uma matriz como:

```text
Sistema: HR Screening Assistant
Risco: viés discriminatório em pré-triagem
Impacto: alto
Probabilidade: média
Controle mínimo: revisão humana, teste de viés, registro de decisão, canal de contestação
Evidência: relatório AIIA, logs de revisão e política de uso
```

### Etapa 5 — SoA

O `soa-architect` define controles aplicáveis:

- inventário de IA;
- política de uso aceitável;
- avaliação de impacto;
- gestão de fornecedores;
- revisão humana;
- monitoramento;
- auditoria interna;
- análise crítica da direção.

### Etapa 6 — Policy pack

O `policy-template-writer` produz modelos para:

- política de uso de IA;
- procedimento de avaliação de riscos;
- registro de incidentes;
- avaliação de fornecedores;
- governança de prompts e dados;
- revisão humana.

### Etapa 7 — Evidence index

O `audit-evidence-collector` organiza uma pasta lógica de provas:

```text
Evidência 01 — Inventário de IA
Evidência 02 — Risk Register
Evidência 03 — AIIA dos sistemas críticos
Evidência 04 — SoA
Evidência 05 — Política de uso de IA
Evidência 06 — Logs de revisão humana
Evidência 07 — Avaliação de fornecedor LLM
Evidência 08 — Ata da revisão executiva
```

### Etapa 8 — Readiness

O `certification-readiness-checker` classifica a empresa:

```text
Situação: parcialmente pronta
Força: inventário e riscos iniciais documentados
Fragilidade: evidências ainda incompletas
Risco comercial: médio/alto se a RFP exigir provas imediatas
Próxima ação: executar sprint de 4–6 semanas para audit readiness
```

---

## 9. Resposta concreta para o cliente/RFP

Após usar o squad, a empresa pode responder:

> A organização mantém inventário documentado dos usos de IA, matriz de riscos por sistema, avaliação de impacto para usos críticos, controles de revisão humana, política de uso aceitável, gestão de fornecedores e plano de melhoria contínua. O programa está estruturado para alinhamento progressivo à ISO/IEC 42001:2023. A organização não declara certificação sem auditoria formal, mas disponibiliza evidências de governança, risco e controles implementados.

Essa resposta é muito mais forte do que uma declaração genérica de responsabilidade.

---

## 10. Resultado esperado para a empresa

Com o squad, a empresa ganha:

- clareza sobre onde usa IA;
- redução de risco jurídico, ético e operacional;
- preparação para RFPs e due diligence;
- linguagem executiva para diretoria;
- evidências organizadas;
- plano de implementação realista;
- base para auditoria futura;
- diferenciação competitiva.

---

## 11. Frase síntese

**Este squad transforma IA invisível e arriscada em governança rastreável, vendável e auditável.**

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
