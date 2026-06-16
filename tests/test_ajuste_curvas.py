import unittest

from src.ajuste_curvas import ajuste_linear_mmq

class TestAjusteCurvas(unittest.TestCase):
    def test_ajuste_linear_mmq_deinf(self):
        pontos = [(8, 2.1), (9, 2.8), (10, 3.1), (11, 4.0), (12, 4.8)]

        a, b = ajuste_linear_mmq(pontos)

        # Baseado nos cálculos exatos: a = 0.66 e b = -3.24
        self.assertAlmostEqual(a, 0.66)
        self.assertAlmostEqual(b, -3.24)

    def test_ajuste_linear_mmq_com_contagem_de_operacoes(self):
        pontos = [(8, 2.1), (9, 2.8), (10, 3.1), (11, 4.0), (12, 4.8)]

        a, b, operacoes = ajuste_linear_mmq(pontos, contar_operacoes=True)

        self.assertAlmostEqual(a, 0.66)
        self.assertAlmostEqual(b, -3.24)
        self.assertIn("multiplicacoes", operacoes)
        self.assertIn("adicoes", operacoes)

    def test_ajuste_linear_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            ajuste_linear_mmq([(1, 1)])

if __name__ == "__main__":
    unittest.main()