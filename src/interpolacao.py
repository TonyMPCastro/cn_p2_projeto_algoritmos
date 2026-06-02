"""Funcoes de interpolacao numerica."""


def interpolar_lagrange(pontos, x, contar_operacoes=False):
    """Calcula o valor interpolado pelo metodo de Lagrange.

    Args:
        pontos: lista de tuplas no formato (x, y).
        x: ponto onde o polinomio interpolador sera avaliado.
        contar_operacoes: se True, tambem retorna a contagem de operacoes.

    Returns:
        Valor interpolado no ponto x, ou (valor, operacoes) quando
        contar_operacoes=True.
    """
    if len(pontos) < 2:
        raise ValueError("Informe pelo menos dois pontos para interpolar.")

    resultado = 0
    operacoes = _criar_contagem_operacoes()

    # Soma todos os termos base L_i(x) multiplicados pelo y correspondente.
    for i in range(len(pontos)):
        xi, yi = pontos[i]
        termo = yi

        # Cada termo usa todos os outros pontos para montar o produto:
        # (x - xj) / (xi - xj).
        for j in range(len(pontos)):
            if i != j:
                xj, _ = pontos[j]

                if xi == xj:
                    raise ValueError("Os valores de x dos pontos devem ser diferentes.")

                numerador = x - xj
                denominador = xi - xj
                operacoes["adicoes"] += 2

                termo = termo * numerador / denominador
                operacoes["multiplicacoes"] += 1

        resultado = resultado + termo
        operacoes["adicoes"] += 1

    if contar_operacoes:
        return resultado, operacoes

    return resultado



def calcular_coeficientes_newton(pontos, contar_operacoes=False):
    """Calcula os coeficientes do polinomio de Newton.

    Os coeficientes sao obtidos pela tabela de diferencas divididas.
    Se contar_operacoes=True, retorna tambem a contagem de operacoes.
    """
    _validar_pontos(pontos)

    coeficientes = []
    diferencas = []
    operacoes = _criar_contagem_operacoes()

    # A primeira coluna da tabela de diferencas divididas sao os valores de y.
    for _, y in pontos:
        diferencas.append(y)

    coeficientes.append(diferencas[0])

    # Cada ordem reduz a tabela ate encontrar o proximo coeficiente de Newton.
    for ordem in range(1, len(pontos)):
        novas_diferencas = []

        for indice in range(len(diferencas) - 1):
            xi = pontos[indice][0]
            xj = pontos[indice + ordem][0]
            numerador = diferencas[indice + 1] - diferencas[indice]
            denominador = xj - xi
            operacoes["adicoes"] += 2

            diferenca = numerador / denominador
            novas_diferencas.append(diferenca)

        diferencas = novas_diferencas
        coeficientes.append(diferencas[0])

    if contar_operacoes:
        return coeficientes, operacoes

    return coeficientes


def interpolar_newton(pontos, x, contar_operacoes=False):
    """Calcula o valor interpolado pelo metodo de Newton.

    Se contar_operacoes=True, retorna tambem a contagem de operacoes.
    """
    coeficientes, operacoes = calcular_coeficientes_newton(
        pontos,
        contar_operacoes=True,
    )
    resultado = coeficientes[0]
    produto = 1

    # Avalia c0 + c1(x-x0) + c2(x-x0)(x-x1) + ...
    for indice in range(1, len(coeficientes)):
        fator = x - pontos[indice - 1][0]
        operacoes["adicoes"] += 1

        produto = produto * fator
        operacoes["multiplicacoes"] += 1

        parcela = coeficientes[indice] * produto
        operacoes["multiplicacoes"] += 1

        resultado = resultado + parcela
        operacoes["adicoes"] += 1

    if contar_operacoes:
        return resultado, operacoes

    return resultado


def interpolar_gregory_newton(pontos, x, h, contar_operacoes=False):
    """Calcula o valor interpolado pelo metodo de Gregory-Newton.

    O metodo usa diferencas finitas progressivas e exige pontos igualmente
    espacados pelo valor de h.
    """
    _validar_pontos(pontos)
    _validar_espacamento_uniforme(pontos, h)

    operacoes = _criar_contagem_operacoes()
    diferencas = [y for _, y in pontos]
    resultado = diferencas[0]
    u = (x - pontos[0][0]) / h
    operacoes["adicoes"] += 1

    produto = 1

    # Monta os termos u, u(u-1)/2!, u(u-1)(u-2)/3!, ...
    for ordem in range(1, len(pontos)):
        novas_diferencas = []

        for indice in range(len(diferencas) - 1):
            diferenca = diferencas[indice + 1] - diferencas[indice]
            operacoes["adicoes"] += 1
            novas_diferencas.append(diferenca)

        diferencas = novas_diferencas
        fator = u - (ordem - 1)
        operacoes["adicoes"] += 1

        produto = produto * fator / ordem
        operacoes["multiplicacoes"] += 1

        parcela = diferencas[0] * produto
        operacoes["multiplicacoes"] += 1

        resultado = resultado + parcela
        operacoes["adicoes"] += 1

    if contar_operacoes:
        return resultado, operacoes

    return resultado


def _criar_contagem_operacoes():
    return {
        "multiplicacoes": 0,
        "adicoes": 0,
    }


def _validar_pontos(pontos):
    """Valida quantidade minima de pontos e impede valores de x repetidos."""
    if len(pontos) < 2:
        raise ValueError("Informe pelo menos dois pontos para interpolar.")

    for i in range(len(pontos)):
        xi, _ = pontos[i]

        for j in range(i + 1, len(pontos)):
            xj, _ = pontos[j]

            if xi == xj:
                raise ValueError("Os valores de x dos pontos devem ser diferentes.")


def _validar_espacamento_uniforme(pontos, h):
    """Verifica se todos os pontos estao separados pelo valor de h."""
    if h == 0:
        raise ValueError("O valor de h deve ser diferente de zero.")

    tolerancia = 1e-9 * max(1, abs(h))

    for indice in range(1, len(pontos)):
        espacamento_atual = pontos[indice][0] - pontos[indice - 1][0]

        if abs(espacamento_atual - h) > tolerancia:
            raise ValueError(
                "Os pontos devem ter espacamento uniforme para Gregory-Newton."
            )
