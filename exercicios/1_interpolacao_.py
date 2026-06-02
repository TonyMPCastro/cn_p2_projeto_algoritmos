import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.interpolacao import (
    interpolar_gregory_newton,
    interpolar_lagrange,
    interpolar_newton,
)


# Lagrange, Newton e Gregory-Newton
def main():

    #     X     Y
    pontos = [
        (1.0, 1.2),
        (2.0, 1.9),
        (3.0, 3.2),
        (4.0, 5.5),
        (5.0, 8.2),
    ]

    x = 3.5

    resultado_lagrange, operacoes_lagrange = interpolar_lagrange(
        pontos,
        x,
        contar_operacoes=True,
    )

    resultado_newton, operacoes_newton = interpolar_newton(
        pontos,
        x,
        contar_operacoes=True,
    )

    resultado_gregory_newton, operacoes_gregory_newton = interpolar_gregory_newton(
        pontos,
        x,
        contar_operacoes=True,
    )

    print()
    print()
    print("     Sistema de telemetria do drone")
    print()
    print("     Pontos conhecidos (tempo, altitude):", pontos)
    print()
    print("     Tempo com falha no sensor:", x, "segundos")
    print()
    print("         Altitude por Lagrange:", resultado_lagrange, "metros")
    print("             Multiplicacoes:", operacoes_lagrange["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes_lagrange["adicoes"])
    print()
    print("         Altitude por Newton:", resultado_newton, "metros")
    print("             Multiplicacoes:", operacoes_newton["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes_newton["adicoes"])
    print()
    print("         Altitude por Gregory-Newton:", resultado_gregory_newton, "metros")
    print("             Multiplicacoes:", operacoes_gregory_newton["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes_gregory_newton["adicoes"])
    print()

if __name__ == "__main__":
    main()
