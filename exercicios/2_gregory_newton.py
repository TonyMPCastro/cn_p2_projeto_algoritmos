import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.interpolacao import interpolar_gregory_newton


# Gregory-Newton
def main():

    #     X       Y
    pontos = [
        (10, 45.0),
        (20, 52.0),
        (30, 60.0),
        (40, 71.0),
    ]

    x = 25
    h = 10

    resultado, operacoes = interpolar_gregory_newton(
        pontos,
        x,
        h,
        contar_operacoes=True,
    )

    print()
    print()
    print("     Sistema de resfriamento do servidor")
    print()
    print("     Pontos conhecidos (minuto, temperatura):", pontos)
    print()
    print("     Intervalo constante h:", h, "minutos")
    print()
    print("     Minuto para estimar:", x)
    print()
    print("         Temperatura por Gregory-Newton:", resultado, "C")
    print("             Multiplicacoes:", operacoes["multiplicacoes"])
    print("             Adicoes/subtracoes:", operacoes["adicoes"])
    print()


if __name__ == "__main__":
    main()
