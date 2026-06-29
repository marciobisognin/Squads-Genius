# SKEPTIC Protocol

SKEPTIC Protocol（建设性怀疑主义）的实施，包含5个严格的预防性软件工程阶段。

## 安装

1. 将 `skeptic-protocol` 文件夹移动或克隆到您的 AIOX squads 目录中。
2. 确保 AIOX CLI 识别该包。
3. 使用 `/sk` 前缀调用代理。

## 它的作用

这个小队应用建设性怀疑主义，在编写包含第一行实现代码的文件之前，强制识别所有潜在的代码缺陷。它用“预测缺陷，用失败的测试去证明，然后再实现解决方案”替代了天真的“构建与测试”方法。

## Pipeline

| 阶段 | 代理 | 角色 | 模型 |
|------|--------|-------|--------|
| 1 | `failure-predictor` | Accusation Specialist | Guardian |
| 2 | `test-engineer` | Defense Specialist | Builder |
| 3 | `solution-implementer` | Trial Developer | Builder |
| 4 | `red-teamer` | Appeal Challenger | Balancer |
| 5 | `skeptic-orchestrator`| Verdict & Protocol Manager | Flow_Master |

## Agents

| 代理 | 头衔 | Archetype | 描述 |
|--------|--------|-----------|-----------|
| `failure-predictor` | Accusation Specialist | Guardian | 详尽地识别故障模式而不产生代码。|
| `test-engineer` | Defense Specialist | Builder | 创建关注指控的测试套件，要求它们故意失败（红阶段）。|
| `solution-implementer` | Trial Developer | Builder | 重构并实现代码，唯一目的是通过测试套件。|
| `red-teamer` | Appeal Challenger | Balancer | 作为对手，试图通过边缘用例（Edge Cases）破坏已创建的解决方案。|
| `skeptic-orchestrator` | Verdict & Protocol Manager | Flow_Master | 确保协议的流通性并撰写官方的 SKEPTIC_REPORT.md。|

## Tasks

| 任务 | 负责人 | Atomic Layer | 描述 |
|------|-------------|-------------|-----------|
| `generateAccusations()` | `FailurePredictor` | Organism | 收集漏洞并详细说明严重程度和概率。|
| `writeFailingTests()` | `TestEngineer` | Organism | 将漏洞转化为实际的负面测试。|
| `implementTrialCode()` | `SolutionImplementer` | Organism | 编码解决方案以满足防御限制。|
| `executeAppeal()` | `RedTeamer` | Molecule | 主动挑战在 Trial 阶段批准的代码库。|
| `generateVerdictReport()`| `SkepticOrchestrator` | Molecule | 评估最终统计数据并生成文档。|

## Workflows

| 工作流 | Pattern | 代理 | 描述 |
|----------|---------|---------|-----------|
| `skeptic_pipeline_execution` | Pipeline | 所有5个代理 | 方法论5个阶段的主要线性执行流程。|
| `red_team_feedback_loop` | Evaluator-Optimizer | `red-teamer`, `failure-predictor`, `solution-implementer` | 发生在上诉（Appeal）破坏代码时的对抗性反馈循环。|

## 配置

- config/coding-standards.md
- config/tech-stack.md
- config/source-tree.md

## 使用

### 可用命令

- `*generate-accusations`: 评估需求并创建 Markdown 指控清单。
- `*write-failing-tests`: 基于指控构建初始测试套件。
- `*implement-trial-code`: 执行生产性代码开发。
- `*execute-appeal`: 执行内部渗透测试或严格的边缘情况审查。
- `*generate-verdict-report`: 编译 SKEPTIC 周期的最终报告。

### 示例

```bash
# 从头开始启动工作流
/sk:failure-predictor
*generate-accusations --objective="开发现有 MFA 的登录系统"
```

##. Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)
[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## 许可证

MIT
