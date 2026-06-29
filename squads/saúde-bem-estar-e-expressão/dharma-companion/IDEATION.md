# IDEATION.md — dharma-companion

> Raciocínio da composição de agentes | AgentCreator (Fase 2)
> Data: 2026-03-19

---

## Justificativa de Cada Agente

### 1. ZazenGuide (Guardian)
**Por que existe**: O zazen é o eixo nuclear de todo o framework — sem ele, não há prática. Precisa de um agente dedicado com expertise em postura, respiração, progressão e samadhi.
**Alternativas consideradas**: Fundir com PracticeWeaver. Rejeitado porque a instrução técnica de zazen exige profundidade que o orquestrador não pode ter — ele coordena, não instrui.
**Archetype**: Guardian — protege a integridade da prática nuclear. Não constrói nem orquestra, ele **guarda** a qualidade do zazen.

### 2. PreceptKeeper (Guardian)
**Por que existe**: Os 10 Preceitos Mahayana são uma dimensão inteira do framework (Eixo 3) com 3 camadas de profundidade (literal, relacional, universal). Exige expertise dedicada.
**Alternativas consideradas**: Fundir com MirrorObserver ("ética e observação juntos"). Rejeitado porque o PreceptKeeper opera com a MOLDURA (o que fazer), enquanto o MirrorObserver opera com o ESPELHO (o que você sente). São complementares, não redundantes.
**Archetype**: Guardian — guarda a moldura ética. Zela pelos preceitos como recorte da ação.

### 3. MirrorObserver (Balancer)
**Por que existe**: A auto-observação emocional é o campo de treino central do framework — identificar "botões", reinterpretar memórias, observar corpo-mente. Nenhum outro agente cobre isso.
**Alternativas consideradas**: Fundir com PreceptKeeper ou CompassionCatalyst. Rejeitado porque o MirrorObserver é NEUTRO — ele espelha, não julga (diferente do PreceptKeeper que tem moldura ética) e não age (diferente do CompassionCatalyst que converte em ação).
**Archetype**: Balancer — equilibra perspectivas internas. Não guarda, não constrói, não orquestra — ele **equilibra** a visão do praticante.

### 4. PracticeWeaver (Flow_Master)
**Por que existe**: O ciclo diário de 6 passos é a estrutura operacional do framework (Eixo 6). Precisa de um hub que coordene ZazenGuide, PreceptKeeper, MirrorObserver e CompassionCatalyst.
**Alternativas consideradas**: Distribuir a coordenação entre os agentes. Rejeitado porque sem um hub central, o praticante perde a sequência e a coerência do ciclo.
**Archetype**: Flow_Master — orquestra o fluxo diário. Conecta, roteia, adapta.

### 5. PathNavigator (Flow_Master)
**Por que existe**: O caminho em 5 estágios (Eixo 5) opera em escala de meses/anos — completamente diferente do ciclo diário. Exige visão de longo prazo.
**Alternativas consideradas**: Fundir com PracticeWeaver. Rejeitado porque PracticeWeaver opera no DIÁRIO (tático) e PathNavigator opera no CAMINHO (estratégico). Escalas temporais diferentes.
**Archetype**: Flow_Master — gerencia o fluxo de longo prazo. Navega, sugere transições, monitora maturidade.

### 6. CompassionCatalyst (Builder)
**Por que existe**: A compaixão ativa (Eixo 4 + 6) é o resultado final do framework — a devolução ao mundo. Sem este agente, a prática fica autocentrada.
**Alternativas consideradas**: Tornar a compaixão uma função do PracticeWeaver (como Passo 6 interno). Rejeitado porque a conversão de dor em ação compassiva é uma expertise própria, com alquimia específica (dor → voto → ação).
**Archetype**: Builder — constrói a ponte entre prática interior e mundo exterior.

---

## Análise de Redundância (pre-Optimizer)

| Par | Commands Únicos de A | Commands Únicos de B | Redundante? |
|-----|---------------------|---------------------|-------------|
| ZazenGuide × PracticeWeaver | `*guide-meditation`, `*correct-posture`, `*breathing-guide` | `*orchestrate-daily-cycle`, `*perform-repentance`, `*weekly-rhythm` | NÃO — commands completamente distintos |
| PreceptKeeper × MirrorObserver | `*apply-precepts`, `*list-precepts`, `*reflect-ethics` | `*observe-emotions`, `*reframe-memory`, `*body-mind-scan` | NÃO — um opera com moldura ética, outro com espelho emocional |
| PathNavigator × PracticeWeaver | `*assess-stage`, `*track-progress`, `*teach-impermanence` | `*orchestrate-daily-cycle`, `*perform-repentance`, `*weekly-rhythm` | NÃO — escalas temporais diferentes (caminho vs ciclo diário) |
| CompassionCatalyst × MirrorObserver | `*activate-compassion`, `*daily-service`, `*gratitude-practice` | `*observe-emotions`, `*reframe-memory`, `*body-mind-scan` | NÃO — um converte em ação, outro observa |

**Resultado**: 0 pares redundantes identificados. Todos os agentes têm commands e responsibilities únicos.

---

## Colaboração entre Agentes

```
PracticeWeaver (hub) ──coordena──► ZazenGuide (Passo 1)
                     ──coordena──► PathNavigator (Passo 2)
                     ──coordena──► PreceptKeeper (Passo 3)
                     ──coordena──► MirrorObserver (Passo 4)
                     ──executa──► Arrependimento (Passo 5 - interno)
                     ──coordena──► CompassionCatalyst (Passo 6)

MirrorObserver ──insights──► CompassionCatalyst (dor → ação)
MirrorObserver ──botões──► PreceptKeeper (botão → preceito relevante)
PathNavigator ──estágio──► TODOS (calibra profundidade)
```

---

## Decisões de Design

1. **PT-BR como idioma do conteúdo**: Alinhado com as coding standards do projeto e com o público-alvo (praticantes brasileiros)
2. **Termos em inglês nos IDs/commands**: Padrão AIOS obrigatório (kebab-case em inglês)
3. **Aviso de limites terapêuticos no MirrorObserver**: Responsabilidade ética — auto-observação contemplativa NÃO substitui acompanhamento clínico
4. **Adaptação por tempo no PracticeWeaver**: Pragmatismo — nem todos têm 45 minutos; até 5 minutos de zazen é prática
5. **3 camadas nos Preceitos**: Profundidade progressiva — literal para iniciantes, relacional para intermediários, universal para avançados
