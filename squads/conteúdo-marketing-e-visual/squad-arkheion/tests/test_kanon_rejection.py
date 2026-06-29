#!/usr/bin/env python3
"""Testes do KÁNŌN — specs FORA do Cânone DEVEM falhar (PRD §15 F0).

    python3 -m unittest tests.test_kanon_rejection -v
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import kanon  # noqa: E402


class TestKanonAceita(unittest.TestCase):
    def test_grade_canonica_passa(self):
        from arkheion import canon
        self.assertEqual(kanon.validar_grade(canon.GRADE_FFMPEG), [])

    def test_card_exemplo_passa(self):
        card = json.loads((ROOT / "examples" / "card_interface_tecnologia.json").read_text(encoding="utf-8"))
        self.assertEqual(kanon.validar_card(card, total_cenas=6), [])

    def test_plano_exemplo_passa(self):
        plano = json.loads((ROOT / "examples" / "plano_sequencial_tecnologia.json").read_text(encoding="utf-8"))
        self.assertEqual(kanon.validar_plano(plano, tamanho_s=60), [])

    def test_footage_exemplo_passa(self):
        spec = json.loads((ROOT / "examples" / "footage_spec_tecnologia.json").read_text(encoding="utf-8"))
        self.assertEqual(kanon.validar_footage(spec), [])


class TestKanonReprova(unittest.TestCase):
    def test_titulo_minusculo_reprova(self):
        card = {"contador": "01 / 06", "titulo": "o problema", "linhas_texto": ["x"],
                "rodape": "m", "metadados_topo_esq": "m"}
        self.assertTrue(any("CAIXA ALTA" in m for m in kanon.validar_card(card)))

    def test_titulo_longo_reprova(self):
        card = {"contador": "01 / 06", "titulo": "UM TÍTULO COM CINCO PALAVRAS AQUI",
                "linhas_texto": ["x"], "rodape": "m", "metadados_topo_esq": "m"}
        self.assertTrue(any("palavras" in m for m in kanon.validar_card(card)))

    def test_contador_invalido_reprova(self):
        card = {"contador": "1/6", "titulo": "TESTE", "linhas_texto": ["x"],
                "rodape": "m", "metadados_topo_esq": "m"}
        self.assertTrue(any("contador" in m for m in kanon.validar_card(card)))

    def test_fonte_proibida_reprova(self):
        card = {"contador": "01 / 06", "titulo": "TESTE", "linhas_texto": ["x"],
                "rodape": "m", "metadados_topo_esq": "m", "fonte_titulo": "Comic Sans"}
        self.assertTrue(any("fonte" in m for m in kanon.validar_card(card)))

    def test_grade_fora_da_faixa_reprova(self):
        grade_ruim = "eq=contrast=2.0:saturation=0.9,noise=alls=2"
        motivos = kanon.validar_grade(grade_ruim)
        self.assertTrue(any("contraste" in m for m in motivos))
        self.assertTrue(any("saturação" in m for m in motivos))
        self.assertTrue(any("vinheta" in m for m in motivos))

    def test_footage_com_neon_reprova(self):
        spec = {"plano": "close", "movimento": "push_lento",
                "prompt_positivo": "cena com neon e holograma 3D", "duracao_s": 10}
        self.assertTrue(any("proibida" in m for m in kanon.validar_footage(spec)))

    def test_plano_com_contador_errado_reprova(self):
        plano = json.loads((ROOT / "examples" / "plano_sequencial_tecnologia.json").read_text(encoding="utf-8"))
        plano["beats"][0]["contador"] = "01 / 09"  # incoerente com 60s/6 cenas
        self.assertTrue(kanon.validar_plano(plano, tamanho_s=60))

    def test_prova_visual_sem_dataviz_reprova(self):
        plano = json.loads((ROOT / "examples" / "plano_sequencial_tecnologia.json").read_text(encoding="utf-8"))
        plano["beats"][4].pop("dataviz", None)
        self.assertTrue(any("dataviz" in m for m in kanon.validar_plano(plano, tamanho_s=60)))


if __name__ == "__main__":
    unittest.main()

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
