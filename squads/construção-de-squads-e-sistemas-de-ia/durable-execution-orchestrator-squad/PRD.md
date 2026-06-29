# Orquestrador de Execução Durável para Squads – Documento de Requisitos do Produto

## Introdução

No repositório Squads‑Genius, os squads são descrições estruturadas de agentes, tarefas e workflows, mas faltam uma plataforma de execução durável e um motor de orquestração. Sem um runtime durável, qualquer falha de infraestrutura, reinício ou interrupção de rede interrompe um agente e obriga a reiniciar toda a operação, aumentando o consumo de tokens e diminuindo a confiabilidade. Em 2025, a execução durável ganhou adoção massiva, com provedores como AWS, Cloudflare e Vercel lançando ofertas específicas para IA【948634456720442†L21-L35】. Esse paradigma garante que o código conclua sua execução apesar de falhas, registrando checkpoints e retomando de onde parou【948634456720442†L40-L46】.

## Problema e Oportunidade

Workflows multiagentes para LLMs são probabilísticos, compostos por várias etapas, usam ferramentas e frequentemente incluem aprovações humanas. Esses fatores criam múltiplos pontos de falha; cada etapa pode falhar por limites de API, alucinações de LLM, tempo de espera de usuários ou quedas de serviço【948634456720442†L65-L114】. Abordagens tradicionais, como retries simples ou filas de jobs, não preservam o estado e exigem que os desenvolvedores implementem lógica de checkpoint manual【948634456720442†L100-L110】. Grandes motores de orquestração, como o Temporal, mostram que a centralização da lógica do workflow, a persistência de estado e a confiabilidade incorporada permitem atingir até cinco noves de disponibilidade sem perda de dados【76773148972022†L68-L81】.

Para que os squads do repositório sejam realmente executáveis, é necessário criar um “Orquestrador de Execução Durável” que permita que qualquer workflow multiagente seja resumido após falhas, escale com segurança, integre aprovações humanas e ofereça observabilidade detalhada. Essa infraestrutura elevará os squads de protótipos conceituais a componentes confiáveis e reutilizáveis.

## Objetivos

- **Garantir execução durável**: preservar estado e retomar workflows do último checkpoint, evitando reexecutar etapas e consumidores de tokens.
- **Orquestrar múltiplas tarefas e agentes**: coordenar tarefas sequenciais, paralelas e condicionais, mantendo contextos e passando dados entre agentes.
- **Suportar aprovações humanas e timers**: incluir gates para pausas indefinidas e retomar somente após sinalização de aprovação, essencial em agentes de IA onde a supervisão humana é crítica【948634456720442†L21-L35】.
- **Apoiar compensações e sagas**: implementar reversão de ações (saga pattern) em caso de falhas parciais, garantindo consistência em workflows distribuídos.
- **Fornecer observabilidade e auditoria**: registrar eventos, decisões, chamadas de ferramentas, tokens usados e custos, conforme recomendado para observabilidade de IA.
- **Escalar e otimizar custos**: distribuir workers horizontalmente, ajustar paralelismo e controlar orçamento por execução.

## Escopo

### Incluso
- Motor durável de orquestração para workflows de squads, com capacidade de registrar e retomar execuções.
- API para iniciar, pausar, retomar, cancelar e monitorar execuções.
- Mecanismo de timers duráveis e sinais para integração de aprovação humana.
- Módulo de compensação para desfazer efeitos colaterais.
- Persistência de estado com armazenamento confiável (banco de dados ou log de eventos).
- Camada de métricas e logs estruturados.
- Suporte a execução local e em nuvem.
- Integração com observabilidade via OpenTelemetry.
- Mecanismo de versionamento de workflows.

### Excluído
- Implementação de agentes de domínio ou squads específicos.
- Criação de interfaces de usuário além de painel básico.
- Sistema de orquestração completo multi-squad (previsto em outro squad).
- Conectores MCP avançados (pertencentes à Factory de Conectores).

