"""Funções de integração numérica."""

def _criar_contagem_operacoes():
    return {
        "multiplicacoes": 0,
        "adicoes": 0,
    }

def integral_trapezios(y, h, contar_operacoes=False):
    """Calcula a integral pela Regra dos Trapézios (Repetida)."""
    operacoes = _criar_contagem_operacoes()
    n = len(y) - 1
    
    soma = y[0] + y[-1]
    operacoes["adicoes"] += 1
    
    for i in range(1, n):
        soma += 2 * y[i]
        operacoes["adicoes"] += 1
        operacoes["multiplicacoes"] += 1
        
    resultado = (h / 2.0) * soma
    operacoes["multiplicacoes"] += 2
    
    if contar_operacoes:
        return resultado, operacoes
    return resultado

def integral_simpson_1_3(y, h, contar_operacoes=False):
    """Calcula a integral pela Regra de 1/3 de Simpson (Repetida)."""
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("O número de subintervalos deve ser par para a regra de 1/3 de Simpson.")
        
    operacoes = _criar_contagem_operacoes()
    soma = y[0] + y[-1]
    operacoes["adicoes"] += 1
    
    for i in range(1, n):
        if i % 2 == 0:
            soma += 2 * y[i]
        else:
            soma += 4 * y[i]
        operacoes["adicoes"] += 1
        operacoes["multiplicacoes"] += 1
        
    resultado = (h / 3.0) * soma
    operacoes["multiplicacoes"] += 2
    
    if contar_operacoes:
        return resultado, operacoes
    return resultado

def integral_simpson_3_8(y, h, contar_operacoes=False):
    """Calcula a integral pela Regra de 3/8 de Simpson (Repetida)."""
    n = len(y) - 1
    if n % 3 != 0:
        raise ValueError("O número de subintervalos deve ser múltiplo de 3 para a regra de 3/8 de Simpson.")
        
    operacoes = _criar_contagem_operacoes()
    soma = y[0] + y[-1]
    operacoes["adicoes"] += 1
    
    for i in range(1, n):
        if i % 3 == 0:
            soma += 2 * y[i]
        else:
            soma += 3 * y[i]
        operacoes["adicoes"] += 1
        operacoes["multiplicacoes"] += 1
        
    resultado = (3.0 * h / 8.0) * soma
    operacoes["multiplicacoes"] += 3
    
    if contar_operacoes:
        return resultado, operacoes
    return resultado

def quadratura_gauss(funcao, a, b, n_pontos, contar_operacoes=False):
    """Calcula a integral usando a Fórmula de Quadratura de Gauss para n=2 ou n=3."""
    operacoes = _criar_contagem_operacoes()
    
    if n_pontos == 2:
        raiz = 1.0 / (3.0 ** 0.5)
        raizes_pesos = [(-raiz, 1.0), (raiz, 1.0)]
    elif n_pontos == 3:
        raiz = (0.6) ** 0.5
        raizes_pesos = [(-raiz, 5.0/9.0), (0.0, 8.0/9.0), (raiz, 5.0/9.0)]
    else:
        raise ValueError("Apenas suportado n=2 e n=3.")
        
    jacobiano = (b - a) / 2.0
    media = (b + a) / 2.0
    operacoes["adicoes"] += 2
    operacoes["multiplicacoes"] += 2
    
    integral = 0.0
    
    for t, w in raizes_pesos:
        x = jacobiano * t + media
        operacoes["multiplicacoes"] += 1
        operacoes["adicoes"] += 1
        
        y = funcao(x)
        
        integral += w * y
        operacoes["multiplicacoes"] += 1
        operacoes["adicoes"] += 1
        
    integral *= jacobiano
    operacoes["multiplicacoes"] += 1
    
    if contar_operacoes:
        return integral, operacoes
    return integral