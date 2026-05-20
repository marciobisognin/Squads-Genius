#!/usr/bin/env python3
import argparse, json, datetime
from pathlib import Path

CRITERIA = [
    ('clareza_do_problema', 15), ('aderencia_institucional', 10), ('potencial_de_impacto', 15),
    ('viabilidade_tecnica', 15), ('validacao_de_demanda', 15), ('capacidade_da_equipe', 10),
    ('potencial_de_mercado_ou_uso_social', 10), ('riscos_pi_lgpd_regulatorios', 10)
]

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def score(data):
    evid = len(data.get('evidencias', []))
    stage = data.get('estagio','').lower()
    base = {
        'clareza_do_problema': 4 if data.get('problema') else 2,
        'aderencia_institucional': 4 if data.get('publico') else 3,
        'potencial_de_impacto': 4 if 'produtor' in data.get('publico','').lower() or 'regional' in data.get('problema','').lower() else 3,
        'viabilidade_tecnica': 4 if 'protótipo' in stage or 'prototipo' in stage else 3,
        'validacao_de_demanda': min(5, 2 + evid),
        'capacidade_da_equipe': 3,
        'potencial_de_mercado_ou_uso_social': 4,
        'riscos_pi_lgpd_regulatorios': 3,
    }
    total=0
    rows=[]
    for k,w in CRITERIA:
        n=base[k]
        pts=n/5*w
        total+=pts
        rows.append({'criterio':k,'peso':w,'nota_0_5':n,'pontos':round(pts,2)})
    trilha = 'incubação' if total>=75 else 'pré-incubação' if total>=55 else 'sensibilização/ideação'
    return round(total,2), trilha, rows

def generate(args):
    data=load(args.input)
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    total,trilha,rows=score(data)
    now=datetime.datetime.now().isoformat(timespec='seconds')
    (out/'01_mapa_oportunidade.md').write_text(f"""# Mapa da Oportunidade Incubável

**Projeto:** {data.get('nome')}
**Proponente:** {data.get('proponente')}
**Gerado em:** {now}

## Problema
{data.get('problema')}

## Público
{data.get('publico')}

## Solução imaginada
{data.get('solucao')}

## Estágio atual
{data.get('estagio')}

## Evidências existentes
""" + ''.join(f"- {e}\n" for e in data.get('evidencias',[])) + "\n## Trilha recomendada\n" + trilha + "\n", encoding='utf-8')
    (out/'02_matriz_incubabilidade.json').write_text(json.dumps({'score':total,'trilha_recomendada':trilha,'criterios':rows}, ensure_ascii=False, indent=2), encoding='utf-8')
    (out/'03_plano_ideia_ao_produto.md').write_text(f"""# Plano da Ideia ao Produto

## Decisão inicial
Score de incubabilidade: **{total}/100**. Trilha recomendada: **{trilha}**.

## Próximos experimentos
1. Entrevistar 10 potenciais usuários do público-alvo.
2. Executar piloto curto com registro de evidências.
3. Definir MVP com até 5 funcionalidades essenciais.
4. Mapear PI/LGPD/regulação antes de exposição pública.
5. Construir PDE com metas de 30, 60 e 90 dias.

## MVP inicial
- Função principal: demonstrar a solução em ambiente real ou simulado.
- Métrica de sucesso: usuário compreende valor e aceita testar/pagar/adotar.
- Evidência mínima: relatório de teste, feedbacks e indicadores.

## Produto final esperado
Solução validada, protótipo demonstrável, modelo de sustentabilidade, PDE e dossiê para banca/demo.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
""", encoding='utf-8')
    print(json.dumps({'ok':True,'output':str(out),'score':total,'trilha':trilha}, ensure_ascii=False))

def main():
    ap=argparse.ArgumentParser(description='Germina360 CLI')
    sub=ap.add_subparsers(dest='cmd', required=True)
    g=sub.add_parser('generate-demo')
    g.add_argument('--input', required=True)
    g.add_argument('--output', required=True)
    args=ap.parse_args()
    if args.cmd=='generate-demo': generate(args)
if __name__=='__main__': main()
