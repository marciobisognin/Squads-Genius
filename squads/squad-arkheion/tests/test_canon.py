#!/usr/bin/env python3
"""Testes do Cânone — garantem hex, geometria, timing e resolução de duração.

Rodam com unittest (stdlib), sem dependências externas.
    python3 -m unittest tests.test_canon -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from arkheion import canon  # noqa: E402


class TestCanon(unittest.TestCase):
    def test_hex_exatos(self):
        self.assertEqual(canon.PALETA_UI["glow"], "#94E4F2")
        self.assertEqual(canon.PALETA_CINE["black"], "#020406")
        self.assertIn("#EDF8F8", canon.HEX_PERMITIDOS)

    def test_timing_canonico(self):
        self.assertEqual(canon.TIMING.fps, 24)
        self.assertEqual(canon.TIMING.cena_s, 10)
        self.assertEqual(canon.TIMING.frames_por_cena, 240)
        self.assertEqual(canon.VELOCIDADE_DIGITACAO_CPS, 25)

    def test_geometria_escala(self):
        g2 = canon.GEOMETRIA.escala(2)
        self.assertEqual(g2.base, 2160)
        self.assertEqual(g2.margem_lateral, 160)

    def test_resolver_duracao_presets(self):
        for alvo, n in [(30, 3), (60, 6), (90, 9)]:
            pd = canon.resolver_duracao(alvo)
            self.assertEqual(pd.n_cenas, n)
            self.assertEqual(len(pd.contadores), n)
            self.assertEqual(pd.contadores[0], f"01 / {n:02d}")
            self.assertEqual(pd.contadores[-1], f"{n:02d} / {n:02d}")

    def test_duracao_60_eh_canonica(self):
        pd = canon.resolver_duracao(60)
        self.assertEqual(list(pd.funcoes), canon.FUNCOES_NARRATIVAS_6)

    def test_duracao_sempre_comeca_e_fecha(self):
        for alvo in (30, 60, 90):
            pd = canon.resolver_duracao(alvo)
            self.assertEqual(pd.funcoes[0], "pergunta_tensao")
            self.assertEqual(pd.funcoes[-1], "conclusao_cta")

    def test_duracao_invalida(self):
        with self.assertRaises(ValueError):
            canon.resolver_duracao(45)   # não múltiplo de 10
        with self.assertRaises(ValueError):
            canon.resolver_duracao(120)  # > 90s / 9 cenas

    def test_ancoras_por_tema(self):
        self.assertIn("servidores", canon.ancoras_para_tema("tecnologia"))
        self.assertIn("livros antigos", canon.ancoras_para_tema("educação e história"))
        self.assertTrue(canon.ancoras_para_tema("tema desconhecido"))  # fallback não vazio


if __name__ == "__main__":
    unittest.main()

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
