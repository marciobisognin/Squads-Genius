"""Demo determinística do PANÓPTES: sela vigílias, força uma retificação e gera o painel."""
from datetime import date
from pathlib import Path
from argos.contracts import PublicacaoNormalizada
from argos.engines.mnemon import Mnemon
from argos.panoptes.ledger import LivroPanoptes
from argos.panoptes.painel import gerar_painel

def _pub(texto: str, hash_conteudo: str) -> PublicacaoNormalizada:
    return PublicacaoNormalizada(id_canonico='dou-2026-07-02-do3-ext-042', fonte='DOU-INLABS', esfera='federal', data_publicacao=date(2026, 7, 2), edicao='124', secao='DO3', orgao='Instituto Federal Farroupilha', tipo_ato='Extrato de Contrato', identifica='Extrato de Contrato nº 42/2026', texto=texto, url_original='https://www.in.gov.br/web/dou/-/extrato-de-contrato-42-2026', hash_conteudo=hash_conteudo)

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    demo = root / 'generated' / 'demo' / 'panoptes'
    runtime = demo / '.argos'
    if (runtime / 'panoptes' / 'livro.jsonl').exists():
        (runtime / 'panoptes' / 'livro.jsonl').unlink()
    if (runtime / 'mnemon.sqlite').exists():
        (runtime / 'mnemon.sqlite').unlink()

    mnemon = Mnemon(runtime / 'mnemon.sqlite')
    mnemon.registrar_publicacao(_pub('EXTRATO DE CONTRATO Nº 42/2026. Contratada: Empresa Alfa Serviços Ltda. Valor global: R$ 1.234.567,89. Vigência: 12 meses a contar de 01/07/2026.', 'a' * 64), agora='2026-07-02T09:00:00+00:00')
    mnemon.registrar_publicacao(_pub('EXTRATO DE CONTRATO Nº 42/2026. Contratada: Empresa Alfa Serviços Ltda. Valor global: R$ 1.834.567,89. Vigência: 18 meses a contar de 01/07/2026.', 'b' * 64), agora='2026-07-03T09:00:00+00:00')

    livro = LivroPanoptes(runtime)
    livro.selar({'run_id': 'argos-2026-07-02-demo0001', 'perfil': 'contratos-iffar-f0', 'data_ref': '2026-07-02', 'corpus_hash': '9f2c' * 16, 'perfil_hash': '11ab' * 16, 'relatorio_hash': '77cd' * 16, 'total_corpus': 12, 'total_relevantes': 3, 'fontes_consultadas': ['DOU-INLABS', 'QD-4305207'], 'retificacoes': []}, selado_em='2026-07-02T09:05:00+00:00')
    livro.selar({'run_id': 'argos-2026-07-03-demo0002', 'perfil': 'contratos-iffar-f0', 'data_ref': '2026-07-03', 'corpus_hash': '3e8d' * 16, 'perfil_hash': '11ab' * 16, 'relatorio_hash': '90ef' * 16, 'total_corpus': 14, 'total_relevantes': 4, 'fontes_consultadas': ['DOU-INLABS', 'QD-4305207', 'DOE-RS'], 'retificacoes': ['dou-2026-07-02-do3-ext-042']}, selado_em='2026-07-03T09:05:00+00:00')

    destino = gerar_painel(demo, output=demo / 'painel-panoptes.html')
    print(f'verificacao: {livro.verificar()}')
    print(f'painel: {destino}')
