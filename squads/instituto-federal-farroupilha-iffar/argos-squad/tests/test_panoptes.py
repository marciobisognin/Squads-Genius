import json
from datetime import date
from pathlib import Path
from argos.contracts import PublicacaoNormalizada
from argos.engines.mnemon import Mnemon
from argos.graph import ArgosPipeline
from argos.panoptes.ledger import GENESIS, LivroPanoptes
from argos.panoptes.painel import UF_GRID, gerar_painel
from argos.panoptes.retificacao import diff_textos, relatorio_retificacoes


def _pub(texto: str, hash_conteudo: str) -> PublicacaoNormalizada:
    return PublicacaoNormalizada(id_canonico='dou-2026-07-02-do3-x1', fonte='DOU-INLABS', esfera='federal', data_publicacao=date(2026, 7, 2), edicao='124', secao='DO3', orgao='IFFar', tipo_ato='Extrato de Contrato', texto=texto, url_original='https://www.in.gov.br/web/dou/-/x1', hash_conteudo=hash_conteudo)


def test_livro_sela_encadeia_e_verifica(tmp_path):
    livro = LivroPanoptes(tmp_path)
    e1 = livro.selar({'run_id': 'r1', 'corpus_hash': 'aaa'}, selado_em='2026-07-02T00:00:00+00:00')
    e2 = livro.selar({'run_id': 'r2', 'corpus_hash': 'bbb'}, selado_em='2026-07-03T00:00:00+00:00')
    assert e1['anterior'] == GENESIS and e2['anterior'] == e1['selo']
    veredito = livro.verificar()
    assert veredito == {'integro': True, 'total': 2, 'quebra_seq': None, 'motivo': 'cadeia íntegra do gênesis ao último selo'}


def test_livro_detecta_adulteracao(tmp_path):
    livro = LivroPanoptes(tmp_path)
    livro.selar({'run_id': 'r1', 'corpus_hash': 'aaa'})
    livro.selar({'run_id': 'r2', 'corpus_hash': 'bbb'})
    linhas = livro.path.read_text(encoding='utf-8').splitlines()
    adulterada = json.loads(linhas[0]); adulterada['corpus_hash'] = 'zzz'
    livro.path.write_text(json.dumps(adulterada, ensure_ascii=False) + '\n' + linhas[1] + '\n', encoding='utf-8')
    veredito = livro.verificar()
    assert veredito['integro'] is False and veredito['quebra_seq'] == 1


def test_retificacao_detecta_numeros_alterados(tmp_path):
    mnemon = Mnemon(tmp_path / 'mnemon.sqlite')
    assert mnemon.registrar_publicacao(_pub('Valor global: R$ 1.234,56. Vigência: 12 meses.', 'h1')) == 'nova'
    assert mnemon.registrar_publicacao(_pub('Valor global: R$ 9.876,54. Vigência: 12 meses.', 'h2')) == 'retificacao'
    dossies = relatorio_retificacoes(mnemon)
    assert len(dossies) == 1
    assert '1.234,56' in dossies[0]['numeros_removidos']
    assert '9.876,54' in dossies[0]['numeros_adicionados']
    assert any(l.startswith('-Valor global') for l in dossies[0]['diff'])


def test_diff_sem_mudanca_numerica():
    resultado = diff_textos('Contrato com a empresa Alfa.', 'Contrato com a empresa Beta.')
    assert resultado['numeros_removidos'] == [] and resultado['numeros_adicionados'] == []
    assert any(l.startswith('+Contrato com a empresa Beta') for l in resultado['diff'])


def test_pipeline_sela_run_no_livro(tmp_path):
    import shutil
    root = tmp_path / 'squad'
    for pasta in ['perfis', 'tests']:
        shutil.copytree(Path(pasta), root / pasta)
    result = ArgosPipeline(root).run(root / 'perfis' / 'contratos-iffar-f0.yaml', date(2026, 7, 2), output_dir=tmp_path / 'out', fixture=True)
    assert result.selo_seq == 1 and result.selo
    veredito = LivroPanoptes(root / '.argos').verificar()
    assert veredito['integro'] is True and veredito['total'] == 1
    md = Path(result.markdown_path).read_text(encoding='utf-8')
    assert 'retificações detectadas: 0' in md


def test_painel_gera_html_autocontido(tmp_path):
    mnemon = Mnemon(tmp_path / '.argos' / 'mnemon.sqlite')
    mnemon.registrar_publicacao(_pub('Valor global: R$ 100,00.', 'h1'))
    mnemon.registrar_publicacao(_pub('Valor global: R$ 200,00.', 'h2'))
    LivroPanoptes(tmp_path / '.argos').selar({'run_id': 'r1', 'corpus_hash': 'aaa', 'total_corpus': 3, 'total_relevantes': 1, 'fontes_consultadas': ['DOU-INLABS'], 'retificacoes': ['dou-2026-07-02-do3-x1']})
    destino = gerar_painel(tmp_path)
    html = destino.read_text(encoding='utf-8')
    assert len(UF_GRID) == 27
    assert 'CADEIA ÍNTEGRA' in html
    assert 'Radar de retificações' in html and '200,00' in html
    assert all(f'>{uf}<' in html for uf in UF_GRID)
    assert '<script src' not in html and '@import' not in html  # autocontido: sem recursos externos
