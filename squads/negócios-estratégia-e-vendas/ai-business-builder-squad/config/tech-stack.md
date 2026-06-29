# Tech Stack: AI Business Builder Squad

This document outlines the open-source tools and technologies integrated into the AI Business Builder Squad for end-to-end business construction and strategic automation.

## 1. Automation & Orchestration
- **n8n**: Primary low-code workflow automation tool for connecting agents, tasks, and external business APIs.
- **AIOS (AI Operating System)**: The core execution framework for squad management, agent lifecycle, and task orchestration.

## 2. Backend & Data Management
- **Supabase**: Open-source Firebase alternative providing PostgreSQL database, authentication, and real-time subscriptions.
- **pgvector**: Vector database extension for Supabase used for RAG (Retrieval-Augmented Generation) and business knowledge base storage.

## 3. AI & Machine Learning
- **Hugging Face**: Source for open-source LLMs (Llama 3, Mistral, Mixtral) and specialized embedding models.
- **Ollama**: Local inference engine for running LLMs on-premise to ensure data privacy for sensitive business strategies.
- **LangChain / LlamaIndex**: Frameworks for building context-aware agentic reasoning and data connectors.

## 4. Content & Marketing
- **WordPress / Ghost**: Open-source Content Management Systems (CMS) for hosting generated marketing assets and SEO content.
- **Mautic**: Open-source marketing automation platform for managing email funnels and lead nurturing sequences.
- **Appsmith / Budibase**: Open-source internal tool builders for creating custom business dashboards.

## 5. Infrastructure & DevOps
- **Docker**: Containerization for consistent deployment of agents and microservices across environments.
- **GitHub Actions**: CI/CD pipelines for automated testing of squad workflows and agent configurations.
- **Traefik**: Modern HTTP reverse proxy and load balancer for managing squad service traffic.

## 6. Communication & Monitoring
- **Mattermost**: Open-source team communication platform for squad output delivery and human-in-the-loop approvals.
- **Grafana / Prometheus**: Monitoring stack for tracking agent performance, API latency, and system resource usage.