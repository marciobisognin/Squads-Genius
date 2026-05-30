![Version](https://img.shields.io/badge/version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/github/license/gutomec/nirvana-readme-architect?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/gutomec/nirvana-readme-architect?style=flat-square&logo=git&logoColor=white)
![Stars](https://img.shields.io/github/stars/gutomec/nirvana-readme-architect?style=flat-square&logo=github)
![AIOS Squad](https://img.shields.io/badge/AIOS-Squad-8A2BE2?style=flat-square&logo=robot&logoColor=white)

# 📜 Nirvana README Architect (NRA)

> AIOS 小队，为任何项目生成完美的 README.md — 结合深度代码库分析、智能模板选择、GitHub Flavored Markdown 的所有功能、25+ 项检查清单验证和最终润色。

## 目录

- [概述](#概述)
- [代理](#代理)
- [流水线](#流水线)
- [快速开始](#快速开始)
- [命令](#命令)
- [架构](#架构)
- [支持的 GitHub 功能](#支持的-github-功能)
- [质量检查清单](#质量检查清单)
- [故障排除](#故障排除)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 概述

**Nirvana README Architect** 是由 5 个专业代理组成的小队，通过流水线将任何代码库转化为专业级 README。

与生成通用模板的简单生成器不同，NRA：

- **分析**实际代码库（技术栈、脚本、环境变量、目录结构）
- 根据项目类型**选择**理想模板（库、CLI、Web 应用、API、Monorepo、移动端、小队）
- 使用 GitHub Flavored Markdown 的**所有**功能**生成**内容
- 通过 25+ 项检查清单和自动评分进行**验证**
- 使用徽章、目录、折叠部分和完美间距进行**润色**

> [!TIP]
> 最低交付分数：**90/100**。NRA 自动返工直到达到此水平。

## 代理

| 代理 | 角色名 | 原型 | 职能 |
|:-----|:-------|:-----|:-----|
| `nra-orchestrator` | **Quill** | FlowMaster | 编排完整流水线 |
| `nra-codebase-analyzer` | **Prism** | Seeker | 深度代码库分析 |
| `nra-content-architect` | **Serif** | Architect | 模板选择和内容生成 |
| `nra-quality-validator` | **Lens** | Guardian | 25+ 项检查清单验证 |
| `nra-polisher` | **Gloss** | Alchemist | 最终润色 |

## 流水线

```
Parse → Scan → Draft → Validate → Polish → Revalidate → Deliver
```

| 阶段 | 代理 | 描述 |
|:-----|:-----|:-----|
| **Parse** | Quill | 识别项目、类型和范围 |
| **Scan** | Prism | 深度代码库分析 |
| **Draft** | Serif | 选择模板并生成内容 |
| **Validate** | Lens | 25+ 项检查清单，评分 |
| **Polish** | Gloss | 目录、徽章、间距 |
| **Deliver** | Quill | 带指标的交付 |

## 快速开始

> [!NOTE]
> 此小队在 **Synkra AIOS** 生态系统中运行，需要配置了框架的 Claude Code。

```bash
git clone https://github.com/gutomec/nirvana-readme-architect.git
squads install gutomec/nirvana-readme-architect

@nra-orchestrator
*readme {项目路径}
```

## 命令

| 命令 | 描述 | 代理 |
|:-----|:-----|:-----|
| `*readme {项目} [类型]` | 完整流水线 | Quill |
| `*readme-full` | 所有 12+ 个章节 | Quill |
| `*readme-quick` | 6 个核心章节 | Quill |
| `*scan` | 深度分析 | Prism |
| `*validate` | 检查清单验证 | Lens |
| `*polish` | 视觉润色 | Gloss |

## 架构

```text
nirvana-readme-architect/
├── agents/          # 5 个专业代理
├── tasks/           # 7 个可执行任务
├── workflows/       # 生成流水线
├── checklists/      # 25+ 验证项
├── templates/       # 带 GFM 的主模板
├── config/          # 标准和技术栈
└── squad.yaml       # 小队清单
```

## 支持的 GitHub 功能

Alerts、Mermaid Diagrams、Tables、Collapsed Sections、Task Lists、Footnotes、Badges、Emojis、kbd Tags、Code Blocks、Diff Blocks、Reference Links — **12 项完整功能**。

## 质量检查清单

| 分数 | 等级 | 操作 |
|:-----|:-----|:-----|
| 90-100 | 🏆 涅槃 | 交付 |
| 75-89 | ⭐ 良好 | 发送润色 |
| 60-74 | ⚠️ 可接受 | 返工 |
| < 60 | ❌ 不足 | 带反馈返工 |

## 故障排除

| 问题 | 解决方案 |
|:-----|:---------|
| 低分 | 通过 `*readme-full` 手动提供数据 |
| 错误模板 | 指定类型：`*readme {项目} api` |

## 贡献

欢迎贡献。提交信息请遵循 [Conventional Commits](https://www.conventionalcommits.org/)。

## 许可证

基于 **MIT** 许可 — 查看 [LICENSE](./LICENSE)。

---

<div align="center">

用 ❤️ 由 [Synkra AIOS](https://github.com/gutomec) 制作

**[Português](./README.md)** · **[English](./README.en.md)** · **[Español](./README.es.md)** · **[العربية](./README.ar.md)** · **[हिन्दी](./README.hi.md)**

</div>
