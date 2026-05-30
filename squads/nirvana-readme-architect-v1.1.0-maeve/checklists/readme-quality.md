---
id: readme-quality
name: readme-quality
type: validation
squad: nirvana-readme-architect
---

# README Quality Checklist

## Estrutura (Blocking — peso 2x)
- [ ] H1 com nome do projeto
- [ ] Descrição concisa (1-2 frases) logo após H1
- [ ] Badges presentes e renderizáveis (sintaxe shields.io válida)
- [ ] TOC com links funcionais (obrigatório para READMEs com > 5 seções)
- [ ] Seção de instalação com code blocks
- [ ] Seção de uso com exemplos reais

## GitHub Features (Advisory — peso 1x)
- [ ] Alerts utilizados (ao menos 3 de: NOTE, TIP, WARNING, IMPORTANT, CAUTION)
- [ ] Mermaid diagram para arquitetura (sintaxe válida)
- [ ] Tables para referência (env vars, scripts, APIs)
- [ ] Collapsed sections para conteúdo extenso (> 30 linhas)
- [ ] Task list para setup checklist
- [ ] Footnotes para referências externas
- [ ] Badges shields.io alinhados com estilo consistente
- [ ] Emojis para visual scanning (uso consistente)
- [ ] kbd tags para atalhos (se aplicável — bônus)
- [ ] Code blocks com linguagem especificada (100% deles)
- [ ] Diff blocks para mudanças (se changelog presente — bônus)

## Conteúdo (Blocking — peso 2x)
- [ ] Instalação testável (copy-paste funcional, comandos completos)
- [ ] Exemplos de uso reais (não placeholders genéricos)
- [ ] Env vars documentadas (se existirem no projeto)
- [ ] Scripts disponíveis documentados (se existirem no projeto)
- [ ] License presente ou referenciada

## Completude (Advisory — peso 1x)
- [ ] Prerequisites listados com versões mínimas
- [ ] Architecture explicada (diagrama ou texto estruturado)
- [ ] Testing documentado (como rodar, framework utilizado)
- [ ] Deployment coberto (ao menos menção ao processo)
- [ ] Troubleshooting incluído (problemas comuns e soluções)
- [ ] Contributing guidelines presentes
- [ ] Changelog ou link para releases

## Fórmula de Score

```
blocking_score = (blocking_passed / blocking_total) * 60
advisory_score = (advisory_passed / advisory_total) * 40
bonus = kbd_present(+2) + diff_present(+2)
final_score = min(100, blocking_score + advisory_score + bonus)
```

## Faixas de Decisão

| Score | Nível | Verdict | Ação |
|-------|-------|---------|------|
| 90-100 | Nirvana | APROVADO | Entregar |
| 75-89 | Bom | POLIR | Enviar para nra-polisher |
| 60-74 | Aceitável | RETRABALHAR | Retornar ao nra-content-architect |
| < 60 | Insuficiente | RETRABALHAR | Retornar ao nra-content-architect com feedback detalhado |
