import unittest

from src.interpolacao import (
    interpolar_lagrange,
    interpolar_newton,
)

class TestInterpolacao(unittest.TestCase):
    def test_interpolar_lagrange_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_lagrange(pontos, 2.5)

        self.assertAlmostEqual(resultado, 6.25)

    def test_interpolar_newton_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_newton(pontos, 2.5)

        self.assertAlmostEqual(resultado, 6.25)

    def test_interpolacao_do_drone(self):
        pontos = [
            (1.0, 1.2),
            (2.0, 1.9),
            (3.0, 3.2),
            (4.0, 5.5),
            (5.0, 8.2),
        ]

        resultado_lagrange = interpolar_lagrange(pontos, 3.5)
        resultado_newton = interpolar_newton(pontos, 3.5)

        self.assertAlmostEqual(resultado_lagrange, 4.2390625)
        self.assertAlmostEqual(resultado_newton, 4.2390625)

    def test_interpolar_lagrange_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            interpolar_lagrange([(1, 1)], 2)

    def test_interpolar_lagrange_rejeita_x_repetido(self):
        pontos = [(1, 1), (1, 2), (2, 4)]

        with self.assertRaises(ValueError):
            interpolar_lagrange(pontos, 1.5)

if __name__ == "__main__":
    unittest.main()
