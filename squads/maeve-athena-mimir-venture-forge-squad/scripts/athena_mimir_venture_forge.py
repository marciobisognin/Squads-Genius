#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def load_case(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip()+"\n", encoding='utf-8')

def gerar(caso, out):
    ideia=caso.get('ideia','Ideia sem título')
    publico=caso.get('publico','Público a definir')
    proposta=caso.get('proposta','Proposta a definir')
    mapa=f"""
# Mapa-Labirinto de Hipóteses

Ideia: {ideia}
Público: {publico}
Proposta de valor: {proposta}

## Yggdrasil do negócio
- Raiz/problema: dor prioritária ainda a comprovar.
- Tronco/proposta: {proposta}
- Ramos/canais: entrevistas, landing page, convite para piloto e pré-venda consultiva.
- Frutos/resultado esperado: compromisso observável antes de construção completa.
- Solo/restrições: orçamento baixo, ciclo curto e necessidade de evidência prática.

## Fio de Ariadne
Hipótese crítica → experimento proporcional → evidência observável → decisão executiva.

## Minotauros do risco
1. O problema pode não ser urgente.
2. O canal pode não alcançar decisores reais.
3. O compromisso declarado pode não virar uso, piloto ou pagamento.
"""
    cartao=f"""
# Cartão-Runa de Teste

Runa/sinal buscado: compromisso qualificado, não apenas elogio.
Hipótese: {publico} aceita conversar ou se cadastrar para validar {ideia}.
Público de teste: {publico}
Travessia Bifröst: entrevista-problema + landing page simples + convite para piloto.
Métrica principal: taxa de compromisso qualificado.
Critério de passagem: pelo menos 10 conversas qualificadas e 30% de intenção forte de piloto.
Duração: 7 a 14 dias.
Custo máximo: baixo.
Decisão esperada: avançar se houver compromisso; redesenhar se houver interesse fraco; pivotar se a dor prioritária for outra.
"""
    sprint=f"""
# Plano de Travessia Bifröst — Sprint de Experimentação

## Semana 1 — Preparar a ponte
- Formular pergunta délfica: o que precisa ser verdade para esta ideia sobreviver?
- Preparar roteiro de entrevista-problema.
- Publicar landing page com proposta clara.
- Convidar 20 pessoas do público-alvo.

## Semana 2 — Atravessar e observar runas
- Executar entrevistas.
- Medir cadastros, respostas e compromissos.
- Consolidar cartão das Nornas: premissa anterior, evidência atual, consequência futura.

## Entregável final
Oráculo de Decisão: avançar, pivotar, redesenhar, testar novamente ou abandonar.
"""
    rel=f"""
# Oráculo de Decisão — Modelo

Ideia analisada: {ideia}
Decisão preliminar: consultar o Poço de Mímir antes de construir.

## Evidências necessárias
- Conversas qualificadas com público-alvo.
- Compromisso observável: cadastro, piloto, pré-venda, agenda ou pagamento.
- Comparação entre dor declarada e comportamento real.

## Interpretação das runas
Cliques, elogios e curiosidade são sinais fracos. Compromisso, tempo, pagamento e uso recorrente são sinais mais fortes.

## Próxima travessia
Executar o cartão-runa de teste e revisar evidências antes de investir em desenvolvimento completo.
"""
    write(out/'mapa-labirinto-hipoteses.md', mapa)
    write(out/'cartao-runa-teste.md', cartao)
    write(out/'travessia-bifrost-sprint.md', sprint)
    write(out/'oraculo-de-decisao.md', rel)

def main():
    ap=argparse.ArgumentParser(description='Maeve Athena-Mímir Venture Forge generator')
    ap.add_argument('case_json')
    ap.add_argument('--output', default='output/demo')
    args=ap.parse_args()
    gerar(load_case(args.case_json), Path(args.output))
    print('ATHENA_MIMIR_VENTURE_FORGE_OK')
if __name__=='__main__': main()
