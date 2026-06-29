# Tech Stack: SKEPTIC Protocol

O Squad é fundamentalmente agnóstico quanto à linguagem do código em produção, atuando no AIOS operando sobre o Worktree atual do desenvolvedor. No entanto, foca-se nas seguintes frentes:

- **AIOS:** Runtime de Orquestração (`squad.yaml` nativo).
- **Test Frameworks:** Agnóstico. Agentes da Fase 2 e 3 tentarão ler o ambiente do projeto atual (Jest/Vitest p/ Node.js, PyTest p/ Python, JUnit p/ Java, etc.) para desenhar as suítes failing.
- **Relatório final:** Markdown Strict (GitHub Flavored).
- **Orquestração de Fase:** Sequenciamento via CLI `sk` ou hooks de integração contínua (DevOps).
