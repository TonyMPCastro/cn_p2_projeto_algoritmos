"""Funções de ajuste de curvas."""

def _criar_contagem_operacoes():
    return {
        "multiplicacoes": 0,
        "adicoes": 0,
    }

def ajuste_linear_mmq(pontos, contar_operacoes=False):
    """Encontra a reta P1(x) = ax + b que melhor se ajusta aos dados (MMQ)."""
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

    a = (n * soma_xy - soma_x * soma_y) / denominador
    b = (soma_y * soma_x2 - soma_x * soma_xy) / denominador
    operacoes["multiplicacoes"] += 4
    operacoes["adicoes"] += 2

    if contar_operacoes:
        return a, b, operacoes

    return a, b