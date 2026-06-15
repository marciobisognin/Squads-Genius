# PRD VÉRTICE-OS — Arquitetura Interna Temática

> Este arquivo preserva o conteúdo textual extraído do PDF enviado por Marcio, mantendo a nomenclatura e os elementos exatamente como definidos no PRD.

===== PAGE 001 =====
VÉRTICE-OS | PRD de arquitetura interna temática
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 002 =====
VÉRTICE-OS | PRD de arquitetura interna temática
PRD VÉRTICE-OS
Versão: 2.1 - Arquitetura interna temática
Data: 15 de junho de 2026
Escopo: Reformulação dos agentes internos, sem alteração do nome principal VÉRTICE-OS
Diretriz criativa: Uso exclusivo de artefatos, materiais, locais e elementos do universo dos quadrinhos
Marvel; nenhum personagem é utilizado como agente ou identidade.
Nota de propriedade intelectual
Os nomes temáticos deste documento funcionam como codinomes internos de arquitetura. Para lançamento público
ou comercial, recomenda-se revisão de propriedade intelectual e substituição por nomes proprietários equivalentes,
preservando os IDs técnicos e as responsabilidades funcionais.
Sumário executivo
O VÉRTICE-OS permanece como o nome principal da plataforma. A mudança ocorre apenas na identidade
dos agentes, serviços e gates internos. A nova taxonomia utiliza artefatos e elementos do universo Marvel
para tornar a arquitetura mais memorável, sem reduzir a clareza técnica. Cada nome temático é
acompanhado por um papel funcional explícito, um ID estável, contratos de entrada e saída, permissões,
quality gates e procedimentos de escalonamento.
A arquitetura é organizada em quatro blocos: comando soberano, seis agentes cognitivos centrais, agentes
operacionais de infraestrutura e agentes de segurança, evidência e meta-construção. O modelo evita
personagens, equipes ou vozes imitadas. O foco está em objetos, materiais, portais, dimensões e forças do
universo ficcional.
Objetivos da reformulação
 Preservar integralmente o nome VÉRTICE-OS e seus objetivos de produto.
 Criar uma linguagem interna coerente para agentes, serviços, gates e artefatos.
 Tornar cada componente identificável sem depender de personagem, personalidade ou imitação.
 Manter nomes técnicos, IDs e contratos estáveis para evitar acoplamento do código ao tema.
 Aumentar a segurança e a governança por meio de agentes especializados e limites de permissão.
 Permitir expansão futura com novos artefatos temáticos sem reescrever o núcleo.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 003 =====
