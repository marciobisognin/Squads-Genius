# Conformidade de Squads — Checklist e Remediação

## Requisitos de Conformidade

Cada squad **DEVE** passar no checklist de **6 pontos**:

| # | Requisito | Descrição | Verificação |
|---|-----------|-----------|-------------|
| 1 | `squad.yaml` | Manifesto principal do squad (YAML format) | `ls squads/<nome>/squad.yaml` |
| 2 | `README.md` | Documentação do squad | `ls squads/<nome>/README.md` |
| 3 | `LICENSE` | Licença MIT (cópia from root) | `ls squads/<nome>/LICENSE` |
| 4 | `agents/` | Diretório de agentes (com `.md` files) | `ls -d squads/<nome>/agents/` |
| 5 | `tasks/` | Diretório de tarefas (com `.yaml` files) | `ls -d squads/<nome>/tasks/` |
| 6 | `workflows/` | Diretório de workflows (com `.yaml` files) | `ls -d squads/<nome>/workflows/` |

**Status atual:** ✅ **87/87 squads conformes (100%)**

---

## Checklist Antes de Fazer Push

Quando você criar um novo squad ou fizer mudanças, rode **localmente**:

```bash
# Verificar conformidade
./scripts/verify-squad-compliance.sh

# Regenerar índice de squads
python3 scripts/regenerate-squad-index.py

# Verificar formato YAML
python3 scripts/normalize-squad-yaml.py
```

Se tudo passar, faça commit e push. O GitHub Actions vai rodar validações automáticas.

---

## Estrutura Mínima de um Squad

```
squads/categoria/meu-squad/
├── squad.yaml              ← Manifesto (YAML)
├── README.md               ← Documentação
├── LICENSE                 ← MIT (cópia from root)
├── agents/                 ← Agentes (.md files)
│   ├── .gitkeep
│   └── meu-agente.md
├── tasks/                  ← Tarefas (.yaml files)
│   ├── .gitkeep
│   └── minha-task.yaml
├── workflows/              ← Workflows (.yaml files)
│   ├── .gitkeep
│   └── meu-workflow.yaml
├── scripts/                ← Scripts (optional)
│   └── script.py
└── examples/               ← Exemplos (optional)
    └── example.md
```

---

## squad.yaml — Campos Obrigatórios

```yaml
name: meu-squad                    # ID técnico (kebab-case)
commercial_name: "Meu Squad"       # Nome para exibição
version: "0.1.0"                   # Semver (X.Y.Z)
language: "pt-BR"                  # Idioma
license: "MIT"                     # Licença
creator: "Seu Nome"                # Criador
positioning: "..."                 # Descrição (1-2 frases)

agents:
  - id: agente-1
    file: "agents/agente-1.md"
    role: "Descrição da função"

tasks:
  - id: tarefa-1
    file: "tasks/tarefa-1.yaml"
    owner: "agente-1"
    objective: "O que faz"

workflows:
  - id: workflow-1
    file: "workflows/workflow-1.yaml"
```

---

## CI/CD — Validação Automática

### GitHub Actions Workflow

Arquivo: `.github/workflows/squad-conformance-check.yml`

**Acionada quando:**
- Push em `squads/` ou `IFFar-Squads/squads/`
- Pull Request afetando squads

**Verifica:**
- ✅ Conformidade 6/6 (LICENSE, README, diretórios)
- ✅ Formato YAML válido
- ✅ Campos obrigatórios em squad.yaml
- ✅ Ausência de secrets/credenciais
- ✅ Versionamento semver

**Se falhar:**
- Build falha (❌ red)
- Mensagem de erro específica
- Instruções de remediação

---

## Remediação Automática (Local)

Se seu squad falhar, rode os scripts de remediação:

### 1. Adicionar LICENSE que falta

```bash
python3 scripts/fix-squad-licenses.py
```

### 2. Criar diretórios faltando

```bash
python3 scripts/fix-squad-structure.py
```

### 3. Converter JSON → YAML

```bash
python3 scripts/normalize-squad-yaml.py
```

### 4. Verificar e visualizar status

```bash
./scripts/verify-squad-compliance.sh
```

---

## Índices & Documentação

### SQUAD_INDEX.md

Regenerado automaticamente com status de conformidade:
- ✅ Indica conformidade completa (6/6)
- ⚠️ Indica conformidade parcial (4-5/6)
- ❌ Indica não conforme (<4/6)

Para atualizar manualmente:
```bash
python3 scripts/regenerate-squad-index.py
```

### README.md

Mostra métricas agregadas:
- Total de squads
- % de conformidade
- Badges de status

---

## FAQ — Perguntas Frequentes

### P: Posso ter um squad sem agentes/tasks/workflows?
**R:** Não. Todos os 6 requisitos são obrigatórios. Se ainda não tem conteúdo, crie os diretórios com `.gitkeep` e README descrevendo o plano.

### P: Qual é o formato correto para squad.yaml?
**R:** **YAML** (não JSON). Use [YAML indentation rules](https://yaml.org/spec/1.2/spec.html). Scripts automáticos convertem JSON → YAML.

### P: Versão deve ser X.Y.Z?
**R:** Sim, [semantic versioning](https://semver.org/). Exemplo: `1.0.0`, `0.2.1`. Não use "não informada" — será convertido para `0.1.0` (draft).

### P: Como adiciono meu squad ao índice?
**R:** Automático! Toda vez que você faz commit com um novo `squad.yaml`, o índice é regenerado.

### P: E se um squad quebrar o CI/CD?
**R:** Corrija localmente com os scripts de remediação, faça novo commit, push novamente. O CI/CD vai rodar de novo.

---

## Referência de Scripts

| Script | Função | Quando Usar |
|--------|--------|-----------|
| `fix-squad-licenses.py` | Adiciona LICENSE a squads | Antes de qualquer commit |
| `fix-squad-structure.py` | Cria diretórios faltando | Novo squad ou estrutura incompleta |
| `normalize-squad-yaml.py` | Converte JSON→YAML, harmoniza versões | Manutenção geral |
| `verify-squad-compliance.sh` | Verifica conformidade local | Antes de PR |
| `regenerate-squad-index.py` | Atualiza SQUAD_INDEX.md | Raramente (automático) |

---

## Contato & Suporte

- **Documentação:** [CLAUDE.md](CLAUDE.md) — integração Claude Code
- **Playbook:** [CLAUDE.md — Construtor de Squads](CLAUDE.md#playbook-completo-de-construção-e-publicação-de-squads)
- **GitHub Issues:** Reporte problemas de conformidade

**Última atualização:** 2026-06-30 | **Status:** 100% conforme (87/87 squads)
