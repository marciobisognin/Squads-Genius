# 🔱 Forge of Solus Prime — Cybersecurity Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> ⚠️ **ESCOPO EXCLUSIVAMENTE DEFENSIVO** — Todas as atividades exigem autorização expressa
> do cliente sobre ativos que ele possui ou tem permissão formal para avaliar. Este squad
> NÃO executa testes de penetração reais, exploits, malware ou qualquer técnica ofensiva
> ativa. Toda análise adversarial é conceitual, baseada em frameworks públicos (MITRE
> ATT&CK, OWASP), e não substitui consultoria de segurança certificada (CISSP, CISM, CEH,
> OSCP).

Squad premium de segurança defensiva, operado por 10 agentes especializados, que fortalece
a postura de segurança digital de organizações: inventário de ativos, modelagem de
ameaças, avaliação de vulnerabilidades, políticas de segurança, playbooks de resposta a
incidentes, conformidade regulatória e conscientização — sempre do lado defensivo.

---

## Artefato de Inspiração: A Forja de Solus Prime (Transformers Prime)

A **Forja de Solus Prime** é uma relíquia sagrada capaz de criar armas e proteções
indestrutíveis, usada pelos Primais para fortalecer defensores — nunca para atacar
indiscriminadamente. Este squad é o equivalente digital: forja defesas robustas —
inventários, modelos de ameaça, políticas, playbooks — sempre com o propósito de proteger,
nunca de atacar.

---

## Visão Geral do Squad

O Forge of Solus Prime Squad transforma um inventário de ativos digitais e contexto
organizacional em um programa completo de segurança defensiva: mapeamento de superfície
de ataque, modelagem de ameaças com STRIDE e MITRE ATT&CK, priorização de vulnerabilidades
por CVSS, geração de políticas de segurança, playbooks de resposta a incidentes, análise
de lacunas de conformidade (LGPD/ISO 27001/SOC 2/NIST CSF), programa de conscientização e
avaliação de risco de cadeia de suprimentos digitais.

**Diferencial central:** Gate ético mandatório de escopo defensivo em toda interação.
Nenhuma atividade é executada sem autorização documentada do proprietário dos ativos, e
toda análise adversarial é puramente conceitual.

---

## Domínio e Casos de Uso

### Para quem este squad foi criado

- CISOs e times de segurança que precisam de avaliação estruturada de postura
- Organizações em processo de adequação a LGPD, ISO 27001, SOC 2 ou NIST CSF
- Times que precisam de políticas de segurança formais e playbooks de incidentes
- Empresas que querem avaliar risco de fornecedores críticos

### Casos de uso típicos

| Situação | Como o Squad Ajuda |
|----------|-------------------|
| Falta de inventário de ativos atualizado | Mapeamento completo de ativos e superfície de ataque |
| Ausência de modelo de ameaças formal | Modelagem STRIDE + MITRE ATT&CK documentada |
| Preparação para auditoria LGPD/ISO 27001 | Relatório de lacunas priorizado por risco e esforço |
| Falta de playbook de resposta a incidentes | Playbooks por tipo de ataque com papéis definidos |
| Risco desconhecido de fornecedores | Avaliação de risco de cadeia de suprimentos digital |

---

## Agentes do Squad

### 1. solus-forge-orchestrator
Coordenador central com gate ético mandatório de escopo defensivo. Verifica autorização
documentada antes de qualquer atividade e consolida as entregas finais.

### 2. asset-inventory-mapper
Inventário de ativos digitais e mapeamento de superfície de ataque.

### 3. threat-model-architect
Modelagem de ameaças com STRIDE, MITRE ATT&CK e Kill Chain.

### 4. vulnerability-assessor
Avaliação e priorização de vulnerabilidades com pontuação CVSS — sem execução de exploits.

### 5. security-policy-writer
Geração de políticas de segurança: PSI, BYOD, nuvem, trabalho remoto, classificação de dados.

### 6. incident-response-planner
Criação de playbooks de resposta a incidentes por tipo de ataque.

### 7. lgpd-iso27001-auditor
Análise de lacunas para LGPD, ISO 27001, SOC 2, NIST CSF.

