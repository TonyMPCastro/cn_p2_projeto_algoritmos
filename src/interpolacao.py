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


def interpolar_gregory_newton(pontos, x, contar_operacoes=False, *, h=None):
    """Calcula o valor interpolado pelo metodo de Gregory-Newton.

    O metodo usa diferencas finitas e exige pontos igualmente espacados.
    A forma progressiva e usada quando x esta mais proximo do inicio da
    tabela; caso contrario, usa a forma regressiva. Quando h e informado,
    ele e usado como espacamento e validado contra os pontos.
    """
    # Ordena uma copia para manter a lista original intacta.
    pontos_ordenados = sorted(pontos, key=lambda ponto: ponto[0])
    _validar_pontos(pontos_ordenados)

    operacoes = _criar_contagem_operacoes()
    espacamento = _validar_espacamento_uniforme(pontos_ordenados, h)
    # A tabela guarda y, primeiras diferencas, segundas diferencas, etc.
    tabela = _calcular_tabela_diferencas_finitas(
        pontos_ordenados,
        operacoes,
    )

    primeiro_x = pontos_ordenados[0][0]
    ultimo_x = pontos_ordenados[-1][0]
    ponto_medio = (primeiro_x + ultimo_x) / 2

    # Perto do inicio, usa diferencas progressivas; perto do fim, regressivas.
    if x <= ponto_medio:
        resultado = tabela[0][0]
        u = (x - primeiro_x) / espacamento
        operacoes["adicoes"] += 1
        indice_diferenca = 0
        usar_progressiva = True
    else:
        resultado = tabela[0][-1]
        u = (x - ultimo_x) / espacamento
        operacoes["adicoes"] += 1
        indice_diferenca = -1
        usar_progressiva = False

    produto = 1

    # Monta os termos u, u(u-1)/2!, u(u-1)(u-2)/3! na progressiva
    # ou u, u(u+1)/2!, u(u+1)(u+2)/3! na regressiva.
    for ordem in range(1, len(tabela)):
        if usar_progressiva:
            fator = u - (ordem - 1)
        else:
            fator = u + (ordem - 1)
        operacoes["adicoes"] += 1

        produto = produto * fator / ordem
        operacoes["multiplicacoes"] += 1

        parcela = tabela[ordem][indice_diferenca] * produto
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


def _validar_espacamento_uniforme(pontos, h=None):
    """Retorna o h quando todos os pontos possuem o mesmo espacamento."""
    espacamento = pontos[1][0] - pontos[0][0]
    tolerancia = 1e-9 * max(1, abs(espacamento))

    if h is not None:
        if h == 0:
            raise ValueError("O valor de h deve ser diferente de zero.")

        tolerancia_h = 1e-9 * max(1, abs(h))

        if abs(espacamento - h) > tolerancia_h:
            raise ValueError("O valor de h deve coincidir com os pontos.")

        espacamento = h
        tolerancia = tolerancia_h

    for indice in range(2, len(pontos)):
        espacamento_atual = pontos[indice][0] - pontos[indice - 1][0]

        if abs(espacamento_atual - espacamento) > tolerancia:
            raise ValueError(
                "Os pontos devem ter espacamento uniforme para Gregory-Newton."
            )

    return espacamento


def _calcular_tabela_diferencas_finitas(pontos, operacoes):
    """Monta a tabela de diferencas finitas usada por Gregory-Newton."""
    tabela = [[y for _, y in pontos]]

    for _ in range(1, len(pontos)):
        diferencas_anteriores = tabela[-1]
        diferencas_atuais = []

        for indice in range(len(diferencas_anteriores) - 1):
            diferenca = (
                diferencas_anteriores[indice + 1]
                - diferencas_anteriores[indice]
            )
            operacoes["adicoes"] += 1
            diferencas_atuais.append(diferenca)

        tabela.append(diferencas_atuais)

    return tabela