## Stakeholders

- **Desenvolvedores de squads**: responsáveis por criar agentes, tasks e workflows.
- **Usuários finais**: beneficiados por squads confiáveis.
- **Equipe de DevOps**: responsável por operação, monitoramento e rollout do orquestrador.
- **Equipe de Segurança e Conformidade**: garante que a execução durável atenda a requisitos regulatórios, protegendo dados sensíveis.

## Casos de Uso

1. **Pesquisa longa com aprovação humana**: um workflow de agente de prospecção de leads planeja, busca, extrai dados e sintetiza. O orquestrador deve permitir que o workflow pause após a etapa de pesquisa para aguardar aprovação humana antes de enviar e‑mails【948634456720442†L65-L114】. Caso o LLM demore horas para responder ou a aprovação atrase, o motor deve suspender sem consumir recursos e retomar sem perder o contexto【948634456720442†L21-L35】.
2. **Integração com APIs externas instáveis**: workflow que usa APIs suscetíveis a rate limit. O orquestrador deve aplicar políticas de retry com backoff e retomar do último ponto, sem duplicar requisições, garantindo exatamente uma vez (exactly‑once).
3. **Automação com compensação**: sequência de atualizações em sistemas externos (e.g., CRM, ERP). Se uma etapa falhar, as etapas anteriores precisam ser revertidas, de acordo com o padrão Saga; o orquestrador deve acionar ações compensatórias.

## Requisitos Funcionais

1. **Registro e controle de workflows**
   - RF1.1: O orquestrador deve permitir registro de workflows com definição de passos (tasks), dependências, paralelismo, timeouts e compensações.
   - RF1.2: Deve suportar versionamento de workflows, permitindo evolução sem interromper execuções antigas.
2. **Execução durável**
   - RF2.1: Para cada passo completado, o orquestrador deve persistir o resultado em armazenamento confiável. Em caso de falha, a execução deve retomar a partir do último passo persistido【172432962056179†L103-L114】.
   - RF2.2: Deve ser possível retomar execuções interrompidas após reinicialização do ambiente ou trocas de worker.
   - RF2.3: Para LLMs e APIs externas, a reexecução não deve gerar cobranças duplicadas; as chamadas devem ser idempotentes ou reutilizadas.
3. **Timers e Sinais**
   - RF3.1: O orquestrador deve oferecer timers duráveis que suspendem execuções sem consumir recursos e disparam após determinado período.
   - RF3.2: Deve aceitar sinais externos (eventos) para prosseguir a execução, viabilizando gates de aprovação humana.
4. **Retry e Backoff**
   - RF4.1: Cada passo deve ter configuração de política de retry, com limites de tentativas, estratégia de backoff e controle de erros transientes.
   - RF4.2: Deve ser possível distinguir erros definitivos de transientes para parar ou continuar.
5. **Compensação**
   - RF5.1: Workflows devem permitir definir actions de compensação para cada passo de efeito colateral. Em caso de falha ou cancelamento, o orquestrador deve orquestrar compensações na ordem inversa (padrão Saga【778145200830822†L119-L123】).
6. **Escalabilidade**
   - RF6.1: O orquestrador deve distribuir execuções entre múltiplos workers e filas.
   - RF6.2: Deve suportar milhares de execuções simultâneas, com controle de paralelismo por squad e priorização.
7. **Observabilidade e Auditoria**
   - RF7.1: Registrar cada evento do workflow (início, término, erro, sinal, compensação).
   - RF7.2: Capturar métricas como latência, tokens de entrada/saída, custo estimado, retries e decisões humanas.
   - RF7.3: Expor logs e traces via OpenTelemetry para monitoramento e análise【76773148972022†L68-L81】.
8. **Segurança e Permissões**
   - RF8.1: Permitir configuração de políticas de execução e acesso por squad e por usuário.
   - RF8.2: Implementar controle de credenciais para chamadas externas, evitando vazamento de segredos.
   - RF8.3: Manter trilha de auditoria para investigações de incidentes.
