# Metodologia

## Princípio de desenho
Os agentes assistem; a decisão e o lançamento oficial seguem humanos. Todo
artefato gerado é rascunho até passar pelo Gate Humano (HG).

## Separação de camadas
1. **Orquestração** (A0) — classifica e roteia, nunca decide mérito.
2. **Núcleo pedagógico** (A1–A5) — produz e valida conteúdo contra o PPC/RDP.
3. **Conformidade & governança** (A6, A7, HG) — consolida, monitora prazos e
   homologa.

## Regra de fonte
Toda afirmação normativa (PPC, RDP, resoluções) deve vir com citação de fonte
recuperável. Na ausência de fonte, o agente responde "inconclusivo" — nunca
inventa um dispositivo normativo.

## Fronteira de dados (LGPD)
- **Público**: PPC, RDP, ementas, resoluções, calendário acadêmico — usado
  desde a Fase 0 do roadmap.
- **Sensível**: frequência, notas, perfil de necessidade educacional
  específica — só circula em ambiente controlado, a partir da Fase 3, e nunca
  é enviado a modelo externo sem autorização.

## Handoff entre agentes
Todo handoff é um payload JSON validado pelo schema `sacp_handoff.schema.json`,
com `agente_origem`, `agente_destino`, `contexto` e `confidence`. Isso permite
auditar a trilha de decisão e religar o pipeline (LangGraph ou equivalente)
sem acoplamento direto entre agentes.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
