import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.interpolacao import (
    interpolar_lagrange,
    interpolar_newton,
)


# Lagrange e Newton
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

    resultado_lagrange = interpolar_lagrange(pontos, x)

    resultado_newton = interpolar_newton(pontos, x)

    print()
    print()
    print("     Sistema de telemetria do drone")
    print()
    print("     Pontos conhecidos (tempo, altitude):", pontos)
    print()
    print("     Tempo com falha no sensor:", x, "segundos")
    print()
    print("         Altitude por Lagrange:", resultado_lagrange, "metros")
    print()
    print("         Altitude por Newton:", resultado_newton, "metros")
    print()

if __name__ == "__main__":
    main()
