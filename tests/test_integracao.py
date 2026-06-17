import unittest

from src.integracao import integral_simpson_3_8

class TestIntegracao(unittest.TestCase):
    def test_integral_simpson_3_8_com_dados_do_exercicio(self):
        # Exercicio 5: Transferencia de servidor
        v = [10, 15, 12, 8]
        h = 2
        
        resultado = integral_simpson_3_8(v, h)
        
        # 3*h/8 * (y0 + 3y1 + 3y2 + y3)
        # = 3*2/8 * (10 + 3*15 + 3*12 + 8)
        # = 6/8 * (10 + 45 + 36 + 8)
        # = 0.75 * 99 = 74.25
        self.assertAlmostEqual(resultado, 74.25)
        
    def test_integral_simpson_3_8_com_contagem_de_operacoes(self):
        v = [10, 15, 12, 8]
        h = 2
        
        resultado, operacoes = integral_simpson_3_8(v, h, contar_operacoes=True)
        
        self.assertAlmostEqual(resultado, 74.25)
        self.assertEqual(
            operacoes,
            {
                "multiplicacoes": 5,
                "adicoes": 3,
            },
        )
        
    def test_integral_simpson_3_8_exige_multiplos_de_tres_intervalos(self):
        # 3 pontos = 2 intervalos (inválido para Simpson 3/8)
        v = [10, 15, 12]
        
        with self.assertRaises(ValueError):
            integral_simpson_3_8(v, 2)

if __name__ == "__main__":
    unittest.main()