### 8. security-awareness-designer
Design de programas de conscientização e simulações conceituais de phishing.

### 9. supply-chain-risk-analyst
Avaliação de risco de terceiros e cadeia de suprimentos digitais.

### 10. red-team-advisor
Perspectiva adversarial conceitual para fortalecer defesas — sem ataques reais.

---

## Pipeline de Execução

1. **Intake and Authorization** — verificação obrigatória de escopo defensivo e autorização documentada
2. **Assessment** — inventário, modelagem de ameaças e vulnerabilidades (HITL de revisão)
3. **Hardening** — políticas, resposta a incidentes e perspectiva adversarial (HITL de aprovação)
4. **Compliance and Awareness** — conformidade, conscientização e risco de terceiros
5. **Synthesis** — consolidação final com revisão humana obrigatória

Workflow completo: [`workflows/cybersecurity-pipeline.yaml`](workflows/cybersecurity-pipeline.yaml)
Quality gates: [`workflows/quality-gates.yaml`](workflows/quality-gates.yaml)

---

## Entregáveis

- Relatório de Inventário de Ativos e Superfície de Ataque
- Relatório de Modelagem de Ameaças (STRIDE + MITRE ATT&CK)
- Scorecard de Postura de Segurança com prioridades CVSS
- Pack de Políticas de Segurança
- Playbook de Resposta a Incidentes
- Relatório de Análise de Lacunas de Conformidade (LGPD/ISO 27001/SOC 2/NIST CSF)
- Plano de Treinamento e Conscientização em Segurança
- Relatório de Risco de Cadeia de Suprimentos Digitais
- Relatório de Perspectiva Adversarial para Fortalecimento Defensivo

---

## Quality Gates

- `escopo_defensivo_confirmado`
- `autorizacao_documentada_verificada`
- `inventario_ativos_validado`
- `modelo_ameacas_revisado_por_humano`
- `politicas_aprovadas_pelo_cliente`
- `playbooks_testados_conceitualmente`
- `conformidade_gap_priorizado`
- `entrega_final_revisada_por_humano`

---

## Disclaimer

Os artefatos gerados por este squad são documentos de suporte técnico para equipes de
segurança autorizadas. Nenhuma atividade ofensiva, exploit ou teste de penetração real é
executado. Toda recomendação pressupõe autorização prévia e documentada do proprietário
dos ativos avaliados. Revisão humana por profissional de segurança qualificado é
obrigatória antes de implementação. Este squad não substitui consultoria de segurança
certificada (CISSP, CISM, CEH, OSCP).

---

## Como Usar

1. Forneça inventário de ativos, contexto setorial e **autorização documentada**
2. Confirme o escopo estritamente defensivo (HITL obrigatório)
3. Acompanhe a avaliação de ameaças e vulnerabilidades
4. Revise o modelo de ameaças (HITL obrigatório)
5. Aprove políticas e playbooks gerados
6. Receba o pacote final após revisão por profissional de segurança qualificado

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml` e `squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/forge-of-solus-prime-cybersecurity-squad/agents/solus-forge-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/forge-of-solus-prime-cybersecurity-squad/agents/solus-forge-orchestrator.md`
> e conduza o fluxo definido em `squads/forge-of-solus-prime-cybersecurity-squad/`. Siga `squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml. Conduza o fluxo para o briefing: <...>
```
- Use **`@caminho/arquivo`** para dar contexto preciso (autocompleta no prompt).
- Disponível em **CLI, app desktop/web (claude.ai/code) e extensões VS Code / JetBrains**.

</details>

<details>
<summary><b>🟦 Cursor</b></summary>

<br>

1. Abra a pasta do repositório no Cursor.
2. No **Chat / Composer (⌘/Ctrl + I)**, referencie os arquivos com `@`:
   ```text
   @squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml @squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/forge-of-solus-prime-cybersecurity-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml #file:squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml @squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/forge-of-solus-prime-cybersecurity-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/forge-of-solus-prime-cybersecurity-squad/squad.yaml` e `squads/forge-of-solus-prime-cybersecurity-squad/workflows/cybersecurity-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
