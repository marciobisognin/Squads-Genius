#!/usr/bin/env python3
import argparse, csv, json, re
from pathlib import Path
from datetime import datetime

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

def parse_simple_yaml(path):
    data = {}
    current = None
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line = raw.rstrip()
        if not line or line.strip().startswith('#'):
            continue
        if re.match(r'^[A-Za-z_]+:', line):
            k, v = line.split(':', 1)
            k = k.strip(); v = v.strip().strip('"')
            if v:
                data[k] = v; current = None
            else:
                data[k] = []; current = k
        elif current and line.strip().startswith('-'):
            data[current].append(line.strip()[1:].strip().strip('"'))
    return data

def main():
    ap = argparse.ArgumentParser(description='Gera demo autoral MIT do pipeline de artigo científico.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    data = parse_simple_yaml(args.input)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    tema = data.get('tema', 'Tema não informado')
    pergunta = data.get('pergunta', 'Pergunta não informada')
    titulo = data.get('titulo', 'Título provisório demonstrativo')
    norma = data.get('norma', 'ABNT/APA a definir')
    afiliacao = 'Instituto Federal Farroupilha Campus Frederico Westphalen RS'

    passport = f'''projeto:
  titulo_provisorio: "{titulo}"
  tema: "{tema}"
  pergunta: "{pergunta}"
  autor: "Marcio Bisognin"
  afiliacao: "{afiliacao}"
  periodico_alvo: ""
  norma: "{norma}"
corpus:
  origem: "demo sem busca externa"
  matriz_evidencias: "matriz_evidencias.csv"
verificacao:
  status: "demonstração estrutural; referências reais não verificadas"
  referencias_verificadas: 0
  referencias_nao_verificadas: 2
  alertas_altos:
    - "Demo não realizou consulta externa; não usar como revisão real."
  alertas_medios: []
decisoes_humanas:
  - "Campo periódico-alvo mantido em branco até definição do usuário."
licenca: "MIT"
rodape: "{FOOTER}"
'''
    (out/'passaporte_material.yaml').write_text(passport, encoding='utf-8')

    article = f'''# {titulo}

**Autor:** Marcio Bisognin  
**Afiliação:** {afiliacao}  
**Periódico-alvo:**  
**Norma:** {norma}  
**Status:** demonstração estrutural, sem busca externa real.

## Resumo

Este manuscrito demonstrativo apresenta a estrutura mínima do pipeline de artigo científico do squad Maeve Atena Mimir. O texto ilustra organização acadêmica, rastreabilidade e marcação de lacunas, mas não deve ser interpretado como revisão bibliográfica concluída.

**Palavras-chave:** pesquisa científica; revisão bibliográfica; integridade acadêmica; inteligência artificial; metodologia.

## 1. Introdução

O tema "{tema}" demanda delimitação conceitual, seleção de bases, critérios de inclusão e verificação das fontes antes da formulação de conclusões. A pergunta orientadora desta demonstração é: {pergunta}

## 2. Referencial teórico

[EVIDÊNCIA PENDENTE] A fundamentação teórica deverá ser construída a partir de fontes verificadas em bases acadêmicas legais, com separação entre estudos empíricos, revisões e documentos institucionais.

## 3. Metodologia

A execução real deverá combinar estratégia de busca documentada, matriz de evidências, triagem por critérios explícitos e auditoria de citações. Nesta demo, a metodologia é apenas estrutural.

## 4. Achados preliminares

[MATERIAL GAP] Não há achados empíricos confirmados nesta execução demonstrativa. O pipeline exige consulta externa antes de qualquer conclusão substantiva.

## 5. Discussão

A principal contribuição do fluxo é impedir que a redação avance sem distinguir hipótese, evidência verificada e lacuna material. Essa separação reduz risco de citação decorativa e extrapolação indevida.

## 6. Considerações finais

O pipeline está operacional para produzir artigos a partir de pesquisa verificada, mas a demo não substitui investigação real.

## Limitações

Esta saída foi gerada sem acesso a bases externas e, por isso, mantém referências reais como não verificadas.

## Referências

Nenhuma referência real foi validada nesta demonstração.

{FOOTER}
'''
    (out/'artigo_imrad.md').write_text(article, encoding='utf-8')

    review = f'''# Parecer de revisão por pares simulada — demo

## Decisão

Revisar substancialmente antes de uso acadêmico real.

## Justificativa

A estrutura do manuscrito está organizada, mas não há corpus verificado. A versão deve retornar às fases de busca, matriz de evidências e auditoria antes da finalização.

## Problemas bloqueantes

| ID | Seção | Problema | Correção exigida |
|---|---|---|---|
| B1 | Referencial | ausência de fontes verificadas | executar busca real e preencher matriz |
| B2 | Achados | inexistência de evidência empírica | inserir somente achados comprovados |

{FOOTER}
'''
    (out/'parecer_revisao_pares.md').write_text(review, encoding='utf-8')

    audit = f'''# Auditoria de integridade acadêmica — demo

## Resultado geral

- Status: bloqueado para uso como artigo real.
- Alertas altos pendentes: 1.
- Data: {now}.

## Alerta alto

A demo não realizou consulta a bases externas; portanto, não contém referências verificadas.

## Decisão

Liberado apenas como teste estrutural do squad. Para uso acadêmico, executar revisão bibliográfica real e repetir auditoria.

{FOOTER}
'''
    (out/'auditoria_integridade.md').write_text(audit, encoding='utf-8')

    response = f'''# Matriz de resposta aos revisores — demo

| Item | Comentário | Resposta | Status |
|---|---|---|---|
| B1 | Falta corpus verificado | Será executada busca real antes da versão final | pendente |
| B2 | Achados não demonstrados | Achados permanecerão marcados como lacuna até haver evidência | pendente |

{FOOTER}
'''
    (out/'resposta_revisores.md').write_text(response, encoding='utf-8')

    with (out/'matriz_evidencias.csv').open('w', newline='', encoding='utf-8') as f:
        wr = csv.writer(f)
        wr.writerow(['id','afirmacao','fonte','status','observacao'])
        wr.writerow(['A1','Tema exige revisão bibliográfica real','fonte pendente','não verificado','demo estrutural'])
        wr.writerow(['A2','Pipeline separa evidência e lacuna','artefato interno do squad','verificado internamente','funcionamento do fluxo'])

    manifest = {'ok': True, 'kind':'article-demo', 'license':'MIT', 'outputs':[p.name for p in sorted(out.iterdir()) if p.is_file()], 'warning':'Demo estrutural; não substitui pesquisa real.'}
    (out/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False))

if __name__ == '__main__':
    main()
