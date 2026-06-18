import os
import sys


RAIZ_DO_PROJETO = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.integracao import integral_simpson_3_8


def main():
    h = 2
    v = [10, 15, 12, 8]

    resultado, operacoes = integral_simpson_3_8(
        v,
        h,
        contar_operacoes=True
    )

    print()
    print("     Transferência de servidor (Simpson 3/8)")
    print(f"     h constante: {h} segundos")
    print(f"     Banda (MB/s): {v}")
    print()
    print(f"         Total transferido: {resultado} MB")
    print(f"             Multiplicações: {operacoes['multiplicacoes']}")
    print(f"             Adições/subtrações: {operacoes['adicoes']}")
    print()


if __name__ == "__main__":
    main()