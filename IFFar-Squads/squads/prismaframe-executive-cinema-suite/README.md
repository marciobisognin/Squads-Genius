<div align="center">

# PrismaFrame Executive Cinema Suite

### Relatórios visuais, apresentações executivas e composições animadas HTML-native em um único fluxo premium.

![status](https://img.shields.io/badge/status-production--ready-0f766e?style=for-the-badge)
![license](https://img.shields.io/badge/license-MIT-f59e0b?style=for-the-badge)
![output](https://img.shields.io/badge/output-HTML%20%7C%20Deck%20%7C%20Motion%20%7C%20PDF-2563eb?style=for-the-badge)

</div>

---

## O que é

O **PrismaFrame Executive Cinema Suite** é um sistema operacional de produção premium para transformar documentos densos, diagnósticos, relatórios técnicos e narrativas institucionais em materiais finais de alto impacto visual.

Ele combina dois mundos:

- estrutura executiva, auditável e visual-first de relatórios premium;
- composição em frames, cenas e movimento, com HTML como fonte de verdade.

O resultado é uma esteira capaz de entregar material pronto para apresentação, leitura executiva, reunião de diretoria, defesa institucional, lançamento, aula, pitch ou briefing audiovisual.

---

## Princípio central

O produto final deve parecer uma peça editorial/profissional pronta, não um artefato de bastidor.

```mermaid
flowchart LR
    A[Documento ou briefing] --> B[Arquitetura narrativa]
    B --> C[Sistema visual]
    C --> D[Relatório ou deck premium]
    D --> E[Composição animada]
    E --> F[QA cleanroom]
    F --> G[Material final pronto]
```

---

## Política de produto final limpo

Todo material destinado ao público final passa por uma etapa de limpeza editorial.

O material final não deve explicitar:

- bastidores de criação;
- nomes de papéis internos;
- instruções de produção;
- estrutura operacional;
- prompts;
- metadados editoriais desnecessários;
- qualquer marca de processo.

A documentação interna do pacote explica a operação; a entrega final mostra apenas o produto acabado.

---

## Para que serve

- Relatórios executivos premium.
- Decks para apresentação institucional.
- Briefings visuais para reuniões estratégicas.
- Materiais com narrativa, evidências, gráficos e roadmap.
- Peças animadas HTML-native para vídeo, social, lançamento ou explicação.
- Conversão de documentos técnicos em material visual pronto para decisão.

---

## Arquitetura do squad

```mermaid
mindmap
  root((PrismaFrame))
    Direção
      Chief Experience Director
      Final Product Curator
    Conteúdo
      Evidence Intake Architect
      Executive Narrative Strategist
      Factual Integrity Auditor
    Visual
      Visual Systems Director
      Data Visualization Architect
      Visual Quality Inspector
    Movimento
      Frame Motion Director
      Cinematic Storyboarder
      Motion Composition Engineer
    Engenharia
      HTML Stage Engineer
      Print PDF Engineer
      Packaging Release Manager
    Cleanroom
      Brand Silence Guardian
      Presentation Readiness Reviewer
```

---

## Entregas finais possíveis

| Entrega | Finalidade |
|---|---|
| `index.html` | Relatório/site premium pronto para apresentação |
| `deck.html` | Deck executivo navegável |
| `motion-composition.html` | Composição em frames para renderização/preview |
| `print-ready.html` | Versão otimizada para PDF |
| `final-manifest.json` | Manifesto técnico limpo do pacote final |
| `qa-cleanroom-report.json` | Evidência de que a entrega final não mostra bastidores |

---

## Workflows

1. **Clean Premium Material** — documento para material visual limpo.
2. **Executive Motion Briefing** — narrativa executiva em composição animada.
3. **Full Presentation Suite** — relatório, deck, composição e pacote final.

---

## Como executar o demo

```bash
python3 scripts/smoke_test.py
```

Saída esperada:

```text
generated/demo/final/index.html
generated/demo/final/deck.html
generated/demo/final/motion-composition.html
generated/demo/final/final-manifest.json
```

---

## Validar o pacote

```bash
python3 scripts/validate_squad.py
```

---

## Estrutura

```text
agents/       papéis especializados
tasks/        etapas operacionais
workflows/    fluxos completos
templates/    templates HTML/CSS limpos
components/   componentes reutilizáveis
contracts/    schemas de entrada/saída
scripts/      build, smoke test e validação
examples/     briefing de exemplo
generated/    saídas de demonstração
validation/   relatórios de validação
```

---

## Licença

MIT. Criado por Marcio Bisognin. Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
