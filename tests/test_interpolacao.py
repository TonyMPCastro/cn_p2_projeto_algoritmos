import unittest

from src.interpolacao import (
    interpolar_gregory_newton,
    interpolar_lagrange,
    interpolar_newton,
    interpolar_spline_cubica,
    interpolar_spline_linear,
)

class TestInterpolacao(unittest.TestCase):
    def test_interpolar_lagrange_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_lagrange(pontos, 2.5)

        self.assertAlmostEqual(resultado, 6.25)

    def test_interpolar_lagrange_com_contagem_de_operacoes(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado, operacoes = interpolar_lagrange(
            pontos,
            2.5,
            contar_operacoes=True,
        )

        self.assertAlmostEqual(resultado, 6.25)
        self.assertEqual(
            operacoes,
            {
                "multiplicacoes": 6,
                "adicoes": 15,
            },
        )

    def test_interpolar_newton_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_newton(pontos, 2.5)

        self.assertAlmostEqual(resultado, 6.25)

    def test_interpolar_newton_com_contagem_de_operacoes(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado, operacoes = interpolar_newton(
            pontos,
            2.5,
            contar_operacoes=True,
        )

        self.assertAlmostEqual(resultado, 6.25)
        self.assertEqual(
            operacoes,
            {
                "multiplicacoes": 4,
                "adicoes": 10,
            },
        )

    def test_interpolar_gregory_newton_progressivo_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_gregory_newton(pontos, 1.5, 1)

        self.assertAlmostEqual(resultado, 2.25)

    def test_interpolar_gregory_newton_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_gregory_newton(pontos, 2.5, 1)

        self.assertAlmostEqual(resultado, 6.25)

    def test_interpolar_gregory_newton_com_contagem_de_operacoes(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado, operacoes = interpolar_gregory_newton(
            pontos,
            2.5,
            1,
            contar_operacoes=True,
        )

        self.assertAlmostEqual(resultado, 6.25)
        self.assertEqual(
            operacoes,
            {
                "multiplicacoes": 4,
                "adicoes": 8,
            },
        )

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
        resultado_gregory_newton = interpolar_gregory_newton(pontos, 3.5, 1.0)

        self.assertAlmostEqual(resultado_lagrange, 4.2390625)
        self.assertAlmostEqual(resultado_newton, 4.2390625)
        self.assertAlmostEqual(resultado_gregory_newton, 4.2390625)

    def test_interpolacao_do_servidor_por_gregory_newton(self):
        pontos = [
            (10, 45.0),
            (20, 52.0),
            (30, 60.0),
            (40, 71.0),
        ]

        resultado = interpolar_gregory_newton(pontos, 25, 10)

        self.assertAlmostEqual(resultado, 55.75)

    def test_interpolar_lagrange_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            interpolar_lagrange([(1, 1)], 2)

    def test_interpolar_lagrange_rejeita_x_repetido(self):
        pontos = [(1, 1), (1, 2), (2, 4)]

        with self.assertRaises(ValueError):
            interpolar_lagrange(pontos, 1.5)

    def test_interpolar_gregory_newton_rejeita_espacamento_irregular(self):
        pontos = [(1, 1), (2, 4), (4, 16)]

        with self.assertRaises(ValueError):
            interpolar_gregory_newton(pontos, 2.5, 1)

    def test_interpolar_gregory_newton_rejeita_h_incorreto(self):
        pontos = [(10, 45.0), (20, 52.0), (30, 60.0), (40, 71.0)]

        with self.assertRaises(ValueError):
            interpolar_gregory_newton(pontos, 25, 5)

    def test_interpolar_spline_linear_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_spline_linear(pontos, 2.5)

        # Linear entre (2,4) e (3,9): 4 + (9-4)/(3-2) * (2.5-2) = 6.5
        self.assertAlmostEqual(resultado, 6.5)

    def test_interpolar_spline_cubica_com_parabola(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        resultado = interpolar_spline_cubica(pontos, 2.5)

        # Spline cubica natural com condicao S''=0 nas extremidades.
        self.assertAlmostEqual(resultado, 6.3125)

    def test_interpolacao_do_braco_robotico(self):
        pontos = [
            (0.0, 2.5),
            (1.0, 4.5),
            (2.0, 3.0),
            (3.0, 6.0),
        ]

        resultado_linear = interpolar_spline_linear(pontos, 1.5)
        resultado_cubica = interpolar_spline_cubica(pontos, 1.5)

        # Linear entre (1.0, 4.5) e (2.0, 3.0): 4.5 + (3.0-4.5)/(2.0-1.0) * 0.5 = 3.75
        self.assertAlmostEqual(resultado_linear, 3.75)

        # Cubica natural deve ser diferente da linear (movimento suave).
        self.assertNotAlmostEqual(resultado_cubica, resultado_linear, places=2)

    def test_spline_linear_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            interpolar_spline_linear([(1, 1)], 1)

    def test_spline_cubica_exige_dois_pontos(self):
        with self.assertRaises(ValueError):
            interpolar_spline_cubica([(1, 1)], 1)

    def test_spline_linear_x_fora_do_intervalo(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        with self.assertRaises(ValueError):
            interpolar_spline_linear(pontos, 5)

    def test_spline_cubica_x_fora_do_intervalo(self):
        pontos = [(1, 1), (2, 4), (3, 9)]

        with self.assertRaises(ValueError):
            interpolar_spline_cubica(pontos, 0)

if __name__ == "__main__":
    unittest.main()
