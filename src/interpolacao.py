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


def interpolar_spline_linear(pontos, x, contar_operacoes=False):
    """Calcula o valor interpolado por Spline Linear.

    Liga cada par de pontos consecutivos por uma reta. E simples e rapido,
    mas pode gerar "quinas" nas juncoes.

    Args:
        pontos: lista de tuplas no formato (x, y), ordenada por x.
        x: ponto onde a spline sera avaliada.
        contar_operacoes: se True, tambem retorna a contagem de operacoes.

    Returns:
        Valor interpolado no ponto x, ou (valor, operacoes) quando
        contar_operacoes=True.
    """
    _validar_pontos(pontos)
    operacoes = _criar_contagem_operacoes()

    # Encontra o intervalo [xi, xi+1] onde x esta contido.
    indice = _encontrar_intervalo(pontos, x)

    xi, yi = pontos[indice]
    xi1, yi1 = pontos[indice + 1]

    # Interpolacao linear: y = yi + (yi1 - yi) / (xi1 - xi) * (x - xi)
    numerador = yi1 - yi
    denominador = xi1 - xi
    operacoes["adicoes"] += 2

    resultado = yi + numerador / denominador * (x - xi)
    operacoes["multiplicacoes"] += 1
    operacoes["adicoes"] += 2

    if contar_operacoes:
        return resultado, operacoes

    return resultado


def interpolar_spline_cubica(pontos, x, contar_operacoes=False):
    """Calcula o valor interpolado por Spline Cubica Natural.

    Constroi polinomios cubicos entre cada par de pontos, garantindo
    continuidade da primeira e da segunda derivada. Nas extremidades,
    a segunda derivada e zero (condicao natural).

    Args:
        pontos: lista de tuplas no formato (x, y), ordenada por x.
        x: ponto onde a spline sera avaliada.
        contar_operacoes: se True, tambem retorna a contagem de operacoes.

    Returns:
        Valor interpolado no ponto x, ou (valor, operacoes) quando
        contar_operacoes=True.
    """
    _validar_pontos(pontos)
    operacoes = _criar_contagem_operacoes()

    n = len(pontos)
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    # --- Passo 1: calcular os intervalos h entre pontos consecutivos ---
    h = []
    for i in range(n - 1):
        h.append(xs[i + 1] - xs[i])
        operacoes["adicoes"] += 1

    # --- Passo 2: montar e resolver o sistema tridiagonal para c ---
    # Condicao natural: c[0] = 0, c[n-1] = 0.
    # Para pontos internos monta-se A*c = b.
    c = [0.0] * n

    if n > 2:
        # Vetores do sistema tridiagonal (tamanho n-2 para pontos internos).
        tamanho = n - 2
        diag_inferior = [0.0] * tamanho
        diag_principal = [0.0] * tamanho
        diag_superior = [0.0] * tamanho
        lado_direito = [0.0] * tamanho

        for i in range(tamanho):
            k = i + 1  # indice real do ponto interno
            diag_principal[i] = 2.0 * (h[k - 1] + h[k])
            operacoes["adicoes"] += 1
            operacoes["multiplicacoes"] += 1

            lado_direito[i] = (
                3.0 * ((ys[k + 1] - ys[k]) / h[k] - (ys[k] - ys[k - 1]) / h[k - 1])
            )
            operacoes["adicoes"] += 3
            operacoes["multiplicacoes"] += 1

            if i > 0:
                diag_inferior[i] = h[k - 1]
            if i < tamanho - 1:
                diag_superior[i] = h[k]

        # Resolve com algoritmo de Thomas (eliminacao para frente + substituicao).
        for i in range(1, tamanho):
            fator = diag_inferior[i] / diag_principal[i - 1]
            operacoes["multiplicacoes"] += 1

            diag_principal[i] = diag_principal[i] - fator * diag_superior[i - 1]
            operacoes["multiplicacoes"] += 1
            operacoes["adicoes"] += 1

            lado_direito[i] = lado_direito[i] - fator * lado_direito[i - 1]
            operacoes["multiplicacoes"] += 1
            operacoes["adicoes"] += 1

        # Substituicao de volta.
        c[tamanho] = lado_direito[tamanho - 1] / diag_principal[tamanho - 1]

        for i in range(tamanho - 2, -1, -1):
            c[i + 1] = (
                (lado_direito[i] - diag_superior[i] * c[i + 2]) / diag_principal[i]
            )
            operacoes["multiplicacoes"] += 1
            operacoes["adicoes"] += 1

    # --- Passo 3: calcular coeficientes a, b, d de cada pedaco ---
    a = ys[:]
    b = [0.0] * (n - 1)
    d = [0.0] * (n - 1)

    for i in range(n - 1):
        d[i] = (c[i + 1] - c[i]) / (3.0 * h[i])
        operacoes["adicoes"] += 1
        operacoes["multiplicacoes"] += 1

        b[i] = (a[i + 1] - a[i]) / h[i] - h[i] * (2.0 * c[i] + c[i + 1]) / 3.0
        operacoes["adicoes"] += 3
        operacoes["multiplicacoes"] += 2

    # --- Passo 4: avaliar no intervalo correto ---
    indice = _encontrar_intervalo(pontos, x)
    dx = x - xs[indice]
    operacoes["adicoes"] += 1

    resultado = a[indice] + b[indice] * dx + c[indice] * dx**2 + d[indice] * dx**3
    operacoes["multiplicacoes"] += 3
    operacoes["adicoes"] += 3

    if contar_operacoes:
        return resultado, operacoes

    return resultado


def _encontrar_intervalo(pontos, x):
    """Encontra o indice i tal que pontos[i].x <= x <= pontos[i+1].x."""
    if x < pontos[0][0] or x > pontos[-1][0]:
        raise ValueError(
            "O valor de x deve estar dentro do intervalo dos pontos fornecidos."
        )

    for i in range(len(pontos) - 1):
        if pontos[i][0] <= x <= pontos[i + 1][0]:
            return i

    # Se x coincide com o ultimo ponto, usa o ultimo intervalo.
    return len(pontos) - 2


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
