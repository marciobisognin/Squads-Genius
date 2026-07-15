# PRD — Breach Compass

## Problema
Operações de cibersegurança falham quando escopo, proveniência, segurança, evidência e reteste são tratados como detalhes.

## Produto
Guiar triagem, preservação, contenção aprovada, investigação, recuperação e aprendizagem sem executar malware ou alterar produção automaticamente.

## Requisitos funcionais
- abrir incidente e registrar relógio
- preservar e delimitar
- construir timeline e hipóteses
- extrair IOCs e lacunas
- propor contenção com aprovação
- planejar erradicação e recuperação
- revisar fator humano
- registrar aprendizados e regressões
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

Este squad incorpora a trilha fornecida por Marcio como um sistema auditável de aprendizagem e operação. Contém 27 recursos/ferramentas e 6 técnicas do seu domínio. O roteador local apenas cataloga, audita disponibilidade e decide `GATED_HANDOFF`, `PLAN_ONLY` ou `DENY`; ele não lança scanners, exploits, payloads ou malware.

```bash
python scripts/capability_router.py catalog
python scripts/capability_router.py audit
python scripts/capability_router.py route --technique malware-dynamic-analysis --context isolated-external-lab --band 3
```
