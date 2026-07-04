from pathlib import Path
from argos.ophthalmoi.dou_inlabs import parse_article
from argos.engines.tekmerion import excerto_literal

def test_excerto_literal():
    pub = parse_article(Path('tests/fixtures/dou_inlabs/2026-07-02-do3-iffar.xml').read_text(encoding='utf-8'))
    assert excerto_literal(pub, 'Instituto Federal Farroupilha - IFFar torna público')
    assert not excerto_literal(pub, 'frase fabricada pelo modelo')
