"""Funções de integração numérica."""
from typing import List, Tuple, Dict, Union, Callable

def _criar_contagem_operacoes() -> Dict[str, int]:
    return {
        "multiplicacoes": 0,
        "adicoes": 0,
    }

def integral_trapezios(
    y: List[float], 
    h: float, 
    contar_operacoes: bool = False
) -> Union[float, Tuple[float, Dict[str, int]]]:
    """Calcula a integral pela Regra dos Trapézios (Repetida).
    
    Args:
        y: Lista de valores da função f(x) nos pontos amostrados.
        h: Tamanho constante do intervalo entre os pontos de x.
        contar_operacoes: Se True, também retorna a contagem de operações.
        
    Returns:
        Valor estimado da área sob a curva (integral).
    """
    operacoes = _criar_contagem_operacoes()
    n = len(y) - 1
    
    # A fórmula dos Trapézios Repetida é: (h/2) * (y_0 + 2y_1 + 2y_2 + ... + 2y_{n-1} + y_n)
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

def integral_simpson_1_3(
    y: List[float], 
    h: float, 
    contar_operacoes: bool = False
) -> Union[float, Tuple[float, Dict[str, int]]]:
    """Calcula a integral pela Regra de 1/3 de Simpson (Repetida).
    
    Args:
        y: Lista de valores da função f(x) nos pontos amostrados.
        h: Tamanho constante do intervalo entre os pontos de x.
        contar_operacoes: Se True, também retorna a contagem de operações.
        
    Returns:
        Valor estimado da área sob a curva (integral).
    """
    n = len(y) - 1
    if n % 2 != 0:
        raise ValueError("O número de subintervalos deve ser par para a regra de 1/3 de Simpson.")
        
    operacoes = _criar_contagem_operacoes()
    soma = y[0] + y[-1]
    operacoes["adicoes"] += 1
    
    # A Regra de 1/3 de Simpson usa os multiplicadores (pesos): 1, 4, 2, 4, 2 ..., 4, 1
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

def integral_simpson_3_8(
    y: List[float], 
    h: float, 
    contar_operacoes: bool = False
) -> Union[float, Tuple[float, Dict[str, int]]]:
    """Calcula a integral pela Regra de 3/8 de Simpson (Repetida).
    
    Args:
        y: Lista de valores da função f(x) nos pontos amostrados.
        h: Tamanho constante do intervalo entre os pontos de x.
        contar_operacoes: Se True, também retorna a contagem de operações.
        
    Returns:
        Valor estimado da área sob a curva (integral).
    """
    n = len(y) - 1
    if n % 3 != 0:
        raise ValueError("O número de subintervalos deve ser múltiplo de 3 para a regra de 3/8 de Simpson.")
        
    operacoes = _criar_contagem_operacoes()
    soma = y[0] + y[-1]
    operacoes["adicoes"] += 1
    
    # A Regra de 3/8 de Simpson usa os multiplicadores (pesos): 1, 3, 3, 2, 3, 3, 2 ..., 3, 3, 1
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

def quadratura_gauss(
    funcao: Callable[[float], float], 
    a: float, 
    b: float, 
    n_pontos: int, 
    contar_operacoes: bool = False
) -> Union[float, Tuple[float, Dict[str, int]]]:
    """Calcula a integral usando a Fórmula de Quadratura de Gauss para n=2 ou n=3.
    
    Args:
        funcao: Função matemática f(x) a ser integrada.
        a: Limite inferior da integral.
        b: Limite superior da integral.
        n_pontos: Número de pontos (nó e pesos) de Gauss (suporta apenas 2 ou 3).
        contar_operacoes: Se True, também retorna a contagem de operações.
        
    Returns:
        Valor estimado da integral definida.
    """
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