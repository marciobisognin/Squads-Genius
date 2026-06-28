# A Disciplina FORJA — framework autoral

Metodologia de Marcio Bisognin que governa **como** um squad autônomo é forjado e
operado. Quatro componentes: cinco **estratos**, o **Anel** de sete atos, sete
**leis invariantes** e seis **patologias** com seus controles.

## Os cinco estratos
| Estrato | Étimo | O que é |
|---|---|---|
| **TÉLOS** | τέλος | Intenção normalizada em critérios verificáveis |
| **LÓGOS** | λόγος | Estrutura racional: requisitos, grafo, contratos SACP |
| **ÓRGANON** | ὄργανον | Aparato de execução: agentes, ferramentas, permissões |
| **KÝKLOS** | κύκλος | O sistema externo que agenda, executa, refuta, julga |
| **MNÉMĒ** | μνήμη | A memória evolutiva que faz cada ciclo melhorar o próximo |

> **Lei dos Cinco Estratos:** agente sem ciclo (`KÝKLOS`) é ferramenta, não
> squad. Todo squad de próxima geração entrega ao menos um `KÝKLOS` auditável
> (mesmo L1) e um gancho de `MNÉMĒ`.

## As sete leis invariantes
1. **Fronteira Determinística** — o LLM só emite JSON; todo cálculo é Python (`Decimal`).
2. **Contrato** — todo handoff é um contrato SACP tipado (`extra=forbid`).
3. **Portão de Cynefin** — classificar antes de agir; caos nunca roda autônomo.
4. **Mínimo Suficiente** — agente novo só por responsabilidade exclusiva.
5. **Élenchos** — nada é "pronto" sem evidência verificável.
6. **Crise Independente** — revisão fria, separada do executor.
7. **Anámnēsis** — todo ciclo deixa ≥1 aprendizado ou descarte explícito.

## As seis patologias e seus controles
| Patologia | Definição | Controle invariante |
|---|---|---|
| **PSEUDO-TÉLOS** | Declarar pronto sem evidência | Gate de evidência obrigatório |
| **OPACIDADE PROGRESSIVA** | Artefatos funcionam sem que se entenda | Resumo humano + ADR + diff |
| **DISPÊNDIO DESGOVERNADO** | Custo escala sem governo | Orçamento + parada após 2 falhas iguais |
| **ABDICAÇÃO** | O humano abandona o juízo | Gates HITL + L3 só allowlisted |
| **METÁSTASE DE AGENTES** | Proliferação redundante | Responsabilidade exclusiva |
| **DERIVA DE CONTRATO** | Handoffs degradam ao longo do Anel | Schema SACP + `extra=forbid` |

## O Portão de Cynefin
| Domínio | Roteamento |
|---|---|
| **Clear** | Determinístico; L3 em rotina allowlisted; pesquisa mínima |
| **Complicated** | Pesquisa + arquitetura; L2; multiagente sob demanda |
| **Complex** | Spikes isolados + ciclos curtos; L1; refutação reforçada |
| **Chaotic** | Estabilizar primeiro; L1 estrito; sem automação |

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
