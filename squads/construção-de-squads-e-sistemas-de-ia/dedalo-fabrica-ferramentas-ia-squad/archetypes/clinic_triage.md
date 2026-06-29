# Arquétipo D — Triagem Clínica (`clinic_triage`)

> Família D · Operacional de nicho (saúde). **Setor regulado: humano no loop obrigatório.**

## Dor canônica
Triagem, histórico e protocolos manuais; tempo de atendimento e risco de omissão altos.

## Dados necessários
- Histórico do paciente, protocolos clínicos, agenda, sintomas relatados.

## Agentes sugeridos
- Coletor de sintomas (formulário), estruturador (LLM-JSON), protocolo (regras Python), profissional humano (gate).

## Integrações
- Prontuário eletrônico, agenda, mensageria — sempre com consentimento.

## Esqueleto de MVP
- Pré-triagem estruturada + sugestão de protocolo + encaminhamento ao profissional.

## Riscos
- Dados sensíveis de saúde (LGPD reforçada); decisão clínica jamais automatizada.

## Gate obrigatório
- NÓMOS exige `human_in_loop_required=true`; saída é apoio, nunca diagnóstico final.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
