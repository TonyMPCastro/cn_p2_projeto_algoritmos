"""Funções de ajuste de curvas."""
from typing import List, Tuple, Dict, Union

def _criar_contagem_operacoes() -> Dict[str, int]:
    return {
        "multiplicacoes": 0,
        "adicoes": 0,
    }

def ajuste_linear_mmq(
    pontos: List[Tuple[float, float]], 
    contar_operacoes: bool = False
) -> Union[Tuple[float, float], Tuple[float, float, Dict[str, int]]]:
    """Encontra a reta P1(x) = ax + b que melhor se ajusta aos dados usando Mínimos Quadrados (MMQ).
    
    Args:
        pontos: Lista de tuplas contendo as coordenadas (x, y) amostradas.
        contar_operacoes: Se True, retorna também um dicionário com a contagem de operações.
        
    Returns:
        Tupla com os coeficientes (a, b) da reta ajustada.
        Se contar_operacoes for True, retorna (a, b, operacoes).
    """
    if len(pontos) < 2:
        raise ValueError("São necessários pelo menos dois pontos para o ajuste linear.")

    operacoes = _criar_contagem_operacoes()
    n = len(pontos)
    soma_x = 0.0
    soma_y = 0.0
    soma_xy = 0.0
    soma_x2 = 0.0

    for x, y in pontos:
        soma_x += x
        soma_y += y
        soma_xy += x * y
        soma_x2 += x * x
        operacoes["adicoes"] += 4
        operacoes["multiplicacoes"] += 2

    denominador = n * soma_x2 - soma_x * soma_x
    operacoes["multiplicacoes"] += 2
    operacoes["adicoes"] += 1

    if denominador == 0:
        raise ValueError("Não é possível ajustar uma reta (pontos colineares verticalmente).")

    # Fórmulas do Método dos Mínimos Quadrados para regressão linear simples (y = ax + b):
    # a = (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)
    # b = (Σy*Σx² - Σx*Σxy) / (n*Σx² - (Σx)²)
    a = (n * soma_xy - soma_x * soma_y) / denominador
    b = (soma_y * soma_x2 - soma_x * soma_xy) / denominador
    operacoes["multiplicacoes"] += 4
    operacoes["adicoes"] += 2

    if contar_operacoes:
        return a, b, operacoes

    return a, b