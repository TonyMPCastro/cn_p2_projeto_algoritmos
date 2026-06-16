import os
import sys

RAIZ_DO_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ_DO_PROJETO)

from src.ajuste_curvas import ajuste_linear_mmq

def main():
    #     x (hora)   y (acessos)
    pontos = [
        (8, 2.1),
        (9, 2.8),
        (10, 3.1),
        (11, 4.0),
        (12, 4.8),
    ]
    x_alvo = 13

    a, b, operacoes = ajuste_linear_mmq(pontos, contar_operacoes=True)
    previsao = a * x_alvo + b

    print()
    print("     Análise de tráfego de rede DEINF (MMQ)")
    print("     Pontos (hora, acessos em milhares):", pontos)
    print()
    print(f"         Equação da Reta P1(x): y = {a:.4f}x + {b:.4f}")
    print(f"         Previsão para {x_alvo}h: {previsao:.4f} mil acessos")
    print("             Multiplicações:", operacoes["multiplicacoes"])
    print("             Adições/subtrações:", operacoes["adicoes"])
    print()

if __name__ == "__main__":
    main()