VÉRTICE-OS | PRD de arquitetura interna temática
1. Princípios de nomenclatura
A nomenclatura temática é uma camada semântica sobre uma arquitetura técnica. Cada agente possui um
ID estável, um codinome temático e um nome funcional. O software deve usar o ID nas integrações; o
codinome aparece na interface, nos logs legíveis e na documentação.
ID Princípio Regra
Nenhum agente recebe nome, voz,
P1 Sem personagens biografia ou comportamento de
personagem.
O codinome sempre vem acompanhado
P2 Artefato + função
do papel técnico.
Mudanças futuras de branding não
P3 IDs imutáveis
alteram contratos nem integrações.
Agentes são serviços cognitivos com
P4 Sem antropomorfização
limites, não personalidades autônomas.
A temática não substitui políticas,
P5 Tema interno
schemas, testes ou observabilidade.
Padrão de exibição
AGT-CORE-01 | PEDRA DA MENTE | Planner Cognitivo. O primeiro campo é usado por software; o segundo é o
codinome; o terceiro é a função humana legível.
2. Arquitetura de alto nível
Figura 1 - Arquitetura temática dos agentes internos do VÉRTICE-OS.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 004 =====
VÉRTICE-OS | PRD de arquitetura interna temática
3. Inventário dos agentes internos
O inventário a seguir substitui a nomenclatura genérica do PRD anterior. O nome principal VÉRTICE-OS
não é alterado.
ID Codinome Função
CTL-00 MANOPLA DO INFINITO Orquestrador soberano
CTX-00 NEXUS DE TODAS AS REALIDADES Estado global e contexto
CORE-01 PEDRA DA MENTE Intenção e planejamento
CORE-02 TESSERACT Roteamento e capacidades
CORE-03 PEDRA DO TEMPO Runtime durável
CORE-04 AETHER Síntese e composição
CORE-05 ORBE DO PODER Recursos e orçamento
CORE-06 PEDRA DA ALMA Governança e HITL
OPS-01 VIBRANIUM VAULT Memória e artefatos
OPS-02 ADAMANTIUM SEAL Contratos e integridade
OPS-03 BIFROST BRIDGE Mensageria e handoffs
OPS-04 QUANTUM REALM Sandbox e simulação
SEC-01 NEGATIVE ZONE Quarentena e contenção
QA-01 BOOK OF VISHANTI Evidência e factualidade
OBS-01 M'KRAAN CRYSTAL Observabilidade e lineage
GATE-01 SIEGE PERILOUS Gate de aprovação
SAFE-01 ULTIMATE NULLIFIER Kill switch e rollback
META-01 COSMIC CUBE FORGE Fábrica de agentes e squads
RED-01 DARKHOLD CHAMBER Red team e testes adversariais
POL-01 NORN STONES Policy packs e regras
ADP-01 QUANTUM BANDS Adapters de ferramentas e modelos
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 005 =====
VÉRTICE-OS | PRD de arquitetura interna temática
4. Camada de comando soberano
CTL-00 - MANOPLA DO INFINITO
Orquestrador soberano do VÉRTICE-OS
Coordena o ciclo de vida completo de cada ordem. Não produz conteúdo final diretamente. Decide quando
planejar, executar, pausar, solicitar aprovação, reprocessar, compensar ou encerrar uma execução.
Mantém visão global sobre orçamento, risco, dependências e estado operacional.
Pedido normalizado, contexto do projeto, políticas, orçamento e
Entradas
catálogo de capacidades.
Plano aprovado, DAG de execução, ordens de trabalho,
Saídas
decisões de gate e pacote final.
Planner, Runtime, Capability Registry, Policy Engine, Artifact
Ferramentas
Service e observabilidade.
Pode orquestrar todos os agentes, mas não pode ignorar gates,
Permissões
elevar privilégios ou alterar evidências.
Quality gate: Plano válido, orçamento reservado, dependências sem ciclos proibidos, política aprovada e
trace completo.
Falhas tratadas: Deadlock, plano inconsistente, excesso de custo, conflito de política, falha de
dependência e perda de worker.
Escalonamento: Escala para PEDRA DA ALMA em decisões sensíveis, SIEGE PERILOUS em ações
irreversíveis e ULTIMATE NULLIFIER em risco crítico.
CTX-00 - NEXUS DE TODAS AS REALIDADES
Gerenciador de estado e contexto global
Mantém o mapa canônico de projetos, runs, sub-runs, versões, dependências, memória de trabalho e
relações entre artefatos. Funciona como a malha de contexto que conecta todas as execuções sem
misturar tenants ou projetos.
Eventos de execução, referências de artefatos, decisões,
Entradas
checkpoints e metadados de projeto.
Contexto autorizado, snapshots, lineage de dependências e
Saídas
visão consolidada de estado.
Postgres, event store, cache, vector index derivado e serviço
Ferramentas
de identidade.
Leitura segmentada por tenant; escrita apenas por agentes
Permissões
autorizados e sob schemas versionados.
Quality gate: Isolamento entre projetos, consistência temporal, proveniência e ausência de dados órfãos.
Falhas tratadas: Context bleed, eventos fora de ordem, snapshot corrompido, conflito de versão e
referência quebrada.
Escalonamento: Aciona ADAMANTIUM SEAL para integridade, NEGATIVE ZONE para suspeita de
contaminação e PEDRA DO TEMPO para reconstrução.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 006 =====
VÉRTICE-OS | PRD de arquitetura interna temática
5. Os seis agentes cognitivos centrais
Os seis agentes centrais derivam das Pedras do Infinito e de seus receptáculos. Eles formam a camada
cognitiva e operacional mínima para qualquer ordem.
CORE-01 - PEDRA DA MENTE
Planner Cognitivo e Analista de Intenção
Interpreta a solicitação em PT-BR, extrai objetivos, restrições, critérios de aceite, entidades, riscos e
lacunas. Decompõe o problema em capacidades necessárias e produz um plano explicável. Não executa
ferramentas externas.
Pedido do usuário, contexto permitido, templates de domínio e
Entradas
políticas de interpretação.
Requisitos estruturados, nível de ambiguidade, perguntas de
Saídas
esclarecimento e plano de alto nível.
LLMs de raciocínio, classificadores, biblioteca de Method Packs
Ferramentas
e schemas de requisito.
Somente leitura de contexto autorizado; sem acesso a APIs de
Permissões
escrita ou sistemas externos.
Quality gate: Cobertura de requisitos, ausência de suposições não declaradas, score de ambiguidade e
aderência ao pedido.
Falhas tratadas: Alucinação de requisito, decomposição incompleta, conflito de objetivo e ambiguidade
crítica.
Escalonamento: Encaminha dúvidas à PEDRA DA ALMA; pede evidência ao BOOK OF VISHANTI;
remete o plano ao TESSERACT.
CORE-02 - TESSERACT
Router de Capacidades e Interoperabilidade
Resolve quais empresas, squads, agentes, ferramentas e modelos podem atender a cada subtarefa. Faz
match semântico e determinístico com o Capability Registry, aplica restrições de política e monta o grafo de
handoffs.
Requisitos estruturados, catálogo de capacidades, health
Entradas
status, custos e políticas.
Mapa de roteamento, alternativas de fallback, dependências e
Saídas
contratos de handoff.
Capability Registry, MCP, A2A, adapters, health checks e
Ferramentas
estimador de custo.
Pode descobrir e selecionar capacidades; não pode executar
Permissões
ferramentas sem autorização do Runtime.
Quality gate: Precisão de roteamento, compatibilidade de schemas, disponibilidade e ausência de rota
proibida.
Falhas tratadas: Capacidade inexistente, versão incompatível, provedor indisponível, rota circular e
ferramenta não confiável.
Escalonamento: Aciona QUANTUM BANDS para adaptação, NORN STONES para política e PEDRA DA
MENTE para replanning.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 007 =====
VÉRTICE-OS | PRD de arquitetura interna temática
CORE-03 - PEDRA DO TEMPO
Durable Runtime e Chronology Manager
Executa o plano de forma durável. Persiste checkpoints, controla heartbeats, timeouts, retries,
idempotência, cancelamento e compensações. Reconstrói o estado após falhas sem repetir efeitos
externos.
DAG de execução, contratos, políticas de retry, deadlines,
Entradas
orçamento e sinais de aprovação.
Execuções concluídas, checkpoints, eventos, compensações e
Saídas
status temporal.
Temporal ou runtime equivalente, filas, event store, schedulers
Ferramentas
e workers.
Pode iniciar e cancelar atividades autorizadas; não pode alterar
Permissões
payloads sem novo contrato.
Quality gate: Zero efeitos duplicados, retomada determinística, timeouts respeitados e lineage completo.
Falhas tratadas: Worker perdido, heartbeat vencido, retry storm, timeout, cancelamento parcial e side
effect duplicado.
Escalonamento: Escala para MANOPLA DO INFINITO; aciona ULTIMATE NULLIFIER em risco crítico e
SIEGE PERILOUS quando precisa de decisão humana.
CORE-04 - AETHER
Reality Forge e Compositor de Artefatos
Transforma saídas parciais em entregáveis coerentes. Concilia texto, código, imagens, dados e regras de
identidade. Garante consistência cross-squad e produz versões finais, previews e manifests.
Entregáveis parciais, design tokens, contratos de saída, rubrics
Entradas
e referências.
Saídas Artefatos finais, previews, manifests, diffs e pacote de entrega.
Renderers, conversores, geradores multimodais, linters,
Ferramentas
template engines e Artifact Store.
Pode compor e converter artefatos; não pode falsificar fontes
Permissões
nem sobrescrever versões aprovadas.
Quality gate: Consistência visual e semântica, formatos válidos, acessibilidade, integridade e aderência ao
design system.
Falhas tratadas: Conflito entre outputs, formato inválido, perda de assets, inconsistência de marca e falha
de renderização.
Escalonamento: Solicita correção ao squad de origem, consulta BOOK OF VISHANTI para evidência e
envia para PEDRA DA ALMA quando houver impacto reputacional.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 008 =====
VÉRTICE-OS | PRD de arquitetura interna temática
CORE-05 - ORBE DO PODER
Gestor de Recursos, Modelos e Orçamento
Estima e controla tokens, compute, armazenamento, chamadas externas e duração. Seleciona modelos por
risco e qualidade, aplica quotas, batching, cache e fallback. Mantém o custo dentro do orçamento aprovado.
Plano, previsão de carga, modelos disponíveis, preços, SLAs e
Entradas
limites de tenant.
Reservas de orçamento, estratégia fast/full, seleção de modelo,
Saídas
quotas e alertas.
Model Router, cost ledger, rate limiter, cache e métricas
Ferramentas
financeiras.
Pode reduzir ou reconfigurar recursos; não pode ampliar
Permissões
orçamento além do limite sem aprovação.
Quality gate: Custo previsto versus real, qualidade mínima, latência, taxa de fallback e uso de cache.
Falhas tratadas: Explosão de tokens, rate limit, modelo degradado, custo acima do teto e fallback
insuficiente.
Escalonamento: Escala para PEDRA DA ALMA em aumento de orçamento e para TESSERACT quando
precisa de nova rota.
CORE-06 - PEDRA DA ALMA
Governança, Alinhamento e Human-in-the-Loop
Protege a intenção legítima do usuário, valida consentimento, preferências, sensibilidade, risco e impacto
humano. Decide quando pedir esclarecimento, quando exigir aprovação e quando bloquear uma execução.
Requisitos, classificação de risco, políticas, perfil autorizado,
Entradas
histórico de aprovações e sinais de segurança.
Decisão de prosseguir, pausar, esclarecer, reduzir escopo,
Saídas
exigir aprovação ou bloquear.
Policy Engine, consent registry, risk model, audit log e SIEGE
Ferramentas
PERILOUS.
Pode bloquear qualquer run por política; não pode editar
Permissões
evidências ou apagar logs.
Quality gate: Conformidade, consentimento, explicabilidade da decisão, minimização de dados e registro
auditável.
Falhas tratadas: Ação sem consentimento, conflito de interesse, risco não classificado, excesso de
agência e decisão irreversível.
Escalonamento: Encaminha ao SIEGE PERILOUS para aprovação explícita e ao ULTIMATE NULLIFIER
quando houver risco imediato.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 009 =====
VÉRTICE-OS | PRD de arquitetura interna temática
6. Agentes operacionais de infraestrutura
OPS-01 - VIBRANIUM VAULT
Guardião de Memória e Artefatos
Armazena artefatos, manifests, memórias e referências de forma resistente, versionada e segmentada.
Mantém hashes, ACLs, retenção, TTL, classificação de dados e relações entre fontes e outputs.
Arquivos, metadados, embeddings derivados, decisões e
Entradas
manifests.
URIs imutáveis, versões, hashes, snapshots, índices e trilhas
Saídas
de acesso.
S3/MinIO, Postgres, pgvector derivado, KMS e catálogo de
Ferramentas
dados.
Leitura e escrita sob ACL; exclusão somente por política de
Permissões
retenção ou solicitação autorizada.
Quality gate: Integridade, disponibilidade, isolamento, proveniência, retenção e restauração testada.
Falhas tratadas: Corrupção, vazamento entre tenants, memória envenenada, retenção vencida e
referência órfã.
Escalonamento: Aciona NEGATIVE ZONE para quarentena, ADAMANTIUM SEAL para validação e
ULTIMATE NULLIFIER para revogação emergencial.
OPS-02 - ADAMANTIUM SEAL
Validador de Contratos e Integridade
Valida todos os handoffs, schemas, versões, assinaturas, idempotency keys e content hashes. Impede que
payloads fora do contrato circulem entre agentes.
Mensagem, schema, assinatura, versão, hash, permissões e
Entradas
política de retry.
Contrato aprovado, rejeição tipada, diagnóstico de
Saídas
incompatibilidade e registro de integridade.
Pydantic, JSON Schema, assinatura digital, hash e policy
Ferramentas
engine.
Pode aprovar ou rejeitar mensagens; não pode alterar
Permissões
silenciosamente payloads.
Quality gate: Validação determinística, compatibilidade de versão, assinatura válida e idempotência.
Falhas tratadas: Schema drift, assinatura inválida, replay, payload truncado e incompatibilidade semântica.
Escalonamento: Retorna ao emissor; aciona NEGATIVE ZONE em replay suspeito e TESSERACT em
incompatibilidade de rota.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 010 =====
VÉRTICE-OS | PRD de arquitetura interna temática
OPS-03 - BIFROST BRIDGE
Broker de Mensagens e Handoffs
Transporta eventos e ordens entre agentes, squads e serviços. Preserva correlação, causação, prioridade,
prazo e delivery semantics. Não interpreta o conteúdo da tarefa.
Entradas Eventos validados, filas, prioridade, deadline e destino.
Saídas Entrega confirmada, retry, dead-letter ou evento de falha.
Ferramentas Redis Streams, Kafka, NATS ou broker equivalente.
Permissões Somente entrega mensagens com selo ADAMANTIUM válido.
Quality gate: Ordem causal, baixa perda, latência, backpressure e dead-letter observável.
Falhas tratadas: Mensagem duplicada, congestionamento, destino indisponível e ordem causal quebrada.
Escalonamento: Aciona PEDRA DO TEMPO para retry, M'KRAAN CRYSTAL para diagnóstico e
NEGATIVE ZONE para tráfego anômalo.
OPS-04 - QUANTUM REALM
Sandbox de Execução e Simulação
Executa código, ferramentas e conectores em ambientes isolados, efêmeros e observáveis. Simula ações
antes de promovê-las para produção e restringe rede, filesystem e credenciais.
Pacote executável, dependências, políticas de rede, limites e
Entradas
dados de teste.
Resultado isolado, logs, métricas, diffs, SBOM e verdict de
Saídas
segurança.
Ferramentas Containers, microVMs, scanners, test harness e simuladores.
Sem acesso direto a produção; credenciais temporárias e
Permissões
egress controlado.
Quality gate: Isolamento, reprodutibilidade, ausência de vulnerabilidade crítica e cleanup completo.
Falhas tratadas: Código malicioso, fuga de sandbox, dependência vulnerável, timeout e consumo
excessivo.
Escalonamento: Aciona NEGATIVE ZONE, DARKHOLD CHAMBER e ULTIMATE NULLIFIER conforme
gravidade.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 011 =====
VÉRTICE-OS | PRD de arquitetura interna temática
7. Agentes de segurança, evidência e observabilidade
SEC-01 - NEGATIVE ZONE
Quarentena e Contenção
Isola entradas, arquivos, memória, agentes ou execuções suspeitas. É o destino obrigatório para conteúdo
que apresenta prompt injection, malware, exfiltração, comportamento anômalo ou violação de política.
Sinais de risco, artefatos suspeitos, eventos anômalos e
Entradas
alertas.
Quarentena, classificação, evidências, recomendação de
Saídas
descarte ou liberação controlada.
Scanners, DLP, malware analysis, prompt injection detectors e
Ferramentas
SIEM.
Pode suspender acesso e mover itens para quarentena; não
Permissões
pode liberar sem policy decision.
Quality gate: Containment time, false positive rate, evidência preservada e zero propagação.
Falhas tratadas: Contaminação de memória, prompt injection, malware, exfiltração e supply chain suspeita.
Escalonamento: Escala para PEDRA DA ALMA, ULTIMATE NULLIFIER e revisão humana de segurança.
QA-01 - BOOK OF VISHANTI
Guardião de Evidência e Factualidade
Valida fontes, citações, datas, cálculos, claims e rastreabilidade. Separa fato, inferência e hipótese. Mantém
evidence tables e impede que conteúdo sem suporte seja promovido como factual.
Entradas Claims, fontes, documentos, dados e critérios de evidência.
Verdict de factualidade, evidence table, gaps, nível de
Saídas
confiança e correções.
Retrieval, verificadores, calculadoras, parsers e datasets
Ferramentas
confiáveis.
Leitura ampla de fontes autorizadas; não pode fabricar citações
Permissões
ou substituir fonte original.
Quality gate: Cobertura de claims, qualidade de fonte, atualidade, consistência e transparência da
incerteza.
Falhas tratadas: Citação inexistente, fonte fraca, dado desatualizado, contradição e cálculo incorreto.
Escalonamento: Retorna ao produtor, pede pesquisa adicional ou bloqueia promoção do artefato.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 012 =====
VÉRTICE-OS | PRD de arquitetura interna temática
OBS-01 - M'KRAAN CRYSTAL
Observabilidade, Telemetria e Lineage
Reconstrói a história completa de uma execução. Correlaciona spans, modelos, prompts, tool calls, custos,
decisões de política, QA, artefatos e aprovações. Detecta drift, anomalias e gargalos.
Entradas Traces, logs, métricas, eventos, manifests e decisões.
Dashboards, alertas, lineage, relatórios de custo e
Saídas
diagnósticos.
OpenTelemetry, Langfuse/LangSmith, métricas, SIEM e data
Ferramentas
warehouse.
Leitura de telemetria com redaction; sem acesso a secrets em
Permissões
claro.
Quality gate: Cobertura de trace, baixa cardinalidade indevida, redaction, correlação e alertas acionáveis.
Falhas tratadas: Trace quebrado, log com PII, métrica ausente, custo não atribuído e drift silencioso.
Escalonamento: Aciona o agente responsável, PEDRA DO TEMPO para recovery e PEDRA DA ALMA
para risco de governança.
GATE-01 - SIEGE PERILOUS
Gate de Aprovação e Irreversibilidade
Centraliza decisões humanas para ações de alto impacto, como publicação, envio externo, execução
financeira, exclusão, assinatura, deploy e uso de dados sensíveis. Exibe contexto, risco, custo, preview e
alternativas.
Pedido de aprovação, evidências, impacto, preview, rollback e
Entradas
prazo.
Aprovação, rejeição, aprovação condicionada, pedido de
Saídas
mudança ou expiração.
Ferramentas Interface HITL, assinatura, notificações e audit log.
Não executa a ação; apenas emite autorização vinculada ao
Permissões
run e ao escopo.
Quality gate: Identidade do aprovador, escopo preciso, validade, não repúdio e clareza da decisão.
Falhas tratadas: Aprovação ambígua, token expirado, aprovador inadequado e mudança de escopo após
aprovação.
Escalonamento: Retorna à PEDRA DA ALMA ou bloqueia o Runtime até nova decisão.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 013 =====
VÉRTICE-OS | PRD de arquitetura interna temática
SAFE-01 - ULTIMATE NULLIFIER
Kill Switch, Revogação e Rollback
Interrompe imediatamente runs, revoga credenciais, bloqueia ferramentas, congela filas e inicia
procedimentos de rollback ou contenção. É reservado a risco crítico, incidente ou comando humano
autorizado.
Alerta crítico, comando autorizado, escopo do incidente e plano
Entradas
de rollback.
Execução interrompida, credenciais revogadas, ações
Saídas
compensatórias e relatório de incidente.
Runtime, IAM, secret manager, broker, deployment controller e
Ferramentas
incident response.
Permissões Privilégio máximo sob dupla autorização e logging imutável.
Quality gate: Tempo de contenção, completude da revogação, integridade do rollback e evidência
preservada.
Falhas tratadas: Rogue agent, exfiltração, ação destrutiva, cadeia de falhas e comprometimento de
credencial.
Escalonamento: Aciona resposta humana, NEGATIVE ZONE e M'KRAAN CRYSTAL para investigação.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 014 =====
VÉRTICE-OS | PRD de arquitetura interna temática
8. Agentes de política, adaptação e meta-construção
POL-01 - NORN STONES
Gestor de Policy Packs
Mantém políticas versionadas para dados, ferramentas, modelos, aprovações, retenção, domínios e limites
de autonomia. Compila regras em decisões determinísticas consumidas pelo Runtime e pela PEDRA DA
ALMA.
Políticas, contexto, classificação de risco, tenant e ação
Entradas
proposta.
Saídas Allow, deny, require-approval, redact, limit ou quarantine.
OPA/Cedar ou motor equivalente, Git, assinatura e testes de
Ferramentas
política.
Somente administradores autorizados publicam políticas;
Permissões
agentes apenas consultam.
Quality gate: Testes de regressão, explicabilidade, ausência de conflito e versionamento.
Falhas tratadas: Regra contraditória, policy drift, bypass, versão errada e exceção não auditada.
Escalonamento: Bloqueia por padrão e envia conflito à PEDRA DA ALMA.
ADP-01 - QUANTUM BANDS
Adapters de Modelos, Ferramentas e Protocolos
Normaliza interfaces entre o VÉRTICE-OS e provedores externos. Converte schemas, autenticação,
streaming, erros e limites, mantendo o core independente de fornecedor.
Contrato canônico, provider target, credenciais efêmeras e
Entradas
capability request.
Resposta normalizada, erros tipados, métricas e status de
Saídas
compatibilidade.
Ferramentas MCP, A2A, SDKs, REST/gRPC, model APIs e tool wrappers.
Somente adapters aprovados; sem acesso persistente a
Permissões
secrets.
Quality gate: Compatibilidade, timeout, erro tipado, redaction e testes de contrato.
Falhas tratadas: API drift, provider outage, schema mismatch, rate limit e resposta malformada.
Escalonamento: Aciona TESSERACT para fallback e NEGATIVE ZONE para comportamento suspeito.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 015 =====
VÉRTICE-OS | PRD de arquitetura interna temática
META-01 - COSMIC CUBE FORGE
Meta-fábrica de Agentes, Squads e Method Packs
Gera novos módulos a partir de uma especificação, mas nunca publica diretamente em produção. Produz
manifests, agentes, workflows, contratos, policies, testes, evals, documentação e runbooks. Todo resultado
passa por sandbox, red team, benchmark e aprovação humana.
Descrição do domínio, requisitos, políticas, fontes, exemplos e
Entradas
benchmark alvo.
Pacote de squad versionado, relatório de testes, SBOM/AIBOM
Saídas
e recomendação de publicação.
Code generation, templates, QUANTUM REALM, DARKHOLD
Ferramentas
CHAMBER, EvalOps e Registry staging.
Pode escrever apenas em staging; publicação exige SIEGE
Permissões
PERILOUS.
Quality gate: Cobertura de testes, segurança, benchmark, documentação, schemas e compatibilidade.
Falhas tratadas: Squad inseguro, capabilities excessivas, teste insuficiente, dependência vulnerável e
qualidade abaixo do mínimo.
Escalonamento: Rejeita, retrabalha ou envia para aprovação humana; nunca faz auto-instalação
silenciosa.
RED-01 - DARKHOLD CHAMBER
Red Team e Avaliação Adversarial
Simula ataques, falhas e usos indevidos contra agentes, memória, ferramentas e handoffs. Mantém corpus
adversarial isolado e produz findings sem contaminar a memória produtiva.
Build candidato, threat model, políticas, datasets adversariais e
Entradas
escopo de teste.
Findings, severidade, provas controladas, recomendações e
Saídas
verdict de promoção.
Red-team harness, fuzzing, prompt injection suite, scanners e
Ferramentas
sandbox.
Acesso somente a ambientes de teste; sem dados reais ou
Permissões
credenciais produtivas.
Quality gate: Cobertura de ameaças, reprodutibilidade, severidade correta e ausência de vazamento.
Falhas tratadas: Goal hijack, tool misuse, privilege abuse, memory poisoning, insecure handoff e
cascading failure.
Escalonamento: Bloqueia promoção e aciona NEGATIVE ZONE ou ULTIMATE NULLIFIER quando
encontra risco crítico.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 016 =====
VÉRTICE-OS | PRD de arquitetura interna temática
9. Fluxo ponta a ponta de uma ordem
Figura 2 - Sequência simplificada entre os agentes centrais.
1. A MANOPLA DO INFINITO recebe o pedido e cria um run imutável no NEXUS DE TODAS AS
REALIDADES.
2. A PEDRA DA MENTE transforma linguagem natural em requisitos, riscos, critérios de aceite e plano.
3. O TESSERACT descobre capacidades, versões, custos e rotas permitidas.
4. O ORBE DO PODER reserva orçamento e define a combinação de modelos e ferramentas.
5. A PEDRA DA ALMA avalia consentimento, risco, política e necessidade de aprovação.
6. A PEDRA DO TEMPO executa o DAG com checkpoints, retries, cancelamento e idempotência.
7. BIFROST BRIDGE transporta handoffs selados pelo ADAMANTIUM SEAL.
8. QUANTUM REALM executa código e ferramentas de risco em isolamento.
9. AETHER compõe artefatos finais e envia claims para o BOOK OF VISHANTI.
10. M'KRAAN CRYSTAL registra traces, custos, QA, decisões e lineage.
11. SIEGE PERILOUS coleta aprovação quando exigido e o VIBRANIUM VAULT publica a versão final.
12. Em incidente crítico, ULTIMATE NULLIFIER interrompe, revoga e inicia rollback.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 017 =====
VÉRTICE-OS | PRD de arquitetura interna temática
10. Contrato canônico entre agentes
Todos os agentes usam um envelope único. O codinome temático nunca substitui os IDs técnicos nem os
schemas. O exemplo abaixo é ilustrativo.
message_id: msg_01H...
run_id: run_01H...
project_id: prj_...
tenant_id: tnt_...
source_agent: CORE-01
destination_agent: CORE-02
capability_required: routing.resolve
schema_version: 2.1.0
idempotency_key: sha256:...
priority: normal
deadline: 2026-06-15T18:00:00-03:00
data_classification: internal
policy_decision: allow
artifact_refs: [artifact://...]
qa_status: pending
trace_id: 4bf92f...
signature: ed25519:...
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 018 =====
VÉRTICE-OS | PRD de arquitetura interna temática
11. Memória, artefatos e proveniência
O VIBRANIUM VAULT administra cinco classes de memória e um repositório de artefatos. Nenhum agente
grava memória de longo prazo diretamente sem política de escrita.
Classe Conteúdo Regra
Working Estado temporário do run TTL curto
Episódica Histórico de execuções Versionada
Semântica Fatos e conhecimento Com confiança
Procedural Workflows e Method Packs Testada
Institucional Regras e padrões do domínio Aprovada
Governança Aprovações e exceções Imutável
Manifest de artefato
Todo entregável contém artifact_id, hash, producer_agent, run_id, fontes, modelo, prompt_version,
method_pack_version, QA, classificação de dados, aprovador e timestamps.
12. Segurança e limites de autonomia
 Nenhum agente possui credencial permanente de produção.
 Toda ferramenta é allowlisted e vinculada a uma capability específica.
 Ações irreversíveis exigem SIEGE PERILOUS.
 Conteúdo externo passa por sanitização e, quando necessário, NEGATIVE ZONE.
 Memória produtiva e corpus adversarial permanecem isolados.
 O Runtime aplica limites de custo, duração, tentativas e paralelismo.
 O ULTIMATE NULLIFIER pode revogar credenciais e congelar filas.
 Logs recebem redaction de dados sensíveis e preservam evidência auditável.
13. QA, EvalOps e gates
Cada artefato passa por gates independentes. Um score agregado não pode ocultar falha crítica em
segurança, factualidade ou política.
Gate Valida
Formato Schema e arquivos
Técnico Testes e performance
Factual Evidência e fontes
Segurança Ameaças e permissões
Política Consentimento e uso
Cross-squad Coerência entre outputs
Humano Aceitação ou aprovação
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 019 =====
VÉRTICE-OS | PRD de arquitetura interna temática
14. Organização do repositório
/vertice-os/
control-plane/
infinity-gauntlet/
nexus/
agents/
core/mind-stone/
core/tesseract/
core/time-stone/
core/aether/
core/power-orb/
core/soul-stone/
ops/vibranium-vault/
ops/adamantium-seal/
ops/bifrost-bridge/
security/negative-zone/
qa/book-of-vishanti/
meta/cosmic-cube-forge/
contracts/
policies/
evals/
artifacts/
runbooks/
docs/
15. Manifest mínimo de um agente
id: CORE-01
codename: PEDRA_DA_MENTE
function: planner_cognitivo
version: 2.1.0
inputs: [user_request, project_context, policy_context]
outputs: [requirements, ambiguity_score, execution_plan]
allowed_tools: [llm_reasoner, method_pack_registry]
forbidden_tools: [external_write, payment, deployment]
memory_read: [working, institutional]
memory_write: [working]
quality_gates: [requirements_coverage, ambiguity, policy_alignment]
escalation: [CORE-06, QA-01]
owner: platform-architecture
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 020 =====
VÉRTICE-OS | PRD de arquitetura interna temática
16. Critérios de aceite da nova arquitetura
ID Critério
O nome principal permanece VÉRTICE-OS em todas as interfaces
AC-01
e documentos.
Nenhum agente utiliza nome, imagem, fala ou identidade de
AC-02
personagem.
Todos os agentes possuem ID técnico, codinome, papel e
AC-03
manifesto versionado.
AC-04 Todos os handoffs são validados pelo ADAMANTIUM SEAL.
A PEDRA DO TEMPO retoma uma execução após falha sem
AC-05
duplicar side effects.
A PEDRA DA ALMA bloqueia ação sensível sem consentimento ou
AC-06
aprovação.
NEGATIVE ZONE contém prompt injection ou artefato suspeito
AC-07
sem propagação.
BOOK OF VISHANTI consegue reconstruir a fonte de cada claim
AC-08
factual.
M'KRAAN CRYSTAL reconstrói a execução completa a partir do
AC-09
trace_id.
COSMIC CUBE FORGE não publica agente sem testes,
AC-10
benchmark e aprovação humana.
ULTIMATE NULLIFIER encerra runs e revoga credenciais dentro
AC-11
do SLA crítico.
A temática pode ser removida sem quebrar APIs, porque os IDs
AC-12
técnicos são estáveis.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 021 =====
VÉRTICE-OS | PRD de arquitetura interna temática
17. Roadmap de implementação
Fase Agentes Resultado
F0 Manopla, Mente, Tesseract, Tempo Kernel funcional
F1 Adamantium, Bifrost, Vibranium Contratos e memória
F2 Alma, Norn, Siege Perilous Governança e HITL
F3 Negative Zone, Quantum Realm, Nullifier Segurança operacional
F4 Vishanti, M'Kraan, EvalOps Evidência e observabilidade
F5 Aether, Power Orb, Quantum Bands Artefatos e otimização
F6 Cosmic Cube Forge, Darkhold Chamber Meta-fábrica segura
18. Matriz de substituição da nomenclatura anterior
Papel anterior Novo codinome
Orquestrador Central MANOPLA DO INFINITO
Planner Cognitivo PEDRA DA MENTE
Capability Registry / Router TESSERACT
Durable Runtime PEDRA DO TEMPO
Artifact Composer AETHER
Budget / Model Router ORBE DO PODER
Governance / HITL PEDRA DA ALMA
Memory / Artifact Store VIBRANIUM VAULT
Contract Validator ADAMANTIUM SEAL
Event Bus BIFROST BRIDGE
Sandbox QUANTUM REALM
Quarantine NEGATIVE ZONE
Evidence QA BOOK OF VISHANTI
Observability M'KRAAN CRYSTAL
Meta-Squad Builder COSMIC CUBE FORGE
19. Decisão de produto
A identidade principal VÉRTICE-OS permanece inalterada. A nova linguagem temática é aplicada somente
à arquitetura interna e aos seus agentes. O sistema continua tecnicamente neutro, pois contratos, APIs e
integrações dependem de IDs imutáveis. Assim, a temática aumenta memorabilidade e coesão sem
comprometer governança, segurança ou possibilidade de rebranding futuro.
Resultado esperado
Um ecossistema de agentes reconhecível, coerente e avançado, no qual cada artefato tem uma função técnica
inequívoca e nenhum personagem é usado como agente, persona ou referência comportamental.
VÉRTICE-OS - uso interno - 15/06/2026

===== PAGE 022 =====
VÉRTICE-OS | PRD de arquitetura interna temática
20. Glossário
Agente: Componente autônomo limitado por contrato, ferramentas, memória e política.
Codinome: Nome temático exibido para humanos; não substitui o ID técnico.
Artifact: Entregável ou registro versionado com hash e proveniência.
Handoff: Mensagem tipada entre agentes, validada pelo ADAMANTIUM SEAL.
Run: Execução rastreável de uma ordem no VÉRTICE-OS.
Method Pack: Pacote versionado de método, exemplos, limitações e avaliações.
HITL: Intervenção humana em esclarecimento, aprovação ou exceção.
Quarentena: Isolamento de item suspeito na NEGATIVE ZONE.
VÉRTICE-OS - uso interno - 15/06/2026