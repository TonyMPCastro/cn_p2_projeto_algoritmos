import os
import sys


RAIZ_DO_PROJETO = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.integracao import quadratura_gauss


def f_torque(x):
    return 5 * (x ** 3) + (x ** 2) - 12 * x + 4


def main():
    a = -1
    b = 1
    n_pontos = 2

    resultado, operacoes = quadratura_gauss(
        f_torque,
        a,
        b,
        n_pontos,
        contar_operacoes=True
    )

    print()
    print("     Cálculo de trabalho do motor (Gauss)")
    print("     Função: f(x) = 5x³ + x² - 12x + 4")
    print(f"     Limites: a={a}, b={b} utilizando n={n_pontos}")
    print()
    print(f"         Trabalho Total (Integral): {resultado:.4f}")
    print(f"             Multiplicações: {operacoes['multiplicacoes']}")
    print(f"             Adições/subtrações: {operacoes['adicoes']}")
    print()


if __name__ == "__main__":
    main()