import unittest

from src.ajuste_curvas import ajuste_linear_mmq

class TestAjusteCurvas(unittest.TestCase):
    def test_ajuste_linear_mmq_com_pontos_do_exercicio(self):
        # x (hora), y (acessos)
        pontos = [
            (8, 2.1),
            (9, 2.8),
            (10, 3.1),
            (11, 4.0),
            (12, 4.8),
        ]
        
        a, b = ajuste_linear_mmq(pontos)
        
        # Testando valores conhecidos baseados no exercicio 4
        # P1(x) = 0.66x - 3.24
        self.assertAlmostEqual(a, 0.66)
        self.assertAlmostEqual(b, -3.24)
        
    def test_ajuste_linear_mmq_com_contagem_de_operacoes(self):
        pontos = [
            (8, 2.1),
            (9, 2.8),
            (10, 3.1),
            (11, 4.0),
            (12, 4.8),
        ]
        
        a, b, operacoes = ajuste_linear_mmq(pontos, contar_operacoes=True)
        
        self.assertAlmostEqual(a, 0.66)
        self.assertAlmostEqual(b, -3.24)
        self.assertEqual(
            operacoes,
            {
                "multiplicacoes": 16,
                "adicoes": 23,
            },
        )
        
    def test_ajuste_linear_mmq_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            ajuste_linear_mmq([(1, 1)])

    def test_ajuste_linear_mmq_rejeita_reta_vertical(self):
        # Pontos alinhados verticalmente causarão divisão por zero
        pontos = [(1, 2), (1, 3)]
        
        with self.assertRaises(ValueError):
            ajuste_linear_mmq(pontos)

if __name__ == "__main__":
    unittest.main()
