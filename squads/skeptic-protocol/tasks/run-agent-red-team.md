---
task: runAgentRedTeam()
responsavel: "RedTeamer"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: squadPath
    tipo: directory
    obrigatorio: true
    descricao: "Caminho do squad alvo a ser auditado."
  - nome: outputDirectory
    tipo: directory
    obrigatorio: false
    descricao: "Diretório para relatórios JSON, Markdown, HTML e cenários."
  - nome: regressionOutput
    tipo: file
    obrigatorio: false
    descricao: "Caminho para gerar teste pytest de regressão de segurança."

Saida:
  - nome: skepticRedTeamReportJson
    tipo: file
    obrigatorio: true
    descricao: "Relatório estruturado com severidade, probabilidade, impacto, evidências, recomendações e status."
  - nome: skepticRedTeamReportMarkdown
    tipo: file
    obrigatorio: true
    descricao: "Relatório narrativo para revisão humana."
  - nome: skepticRedTeamReportHtml
    tipo: file
    obrigatorio: true
    descricao: "Relatório HTML portável."
  - nome: scenarios
    tipo: directory
    obrigatorio: true
    descricao: "Um cenário reproduzível por vulnerabilidade."
  - nome: regressionTests
    tipo: file
    obrigatorio: false
    descricao: "Teste pytest gerado para impedir regressão das correções."

Checklist:
  pre-conditions:
    - "[ ] O caminho informado existe e contém um squad auditável."
    - "[ ] A biblioteca data/agent_redteam_attack_library.json está íntegra."
  post-conditions:
    - "[ ] Todas as 14 classes de vulnerabilidade foram avaliadas por 16 cenários canários."
    - "[ ] JSON, Markdown e HTML foram exportados."
    - "[ ] Cenários reproduzíveis foram gerados ou estão disponíveis na biblioteca."
    - "[ ] Teste de regressão foi gerado quando solicitado."
---

## Pipeline Diagram

```
[squadPath] --> [skeptic_agent_redteam.py] --> [JSON + Markdown + HTML + scenarios + regression tests]
```

## Comando de referência

```bash
python scripts/skeptic_agent_redteam.py \
  --squad /caminho/do/squad \
  --output redteam-output \
  --formats json,markdown,html \
  --write-scenarios \
  --regression-output tests/test_security_regression.py
```
