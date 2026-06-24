# Lumen Verbi — Squad Bíblico de IA

> Squad multiagente que personifica figuras bíblicas e historiadores especializados
> para explicar a Palavra de Deus com perspectiva teológica e contexto histórico-cultural.

Um orquestrador (**MSCA**) analisa a consulta em linguagem natural, seleciona e
combina os agentes mais relevantes a partir de uma **Base de Dados de Conhecimento
(BDC)** e compõe uma resposta coesa — sempre sob **guardrails teológicos**.

> ⚠️ **Aviso.** As personas são representações **didáticas de IA**, não a voz real
> das figuras sagradas nem revelação. A ferramenta é educativa e não substitui
> aconselhamento pastoral, doutrinário ou acadêmico.

## Visão geral

- **13 agentes:** 1 orquestrador (MSCA), 1 curador da BDC, 1 guardião teológico,
  7 personas bíblicas e 3 historiadores.
- **10 tasks** e **3 workflows** cobrindo o fluxo de interação do PRD.
- **4 scripts determinísticos** + **3 arquivos de dados** (BDC versionada).
- Origem: PRDs `prd_squad_biblico.md` e `prd_squad_biblico_arquitetura.md`.

## Agentes

### Núcleo
| Agente | Papel |
|--------|-------|
| `mestre-escriba-orquestrador` | MSCA: PLN, seleção/combinação e composição. |
| `curador-bdc` | Recupera contexto da BDC (RAG) e cita fontes. |
| `guardiao-teologico` | Quality gate de fidelidade e guardrails. |

### Personas bíblicas
| Agente | Testamento | Foco |
|--------|-----------|------|
| `persona-jesus` | Novo | Evangelhos, Reino de Deus, amor, graça |
| `persona-moises` | Antigo | Êxodo, Lei Mosaica, aliança |
| `persona-paulo` | Novo | Epístolas, graça, fé, justificação |
| `persona-davi` | Antigo | Salmos, adoração, arrependimento |
| `persona-maria` | Novo | Anunciação, Magnificat, encarnação |
| `persona-pedro` | Novo | Atos, negação e restauração, esperança |
| `persona-salomao` | Antigo | Provérbios, Eclesiastes, sabedoria |

### Historiadores
| Agente | Especialização |
|--------|----------------|
| `historiador-antigo-testamento` | Antigo Oriente Próximo, arqueologia bíblica |
| `historiador-novo-testamento` | Segundo Templo, mundo greco-romano |
| `critico-textual` | Manuscritos, variantes, línguas originais, cânon |

## Fluxo (MSCA)

`intake → PLN/intenção → recuperação BDC → seleção/combinação → resposta da
persona → contexto histórico (condicional) → composição → guardrails (gate) →
refinamento → registro`. Detalhes em [`docs/arquitetura_msca.md`](docs/arquitetura_msca.md).

## Scripts determinísticos

Python 3.11+, sem dependências externas para execução (PyYAML só para o validador do construtor).

```bash
# Selecionar/combinar agentes a partir de uma consulta
python3 scripts/selecionar_agentes.py --consulta "Qual o significado do Sermão da Montanha?"

# Extrair referências bíblicas estruturadas
python3 scripts/parse_referencia_biblica.py --texto "Explique Mateus 5:1-12 e João 3:16"

# Montar o prompt de sistema de uma persona (com guardrails)
python3 scripts/montar_prompt_persona.py --agente persona-paulo --consulta "Fale sobre a graça"

# Validar guardrails de uma resposta (quality gate)
python3 scripts/validar_fidelidade.py --arquivo examples/exemplo_resposta_combinada.md
```

### Testes

```bash
python3 -m pytest -q          # a partir da raiz do squad
```

## Base de Dados de Conhecimento (BDC)

Metadados versionados em `scripts/data/` (perfis, mapa semântico, índice de
livros). Textos bíblicos integrais **não** são versionados — a BDC referencia
fontes de domínio público / APIs externas. Ver
[`docs/base_de_conhecimento_bdc.md`](docs/base_de_conhecimento_bdc.md).

## Guardrails

Representação didática, sem citações inventadas, separação de camadas (texto ×
história × interpretação), neutralidade denominacional. Ver
[`docs/guardrails_teologicos.md`](docs/guardrails_teologicos.md).

## Como ativar em uma sessão

1. Leia `squad.yaml` e assuma a persona do `mestre-escriba-orquestrador`.
2. Siga o workflow `full_biblical_consultation_pipeline` (ou `quick_single_persona` /
   `historical_context_deep_dive`).
3. Antes de exibir qualquer resposta, passe pelo gate do `guardiao-teologico`.

## Estrutura

```
lumen-verbi-squad-biblico/
├── squad.yaml
├── agents/            # 13 agentes
├── tasks/             # 10 tasks
├── workflows/         # 3 workflows
├── scripts/           # 4 scripts + data/ (BDC)
├── docs/              # arquitetura, BDC, guardrails
├── examples/          # consultas, seleção e resposta de exemplo
└── tests/             # testes dos scripts
```

## Roadmap (do PRD)

- Integração com banco vetorial + RAG sobre textos completos.
- UI com exibição por agente, histórico e opções de refinamento.
- Métricas: taxa de resposta relevante, tempo médio, engajamento, satisfação.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
