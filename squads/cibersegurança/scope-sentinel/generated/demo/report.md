# Relatório Scope Sentinel

## Escopo
- Base de autorização: local lab
- Ativos: 1

## Observações

### http://127.0.0.1:38821
- IPs resolvidos: 127.0.0.1
- `http://127.0.0.1:38821/` — 200; 50 bytes
- `http://127.0.0.1:38821/robots.txt` — 200; 23 bytes
- `http://127.0.0.1:38821/sitemap.xml` — 404; 335 bytes
- `http://127.0.0.1:38821/.well-known/security.txt` — 404; 335 bytes
- `http://127.0.0.1:38821/3af41af0aba9e05d3b0f047e` — 404; 335 bytes

## Limitações
- no authentication
- no exploit payloads
- fixed five-request path set per asset
- no port scan in collector

## Próximo passo
Revisão manual, correlação de versões/advisories e reteste após remediação.