9. **API e SDK**
   - RF9.1: Disponibilizar API para iniciar e controlar execuções.
   - RF9.2: Fornecer SDK (Python) para implementar tasks e definir workflows de forma declarativa.
   - RF9.3: Integrar com manifestos `workflow.yaml` dos squads.

## Requisitos Não Funcionais

- **Confiabilidade**: garantir disponibilidade de 99.9% inicialmente, com meta de 99.99%. Desdobrar replicação e alta disponibilidade.
- **Desempenho**: latência de orquestração não deve exceder 50 ms por transição interna.
- **Escalabilidade**: suportar aumento de cargas horizontais sem degradar desempenho.
- **Compatibilidade**: o orquestrador deve funcionar em ambientes locais e cloud; compatível com Python 3.11+.
- **Segurança**: cumprir boas práticas de segurança, criptografia em repouso e em trânsito, controle de acesso baseado em funções.
- **Usabilidade**: oferecer APIs claras e documentação extensa.
- **Manutenibilidade**: arquitetura modular, com componentes plugáveis (storage, mensageria).
- **Legalidade e Compliance**: atender a normas ISO 42001 e LGPD, com suporte a políticas de retenção e exclusão.

## Arquitetura Proposta

### Visão Geral

A arquitetura do Orquestrador de Execução Durável será composta por:

1. **Serviço de Orquestração**: núcleo responsável por registrar workflows, coordenar passos, gerar eventos de persistência e orquestrar compensações. Inspirado em engines como Temporal, ele separa a definição do workflow da infraestrutura de execução, garantindo que cada passo seja persistido e possa ser retomado em caso de falha【172432962056179†L103-L114】.
2. **Workers**: processos que executam tarefas definidas. Podem ser escalados horizontalmente; devem ser idempotentes e receber parâmetros de contexto.
3. **Armazenamento Durável**: banco de dados de eventos/jornal que registra o histórico de execuções, passos e resultados. Permite replay e auditoria.
4. **Scheduler & Timer Service**: serviço para timers duráveis, permitindo suspender workflows sem ocupar recursos.
5. **Serviço de Sinais**: canal para receber eventos externos (aprovação humana, resultados de ferramentas).
6. **API & Gateway**: expõe endpoints REST/GraphQL para clientes iniciarem e controlarem execuções e consulta de status.
7. **Observability**: camada de coleta de métricas e traces, integrada ao OpenTelemetry, permitindo dashboards e alertas.
8. **Queue/Message Broker**: camada de filas para distribuir tarefas para workers, suportando priorização e retries.
9. **Compliance & Security Layer**: integra políticas de acesso, criptografia, roteamento de credenciais e logging seguro.

### Integração com Squads

Cada squad existente no repositório define seus workflows em YAML. O orquestrador lerá esses manifests e converterá em objetos de workflow. Os agents serão implementados como atividades (tasks). A integração com outros squads (p.ex., Observability, Security Gateway) ocorrerá através de middlewares: o runtime enviará eventos para o squad de observabilidade e delegará validações ao Security Gateway.

## Modelos de Dados (simplificado)

- **WorkflowDefinition**: id, versão, lista de passos, dependências, políticas de retry e compensação.
- **WorkflowInstance**: id, workflowDefinitionId, status (running, paused, failed, completed, cancelled), data de início, dados de entrada.
- **TaskInstance**: id, workflowInstanceId, nome, status, resultado, número de tentativas, timestamps.
- **Signal**: id, workflowInstanceId, tipo (aprovação, cancelamento, timeout), payload.
- **Timer**: id, workflowInstanceId, data/hora de disparo, status.
- **CompensationAction**: id, taskInstanceId, tipo de compensação, status.
- **EventLog**: id, workflowInstanceId, taskInstanceId, timestamp, tipo (started, completed, failed, compensated), metadata.

## Roadmap Proposto

