#!/usr/bin/env python3
import argparse, json, csv
from pathlib import Path

FOOT = 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.'

def norm(s):
    return (s or '').lower()

def main():
    ap = argparse.ArgumentParser(description='Demo operacional do Trajetória Evidenciada Squad')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / '03_revisao_manual').mkdir(exist_ok=True)
    (out / 'processo_final').mkdir(exist_ok=True)

    servidor = data.get('servidor') or {}
    pend = []
    for key in ['nome_completo', 'rsc_pretendido']:
        if not servidor.get(key):
            pend.append(key)
    servidor['pendencias'] = pend
    servidor['fonte_dados'] = 'demo_input_ou_usuario'
    (out / '00_dados_servidor.json').write_text(json.dumps(servidor, ensure_ascii=False, indent=2), encoding='utf-8')

    docs = data.get('documentos', [])
    with (out / '01_catalogo_documentos.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id_documento','arquivo_origem','paginas','tipo','numero','data','assunto','emissor','confianca','status'])
        for i, d in enumerate(docs, 1):
            conf = 'baixa' if d.get('tipo') in ('indefinido','outro','') or not d.get('data') else 'alta'
            status = 'revisao_manual' if conf == 'baixa' else 'classificado'
            w.writerow([f'Doc. {i:02d}', d.get('arquivo',''), d.get('paginas','1'), d.get('tipo','indefinido'), d.get('numero',''), d.get('data',''), d.get('assunto',''), d.get('emissor',''), conf, status])
            if status == 'revisao_manual':
                review = f"""# Documento para revisão manual

Arquivo: {d.get('arquivo')}

Motivo: metadados insuficientes ou classificação insegura.

{FOOT}
"""
                (out / '03_revisao_manual' / f'Doc_{i:02d}_revisar.md').write_text(review, encoding='utf-8')

    used = set()
    total = 0.0
    with (out / '02_matriz_pontuacao.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['criterio','descricao','pontos_maximos','documento_vinculado','pontos_sugeridos','justificativa','status'])
        for c in data.get('criterios', []):
            best = None
            best_score = -1
            for i, d in enumerate(docs, 1):
                if i in used:
                    continue
                text = norm(' '.join([d.get('tipo',''), d.get('assunto',''), d.get('texto','')]))
                score = sum(1 for kw in c.get('palavras_chave', []) if norm(kw) in text)
                if score > best_score:
                    best = (i, d, score)
                    best_score = score
            if best and best_score > 0:
                i, d, score = best
                used.add(i)
                pts = float(c.get('pontos', 0))
                total += pts
                w.writerow([c.get('criterio'), c.get('criterio'), c.get('pontos'), f'Doc. {i:02d}', pts, 'Enquadramento demonstrativo por palavras-chave e uso único do documento.', 'sugerido_para_revisao'])
            else:
                w.writerow([c.get('criterio'), c.get('criterio'), c.get('pontos'), '', '0', 'Nenhum documento identificado com segurança.', 'revisao_manual'])

    memorial = f"""# Memorial descritivo — versão demonstrativa

Eu, {servidor.get('nome_completo','[NOME DO SERVIDOR]')}, apresento este memorial como uma narrativa da minha trajetória profissional e dos saberes e competências desenvolvidos no exercício do meu cargo.

Ao longo da minha atuação institucional, participei de atividades que ampliaram minha compreensão sobre planejamento, responsabilidade administrativa, cooperação em equipes e contribuição para o funcionamento da instituição. Essas experiências não se limitam ao cumprimento formal de tarefas; elas revelam um percurso de aprendizagem prática, amadurecimento profissional e construção de competências aplicadas ao serviço público.

A participação em comissões e atividades institucionais contribuiu para que eu desenvolvesse visão sistêmica sobre processos, tomada de decisão, organização de rotinas e articulação entre diferentes setores (Doc. 01). Da mesma forma, as capacitações realizadas fortaleceram minha capacidade de qualificar o trabalho cotidiano, atualizar procedimentos e aprimorar a entrega institucional (Doc. 02).

Este memorial não pretende ser uma simples listagem de documentos. Os documentos anexados servem como lastro objetivo para demonstrar uma trajetória de trabalho, aprendizagem e contribuição, indicando como os saberes adquiridos foram mobilizados em benefício da instituição.

{FOOT}
"""
    (out / '04_memorial_primeira_pessoa.md').write_text(memorial, encoding='utf-8')

    ordem = f"""# Ordem sugerida do processo RSC

1. Capa do processo.
2. Dados do servidor.
3. Planilha/matriz de pontuação.
4. Memorial descritivo em primeira pessoa.
5. Documentos comprobatórios organizados pela matriz.
6. Pasta de revisão manual, se houver.
7. Relatório de auditoria.

Pontuação demonstrativa sugerida: {total}

{FOOT}
"""
    (out / '05_ordem_processo.md').write_text(ordem, encoding='utf-8')

    auditoria = f"""# Relatório de auditoria RSC

## Resultado demonstrativo
- Documentos analisados: {len(docs)}
- Pontuação demonstrativa sugerida: {total}
- Documentos em revisão manual: {len(list((out / '03_revisao_manual').glob('*.md')))}

## Alertas
- Esta saída é demonstrativa e precisa ser revisada pelo usuário.
- A pontuação depende da planilha/norma oficial indicada.
- O processo final deve ser conferido antes de protocolo.

{FOOT}
"""
    (out / '06_relatorio_auditoria.md').write_text(auditoria, encoding='utf-8')
    print(json.dumps({'ok': True, 'output': str(out), 'pontuacao_demo': total}, ensure_ascii=False))

if __name__ == '__main__':
    main()
