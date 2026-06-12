name: Integra Incubadora Operations Squad
description: >
  Squad multi-agente para operacionalização completa da incubadora IDNE (Instituto Federal Farroupilha - Campus Frederico Westphalen).
  Automatiza o pipeline de startups, avaliação TRL, geração de Lean Canvas, gestão de mentorias, eventos e relatórios institucionais
  (SEBRAE/FINEP/IFFar).
version: 1.0.0
author: Marcio Bisognin
instagram: '@marciobisognin'
license: MIT

agents:
  - name: intake-coordinator
    role: Triagem e classificação inicial de startups
    description: Avalia a elegibilidade inicial, aplica critérios de triagem e classifica a startup
    skills: [data-validation, form-processing, scoring]
    
  - name: trl-assessor
    role: Avaliação de maturidade tecnológica
    description: Aplica a metodologia TRL (Technology Readiness Level) para avaliar maturidade tecnológica das startups
    skills: [technical-assessment, trl-methodology, evidence-evaluation]
    
  - name: lean-canvas-architect
    role: Modelagem e validação de negócio
    description: Constrói e valida o Lean Canvas, identificando hipóteses críticas e experimentos de validação
    skills: [business-modeling, lean-canvas, hypothesis-validation]
    
  - name: mentorship-matcher
    role: Matching inteligente e gestão de mentorias
    description: Realiza matching inteligente entre startups e mentores, considerando área de expertise, disponibilidade e histórico
    skills: [matching-algorithms, mentorship-management, progress-tracking]
    
  - name: event-manager
    role: Planejamento e execução de eventos
    description: Planeja, organiza e avalia eventos (workshops, demo days, mentorias coletivas)
    skills: [event-planning, logistics, post-event-analysis]
    
  - name: compliance-auditor
    role: Verificação de conformidade
    description: Verifica conformidade com normativos SEBRAE/FINEP/IFFar, identifica gaps e propõe ações corretivas
    skills: [compliance-checking, regulatory-knowledge, audit-trail]
    
  - name: report-generator
    role: Geração de relatórios institucionais
    description: Gera relatórios trimestrais e anuais para SEBRAE, FINEP e Reitoria do IFFar
    skills: [report-writing, data-visualization, template-rendering]
    
  - name: dashboard-monitor
    role: Monitoramento e KPIs
    description: Visualiza KPIs, status de startups, pipeline, mentorias e eventos em tempo real
    skills: [data-visualization, dashboard-design, alerting]

workflows:
  - name: startup-pipeline
    description: Fluxo completo de admissão e acompanhamento de startups
    stages: [intake, trl-assessment, lean-canvas, admission, mentorship, event-management, compliance, reporting]
    
  - name: trl-assessment
    description: Avaliação periódica de maturidade tecnológica
    stages: [data-collection, evidence-review, trl-scoring, report-generation]
    
  - name: mentorship-cycle
    description: Ciclo de matching, sessões e avaliação de mentorias
    stages: [needs-analysis, mentor-matching, session-scheduling, progress-tracking]
    
  - name: event-management
    description: Planejamento, execução e avaliação de eventos
    stages: [planning, logistics, execution, post-event-analysis]
    
  - name: quarterly-reporting
    description: Geração de relatórios trimestrais
    stages: [data-collection, analysis, report-generation, review, submission]
