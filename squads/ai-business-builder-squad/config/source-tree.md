# Source Tree: AI Business Builder Squad

This document outlines the organizational structure for the AI Business Builder Squad assets, agents, and configurations.

## Directory Structure

```text
ai-business-builder-squad/
├── squad.yaml                 # Squad manifest and entry point
├── agents/                    # AI Agent definitions (System Prompts)
│   ├── business-strategist.md
│   ├── market-analyst.md
│   ├── brand-architect.md
│   ├── content-strategist.md
│   ├── funnel-engineer.md
│   ├── copywriter-ai.md
│   ├── product-architect.md
│   └── strategic-mentor.md
├── tasks/                     # Atomic task definitions
│   ├── ideation-and-validation.md
│   ├── brand-identity-creation.md
│   ├── social-media-automation.md
│   ├── marketing-funnel-design.md
│   ├── product-conception-framework.md
│   └── strategic-growth-mentorship.md
├── workflows/                 # Multi-agent orchestration logic
│   ├── business-launch-pipeline.yaml
│   └── content-to-conversion-flow.yaml
├── config/                    # Squad-level configuration
│   ├── coding-standards.md
│   ├── tech-stack.md
│   └── source-tree.md
├── assets/                    # Static assets (logos, templates, brand kits)
└── outputs/                   # Generated business artifacts and reports
```

## Component Descriptions

- **agents/**: Contains the persona and behavioral instructions for each specialized AI agent.
- **tasks/**: Defines specific, repeatable actions that agents perform within the business lifecycle.
- **workflows/**: YAML files defining the sequence and logic of agent interactions for complex goals.
- **config/**: Governance and technical specifications for the squad's operation.
- **assets/**: Storage for non-executable business resources like design files and templates.
- **outputs/**: The destination for all generated business plans, marketing copy, and strategic reports.