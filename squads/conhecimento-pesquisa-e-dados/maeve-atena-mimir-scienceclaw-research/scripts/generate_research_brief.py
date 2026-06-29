#!/usr/bin/env python3
import argparse, csv, json, re
from pathlib import Path
from datetime import datetime

def parse_simple_yaml(path):
    data={}
    current=None
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line=raw.rstrip()
        if not line or line.strip().startswith('#'): continue
        if re.match(r'^[A-Za-z_]+:', line):
            k,v=line.split(':',1); k=k.strip(); v=v.strip().strip('"')
            if v:
                data[k]=v; current=None
            else:
                data[k]=[]; current=k
        elif current and line.strip().startswith('-'):
            data[current].append(line.strip()[1:].strip().strip('"'))
    return data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    data=parse_simple_yaml(args.input)
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    tema=data.get('tema','Tema não informado')
    pergunta=data.get('pergunta','Pergunta não informada')
    bases=data.get('bases_sugeridas',[])
    now=datetime.now().strftime('%Y-%m-%d %H:%M')
    metodologia=f"""# Metodologia de busca — demo

- Tema: {tema}
- Pergunta: {pergunta}
- Público: {data.get('publico','não informado')}
- Produto: {data.get('produto','não informado')}
- Profundidade: {data.get('profundidade','demo')}
- Data de geração: {now}

## Bases sugeridas
{chr(10).join('- '+b for b in bases)}

## Nota
Este arquivo é uma demonstração operacional. Em execução real, as bases devem ser consultadas por ferramentas externas e os resultados inseridos na matriz com rastreabilidade.
"""
    (out/'metodologia_busca.md').write_text(metodologia, encoding='utf-8')
    rows=[
        ['E1','Fonte demonstrativa 1','não verificado','ano não verificado','artigo/base acadêmica sugerida',bases[0] if bases else 'base sugerida','URL pendente','DOI pendente','não verificado','Potencial pedagógico deve ser confirmado por busca real','Demo sem consulta externa'],
        ['E2','Fonte demonstrativa 2','não verificado','ano não verificado','revisão/relatório sugerido',bases[1] if len(bases)>1 else 'base sugerida','URL pendente','DOI pendente','não verificado','Riscos e vieses exigem fontes primárias','Demo sem consulta externa'],
    ]
    with (out/'matriz_evidencias.csv').open('w', newline='', encoding='utf-8') as f:
        wr=csv.writer(f); wr.writerow(['id','titulo','autores','ano','tipo_fonte','base','url','doi_ou_identificador','status_verificacao','achado_principal','limitacoes']); wr.writerows(rows)
    rel=f"""# Relatório de Pesquisa — demonstração

## Pergunta de pesquisa
{pergunta}

## Síntese executiva
Este relatório demonstra o funcionamento estrutural do squad Maeve Atena Mimir. Ele não substitui uma busca real em bases acadêmicas; sua função é gerar o pacote mínimo de saída para validação do workflow.

## Achados preliminares
- O tema exige busca em bases acadêmicas e educacionais.
- Toda referência deve ser marcada como verificada, parcialmente verificada ou não verificada.
- A matriz de evidências deve separar achados empíricos, revisões e literatura cinzenta.

## Lacunas e agenda
- Levantar estudos empíricos recentes.
- Separar evidências por etapa da educação básica.
- Avaliar riscos: privacidade, plágio, dependência cognitiva, viés e desigualdade de acesso.

## Referências
Nenhuma referência real foi inserida nesta demo. Status: não verificado.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
    (out/'relatorio_pesquisa.md').write_text(rel, encoding='utf-8')
    (out/'referencias_verificadas.md').write_text('# Referências verificadas\n\nDemo: nenhuma referência real verificada.\n', encoding='utf-8')
    (out/'lacunas_e_agenda.md').write_text('# Lacunas e agenda\n\n- Executar busca real.\n- Validar fontes.\n- Construir síntese crítica final.\n', encoding='utf-8')
    (out/'reflexao_pos_tarefa.md').write_text('# Reflexão pós-tarefa\n\nA demo validou a estrutura de arquivos; próxima execução deve integrar busca acadêmica real.\n', encoding='utf-8')
    manifest={'ok': True, 'squad':'Maeve Atena Mimir', 'tema':tema, 'outputs':[p.name for p in sorted(out.iterdir()) if p.is_file()]}
    (out/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False))
if __name__=='__main__': main()
