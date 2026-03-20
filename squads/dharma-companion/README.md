# Dharma Companion

> Sistema contemplativo Zen-budista de transformação pessoal — zazen, preceitos éticos, auto-observação e compaixão em ação.

## Instalação

```bash
npx squads add dharma-companion
```

## O que Faz

O Dharma Companion é um **squad de assistência contemplativa** que guia o praticante na implementação de um framework de prática Zen-budista estruturado em 6 eixos:

- **Zazen** — meditação sentada como prática nuclear
- **Preceitos Mahayana** — moldura ética para a vida cotidiana
- **Auto-observação** — identificação de gatilhos emocionais ("botões")
- **Ciclo diário** — 6 passos integrados de prática
- **Caminho contemplativo** — 5 estágios de transformação
- **Compaixão ativa** — conversão de insights em ações concretas

Da inquietação inicial à devolução ao mundo, o squad acompanha cada passo com instrução precisa, reflexão ética e ternura.

## Pipeline — Ciclo Diário de 6 Passos

| Passo | Agente | Ação | Tempo Mín. |
|-------|--------|------|------------|
| 1 | 🧘 ZazenGuide | Assentar-se — sessão de zazen | 5 min |
| 2 | 🧭 PathNavigator | Lembrar-se — impermanência e interdependência | 1 min |
| 3 | ⚖️ PreceptKeeper | Escolher — 1-2 preceitos para o dia | 2 min |
| 4 | 🪞 MirrorObserver | Observar — notar os "botões" ao longo do dia | contínuo |
| 5 | 🔄 PracticeWeaver | Arrepender-se — ritual de arrependimento e recomeço | 1 min |
| 6 | 💚 CompassionCatalyst | Servir — ação concreta de cuidado e ternura | contínuo |

## Agentes

| Icon | Nome | Archetype | Responsabilidade |
|------|------|-----------|------------------|
| 🧘 | ZazenGuide | Guardian | Instrução de zazen: postura, respiração, progressão |
| ⚖️ | PreceptKeeper | Guardian | Aplicação dos 10 Preceitos Mahayana |
| 🪞 | MirrorObserver | Balancer | Auto-observação emocional, mapa de "botões" |
| 🔄 | PracticeWeaver | Flow_Master | Orquestração do ciclo diário de 6 passos |
| 🧭 | PathNavigator | Flow_Master | Navegação nos 5 estágios do caminho |
| 💚 | CompassionCatalyst | Builder | Conversão de insights em ações de compaixão |

## Tasks

| Task | Responsável | Atomic Layer |
|------|-------------|-------------|
| `guideMeditation()` | ZazenGuide | Organism |
| `applyPrecepts()` | PreceptKeeper | Organism |
| `observeEmotions()` | MirrorObserver | Organism |
| `orchestrateDailyCycle()` | PracticeWeaver | Organism |
| `assessStage()` | PathNavigator | Molecule |
| `activateCompassion()` | CompassionCatalyst | Molecule |
| `performRepentance()` | PracticeWeaver | Atom |
| `trackProgress()` | PathNavigator | Molecule |

## Workflows

### daily_practice_cycle
Ciclo diário coordenado pelo PracticeWeaver — da meditação matinal ao serviço vespertino.
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [Arrependimento] → [CompassionCatalyst]
```

### contemplative_path_progression
Pipeline de progressão nos 5 estágios contemplativos — da busca inicial à devolução ao mundo.
```
[PathNavigator] → avalia estágio → ajusta profundidade → [Todos os agentes adaptam]
```

## Os 5 Estágios do Caminho

| # | Estágio | Descrição |
|---|---------|-----------|
| 1 | 🌊 Inquietação e Busca | Vazio, perguntas existenciais, busca dispersa |
| 2 | 🌱 Encontro com a Prática | Contato com zazen, primeiros retiros, transformação |
| 3 | 🔥 Ruptura e Dedicação | Compromisso, mudanças de vida, treino intenso |
| 4 | 🏔️ Aprofundamento | Integração prática-vida, "misticismo realista" |
| 5 | 🌍 Devolução ao Mundo | Ensinar, compartilhar, compaixão em larga escala |

## Configuração

- `config/coding-standards.md` — Convenções de código e tom
- `config/tech-stack.md` — Tecnologias e tradição
- `config/source-tree.md` — Estrutura de diretórios

## Uso

### Ciclo diário completo
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### Agentes individuais
```
/dc:zazen-guide             — Sessão de zazen
/dc:precept-keeper           — Preceitos do dia
/dc:mirror-observer          — Observação emocional
/dc:path-navigator           — Avaliação de estágio
/dc:compassion-catalyst      — Ação compassiva
/dc:practice-weaver          — Ciclo diário completo
```

## Autor

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## Licença

MIT
