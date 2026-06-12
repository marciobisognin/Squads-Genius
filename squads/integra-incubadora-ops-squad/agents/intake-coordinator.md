name: Integra Incubadora Operations Squad
description: >
  Squad multi-agente para operacionaliza%C3%A7%C3%A3o completa da incubadora IDNE (Instituto Federal Farroupilha - Campus Frederico Westphalen).
  Automatiza o pipeline de startups, avalia%C3%A7%C3%A3o TRL, gera%C3%A7%C3%A3o de Lean Canvas, gest%C3%A3o de mentorias, eventos e relat%C3%B3rios institucionais
  (SEBRAE/FINEP/IFFar).
version: 1.0.0
author: Marcio Bisognin
instagram: '@marciobisognin'
license: MIT

agents:
  - name: intake-coordinator
    role: Triagem e classifica%C3%A7%C3%A3o inicial de startups
    description: Avalia a elegibilidade inicial, aplica crit%C3%A9rios de triagem e classifica a startup
    skills: [data-validation, form-processing, scoring]
    
  - name: trl-assessor
    role: Avalia%C3%A7%C3%A3o de maturidade tecnol%C3%B3gica
    description: Aplica a metodologia TRL (Technology Readiness Level) para avaliar maturidade tecnol%C3%B3gica das startups
    skills: [technical-assessment, trl-methodology, evidence-evaluation]
    
  - name: lean-canvas-architect
    role: Modelagem e valida%C3%A7%C3%A3o de neg%C3%B3cio
    description: Constr%C3%B3i e valida o Lean Canvas, identificando hip%C3%B3teses cr%C3%ADticas e experimentos de valida%C3%A7%C3%A3o
    skills: [business-modeling, lean-canvas, hypothesis-validation]
    
  - name: mentorship-matcher
    role: Matching inteligente e gest%C3%A3o de mentorias
    description: Realiza matching inteligente entre startups e mentores, considerando %C3%A1rea de expertise, disponibilidade e hist%C3%B3rico
    skills: [matching-algorithms, mentorship-management, progress-tracking]
    
  - name: event-manager
    role: Planejamento e execu%C3%A7%C3%A3o de eventos
    description: Planeja, organiza e avalia eventos (workshops, demo days, mentorias coletivas)
    skills: [event-planning, logistics, post-event-analysis]
    
  - name: compliance-auditor
    role: Verifica%C3%A7%C3%A3o de conformidade
    description: Verifica conformidade com normativos SEBRAE/FINEP/IFFar, identifica gaps e prop%C3%B5e a%C3%A7%C3%B5es corretivas
    skills: [compliance-checking, regulatory-knowledge, audit-trail]
    
  - name: report-generator
    role: Gera%C3%A7%C3%A3o de relat%C3%B3rios institucionais
    description: Gera relat%C3%B3rios trimestrais e anuais para SEBRAE, FINEP e Reitoria do IFFar
    skills: [report-writing, data-visualization, template-rendering]
    
  - name: dashboard-monitor
    role: Monitoramento e KPIs
    description: Visualiza KPIs, status de startups, pipeline, mentorias e eventos em tempo real
    skills: [data-visualization, dashboard-design, alerting]

workflows:
  - name: startup-pipeline
    description: Fluxo completo de admiss%C3%A3o e acompanhamento de startups
    stages: [intake, trl-assessment, lean-canvas, admission, mentorship, event-management, compliance, reporting]
    
  - name: trl-assessment
    description: Avalia%C3%A7%C3%A3o peri%C3%B3dica de maturidade tecnol%C3%B3gica
    stages: [data-collection, evidence-review, trl-scoring, report-generation]
    
  - name: mentorship-cycle
    description: Ciclo de matching, sess%C3%B5es e avalia%C3%A7%C3%A3o de mentorias
    stages: [needs-analysis, mentor-matching, session-scheduling, progress-tracking]
    
  - name: event-management
    description: Planejamento, execu%C3%A7%C3%A3o e avalia%C3%A7%C3%A3o de eventos
    stages: [planning, logistics, execution, post-event-analysis]
    
  - name: quarterly-reporting
    description: Gera%C3%A7%C3%A3o de relat%C3%B3rios trimestrais
    stages: [data-collection, analysis, report-generation, review, submission]
