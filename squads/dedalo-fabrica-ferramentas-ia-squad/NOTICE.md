# NOTICE

**DÉDALO — Fábrica de Ferramentas IA** (`dedalo-fabrica-ferramentas-ia-squad`) é um squad do
repositório Squads-Genius, gerado com o **Maeve Genius Forge** a partir do PRD
"Squad FÁBRICA DE FERRAMENTAS IA (DÉDALO) v3.0" fornecido pelo usuário.

## Natureza do squad
DÉDALO é uma **camada de transformação de conhecimento em software**: recebe vídeos, briefings,
dores ou processos e produz diagnóstico, PRD rastreável, arquitetura, backlog, protótipo e
`squad.yaml` agnóstico de plataforma. Não é um gerador de ideias soltas: é um mecanismo
auditável com determinismo, rastreabilidade e red-team obrigatório.

## Invariante central
Os **LLMs emitem exclusivamente JSON estruturado**. **Toda lógica determinística — scoring de
oportunidade, priorização impacto/esforço/risco, métricas, validação — roda em Python puro**,
jamais no LLM. Isso garante reprodutibilidade, auditabilidade e rastreabilidade
fonte → requisito → feature.

## Integridade probatória
Fontes inacessíveis/protegidas por login são **marcadas explicitamente** e **nunca inventadas**.
Evidência é sempre separada de hipótese, estimativa e recomendação.

## Marca e propriedade intelectual
Nenhuma marca, prompt, texto ou ativo proprietário de terceiros é copiado. Codinomes
greco-latinos são usados como vocabulário epistêmico próprio.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
