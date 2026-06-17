import unittest

from src.integracao import integral_simpson_3_8, integral_trapezios, integral_simpson_1_3

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

    def test_integral_trapezios_com_dados_do_exercicio(self):
        # Exercicio 6: Distância percorrida por carro elétrico
        v = [0, 40, 65, 80, 90]
        h = 0.5
        
        resultado = integral_trapezios(v, h)
        
        # h/2 * (y0 + 2y1 + 2y2 + 2y3 + y4)
        # = 0.5/2 * (0 + 2*40 + 2*65 + 2*80 + 90)
        # = 0.25 * (0 + 80 + 130 + 160 + 90)
        # = 0.25 * 460 = 115.0
        self.assertAlmostEqual(resultado, 115.0)

    def test_integral_simpson_1_3_com_dados_do_exercicio(self):
        v = [0, 40, 65, 80, 90]
        h = 0.5
        
        resultado = integral_simpson_1_3(v, h)
        
        # h/3 * (y0 + 4y1 + 2y2 + 4y3 + y4)
        # = 0.5/3 * (0 + 4*40 + 2*65 + 4*80 + 90)
        # = (0.5/3) * (0 + 160 + 130 + 320 + 90)
        # = (0.5/3) * 700 = 350 / 3 = 116.66666...
        self.assertAlmostEqual(resultado, 116.66666666666666)

    def test_integral_simpson_1_3_exige_pares_de_intervalos(self):
        # 4 pontos = 3 intervalos (inválido para Simpson 1/3)
        v = [0, 40, 65, 80]
        
        with self.assertRaises(ValueError):
            integral_simpson_1_3(v, 0.5)

if __name__ == "__main__":
    unittest.main()
