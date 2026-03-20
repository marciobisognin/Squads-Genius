# Dharma Companion

> 禅宗佛教个人转化修行系统 — 坐禅 (zazen)、道德戒律、自我观察与践行慈悲。

## 安装 (Instalação)

```bash
npx squads add dharma-companion
```

## 功能介绍 (O que Faz)

Dharma Companion 是一个 **沉思辅助小队 (squad)**，指导修行者实践基于 6 个维度的禅宗修行框架：

- **Zazen** — 坐禅作为核心修行
- **大乘戒律 (Mahayana Precepts)** — 日常生活的道德准则
- **自我观察** — 识别情绪触发点 ("按钮")
- **日常循环** — 6 个综合的修行步骤
- **沉思之路** — 转化的 5 个阶段
- **积极慈悲** — 将内省转化为实际行动

从最初的烦躁不安到回馈世界，本小队在每一个步骤中提供精准指导、道德反思与温柔陪伴。

## Pipeline — 6步日常循环

| 步骤 | Agente | 行动 (Ação) | 最短时间 |
|------|--------|-----------|---------|
| 1 | 🧘 ZazenGuide | 安顿身心 — zazen 会话 | 5 分钟 |
| 2 | 🧭 PathNavigator | 忆念 — 无常与相互依存 | 1 分钟 |
| 3 | ⚖️ PreceptKeeper | 选择 — 每日 1-2 条戒律 | 2 分钟 |
| 4 | 🪞 MirrorObserver | 观察 — 留意全天的 "按钮" | 持续 |
| 5 | 🔄 PracticeWeaver | 忏悔 — 忏悔与重新开始的仪式 | 1 分钟 |
| 6 | 💚 CompassionCatalyst | 服务 — 关怀与温柔的具体行动 | 持续 |

## Agentes

| Icon | Nome | Archetype | 职责 (Responsabilidade) |
|------|------|-----------|------------------------|
| 🧘 | ZazenGuide | Guardian | zazen 指导：姿势、呼吸、进阶 |
| ⚖️ | PreceptKeeper | Guardian | 大乘十戒的应用 |
| 🪞 | MirrorObserver | Balancer | 情绪自我观察、"按钮" 映射 |
| 🔄 | PracticeWeaver | Flow_Master | 协调 6 步日常循环 |
| 🧭 | PathNavigator | Flow_Master | 引导修行的 5 个阶段 |
| 💚 | CompassionCatalyst | Builder | 将内省转化为慈悲行动 |

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
由 PracticeWeaver 协调的日常循环 — 从晨间冥想到晚间服务。
```
[ZazenGuide] → [PathNavigator] → [PreceptKeeper] → [MirrorObserver] → [忏悔] → [CompassionCatalyst]
```

### contemplative_path_progression
沉思之路 5 个阶段的进阶流程 — 从最初的寻觅到回馈世界。
```
[PathNavigator] → 评估阶段 → 调整深度 → [所有 agents 适配]
```

## 修行的 5 个阶段

| # | 阶段 (Estágio) | 描述 (Descrição) |
|---|--------------|----------------|
| 1 | 🌊 焦躁与寻觅 | 空虚、存在主义疑问、分散的寻找 |
| 2 | 🌱 与修行相遇 | 接触 zazen，初次闭关，转化 |
| 3 | 🔥 破局与奉献 | 承诺、生活改变、密集训练 |
| 4 | 🏔️ 深化 | 修行与生活的整合，"现实主义的神秘主义" |
| 5 | 🌍 回馈世界 | 教导、分享、大规模的慈悲 |

## 配置 (Configuração)

- `config/coding-standards.md` — 代码规范与基调
- `config/tech-stack.md` — 技术与传统
- `config/source-tree.md` — 目录结构

## 使用指南 (Uso)

### 完整的日常循环
```
/dc:practice-weaver
*orchestrate-daily-cycle --time-available=30
```

### 独立的 Agentes
```
/dc:zazen-guide             — zazen 会话
/dc:precept-keeper           — 每日戒律
/dc:mirror-observer          — 情绪观察
/dc:path-navigator           — 阶段评估
/dc:compassion-catalyst      — 慈悲行动
/dc:practice-weaver          — 完整的日常循环
```

## 作者 (Autor)

Marcio Bisognin
- [Squads Platform](https://squads.sh/pt)
- [Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## 许可证 (Licença)

MIT
