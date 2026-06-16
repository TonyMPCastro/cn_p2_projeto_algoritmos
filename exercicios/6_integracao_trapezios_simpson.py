import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.integracao import integral_simpson_1_3, integral_trapezios

def main():
    h = 0.5
    v = [0, 40, 65, 80, 90]

    resultado_trap, op_trap = integral_trapezios(v, h, contar_operacoes=True)
    resultado_simp, op_simp = integral_simpson_1_3(v, h, contar_operacoes=True)

    print()
    print("     Distância percorrida por Carro Elétrico")
    print("     h constante:", h, "horas")
    print("     Velocidade (km/h):", v)
    print()
    print("         Distância por Trapézios:", resultado_trap, "km")
    print("             Multiplicações:", op_trap["multiplicacoes"])
    print("             Adições/subtrações:", op_trap["adições"])
    print()
    print("         Distância por Simpson 1/3:", resultado_simp, "km")
    print("             Multiplicações:", op_simp["multiplicacoes"])
    print("             Adições/subtrações:", op_simp["adições"])
    print()

if __name__ == "__main__":
    main()