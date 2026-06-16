import unittest

from src.integracao import (
    integral_simpson_1_3,
    integral_simpson_3_8,
    integral_trapezios,
    quadratura_gauss,
)

class TestIntegracao(unittest.TestCase):
    def test_integral_trapezios_carro_eletrico(self):
        v = [0, 40, 65, 80, 90]
        h = 0.5
        
        resultado = integral_trapezios(v, h)
        
        # Área exata pela regra dos trapézios com estes dados é 115.0
        self.assertAlmostEqual(resultado, 115.0)

    def test_integral_simpson_1_3_carro_eletrico(self):
        v = [0, 40, 65, 80, 90]
        h = 0.5
        
        resultado = integral_simpson_1_3(v, h)
        
        # Área exata por Simpson 1/3 é aprox 116.666...
        self.assertAlmostEqual(resultado, 116.66666666666667)

    def test_integral_simpson_3_8_servidor(self):
        v = [10, 15, 12, 8]
        h = 2
        
        resultado = integral_simpson_3_8(v, h)
        
        # Área exata por Simpson 3/8 é 74.25
        self.assertAlmostEqual(resultado, 74.25)

    def test_quadratura_gauss_n2_torque_motor(self):
        def f(x):
            return 5*(x**3) + (x**2) - 12*x + 4
            
        resultado = quadratura_gauss(f, -1, 1, 2)
        
        # A integral exata do polinómio no intervalo [-1, 1] é 26/3 (~8.666)
        self.assertAlmostEqual(resultado, 8.666666666666666)
        
    def test_quadratura_gauss_n3_torque_motor(self):
        def f(x):
            return 5*(x**3) + (x**2) - 12*x + 4
            
        resultado = quadratura_gauss(f, -1, 1, 3)
        self.assertAlmostEqual(resultado, 8.666666666666666)

if __name__ == "__main__":
    unittest.main()