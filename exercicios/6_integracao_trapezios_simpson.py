import os
import sys


RAIZ_DO_PROJETO = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.integracao import integral_simpson_1_3, integral_trapezios


def main():
    h = 0.5
    v = [0, 40, 65, 80, 90]

    resultado_trap, op_trap = integral_trapezios(
        v,
        h,
        contar_operacoes=True
    )

    resultado_simp, op_simp = integral_simpson_1_3(
        v,
        h,
        contar_operacoes=True
    )

    print()
    print("     Distância percorrida por Carro Elétrico")
    print(f"     h constante: {h} horas")
    print(f"     Velocidade (km/h): {v}")
    print()

    print(f"         Distância por Trapézios: {resultado_trap} km")
    print(f"             Multiplicações: {op_trap['multiplicacoes']}")
    print(f"             Adições/subtrações: {op_trap['adicoes']}")
    print()

    print(f"         Distância por Simpson 1/3: {resultado_simp} km")
    print(f"             Multiplicações: {op_simp['multiplicacoes']}")
    print(f"             Adições/subtrações: {op_simp['adicoes']}")
    print()


if __name__ == "__main__":
    main()