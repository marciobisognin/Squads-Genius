---
task:
  name: brand-dna-mapping
  id: brand-dna-mapping
  title: "Mapeamento de DNA de Marca e Posicionamento de Autoridade"
  icon: "🧬"
  description: >
    Tarefa de diagnóstico do propósito, valores, voz e diferencial único do profissional,
    seguida da arquitetura de posicionamento de autoridade no nicho-alvo. Base para todos
    os outros entregáveis do squad.
  estimated_duration: "1 a 2 dias úteis"
  squad: soulsword-personal-branding-squad
  workflow: personal-branding-pipeline.yaml
  output_format: Documento de DNA de Marca + Declaração de Posicionamento de Autoridade

inputs:
  required:
    - perfil_profissional: "Nome, cargo, área de atuação e mercado-alvo"
    - autodescricao: "Propósito, valores, conquistas e diferenciais percebidos"
  optional:
    - conteudos_existentes: "Posts, artigos e palestras já publicados"
    - perfil_linkedin: "URL ou captura de tela do perfil atual"

outputs:
  primary:
    - name: "Documento de DNA de Marca"
      description: "Propósito, valores, voz e diferencial único consolidados"
    - name: "Declaração de Posicionamento de Autoridade"
      description: "Território único de autoridade frente ao mercado-alvo"
  secondary:
    - "Mapa de Posicionamento Competitivo"

hitl_checkpoints:
  - id: brand_dna_validation
    description: "Validação do profissional sobre o DNA de marca diagnosticado"
    required: true
    blocker: true
---

# Tarefa: Mapeamento de DNA de Marca e Posicionamento de Autoridade

## Visão Geral

Esta tarefa é a fundação do pipeline Soulsword. Antes de qualquer conteúdo ou estratégia de
visibilidade, é preciso diagnosticar com precisão quem o profissional genuinamente é — não
quem ele acha que o mercado quer que ele seja. O resultado é o DNA de Marca, validado pelo
próprio profissional, e o Posicionamento de Autoridade, que define o território único que
ele ocupará no mercado.

## Passo a Passo

### Passo 1 — Coleta de Autodescrição e Conteúdos Existentes

**Agente responsável:** brand-dna-analyst

**Ações:**
1. Receber autodescrição estruturada: propósito, valores, conquistas, diferenciais percebidos
2. Coletar conteúdos já publicados (posts, artigos, palestras) como evidência de voz real
3. Identificar lacunas entre como o profissional se descreve e como já se comunica publicamente

**Output:** Briefing consolidado de autodescrição + conteúdos de referência

---

### Passo 2 — Diagnóstico de Propósito, Valores e Voz

**Agente responsável:** brand-dna-analyst

**Ações:**
1. Extrair propósito central: por que o profissional faz o que faz, além do resultado financeiro
2. Identificar 3 a 5 valores recorrentes na autodescrição e nos conteúdos publicados
3. Caracterizar a voz: tom, vocabulário típico, nível de formalidade, uso de humor/storytelling
4. Identificar o diferencial único: o que torna este profissional diferente de outros no mesmo nicho

**Output:** Documento de DNA de Marca (rascunho)

---

### Passo 3 — HITL: Validação do DNA de Marca

**Responsável:** Usuário/Profissional

**O que revisar:**
- O propósito identificado reflete a motivação real, não uma versão idealizada
- Os valores soam autênticos quando lidos em voz alta
- A voz descrita corresponde a como o profissional realmente se comunica
- O diferencial único é verificável, não apenas aspiracional

**Gate de qualidade:** gate `brand_dna_validated_by_professional` do quality-gates.yaml

---

### Passo 4 — Mapeamento de Posicionamento Competitivo

**Agente responsável:** positioning-architect

**Ações:**
1. Identificar outros profissionais de referência no mesmo nicho e mercado-alvo
2. Mapear como cada referência se posiciona: tema central, formato de conteúdo, tom
3. Aplicar lógica de Blue Ocean: identificar espaços de autoridade ainda não ocupados

**Output:** Mapa de Posicionamento Competitivo

---

### Passo 5 — Declaração de Posicionamento de Autoridade

**Agente responsável:** positioning-architect

**Ações:**
1. Definir o território único de autoridade que o profissional ocupará
2. Redigir a declaração de posicionamento: "Para [público], eu sou o profissional que [diferencial único], diferente de [referências do nicho] porque [razão]"
3. Validar que o posicionamento é defensável com evidências reais do DNA de marca

**Output:** Declaração de Posicionamento de Autoridade

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Validação humana | DNA de marca aprovado pelo profissional antes de avançar |
| Autenticidade | Diferencial único corresponde a evidência real, não aspiração |
| Singularidade | Posicionamento ocupa território distinto da concorrência mapeada |
| Coerência | Voz descrita é consistente com os conteúdos já publicados analisados |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
