# PRD — Scope Sentinel

## Problema
Operações de cibersegurança falham quando escopo, proveniência, segurança, evidência e reteste são tratados como detalhes.

## Produto
Transformar escopo autorizado em coleta de baixo impacto, achados validados, priorização e reteste sem exploração destrutiva.

## Requisitos funcionais
- validar escopo e autorização
- inventariar superfície pública
- coletar evidência de baixo impacto
- correlacionar versões e advisories
- revisar falsos positivos
- priorizar remediação
- emitir relatório e reteste
- CLI determinística com saídas JSON/CSV/Markdown.
- validação estrutural e smoke test local.
- bloqueio explícito de ações ofensivas destrutivas.

## Requisitos não funcionais
- Python standard library; compatível com Termux.
- dados sintéticos nos exemplos.
- nenhum segredo nos outputs.
- arquivos reprodutíveis e hashes quando empacotados.

## Critérios de aceite
- `squad.yaml` e arquivos declarados existem.
- CLI compila e executa os comandos documentados.
- smoke test gera entregáveis não vazios.
- teste unitário passa.
- secret scan não encontra credenciais.

## Integração da trilha de cibersegurança — v2

Este squad incorpora a trilha fornecida por Marcio como um sistema auditável de aprendizagem e operação. Contém 53 recursos/ferramentas e 14 técnicas do seu domínio. O roteador local apenas cataloga, audita disponibilidade e decide `GATED_HANDOFF`, `PLAN_ONLY` ou `DENY`; ele não lança scanners, exploits, payloads ou malware.

```bash
python scripts/capability_router.py catalog
python scripts/capability_router.py audit
python scripts/capability_router.py route --technique controlled-exploit-validation --context lab --band 3
```
