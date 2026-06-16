import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.interpolacao import interpolar_spline_cubica, interpolar_spline_linear


# Spline Linear e Spline Cubica Natural
def main():

    #     t (seg)   y (posicao em cm)
    pontos = [
        (0.0, 2.5),
        (1.0, 4.5),
        (2.0, 3.0),
        (3.0, 6.0),
    ]

    t = 1.5

    resultado_linear, operacoes_linear = interpolar_spline_linear(
        pontos,
        t,
        contar_operacoes=True,
    )

    resultado_cubica, operacoes_cubica = interpolar_spline_cubica(
        pontos,
        t,
        contar_operacoes=True,
    )

    print()
    print()
    print("     Braco robotico da cortadora a laser")
    print()
    print("     Keyframes conhecidos (tempo em seg, posicao em cm):", pontos)
    print()
    print("     Instante para interpolar:", t, "segundos")
    print()
    print("         Posicao por Spline Linear:", resultado_linear, "cm")
    print("             Multiplicacoes:", operacoes_linear["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes_linear["adicoes"])
    print()
    print("         Posicao por Spline Cubica Natural:", resultado_cubica, "cm")
    print("             Multiplicacoes:", operacoes_cubica["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes_cubica["adicoes"])
    print()


if __name__ == "__main__":
    main()