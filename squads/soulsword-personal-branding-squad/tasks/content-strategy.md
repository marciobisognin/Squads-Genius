---
task:
  name: content-strategy
  id: content-strategy
  title: "Estratégia de Conteúdo Omnicanal e Visibilidade Estratégica"
  icon: "📰"
  description: >
    Tarefa de construção do calendário editorial 90 dias, otimização de LinkedIn, criação
    de thought leadership, kit do palestrante e roadmap de visibilidade PR. Pressupõe
    DNA de marca e posicionamento já validados.
  estimated_duration: "2 a 3 dias úteis"
  squad: soulsword-personal-branding-squad
  workflow: personal-branding-pipeline.yaml
  output_format: Plano de Conteúdo 90 Dias + Kit do Palestrante + Roadmap de Visibilidade PR
  prerequisite_task: brand-dna-mapping.md

inputs:
  required:
    - dna_de_marca: "Documento de DNA de Marca validado"
    - posicionamento: "Declaração de Posicionamento de Autoridade validada"
    - objetivo_marca: "Visibilidade, novos clientes, oportunidades, palestras"
  optional:
    - tom_de_voz: "Exemplos de referência de tom preferido"
    - canais_prioritarios: "LinkedIn, Instagram, YouTube, Substack, X"

outputs:
  primary:
    - name: "Plano de Estratégia de Conteúdo 90 Dias"
      description: "Calendário editorial omnicanal com temas, formatos e cadência"
    - name: "Kit do Palestrante"
      description: "Bios multi-formato, speaker one-sheet e media kit"
    - name: "Roadmap de Visibilidade PR"
      description: "Alvos priorizados de podcasts, imprensa e colaborações"
  secondary:
    - "Guia de Otimização de Perfil LinkedIn"
    - "5 Artigos/Threads de Thought Leadership"

hitl_checkpoints:
  - id: content_authenticity_review
    description: "Revisão de autenticidade do conteúdo produzido pelo profissional"
    required: true
    blocker: true
  - id: speaker_kit_and_pr_approval
    description: "Aprovação do kit do palestrante e roadmap de PR"
    required: true
    blocker: true
---

# Tarefa: Estratégia de Conteúdo Omnicanal e Visibilidade Estratégica

## Visão Geral

Com o DNA de marca e o posicionamento já validados, esta tarefa constrói a execução: o que
publicar, onde otimizar presença, e como buscar visibilidade externa via palestras e PR.

**Pré-requisito:** DNA de marca e posicionamento aprovados na task `brand-dna-mapping.md`.

## Passo a Passo

### Passo 1 — Calendário Editorial Omnicanal de 90 Dias

**Agente responsável:** content-calendar-strategist

**Ações:**
1. Definir pilares de conteúdo alinhados ao posicionamento de autoridade (3 a 5 pilares)
2. Distribuir cadência por canal (LinkedIn, Instagram, YouTube, Substack, X) conforme objetivo de marca
3. Mapear formatos por canal (posts, carrosséis, vídeos curtos, newsletters, threads)
4. Construir calendário semana a semana para os 90 dias

**Output:** Plano de Estratégia de Conteúdo 90 Dias

---

### Passo 2 — Otimização de Perfil LinkedIn

**Agente responsável:** linkedin-optimizer

**Ações:**
1. Reescrever headline alinhada ao posicionamento de autoridade
2. Reestruturar seção "Sobre" com narrativa de propósito e prova social
3. Recomendar conteúdo para seção "Featured" (destaques)
4. Definir estratégia de cadência e formato de posts para o algoritmo do LinkedIn

**Output:** Guia de Otimização de Perfil LinkedIn

---

### Passo 3 — Criação de Thought Leadership

**Agente responsável:** thought-leadership-writer

**Ações:**
1. Selecionar 5 temas alinhados ao posicionamento e às perguntas mais relevantes do público-alvo
2. Escrever artigos/threads com voz autêntica do profissional (validada no DNA de marca)
3. Garantir originalidade: nenhum conteúdo copiado ou parafraseado sem atribuição

**Output:** 5 Artigos/Threads de Thought Leadership

---

### Passo 4 — HITL: Revisão de Autenticidade do Conteúdo

**Responsável:** Usuário/Profissional

**O que revisar:**
- O tom de voz do conteúdo produzido reflete como o profissional realmente se comunica
- Os temas escolhidos são relevantes e verdadeiramente representativos
- Nenhuma afirmação exagera resultados ou credenciais

**Gate de qualidade:** gate `content_authenticity_reviewed` do quality-gates.yaml

---

### Passo 5 — Kit do Palestrante e Roadmap de Visibilidade PR

**Agentes responsáveis:** speaker-pitch-designer, pr-visibility-planner

**Ações:**
1. Construir bios multi-formato, speaker one-sheet e media kit (speaker-pitch-designer)
2. Mapear alvos de PR (podcasts, veículos, eventos, colaborações) priorizados por alinhamento de audiência (pr-visibility-planner)
3. Redigir pitches personalizados para os alvos prioritários

**Output:** Kit do Palestrante + Roadmap de Visibilidade PR

---

### Passo 6 — HITL: Aprovação Final de Kit e Roadmap

**Responsável:** Usuário/Profissional

**O que revisar:**
- Prova social no kit do palestrante é verificável
- Alvos de PR são relevantes e não conflitam com restrições do profissional

**Gate de qualidade:** gate `speaker_kit_approved` e `pr_targets_validated` do quality-gates.yaml

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Cobertura de canais | Calendário cobre todos os canais prioritários definidos pelo objetivo |
| Autenticidade de conteúdo | 100% do conteúdo aprovado pelo profissional como tom autêntico |
| Originalidade | Zero conteúdo copiado ou parafraseado sem atribuição |
| Alvos de PR | Cada alvo tem justificativa de alinhamento de audiência |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
