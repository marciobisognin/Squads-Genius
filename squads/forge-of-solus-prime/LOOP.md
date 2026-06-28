# LOOP.md — O Anel da Forja (estrato KÝKLOS)

O `KÝKLOS` não é um laço genérico; é um ciclo nomeado de **sete atos**, cada um
com entrada, saída e critério de passagem (gate).

```text
NÓESIS → BOULḖ → DIAÍRESIS → PRÂXIS → ÉLENCHOS → KRÍSIS → ANÁMNĒSIS
                                ↑__________________|
                       (self-healing: reparo guiado por diagnóstico,
                        retries limitados e escalonamento humano)
```

| Ato | Étimo | Função | Gate |
|---|---|---|---|
| 1. *NÓESIS* | νόησις | Compreender intenção e estado | Briefing normalizado + Cynefin |
| 2. *BOULḖ* | βουλή | Decidir estratégia/autonomia/topologia | Plano + nível L1/L2/L3 |
| 3. *DIAÍRESIS* | διαίρεσις | Decompor em 3–7 tarefas contratuais | Cada tarefa com contrato completo |
| 4. *PRÂXIS* | πρᾶξις | Executar a microtarefa permitida | Artefato + log + custo |
| 5. *ÉLENCHOS* | ἔλεγχος | Refutar "pronto" com evidência | Validação verde + evidência |
| 6. *KRÍSIS* | κρίσις | Julgar friamente, em sessão separada | Veredito do revisor independente |
| 7. *ANÁMNĒSIS* | ἀνάμνησις | Consolidar aprendizado | ≥1 aprendizado ou descarte |

## Escada de autonomia

| Nível | Nome | Permissões | Cynefin típico |
|---|---|---|---|
| **L1** | *Report-only* | Analisa, recomenda, rascunhos; não altera fonte de verdade | Complex / Chaotic |
| **L2** | *Assisted fixes* | Altera localmente, testa, propõe commit; humano aprova publicação | Complicated |
| **L3** | *Unattended bounded* | Executa rotinas allowlisted, com rollback e orçamento | Clear, escopo fechado |

**Padrão do produto: L1.** Subir de nível exige aprovação humana registrada no
`run_state.json`. *Chaotic* nunca passa de L1 — estabiliza-se o domínio primeiro.

## Self-healing e HITL
- Em *ÉLENCHOS*/*KRÍSIS*: diagnostica → propõe reparo (JSON) → aplica patch (Python) → re-executa o gate.
- Retries limitados (padrão: **2**). **Falha idêntica 2x consecutivas → escala para humano.**
- Gates HITL obrigatórios antes de: subir autonomia; incorporar ferramenta de risco médio/alto; qualquer ação destrutiva ou de publicação.

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
