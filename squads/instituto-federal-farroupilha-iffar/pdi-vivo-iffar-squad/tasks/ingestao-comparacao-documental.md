# Task — Ingestão e comparação documental

## Objetivo
Transformar documentos do PDI (vigente, anterior, metodologia, relatórios e proposta do novo ciclo) em base de conhecimento auditável e mapa comparativo entre ciclos.

## Entradas
- PDFs, DOCX, Markdown e páginas oficiais do PDI.
- Metodologia e relatórios de acompanhamento.
- Proposta do novo ciclo (ex.: PDI Vivo 2027–2034).

## Passos
1. Listar e classificar as fontes (oficial, interna, proposta).
2. Executar `scripts/extract_pdi_text.py` para cada fonte (gera texto limpo, métricas e hash SHA-256).
3. Executar `scripts/compare_pdi_cycles.py` entre o ciclo anterior e o novo (incidência de termos de gestão viva).
4. Produzir mapa comparativo: o que permanece, o que muda, o que precisa ser repactuado.
5. Registrar relatório de lacunas e parecer de governança/LGPD.

## Saídas
- Base de conhecimento (textos extraídos + métricas + hashes).
- Comparativo de ciclos (CSV + Markdown).
- Relatório de lacunas e parecer de governança.

## Regras
- Nunca inventar conteúdo ausente; sinalizar lacuna.
- Preservar fontes, datas e versões.
- Separar observado, inferido, hipótese, recomendação e risco.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