1. **Fase 0 – Preparação (0‑1 mês)**
   - Levantar requisitos detalhados com stakeholders.
   - Selecionar tecnologia base (própria ou integração com Temporal/Restate).
   - Definir schema de workflow e modelo de dados.
2. **Fase 1 – MVP (1‑3 meses)**
   - Implementar registro e execução linear de workflows com persistência.
   - Implementar timers duráveis e reinício após falhas simples.
   - Expor API básica para iniciar e consultar status.
   - Integrar com squads existentes via YAML.
3. **Fase 2 – Retrys, Aprovações e Compensações (3‑5 meses)**
   - Adicionar políticas de retry com backoff.
   - Implementar sinais para gates de aprovação humana【948634456720442†L21-L35】.
   - Implementar módulo de compensação e suporte a sagas【778145200830822†L119-L123】.
   - Desenvolver painel básico de monitoramento.
4. **Fase 3 – Observabilidade e Segurança (5‑7 meses)**
   - Integrar OpenTelemetry e capturar métricas de tokens, custos e latências.
   - Integrar com o Aegis Security Gateway e o Observability Squad.
   - Implementar controle de permissões, auditoria e políticas de budget.
5. **Fase 4 – Escalabilidade e Alta Disponibilidade (7‑9 meses)**
   - Suportar execução paralela massiva, com sharding e filas dedicadas.
   - Introduzir replicação multi‑região, inspirada em features como Temporal Nexus e High Availability【620160071348530†L72-L87】.
   - Publicar documentação e SDKs.
6. **Fase 5 – Otimizações e Extensões (9‑12 meses)**
   - Integrações com connectors MCP.
   - Suporte a múltiplos squads simultâneos com roteamento inteligente.
   - Implementar simulações, teste de stress e benchmarking integrados.

## Critérios de Aceitação

- Uma execução de workflow que contenha cinco etapas (planejamento, busca, extração, aprovação e síntese) deve completar mesmo se o worker reiniciar no meio do processo, retomando exatamente no último passo persistido sem duplicar chamadas.
- Um workflow com gate de aprovação deve pausar indefinidamente e retomar apenas quando um sinal de aprovação for recebido.
- Cancelar uma execução deve acionar compensações configuradas e registrar eventos correspondentes.
- As métricas de cada execução (latência total, tokens, custo, retries) devem estar disponíveis via API/telemetria.
- Testes de queda (kill workers) não devem causar perda de dados ou corromper estados.

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
| --- | --- | --- | --- |
| Complexidade técnica elevada e curva de aprendizado | Média | Alta | Adotar engine existente (ex.: Temporal) no início; treinar equipe; investir em documentação. |
| Uso excessivo de armazenamento e logs de eventos | Alta | Média | Implementar políticas de retenção e compressão; permitir exportação e arquivamento. |
| Dependência de fornecedores externos se integrar engine SaaS | Média | Média | Considerar solução open‑source; evitar lock-in; desenhar abstrações intercambiáveis. |
| Segurança de dados sensíveis | Alta | Alta | Integrar Security Gateway; criptografar dados; aplicar controles de acesso rigorosos. |
| Atrasos de projeto por integração com squads externos | Média | Média | Planejar roadmap com entregas incrementais; priorizar funcionalidades críticas. |

## Conclusão

O Orquestrador de Execução Durável transformará o repositório Squads‑Genius em uma plataforma operacional capaz de executar workflows de IA complexos com confiabilidade, rastreabilidade e resiliência. Ao adotar princípios de execução durável – persistindo estado, permitindo retries automáticos, incorporando timers e sinais, e fornecendo observabilidade – a solução abordará diretamente os desafios únicos de agentes de IA que são probabilísticos, compostos e de longa duração【948634456720442†L21-L35】. Inspirado em engines como Temporal, que demonstram melhoria dramática de uptime e eliminação de perda de dados【76773148972022†L68-L81】, este PRD define um caminho estruturado para construção e entrega de uma peça fundamental para a maturidade do ecossistema de squads.
