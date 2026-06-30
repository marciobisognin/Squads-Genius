# Squads Gateway — Catálogo Vivo e Roteador

**Versão:** 0.1.0 (Fase 1 completa)  
**Status:** Operational Prototype  
**Licença:** MIT  
**Criado por:** Marcio Bisognin

---

## 📋 O que é?

O **Squads Gateway** é um sistema de descoberta, roteamento e execução de squads que transforma o Squads-Genius de uma coleção de 86 squads em um catálogo **consultável, roteável e auditável**.

```
┌─────────────────────────────────────────────────────────────┐
│  Intake JSON → StateGraph Router → Index JSON/SQLite → Rank │
│       ↓              ↓                    ↓                  │
│   Gate HITL      Handoff Contract      Audit Log JSONL      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Fase 1: Índice Canônico (✅ Concluída)

### O que faz

- **Indexação determinística**: varre `squads/` e `IFFar-Squads/`, extrai metadados de cada `squad.yaml`
- **Sem dependências externas**: usa apenas stdlib Python 3.11+
- **Validação de integridade**: detecta links quebrados, valida estrutura
- **Auditoria completa**: relatório JSON com cobertura, domínios, status, gaps

### Resultados (snapshot atual)

| Métrica | Valor | Status |
|---------|-------|--------|
| **Squads indexados** | 86 | ✅ 100% |
| **Com agentes** | 71 | ✅ 83% |
| **Com tarefas** | 63 | ✅ 73% |
| **Com workflows** | 71 | ✅ 83% |
| **Links quebrados** | 0 | ✅ Clean |
| **Tempo indexação** | ~1s | ✅ < 10s |

### Saídas geradas

```
squads_index.json       # Índice estruturado (250 KB)
gateway_audit.json      # Relatório de auditoria
```

---

## 🔍 Fase 2: Busca e Roteamento (Em implementação)

### Comandos CLI

```bash
# Indexar todos os squads
python3 -m tools.squads_gateway index \
  --repo . \
  --output squads_index.json

# Buscar por termo
python3 -m tools.squads_gateway search \
  --index squads_index.json \
  --term "conteúdo" \
  --top 5

# Rotear tarefa ao melhor squad
python3 -m tools.squads_gateway route \
  --index squads_index.json \
  --task "Preciso criar conteúdo para instagram" \
  --top 3 \
  --threshold 2.0
```

### Scoring determinístico

- **Base**: overlap de palavras-chave entre tarefa e squad/agentes
- **Pesos**: agente (2.0x) > squad keywords (1.0x)
- **Deduplicação**: mantém melhor score por squad
- **GAP analysis**: sinaliza quando nenhum squad atinge limiar

Exemplo de saída:

```json
{
  "task": "Preciso criar conteúdo para instagram",
  "recommendations": [
    {
      "score": 2.0,
      "squad": "VetorNexo",
      "path": "squads/conteúdo-marketing-e-visual/vetornexo-premium-squad",
      "agent": "ocr-semantics",
      "evidence": "Match: conteúdo",
      "matched_keywords": ["conteúdo"]
    }
  ]
}
```

---

## 📦 Fase 3: Handoff e Auditoria (Roadmap)

- **Contratos Pydantic v2**: definições estruturadas com `extra="forbid"`
- **Ativação**: CLI gera prompt e checklist para iniciar squad
- **Logs JSONL**: rastreamento completo de decisões com hash
- **Memória de decisão**: feedback (sucesso/falha) ajusta pesos

---

## 🏗️ Arquitetura

```
tools/squads_gateway/
├─ __init__.py                    # Entry point
├─ __main__.py                    # CLI entry (python3 -m)
├─ schemas.py                     # Contratos (dataclasses)
├─ indexer.py                     # Varredura e catalogação
├─ ranker.py                      # Scoring determinístico
├─ cli.py                         # Comandos (index, search, route)
├─ tests/
│  ├─ test_indexing.py           # Testes de indexação
│  ├─ test_ranking.py            # Testes de ranking
│  └─ test_fixtures.py           # (próximo)
└─ README.md                      # Este arquivo
```

### Componentes (Fase 1-3)

| Componente | Status | Descrição |
|------------|--------|-----------|
| **indexer** | ✅ Completo | Varre squad.yaml, extrai metadados, valida |
| **ranker** | ✅ Completo | Scoring léxico determinístico |
| **router** | 🔄 Em progresso | LangGraph StateGraph (Fase 3) |
| **contract_builder** | 📋 Roadmap | Gera contratos de ativação |
| **audit_logger** | 📋 Roadmap | Log JSONL com trilha auditável |
| **memory_store** | 📋 Roadmap | Ajusta pesos com feedback |
| **cli** | ✅ Funcional | index, search, route operacionais |

---

## 🧪 Testes

### Executar testes de indexação

```bash
python3 tools/squads_gateway/tests/test_indexing.py
```

Testes incluem:
- ✅ Tokenização e extração de palavras-chave
- ✅ Carregamento de squad.yaml e JSON
- ✅ Indexação de squad único
- ✅ Criação de índice completo
- ✅ Exclusão de padrões (backup, media, etc)

### Executar testes de ranking

```bash
python3 tools/squads_gateway/tests/test_ranking.py
```

Testes incluem:
- ✅ Roteamento com squad simples
- ✅ Squads sem agentes específicos
- ✅ Queries vazias/sem match
- ✅ Deduplicação de squads

---

## 📊 Métricas de Sucesso (PRD)

| KPI | Alvo | Status |
|-----|------|--------|
| Squads indexados | 100% | ✅ 86/86 (100%) |
| Links quebrados | 0 | ✅ 0 detectados |
| Top-3 accuracy | ≥90% | 🔄 Em validação |
| Tempo indexação | < 10s | ✅ ~1s |
| Trilha auditável | Sim | 🔄 Fase 3 |

---

## 🔧 Dependências

**Fase 1-2**: Nenhuma (stdlib Python 3.11+)  
**Fase 3**: Pydantic v2 (opcional, com fallback dataclasses)

```bash
# Mínimo:
python3 --version  # >= 3.11
```

---

## 📝 Próximos passos

### Curto prazo (1-2 semanas)

- [ ] 30 fixtures de roteamento baseadas em SQUAD_INDEX.md
- [ ] Validar Top-3 accuracy ≥90%
- [ ] LangGraph StateGraph para orquestração
- [ ] Contratos de ativação (prompt + checklist)

### Médio prazo (Fase 3)

- [ ] Audit log JSONL com rastreabilidade completa
- [ ] Gate HITL para ações críticas
- [ ] Memory system com feedback (sucesso/falha)
- [ ] Integração com site (docs/)

---

## 🤝 Como usar nos principais LLMs de codificação

### Claude Code / Claude.ai

```
Ativar squad via CLI:
  cd /home/user/Squads-Genius
  python3 -m tools.squads_gateway route --index squads_index.json \
    --task "minha demanda aqui"

Ou importar como módulo:
  from tools.squads_gateway import IndexEntry
  from tools.squads_gateway.indexer import create_index
  index = create_index(Path("."))
```

### GitHub Copilot / Cursor / Windsurf

Use como ferramenta shell no seu projeto:

```bash
./tools/squads_gateway/cli.py route --task "..."
```

---

## 📄 Licença & Créditos

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.

---

**Última atualização:** 2026-06-29  
**Versão:** 0.1.0-phase-1
