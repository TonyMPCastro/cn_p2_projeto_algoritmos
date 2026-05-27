"""Funcoes de interpolacao numerica."""


def interpolar_lagrange(pontos, x):
    """Calcula o valor interpolado pelo metodo de Lagrange.

    Args:
        pontos: lista de tuplas no formato (x, y).
        x: ponto onde o polinomio interpolador sera avaliado.

    Returns:
        Valor interpolado no ponto x.
    """
    if len(pontos) < 2: # erro de numero insuficiente de pontos
        raise ValueError("Informe pelo menos dois pontos para interpolar.")

    resultado = 0

    for i in range(len(pontos)):#começa a iterar pelos pontos, para cada ponto calcula o termo de Lagrange correspondente e soma ao resultado

        xi, yi = pontos[i]#pega o ponto atual, que sera usado para calcular o termo de Lagrange correspondente a esse ponto. O termo de Lagrange é calculado multiplicando o valor de y do ponto atual por um produto que envolve os outros pontos. O produto é calculado iterando pelos outros pontos e multiplicando o termo por (x - xj) / (xi - xj), onde xj é o valor de x do outro ponto e xi é o valor de x do ponto atual. Isso garante que o termo de Lagrange seja igual a yi quando x for igual a xi, e seja zero quando x for igual a qualquer outro valor de x dos pontos.
        
        termo = yi #inicia o termo de Lagrange com o valor de y do ponto atual

        for j in range(len(pontos)):#itera pelos outros pontos para calcular o produto do termo de Lagrange
            if i != j: #verifica se o ponto atual é diferente do ponto que está sendo iterado, para evitar multiplicar por zero
                xj, _ = pontos[j] #pega o valor de x do outro ponto, que sera usado para calcular o produto do termo de Lagrange

                if xi == xj: #verifica se os valores de x dos pontos são iguais, o que não é permitido para a interpolação de Lagrange, pois causaria uma divisão por zero.
                    raise ValueError("Os valores de x dos pontos devem ser diferentes.")

                termo = termo * (x - xj) / (xi - xj)#calcula o produto do termo de Lagrange multiplicando o termo atual por (x - xj) / (xi - xj), onde xj é o valor de x do outro ponto e xi é o valor de x do ponto atual. 
                #Isso garante que o termo de Lagrange seja igual a yi quando x for igual a xi, e seja zero quando x for igual a qualquer outro valor de x dos pontos.
        
        #após calcular o termo de Lagrange para o ponto atual, ele é somado ao resultado final. O resultado final é a soma de todos os termos de Lagrange, que é o valor interpolado no ponto x.
        resultado = resultado + termo

    return resultado



def calcular_coeficientes_newton(pontos):
    """Calcula os coeficientes do polinomio de Newton.

    Os coeficientes sao obtidos pela tabela de diferencas divididas.
    """
    _validar_pontos(pontos)

    coeficientes = []
    diferencas = []

    for _, y in pontos:
        diferencas.append(y)

    coeficientes.append(diferencas[0])

    for ordem in range(1, len(pontos)):
        novas_diferencas = []

        for indice in range(len(diferencas) - 1):
            xi = pontos[indice][0]
            xj = pontos[indice + ordem][0]
            diferenca = (diferencas[indice + 1] - diferencas[indice]) / (xj - xi)
            novas_diferencas.append(diferenca)

        diferencas = novas_diferencas
        coeficientes.append(diferencas[0])

    return coeficientes


def interpolar_newton(pontos, x):
    """Calcula o valor interpolado pelo metodo de Newton."""
    coeficientes = calcular_coeficientes_newton(pontos)
    resultado = coeficientes[0]
    produto = 1

    for indice in range(1, len(coeficientes)):
        produto = produto * (x - pontos[indice - 1][0])
        resultado = resultado + coeficientes[indice] * produto

    return resultado


def _validar_pontos(pontos):
    if len(pontos) < 2:
        raise ValueError("Informe pelo menos dois pontos para interpolar.")

    for i in range(len(pontos)):
        xi, _ = pontos[i]

        for j in range(i + 1, len(pontos)):
            xj, _ = pontos[j]

            if xi == xj:
                raise ValueError("Os valores de x dos pontos devem ser diferentes.")
